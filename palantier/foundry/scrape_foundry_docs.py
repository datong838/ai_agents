#!/usr/bin/env python3
"""
Mirror Palantir Foundry「数据连接与集成」docs (zh) to docs/palantier/foundry/.

Usage:
  python scrape_foundry_docs.py              # full run
  python scrape_foundry_docs.py --limit 10   # pilot
  python scrape_foundry_docs.py --skip-existing
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Any
from urllib.parse import urljoin, urlparse

import requests

ROOT = Path(__file__).resolve().parent
META = ROOT / "meta"
PAGES = ROOT / "pages"
IMAGES = ROOT / "images"

BASE = "https://www.palantir.com"
ENTRY_PATH = "/zh/foundry/data-integration/overview/"
# Ontology 专章入口（侧栏含 ontology / ontology-manager / object-indexing 等 · 约 316 页）
ONTOLOGY_ENTRY = "/zh/foundry/ontology/overview/"
SCOPE_PREFIX = "/zh/foundry/"

NEXT_DATA_RE = re.compile(
    r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', re.DOTALL
)
MD_LINK_RE = re.compile(r"(!?\[[^\]]*\])\(([^)]+)\)")
RESOURCE_RE = re.compile(r"/docs/resources/[^\s\"')]+")


def fix_mojibake(text: str) -> str:
    """Palantir zh JSON sometimes stores UTF-8 bytes as Latin-1 codepoints."""
    if not text:
        return text
    try:
        return text.encode("latin-1").decode("utf-8")
    except (UnicodeDecodeError, UnicodeEncodeError):
        return text


@dataclass
class PageResult:
    url_path: str
    ok: bool
    title: str = ""
    local_path: str = ""
    error: str = ""
    content_links: list[str] = field(default_factory=list)
    assets: list[str] = field(default_factory=list)
    prev: str | None = None
    next: str | None = None


class Scraper:
    def __init__(self, workers: int = 4, delay: float = 0.25, skip_existing: bool = False):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": "wchat-foundry-mirror/1.0 (internal research; +https://palantir.com)",
                "Accept-Language": "zh-CN,zh;q=0.9",
            }
        )
        self.workers = workers
        self.delay = delay
        self.skip_existing = skip_existing
        self._lock = Lock()
        self._asset_cache: dict[str, str] = {}  # remote -> local rel from pages/
        self.stats = {"ok": 0, "fail": 0, "skipped": 0, "images": 0}

    def fetch_next_data(self, url_path: str) -> dict[str, Any]:
        if not url_path.startswith("/"):
            url_path = "/" + url_path
        url = BASE + "/docs" + url_path
        for attempt in range(4):
            try:
                r = self.session.get(url, timeout=90)
                r.raise_for_status()
                m = NEXT_DATA_RE.search(r.text)
                if not m:
                    raise ValueError("no __NEXT_DATA__")
                return json.loads(m.group(1))["props"]["pageProps"]
            except Exception as e:
                if attempt == 3:
                    raise
                time.sleep(2 ** attempt)
        raise RuntimeError("unreachable")

    def collect_sidebar_urls(self, items: list) -> list[dict]:
        out: list[dict] = []

        def walk(nodes, parent: str | None = None):
            for i, node in enumerate(nodes):
                if node.get("type") == "pageLink":
                    link = node.get("link", {})
                    url = link.get("url", "")
                    if url.startswith(SCOPE_PREFIX):
                        entry = {
                            "url": url,
                            "title": fix_mojibake(link.get("text", "")),
                            "pageId": node.get("pageId", ""),
                            "parent": parent,
                            "order": i,
                        }
                        out.append(entry)
                        walk([], entry["url"])  # no children for pageLink
                elif node.get("type") == "pageGroup":
                    group_id = f"group:{node.get('title', '')}"
                    for child in node.get("pages", []):
                        walk([child], group_id)
                elif node.get("pages"):
                    walk(node["pages"], parent)
                elif node.get("items"):
                    walk(node["items"], parent)

        walk(items)
        # dedupe preserving order
        seen = set()
        unique = []
        for item in out:
            if item["url"] not in seen:
                seen.add(item["url"])
                unique.append(item)
        return unique

    def url_to_page_path(self, url_path: str) -> Path:
        p = url_path.strip("/")
        # zh/foundry/data-integration/overview -> pages/zh/foundry/data-integration/overview.md
        return PAGES / f"{p}.md"

    def download_asset(self, asset_url: str) -> str:
        """Return local path relative to PAGES root (e.g. ../images/foundry/...)."""
        with self._lock:
            if asset_url in self._asset_cache:
                return self._asset_cache[asset_url]

        if asset_url.startswith("/"):
            full = BASE + asset_url
        elif asset_url.startswith("http"):
            full = asset_url
        else:
            full = urljoin(BASE + "/docs/resources/", asset_url)

        parsed = urlparse(full)
        # /docs/resources/foundry/data-integration/1-Data.svg -> images/foundry/...
        rel = parsed.path
        if rel.startswith("/docs/resources/"):
            rel = rel[len("/docs/resources/") :]
        local = IMAGES / rel.lstrip("/")
        local.parent.mkdir(parents=True, exist_ok=True)

        if not local.exists():
            for attempt in range(4):
                try:
                    resp = self.session.get(full, timeout=60)
                    resp.raise_for_status()
                    local.write_bytes(resp.content)
                    with self._lock:
                        self.stats["images"] += 1
                    break
                except Exception:
                    if attempt == 3:
                        raise
                    time.sleep(2 ** attempt)

        # relative from pages/zh/foundry/... (3 levels) -> ../../../images/...
        rel_from_pages = Path("..") / ".." / ".." / "images" / rel.lstrip("/").replace("/docs/resources/", "")
        if str(rel_from_pages).startswith(".."):
            cached = str(rel_from_pages).replace("\\", "/")
        else:
            cached = f"../../images/{rel.lstrip('/')}"

        with self._lock:
            self._asset_cache[asset_url] = cached
        return cached

    def rewrite_markdown(self, md: str, page_props: dict) -> tuple[str, list[str]]:
        assets_downloaded: list[str] = []

        # docAssetMetadata keys
        for asset_path in page_props.get("docAssetMetadata", {}):
            try:
                local = self.download_asset(asset_path)
                assets_downloaded.append(asset_path)
                fname = Path(asset_path).name
                md = md.replace(fname, local.split("/")[-1])  # minimal; fix paths below
            except Exception:
                pass

        def replace_link(match: re.Match) -> str:
            prefix, target = match.group(1), match.group(2)
            if target.startswith("#") or target.startswith("mailto:"):
                return match.group(0)
            # normalize internal doc links
            if target.startswith("/docs/"):
                target = target[len("/docs") :]
            if target.startswith("/foundry/"):
                target = "/zh" + target
            if "/docs/resources/" in target or target.startswith("../../foundry-docs"):
                try:
                    if target.startswith("../../"):
                        # ../../foundry-docs/data-integration/media/1-Data.svg
                        fname = Path(target).name
                        for key in page_props.get("docAssetMetadata", {}):
                            if Path(key).name == fname:
                                local = self.download_asset(key)
                                assets_downloaded.append(key)
                                return f"{prefix}({local})"
                    else:
                        local = self.download_asset(target)
                        assets_downloaded.append(target)
                        return f"{prefix}({local})"
                except Exception:
                    pass
            return f"{prefix}({target})"

        md = MD_LINK_RE.sub(replace_link, md)

        # remaining resource refs in raw markdown
        for ref in RESOURCE_RE.findall(md):
            try:
                local = self.download_asset(ref)
                assets_downloaded.append(ref)
                md = md.replace(ref, local)
            except Exception:
                pass

        return md, assets_downloaded

    def extract_content_links(self, md: str) -> list[str]:
        links = []
        for m in MD_LINK_RE.finditer(md):
            target = m.group(2)
            if target.startswith("#") or target.startswith("http") or target.startswith("mailto:"):
                continue
            if target.startswith("/docs/"):
                target = target[len("/docs") :]
            if target.startswith("/foundry/"):
                target = "/zh" + target
            if target.startswith(SCOPE_PREFIX):
                links.append(target.rstrip("/") + ("/" if not target.endswith("/") else ""))
        return links

    def process_page(self, url_path: str, nav_title: str = "") -> PageResult:
        url_path = url_path if url_path.endswith("/") else url_path + "/"
        local_file = self.url_to_page_path(url_path)
        result = PageResult(url_path=url_path, ok=False)

        if self.skip_existing and local_file.exists():
            self.stats["skipped"] += 1
            result.ok = True
            result.local_path = str(local_file.relative_to(ROOT))
            try:
                text = local_file.read_text(encoding="utf-8")
                fm_m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
                if fm_m:
                    meta = json.loads(fm_m.group(1))
                    result.prev = meta.get("previous")
                    result.next = meta.get("next")
                    result.title = meta.get("title", "")
                    body = text[fm_m.end() :]
                    result.content_links = self.extract_content_links(body)
            except Exception:
                pass
            return result

        time.sleep(self.delay)
        try:
            pp = self.fetch_next_data(url_path)
            md = fix_mojibake(pp.get("markdown") or "")
            title = fix_mojibake(nav_title)
            meta = pp.get("metadata", {})
            if isinstance(meta, dict):
                data = meta.get("data") or meta
                if isinstance(data, dict):
                    title = fix_mojibake(data.get("title", title) or title)

            neighbours = pp.get("pageNeighbours", {})
            prev_p = neighbours.get("previousPage", {}) or {}
            next_p = neighbours.get("nextPage", {}) or {}
            result.prev = prev_p.get("url")
            result.next = next_p.get("url")

            md, assets = self.rewrite_markdown(md, pp)
            result.assets = assets
            result.content_links = self.extract_content_links(md)
            result.title = title

            local_file.parent.mkdir(parents=True, exist_ok=True)
            frontmatter = {
                "source_url": BASE + "/docs" + url_path,
                "title": title,
                "page_id": pp.get("pageId"),
                "category_id": pp.get("categoryId"),
                "section_id": pp.get("sectionId"),
                "previous": result.prev,
                "next": result.next,
                "scraped_at": datetime.now(timezone.utc).isoformat(),
            }
            content = (
                "---\n"
                + json.dumps(frontmatter, ensure_ascii=False, indent=2)
                + "\n---\n\n"
                + md
            )
            local_file.write_text(content, encoding="utf-8")
            result.ok = True
            result.local_path = str(local_file.relative_to(ROOT))
            self.stats["ok"] += 1
        except Exception as e:
            result.error = str(e)
            self.stats["fail"] += 1
        return result

    def run(self, limit: int | None = None, entry: str | None = None, meta_prefix: str = "") -> dict:
        META.mkdir(parents=True, exist_ok=True)
        PAGES.mkdir(parents=True, exist_ok=True)
        IMAGES.mkdir(parents=True, exist_ok=True)

        entry_path = entry or ENTRY_PATH
        prefix = f"{meta_prefix}-" if meta_prefix else ""

        print(f"Fetching sidebar from entry: {entry_path}", flush=True)
        entry_pp = self.fetch_next_data(entry_path)
        sidebar = entry_pp.get("sidebarNavProps", {})
        (META / f"{prefix}sidebar-nav.json").write_text(
            json.dumps(sidebar, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        nav_urls = self.collect_sidebar_urls(sidebar.get("items", []))
        if limit:
            nav_urls = nav_urls[:limit]

        url_index = {item["url"]: item for item in nav_urls}
        (META / f"{prefix}url-index.json").write_text(
            json.dumps(url_index, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"Pages to scrape: {len(nav_urls)}", flush=True)

        results: list[PageResult] = []
        with ThreadPoolExecutor(max_workers=self.workers) as pool:
            futures = {
                pool.submit(self.process_page, item["url"], item.get("title", "")): item
                for item in nav_urls
            }
            for i, fut in enumerate(as_completed(futures), 1):
                res = fut.result()
                results.append(res)
                if i % 25 == 0 or i == len(nav_urls):
                    print(
                        f"  [{i}/{len(nav_urls)}] ok={self.stats['ok']} "
                        f"fail={self.stats['fail']} skip={self.stats['skipped']}",
                        flush=True,
                    )

        # build link graph
        nodes = []
        edges = []
        url_set = {r.url_path for r in results if r.ok}

        for item in nav_urls:
            nodes.append(
                {
                    "id": item["url"],
                    "title": item.get("title", ""),
                    "pageId": item.get("pageId", ""),
                    "local": str(self.url_to_page_path(item["url"]).relative_to(ROOT)),
                }
            )
            if item.get("parent") and not item["parent"].startswith("group:"):
                edges.append({"from": item["parent"], "to": item["url"], "type": "sidebar"})
            elif item.get("parent"):
                edges.append({"from": item["parent"], "to": item["url"], "type": "sidebar_group"})

        for res in results:
            if not res.ok:
                continue
            if res.prev and res.prev in url_set:
                edges.append({"from": res.url_path, "to": res.prev, "type": "prev"})
            if res.next and res.next in url_set:
                edges.append({"from": res.url_path, "to": res.next, "type": "next"})
            for link in res.content_links:
                norm = link if link.endswith("/") else link + "/"
                if norm in url_set:
                    edges.append({"from": res.url_path, "to": norm, "type": "content"})

        graph = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "entry": entry_path,
            "meta_prefix": meta_prefix or None,
            "node_count": len(nodes),
            "edge_count": len(edges),
            "nodes": nodes,
            "edges": edges,
        }
        (META / f"{prefix}link-graph.json").write_text(
            json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8"
        )

        failures = [
            {"url": r.url_path, "error": r.error}
            for r in results
            if not r.ok
        ]
        report = {
            "finished_at": datetime.now(timezone.utc).isoformat(),
            "entry": entry_path,
            "meta_prefix": meta_prefix or None,
            "total": len(nav_urls),
            "stats": self.stats,
            "failures": failures,
        }
        (META / f"{prefix}scrape-report.json").write_text(
            json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        return report


def main():
    parser = argparse.ArgumentParser(
        description="Mirror Palantir Foundry docs (zh) to docs/palantier/foundry/"
    )
    parser.add_argument("--limit", type=int, default=None, help="Pilot: scrape first N pages")
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--delay", type=float, default=0.25)
    parser.add_argument("--skip-existing", action="store_true")
    parser.add_argument(
        "--entry",
        default=None,
        help=f"Sidebar entry URL path (default: {ENTRY_PATH}). "
        f"Ontology TOC: {ONTOLOGY_ENTRY}",
    )
    parser.add_argument(
        "--meta-prefix",
        default="",
        help="Prefix for meta JSON files (e.g. ontology → ontology-url-index.json). "
        "Keeps data-integration index intact when scraping Ontology chapter.",
    )
    parser.add_argument(
        "--ontology",
        action="store_true",
        help=f"Shortcut: entry={ONTOLOGY_ENTRY} meta-prefix=ontology",
    )
    args = parser.parse_args()

    entry = args.entry
    meta_prefix = args.meta_prefix
    if args.ontology:
        entry = entry or ONTOLOGY_ENTRY
        meta_prefix = meta_prefix or "ontology"

    scraper = Scraper(
        workers=args.workers,
        delay=args.delay,
        skip_existing=args.skip_existing,
    )
    report = scraper.run(limit=args.limit, entry=entry, meta_prefix=meta_prefix)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    sys.exit(1 if report["failures"] else 0)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Rebuild link-graph.json from saved pages (frontmatter + markdown links)."""
import json
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
META = ROOT / "meta"
PAGES = ROOT / "pages"
SCOPE_PREFIX = "/zh/foundry/"
MD_LINK_RE = re.compile(r"(!?\[[^\]]*\])\(([^)]+)\)")
FM_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def extract_links(md: str) -> list[str]:
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
            norm = target if target.endswith("/") else target + "/"
            links.append(norm)
    return links


def main():
    sidebar = json.loads((META / "sidebar-nav.json").read_text(encoding="utf-8"))
    url_index = json.loads((META / "url-index.json").read_text(encoding="utf-8"))
    url_set = set(url_index.keys())

    nodes = []
    edges = []
    for url, item in url_index.items():
        local = PAGES / Path(url.strip("/"))
        local_md = local.with_suffix(".md")
        nodes.append({
            "id": url,
            "title": item.get("title", ""),
            "pageId": item.get("pageId", ""),
            "local": str(local_md.relative_to(ROOT)).replace("\\", "/"),
        })

    # sidebar group edges from url_index parent field
    for url, item in url_index.items():
        parent = item.get("parent")
        if parent and not str(parent).startswith("group:"):
            edges.append({"from": parent, "to": url, "type": "sidebar"})

    for md_file in PAGES.rglob("*.md"):
        text = md_file.read_text(encoding="utf-8")
        fm_m = FM_RE.match(text)
        body = text[fm_m.end() :] if fm_m else text
        meta = json.loads(fm_m.group(1)) if fm_m else {}
        url_path = "/" + str(md_file.relative_to(PAGES)).replace("\\", "/").replace(".md", "/")

        prev = meta.get("previous")
        nxt = meta.get("next")
        if prev and prev in url_set:
            edges.append({"from": url_path, "to": prev, "type": "prev"})
        if nxt and nxt in url_set:
            edges.append({"from": url_path, "to": nxt, "type": "next"})

        for link in extract_links(body):
            if link in url_set:
                edges.append({"from": url_path, "to": link, "type": "content"})

    graph = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "entry": "/zh/foundry/data-integration/overview/",
        "node_count": len(nodes),
        "edge_count": len(edges),
        "edge_types": {
            t: sum(1 for e in edges if e["type"] == t)
            for t in sorted({e["type"] for e in edges})
        },
        "nodes": nodes,
        "edges": edges,
    }
    (META / "link-graph.json").write_text(
        json.dumps(graph, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps(graph["edge_types"], ensure_ascii=False))
    print("nodes", graph["node_count"], "edges", graph["edge_count"])


if __name__ == "__main__":
    main()

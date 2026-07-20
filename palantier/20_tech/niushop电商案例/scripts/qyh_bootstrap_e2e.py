# -*- coding: utf-8 -*-
"""
栖月汇全栈 bootstrap（临时脚本 · 代手工）：
  Org/测试工作区 → JDBC 数据操作系统 → Ontology(OT/Link/边) → Inbox Module
  → Action/Draft → AIP Tool/Chat → Funnel/Schedule

零行业定制码：仅调通用 /v1/* API。凭据来自案例 .env。

用法:
  python scripts/qyh_bootstrap_e2e.py
  python scripts/qyh_bootstrap_e2e.py --skip-chat
  # 冒烟可加 --limit 30；默认 limit=0 全量孪生
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT / ".env"
REPORT_PATH = ROOT / "fixtures" / "e2e-bootstrap-report.json"
DEFAULT_API = "http://127.0.0.1:8080"

ORG_ID = "org-qyh"
ORG_NAME = "栖月汇"
PROJECT_ID = "qyh-test"
PROJECT_NAME = "测试工作区"
SOURCE_ID = "src-qyh-jdbc"

# table, objectType, idField, zhName
TABLES: list[tuple[str, str, str, str]] = [
    ("ns_site", "Site", "site_id", "站点"),
    ("ns_weapp", "Weapp", "weapp_id", "小程序端"),
    ("ns_member", "Member", "member_id", "会员"),
    ("ns_member_level", "MemberLevel", "level_id", "会员等级"),
    ("ns_member_address", "MemberAddress", "id", "会员地址"),
    ("ns_goods", "Goods", "goods_id", "商品"),
    ("ns_goods_sku", "GoodsSku", "sku_id", "商品SKU"),
    ("ns_goods_weapp", "GoodsWeapp", "id", "商品端可见"),
    ("ns_goods_category", "GoodsCategory", "category_id", "商品分类"),
    ("ns_order", "Order", "order_id", "订单"),
    ("ns_order_goods", "OrderLine", "order_goods_id", "订单行"),
    ("ns_pay", "Payment", "id", "支付"),
    ("ns_store", "Store", "store_id", "门店"),
    ("ns_express_delivery_package", "ExpressPackage", "id", "快递包裹"),
]

LINK_TYPES = [
    {
        "id": "lt-order-member",
        "name": "订单归属会员",
        "srcType": "Order",
        "dstType": "Member",
        "rel": "placedBy",
        "cardinality": "MANY_TO_ONE",
        "published": True,
    },
    {
        "id": "lt-orderline-order",
        "name": "订单行归属订单",
        "srcType": "OrderLine",
        "dstType": "Order",
        "rel": "lineOf",
        "cardinality": "MANY_TO_ONE",
        "published": True,
    },
    {
        "id": "lt-orderline-sku",
        "name": "订单行指向SKU",
        "srcType": "OrderLine",
        "dstType": "GoodsSku",
        "rel": "forSku",
        "cardinality": "MANY_TO_ONE",
        "published": True,
    },
    {
        "id": "lt-sku-goods",
        "name": "SKU归属商品",
        "srcType": "GoodsSku",
        "dstType": "Goods",
        "rel": "skuOf",
        "cardinality": "MANY_TO_ONE",
        "published": True,
    },
]


def load_env(path: Path) -> dict[str, str]:
    data: dict[str, str] = {
        "NIUSHOP_DB_HOST": "127.0.0.1",
        "NIUSHOP_DB_PORT": "13306",
        "NIUSHOP_DB_USER": "niushop",
        "NIUSHOP_DB_NAME": "niushop_b2c_v5",
        "AOS_API_BASE": DEFAULT_API,
        "AOS_BEARER": "dev",
        "AOS_ORG_ID": ORG_ID,
        "AOS_PROJECT_ID": PROJECT_ID,
    }
    if not path.is_file():
        raise SystemExit(f"缺少 {path}")
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        data[k.strip()] = v.strip().strip('"').strip("'")
    if not data.get("NIUSHOP_DB_PASSWORD"):
        raise SystemExit("NIUSHOP_DB_PASSWORD 未设置")
    return data


def conn_payload(cfg: dict[str, str]) -> dict[str, Any]:
    return {
        "host": cfg["NIUSHOP_DB_HOST"],
        "port": int(cfg["NIUSHOP_DB_PORT"]),
        "user": cfg["NIUSHOP_DB_USER"],
        "password": cfg["NIUSHOP_DB_PASSWORD"],
        "database": cfg["NIUSHOP_DB_NAME"],
    }


class Api:
    def __init__(self, base: str, bearer: str, org: str, project: str):
        self.base = base.rstrip("/")
        self.bearer = bearer
        self.org = org
        self.project = project

    def call(
        self,
        method: str,
        path: str,
        body: dict[str, Any] | None = None,
        *,
        org: str | None = None,
        project: str | None = None,
        ignore_http: set[int] | None = None,
    ) -> dict[str, Any]:
        url = self.base + path
        data = None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Authorization": f"Bearer {self.bearer}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "X-Org-Id": org or self.org,
                "X-Project-Id": project or self.project,
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                raw = resp.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")
            if ignore_http and exc.code in ignore_http:
                try:
                    return json.loads(detail) if detail else {"ok": False, "http": exc.code}
                except json.JSONDecodeError:
                    return {"ok": False, "http": exc.code, "detail": detail[:300]}
            raise RuntimeError(f"{method} {path} → HTTP {exc.code}: {detail[:600]}") from exc
        except urllib.error.URLError as exc:
            raise RuntimeError(f"{method} {path} → 无法连接 {self.base}: {exc}") from exc


def redact(obj: Any) -> Any:
    if isinstance(obj, dict):
        return {
            k: ("***" if str(k).lower() in {"password", "passwd"} else redact(v))
            for k, v in obj.items()
        }
    if isinstance(obj, list):
        return [redact(x) for x in obj]
    return obj


def step_org(api: Api, report: dict[str, Any]) -> None:
    # bootstrap from default tenant
    created = api.call(
        "POST",
        "/v1/orgs",
        {"name": ORG_NAME, "id": ORG_ID},
        org="dev-org",
        project="dev-project",
        ignore_http={409, 400},
    )
    report["org"] = created
    ws = api.call(
        "POST",
        "/v1/workspaces",
        {"name": PROJECT_NAME, "id": PROJECT_ID},
        org=ORG_ID,
        project="dev-project",
        ignore_http={400, 409, 403},
    )
    report["workspace"] = ws
    api.call("POST", f"/v1/orgs/{ORG_ID}/enter", {}, org=ORG_ID, project=PROJECT_ID, ignore_http={403, 400})
    api.call(
        "POST",
        f"/v1/workspaces/{PROJECT_ID}/enter",
        {},
        org=ORG_ID,
        project=PROJECT_ID,
        ignore_http={400, 403, 404},
    )
    me = api.call("GET", "/v1/me", org=ORG_ID, project=PROJECT_ID)
    report["me"] = me
    print(f"[ok] org={ORG_ID} workspace={PROJECT_ID} me.org={me.get('orgId')}")


def step_ontology_types(api: Api, report: dict[str, Any]) -> None:
    ots = []
    for _, ot, _, zh in TABLES:
        body = {
            "id": ot,
            "name": zh,
            "description": f"QYH twin OT {ot}",
            "properties": [],
            "publish": False,
        }
        r = api.call("POST", "/v1/ontology/object-types", body, ignore_http={400, 422})
        ots.append({"id": ot, "result": "exists_or_created", "lintOk": (r.get("lint") or {}).get("ok")})
    report["objectTypes"] = ots
    lts = []
    for lt in LINK_TYPES:
        body_lt = {**lt, "published": False}
        r = api.call("POST", "/v1/ontology/link-types", body_lt, ignore_http={400, 422})
        lts.append({"id": lt["id"], "status": "ok_or_exists", "httpHint": r.get("code")})
    report["linkTypes"] = lts
    print(f"[ok] OT={len(ots)} LinkType={len(lts)}")


def step_data_os(api: Api, cfg: dict[str, str], limit: int, report: dict[str, Any]) -> None:
    api.call("POST", "/v1/sources", {"id": SOURCE_ID, "type": "jdbc-mysql"}, ignore_http={400})
    tables_out: dict[str, Any] = {}
    for table, ot, id_field, zh in TABLES:
        pipe_id = f"pipe-qyh-{table}"
        api.call(
            "POST",
            "/v1/pipelines",
            {
                "id": pipe_id,
                "sourceId": SOURCE_ID,
                "datasetRid": f"ri.dataset.qyh.{table}",
                "objectTypeHint": ot,
                "displayName": zh,
                "name": zh,
            },
            ignore_http={400},
        )
        api.call(
            "PATCH",
            f"/v1/datasets/ri.dataset.qyh.{table}",
            {"objectTypeHint": ot, "displayName": zh, "name": zh},
            ignore_http={404, 400},
        )
        api.call(
            "POST",
            "/v1/syncs",
            {"id": f"sync-qyh-{table}", "sourceId": SOURCE_ID},
            ignore_http={400},
        )
        body = {
            **conn_payload(cfg),
            "table": table,
            "objectType": ot,
            "idField": id_field,
            "includeAll": True,
            "autoCreateObjectType": True,
            "limit": limit,
        }
        # 探活只采少量；ingest 用 limit（0=全量孪生），避免全表拉两次
        probe_body = {**body, "limit": 5 if limit <= 0 else min(limit, 5)}
        probe = api.call("POST", "/v1/connectors/jdbc-mysql/probe", probe_body)
        ingest = {"skipped": True}
        if probe.get("ok") and probe.get("mode") == "live":
            ingest = api.call("POST", "/v1/connectors/jdbc-mysql/ingest", body)
            print(
                f"[ok] {table} → {ot} written={ingest.get('written')}"
                f" tableRowCount={ingest.get('tableRowCount')} full={ingest.get('fullTable')}"
            )
        else:
            print(f"[fail] probe {table}: {probe.get('detail') or probe.get('mode')}")
        tables_out[table] = {
            "objectType": ot,
            "probe": {"ok": probe.get("ok"), "rows": probe.get("rowsSampled"), "detail": probe.get("detail")},
            "ingest": {
                "ok": ingest.get("ok"),
                "written": ingest.get("written"),
                "mode": ingest.get("mode"),
            },
        }
    report["tables"] = tables_out


def step_links(api: Api, limit: int, report: dict[str, Any]) -> None:
    """Build edges from ingested Order/OrderLine samples via object list."""
    orders = api.call("GET", "/v1/objects/Order")
    lines = api.call("GET", "/v1/objects/OrderLine")
    skus = api.call("GET", "/v1/objects/GoodsSku")
    order_items = (orders.get("items") or [])[:limit]
    line_items = (lines.get("items") or [])[:limit]
    edges: list[dict[str, str]] = []
    for o in order_items:
        # list_objects flattens props onto item
        mid = o.get("member_id")
        oid = o.get("id") or o.get("objectId")
        if mid is not None and oid is not None:
            edges.append(
                {
                    "srcType": "Order",
                    "srcId": str(oid),
                    "rel": "placedBy",
                    "dstType": "Member",
                    "dstId": str(mid),
                }
            )
    sku_ids = {
        str(s.get("id") or s.get("objectId"))
        for s in (skus.get("items") or [])
        if s.get("id") or s.get("objectId")
    }
    for ln in line_items:
        lid = ln.get("id") or ln.get("objectId")
        oid = ln.get("order_id")
        sid = ln.get("sku_id")
        if lid is None:
            continue
        if oid is not None:
            edges.append(
                {
                    "srcType": "OrderLine",
                    "srcId": str(lid),
                    "rel": "lineOf",
                    "dstType": "Order",
                    "dstId": str(oid),
                }
            )
        if sid is not None and str(sid) in sku_ids:
            edges.append(
                {
                    "srcType": "OrderLine",
                    "srcId": str(lid),
                    "rel": "forSku",
                    "dstType": "GoodsSku",
                    "dstId": str(sid),
                }
            )
    if edges:
        r = api.call("POST", "/v1/ontology/edges", {"edges": edges[:500]})
        report["edges"] = {"submitted": r.get("submitted"), "sample": len(edges)}
        print(f"[ok] graph edges submitted={r.get('submitted')}")
    else:
        report["edges"] = {"submitted": 0, "note": "no samples to link"}
        print("[warn] no edges built")


def step_workbench(api: Api, report: dict[str, Any]) -> None:
    mod = api.call(
        "POST",
        "/v1/modules",
        {
            "name": "订单 Inbox",
            "description": "栖月汇测试工作区 · Order 态势收件",
            "objectType": "Order",
            "entryPath": "/workbench/inbox",
            "widgets": [{"type": "objectList", "objectType": "Order"}],
            "buddyBound": True,
            "markings": ["public"],
        },
        ignore_http={400},
    )
    report["module"] = {"id": mod.get("id"), "objectType": mod.get("objectType") or "Order"}
    funnel = api.call("GET", "/v1/funnel/Order/status", ignore_http={404})
    report["funnelOrder"] = funnel
    print(f"[ok] module Inbox objectType=Order funnel={funnel.get('stage')}")


def step_aip(api: Api, cfg: dict[str, str], limit: int, skip_chat: bool, report: dict[str, Any]) -> None:
    act = api.call(
        "POST",
        "/v1/actions/types",
        {
            "id": "AnnotateOrder",
            "name": "标注订单",
            "objectType": "Order",
            "parameters": [{"name": "note", "type": "string"}],
            "requiredMarkings": [],
            "submissionCriteria": [],
        },
        ignore_http={400},
    )
    report["actionType"] = {"id": act.get("id") or "AnnotateOrder"}
    orders = api.call("GET", "/v1/objects/Order")
    items = orders.get("items") or []
    oid = None
    if items:
        oid = str(items[0].get("id") or items[0].get("objectId"))
    draft = {}
    if oid:
        draft = api.call(
            "POST",
            "/v1/aip/drafts",
            {
                "actionTypeId": "AnnotateOrder",
                "objectType": "Order",
                "objectId": oid,
                "title": "孪生标注：跟进订单",
                "proposed": {"note": "QYH E2E bootstrap draft"},
            },
            ignore_http={400, 422},
        )
    report["draft"] = {
        "id": draft.get("id"),
        "status": draft.get("status"),
        "objectId": oid,
    }
    tools = api.call("GET", "/v1/aip/tools")
    report["tools"] = {"count": len(tools.get("items") or tools.get("tools") or [])}
    if not skip_chat:
        chat = api.call(
            "POST",
            "/v1/aip/chat",
            {"message": "列出当前工作区订单对象类型 Order 的用途（简短）", "toolsEnabled": True},
            ignore_http={400, 500, 502, 503},
        )
        report["chat"] = {
            "ok": "error" not in chat or chat.get("reply") or chat.get("message"),
            "keys": list(chat.keys())[:12],
        }
    sch = api.call(
        "POST",
        "/v1/schedules",
        {
            "id": "sch-qyh-order",
            "name": "订单短周期拉数",
            "cron": "*/15 * * * *",
            "pipelineId": "pipe-qyh-ns_order",
            "enabled": True,
            "ingest": {
                "pluginId": "jdbc-mysql",
                **conn_payload(cfg),
                "table": "ns_order",
                "objectType": "Order",
                "idField": "order_id",
                "includeAll": True,
                "autoCreateObjectType": True,
                "limit": limit,
            },
        },
        ignore_http={400},
    )
    run = api.call("POST", f"/v1/schedules/{sch.get('id') or 'sch-qyh-order'}/run", ignore_http={400, 404})
    report["schedule"] = {"id": sch.get("id"), "lastRun": run.get("lastRun")}
    print(
        f"[ok] AIP draft={draft.get('id')} tools~={report['tools']['count']} "
        f"schedule_run written={(run.get('lastRun') or {}).get('written')}"
    )


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--api", default=None)
    ap.add_argument(
        "--limit",
        type=int,
        default=0,
        help="每表 ingest 行数上限；0=全量孪生（默认）。>0 仅冒烟/调试",
    )
    ap.add_argument("--skip-chat", action="store_true")
    ap.add_argument("--skip-ingest", action="store_true", help="只跑 Org/OT/AIP（调试）")
    args = ap.parse_args()

    cfg = load_env(ENV_PATH)
    base = (args.api or cfg.get("AOS_API_BASE") or DEFAULT_API).rstrip("/")
    bearer = cfg.get("AOS_BEARER") or "dev"
    org = cfg.get("AOS_ORG_ID") or ORG_ID
    project = cfg.get("AOS_PROJECT_ID") or PROJECT_ID
    api = Api(base, bearer, org, project)

    report: dict[str, Any] = {
        "at": datetime.now(timezone.utc).isoformat(),
        "api": base,
        "orgId": org,
        "projectId": project,
        "limit": args.limit,
    }
    print(f"E2E bootstrap api={base} org={org} project={project}")

    try:
        health = api.call("GET", "/v1/health", org="dev-org", project="dev-project")
        report["health"] = health
    except RuntimeError as exc:
        print(f"[fail] API: {exc}", file=sys.stderr)
        return 2

    fails = 0
    try:
        step_org(api, report)
        step_ontology_types(api, report)
        if not args.skip_ingest:
            step_data_os(api, cfg, args.limit, report)
            step_links(api, args.limit, report)
        step_workbench(api, report)
        step_aip(api, cfg, args.limit, args.skip_chat, report)
    except RuntimeError as exc:
        fails += 1
        report["error"] = str(exc)
        print(f"[fail] {exc}", file=sys.stderr)

    # summary fail count from tables
    for t, detail in (report.get("tables") or {}).items():
        if not (detail.get("ingest") or {}).get("ok"):
            fails += 1

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(json.dumps(redact(report), ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"report → {REPORT_PATH}")
    if fails:
        print(f"完成但有失败项 count≈{fails}", file=sys.stderr)
        return 1
    print("QYH E2E bootstrap OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

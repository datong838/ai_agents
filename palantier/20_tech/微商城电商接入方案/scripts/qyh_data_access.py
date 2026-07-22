# -*- coding: utf-8 -*-
"""
栖月汇 QYH.1：脚本代手工 — 经 AOS 真实 API 完成 JDBC 探活 / Source·Pipeline·Sync 注册 / 分表 ingest。

前置：
  1. SSH 隧道：本机 13306 → 远端 MySQL（案例 .env）
  2. aos-api 已起（默认 http://127.0.0.1:8080），AOS_AUTH_ALLOW_DEV=1
  3. 可选：先跑 apply_aos_mysql_env.ps1（本脚本请求体自带连接覆盖，可不依赖平台 .env）

用法（在案例目录或本目录）:
  python scripts/qyh_data_access.py
  python scripts/qyh_data_access.py --limit 20 --dry-run
  python scripts/qyh_data_access.py --tables ns_order,ns_goods

原则：零行业定制码；仅调通用 /v1/sources|/v1/pipelines|/v1/syncs|/v1/connectors/jdbc-mysql/*
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
REPORT_PATH = ROOT / "fixtures" / "bootstrap-report.json"
DEFAULT_API = "http://127.0.0.1:8080"

# T0～T6 MVP 关键表（案例 00 §3 / §4）；路径 A 分表，非 Join
QYH_MVP_TABLES: list[tuple[str, str, str]] = [
    ("ns_site", "Site", "site_id"),
    ("ns_weapp", "Weapp", "weapp_id"),
    ("ns_member", "Member", "member_id"),
    ("ns_member_level", "MemberLevel", "level_id"),
    ("ns_member_address", "MemberAddress", "id"),
    ("ns_goods", "Goods", "goods_id"),
    ("ns_goods_sku", "GoodsSku", "sku_id"),
    ("ns_goods_weapp", "GoodsWeapp", "id"),
    ("ns_goods_category", "GoodsCategory", "category_id"),
    ("ns_order", "Order", "order_id"),
    ("ns_order_goods", "OrderLine", "order_goods_id"),
    ("ns_pay", "Payment", "id"),
    ("ns_store", "Store", "store_id"),
    ("ns_express_delivery_package", "ExpressPackage", "id"),
]

SOURCE_ID = "src-qyh-jdbc"


def load_env(path: Path) -> dict[str, str]:
    data: dict[str, str] = {
        "NIUSHOP_DB_HOST": "127.0.0.1",
        "NIUSHOP_DB_PORT": "13306",
        "NIUSHOP_DB_USER": "niushop",
        "NIUSHOP_DB_NAME": "niushop_b2c_v5",
        "AOS_API_BASE": DEFAULT_API,
        "AOS_BEARER": "dev",
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


def api_json(
    base: str,
    method: str,
    path: str,
    bearer: str,
    body: dict[str, Any] | None = None,
    *,
    org_id: str = "org-qyh",
    project_id: str = "qyh-test",
) -> dict[str, Any]:
    url = base.rstrip("/") + path
    data = None if body is None else json.dumps(body, ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={
            "Authorization": f"Bearer {bearer}",
            "Content-Type": "application/json",
            "Accept": "application/json",
            "X-Org-Id": org_id,
            "X-Project-Id": project_id,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            raw = resp.read().decode("utf-8")
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"{method} {path} → HTTP {exc.code}: {detail[:500]}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"{method} {path} → 无法连接 API ({base}): {exc}") from exc


def redact(obj: Any) -> Any:
    """报告中去掉 password。"""
    if isinstance(obj, dict):
        out = {}
        for k, v in obj.items():
            if str(k).lower() in {"password", "passwd"}:
                out[k] = "***"
            else:
                out[k] = redact(v)
        return out
    if isinstance(obj, list):
        return [redact(x) for x in obj]
    return obj


def ensure_source(base: str, bearer: str, report: dict[str, Any]) -> None:
    try:
        item = api_json(
            base,
            "POST",
            "/v1/sources",
            bearer,
            {"id": SOURCE_ID, "type": "jdbc-mysql"},
        )
        report["source"] = item
        print(f"[ok] source registered id={SOURCE_ID}")
    except RuntimeError as exc:
        # 重复注册可能 4xx；列出已有则继续
        listed = api_json(base, "GET", "/v1/sources", bearer)
        ids = [x.get("id") for x in (listed.get("items") or [])]
        if SOURCE_ID in ids:
            report["source"] = {"id": SOURCE_ID, "status": "already_present"}
            print(f"[ok] source already present id={SOURCE_ID}")
        else:
            raise exc


def ensure_pipeline_sync(base: str, bearer: str, table: str, report_tables: dict[str, Any]) -> None:
    pipe_id = f"pipe-qyh-{table}"
    try:
        pipe = api_json(
            base,
            "POST",
            "/v1/pipelines",
            bearer,
            {"id": pipe_id, "sourceId": SOURCE_ID, "datasetRid": f"ri.dataset.qyh.{table}"},
        )
    except RuntimeError:
        pipe = {"id": pipe_id, "status": "already_or_error_continue"}
    try:
        sync = api_json(
            base,
            "POST",
            "/v1/syncs",
            bearer,
            {"id": f"sync-qyh-{table}", "sourceId": SOURCE_ID},
        )
    except RuntimeError:
        sync = {"status": "skip"}
    report_tables[table] = {**(report_tables.get(table) or {}), "pipeline": pipe, "sync": sync}


def probe_ingest_table(
    base: str,
    bearer: str,
    cfg: dict[str, str],
    table: str,
    object_type: str,
    id_field: str,
    limit: int,
    dry_run: bool,
) -> dict[str, Any]:
    body = {
        **conn_payload(cfg),
        "table": table,
        "objectType": object_type,
        "limit": limit,
        "includeAll": True,
        "idField": id_field,
        "autoCreateObjectType": True,
    }
    probe_body = {**body, "limit": 5 if limit <= 0 else min(limit, 5)}
    probe = api_json(base, "POST", "/v1/connectors/jdbc-mysql/probe", bearer, probe_body)
    result: dict[str, Any] = {
        "objectType": object_type,
        "idField": id_field,
        "probe": {
            "ok": probe.get("ok"),
            "mode": probe.get("mode"),
            "rowsSampled": probe.get("rowsSampled"),
            "tableRowCount": probe.get("tableRowCount"),
            "table": probe.get("table"),
            "detail": probe.get("detail"),
        },
    }
    if not probe.get("ok") or probe.get("mode") != "live":
        print(f"[fail] probe {table}: {probe.get('detail') or probe.get('mode')}")
        return result
    print(f"[ok] probe {table} sample={probe.get('rowsSampled')} tableRowCount={probe.get('tableRowCount')}")
    if dry_run:
        result["ingest"] = {"skipped": True, "reason": "dry-run"}
        return result
    ingest = api_json(base, "POST", "/v1/connectors/jdbc-mysql/ingest", bearer, body)
    result["ingest"] = {
        "ok": ingest.get("ok"),
        "mode": ingest.get("mode"),
        "written": ingest.get("written"),
        "tableRowCount": ingest.get("tableRowCount"),
        "fullTable": ingest.get("fullTable"),
        "objectType": ingest.get("objectType"),
        "detail": ingest.get("detail"),
    }
    print(
        f"[ok] ingest {table} written={ingest.get('written')} "
        f"tableRowCount={ingest.get('tableRowCount')} → {object_type}"
    )
    return result


def main() -> int:
    ap = argparse.ArgumentParser(description="栖月汇 JDBC 数据接入脚本（代手工）")
    ap.add_argument("--api", default=None, help="AOS API base，默认 .env AOS_API_BASE 或 :8080")
    ap.add_argument(
        "--limit",
        type=int,
        default=0,
        help="每表 probe/ingest 行数上限；0=全量（默认）。>0 仅冒烟",
    )
    ap.add_argument("--dry-run", action="store_true", help="只 probe + 注册，不 ingest")
    ap.add_argument(
        "--tables",
        default="",
        help="逗号分隔表名；默认 T0～T6 MVP 全表",
    )
    args = ap.parse_args()

    cfg = load_env(ENV_PATH)
    base = (args.api or cfg.get("AOS_API_BASE") or DEFAULT_API).rstrip("/")
    bearer = cfg.get("AOS_BEARER") or "dev"

    wanted = {t.strip() for t in args.tables.split(",") if t.strip()}
    tables = [t for t in QYH_MVP_TABLES if not wanted or t[0] in wanted]
    if not tables:
        raise SystemExit("--tables 无匹配项")

    report: dict[str, Any] = {
        "at": datetime.now(timezone.utc).isoformat(),
        "api": base,
        "sourceId": SOURCE_ID,
        "connection": {
            "host": cfg["NIUSHOP_DB_HOST"],
            "port": int(cfg["NIUSHOP_DB_PORT"]),
            "database": cfg["NIUSHOP_DB_NAME"],
            "user": cfg["NIUSHOP_DB_USER"],
        },
        "dryRun": args.dry_run,
        "limit": args.limit,
        "tables": {},
    }

    print(f"API={base} db={cfg['NIUSHOP_DB_NAME']}@{cfg['NIUSHOP_DB_HOST']}:{cfg['NIUSHOP_DB_PORT']}")
    print(f"tables={len(tables)} dry_run={args.dry_run} limit={args.limit}")

    try:
        health = api_json(base, "GET", "/v1/connectors/jdbc-mysql/health", bearer)
        report["connectorHealth"] = health
        print(f"[ok] connector health pluginId={health.get('pluginId')}")
    except RuntimeError as exc:
        print(f"[fail] API/health: {exc}", file=sys.stderr)
        return 2

    ensure_source(base, bearer, report)

    fails = 0
    for table, object_type, id_field in tables:
        ensure_pipeline_sync(base, bearer, table, report["tables"])
        try:
            detail = probe_ingest_table(
                base, bearer, cfg, table, object_type, id_field, args.limit, args.dry_run
            )
            report["tables"][table] = {**(report["tables"].get(table) or {}), **detail}
            if not (detail.get("probe") or {}).get("ok"):
                fails += 1
            elif not args.dry_run and not (detail.get("ingest") or {}).get("ok"):
                fails += 1
        except RuntimeError as exc:
            fails += 1
            report["tables"][table] = {
                **(report["tables"].get(table) or {}),
                "error": str(exc),
            }
            print(f"[fail] {table}: {exc}", file=sys.stderr)

    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
    REPORT_PATH.write_text(
        json.dumps(redact(report), ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"report → {REPORT_PATH}")
    if fails:
        print(f"完成但有 {fails} 表失败", file=sys.stderr)
        return 1
    print("QYH.1 bootstrap OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

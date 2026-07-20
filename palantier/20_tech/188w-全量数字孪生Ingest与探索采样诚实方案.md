# 188w · 全量数字孪生 Ingest 与探索采样诚实方案

| 字段 | 内容 |
|------|------|
| 状态 | ✅ **v1.0** · 已编码 |
| 版本 | **v1.0** · 2026-07-20 |
| 对齐 | [182w](182w-外部数据源数字孪生与全栈能力验证方案.md) · [05](../05-数据集成Connectors-Pipeline-Dataset产品方案.md) · 上线态禁演示限流 |
| 触发 | 用户确认：数字孪生要**全量真实**；探索页「8 行」不可冒充库容 |

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 上线态 · 禁临时代码 | 产品面与默认 ingest **不做** `--limit 40` 演示夹具 |
| 方案先行 | 先定 limit 语义与 UI 文案，再改代码 |
| 最小更改 | 修 JDBC limit=0；bootstrap 默认全量；探索页诚实采样 |

---

## 1. 问题分层

| 层 | 现状 | 目标 |
|----|------|------|
| **探索 UI** | `limit:8` + 切 6 列 +「刷新采样」却显示成「8 行」像全量 | **采样预览**：显示 N 行样本 + **库内总数**；列不无故砍到 6 |
| **Ingest** | bootstrap `--limit 40`；API `limit or 100` 使 `0` 失效 | **默认全量**（`limit<=0` = 无 SQL LIMIT） |
| **调度** | schedule ingest 同带 limit | 全量孪生时 schedule 亦 `limit:0` |

红线：**采样只存在于「探索/预览」读路径**；写路径（ingest / schedule run）默认全量。

---

## 2. 平台语义（JDBC）

| API / 参数 | 语义 |
|------------|------|
| `POST .../ingest` · `limit` 省略或 `≤0` | **全表** `SELECT *` → 全量 upsert |
| `POST .../ingest` · `limit>0` | 仅调试/冒烟封顶（显式） |
| `POST .../probe` · 默认 `5` | 探活采样；`≤0` 亦全表（慎用） |
| 响应 | 增加 `tableRowCount`（`COUNT(*)`）便于 UI 诚实展示 |

修复点：`wave_ext` 中 `int(body.get("limit") or 100)` —— `0` 被当成缺省，**必须改为显式解析**。

超时：全量拉数时放宽 `read_timeout`（探活仍短超时）。

---

## 3. 案例脚本（栖月汇）

| 项 | 变更 |
|----|------|
| `qyh_bootstrap_e2e.py` | `--limit` **默认 `0`（全量）**；文档注明 `>0` 仅冒烟 |
| `qyh_data_access.py` | 默认 `0` |
| `README.md` | 一键命令改为全量；去掉「临时演示 limit 40」口径 |

脚本仍是「代手工」配置夹具，**数据本身必须是线上全量**，不是演示子集。

---

## 4. 产品 UI

| 页 | 变更 |
|----|------|
| Source 探索 | 文案：`采样预览 · 显示 N 行（库内共 M）`；列展示放宽；刷新真正重拉采样 |
| 数据集预览 | 保持分页/limit 读预览，但标明预览且用 `total` |

---

## 5. 验收

- [x] `limit=0` 语义：API 不再把 0 吃成 100；probe 无 SQL LIMIT
- [x] 探索页文案：采样预览 + 库内 total（analytics total 用 query 总数）
- [x] bootstrap / data_access 默认 `--limit 0`；README 全量口径
- [x] 索引挂 188w
- [x] 线上重跑栖月汇全量 ingest（需隧道 + API 重启）· 人工验收 written≈COUNT(*)
  - 证据：`ns_order` written=167=tableRowCount · `ns_order_goods` 216 · schedule_run 167 · 2026-07-20

## 6. 风险

| 风险 | 缓解 |
|------|------|
| 大表一次进内存 | 中小电商表可接受；后续再加游标分批（本波不做） |
| 全量超时 | ingest 连接拉长 read/write timeout |
| 误操作全量 | 产品默认即孪生全量；冒烟用显式 `--limit N` |

*v1.0 · w1*

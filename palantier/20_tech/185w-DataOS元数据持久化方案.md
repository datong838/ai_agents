# 185w · Data OS 元数据持久化方案（Source / Sync / Pipeline / Dataset）

| 字段 | 内容 |
|------|------|
| 状态 | ✅ **v1.2** · list 租户过滤 |
| 版本 | **v1.2** · 2026-07-20 |
| 分支 | **`w1`** |
| 触发 | 重启后数据连接/数据集清空；产品面出现 `demo-file-wo` 演示垃圾 |
| 对齐 | [75](75-去演示端面壳方案.md) · [164](164-TWA10-组织工作区创建与邀请审批方案.md) v1.1 · [182w](182w-外部数据源数字孪生与全栈能力验证方案.md) · production-ui-no-temp |

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 中文 · 先方案后编码 | 本文后改 `wave_ext` / 新 store |
| 上线态 | 可注册的 Source/Pipeline **真持久化**；禁止内存冒充交付 |
| 最小更改 | 写穿 PG + 启动 load；API 路径不变 |
| 去演示 | 默认 **不** 自动种 `demo-file-wo`；仅 `AOS_DEMO_DATA_SEED=1` 或 demo story `force` |

---

## 1. 问题

| 层 | 现状 | 重启后 |
|----|------|--------|
| Org / 工作区 / 成员 | PG（164 v1.1） | ✅ 保留 |
| Source / Sync / Pipeline / Dataset / Schedule | `wave_ext` 进程字典 | ❌ 清空 |
| 演示种子 | `list_pipelines` 自动 `ensure_demo_data_seed` | 污染正式数据连接页 |

硬约束（用户已决）：**以后不允许再出现丢数据 / 没持久化。**

---

## 2. 目标 / 非目标

### 2.1 目标

1. `meta_source` · `meta_pipeline` · `meta_dataset` · `meta_sync` · `meta_schedule` · `meta_dataset_history` 落 PG。  
2. 启动 `boot_data_os()`：schema → load → **clear demo surface**（除非显式开种子）。  
3. create/patch 写穿；list 读内存缓存（与 tenant_catalog 同模式）。  
4. DoD：注册 Source+Pipeline → 重启 API → `/v1/sources` `/v1/datasets` 仍在。  
5. 产品默认无 `demo-file-wo`。

### 2.2 非目标（本刀）

- CDC 全表行级湖仓持久化（obj_instance 已在 PG；本刀只管 **接入元数据**）  
- Schedule 真 cron 守护进程（保留 `/run` 点跑）  

### 2.3 补刀（v1.2）· list 按租户过滤

185w 初版「list 先不过滤」已不够：多组织切换后数据连接页会串源。  
**目标**：`GET /v1/sources`（及同面 Pipeline/Dataset/Sync/Schedule list）按 `principal.org_id` 过滤；无 `orgId` 的历史行视为 **legacy 可见于当前 org**（兼容旧内存种子），不跨 org 泄漏带戳行。

| API | 过滤键 |
|-----|--------|
| `/v1/sources` | `orgId` |
| `/v1/pipelines` | 经 `sourceId` → source.`orgId`；pipeline 自身无 org 时跟 source |
| `/v1/datasets` | 经 `sourceId`；无则放行当前（legacy） |
| `/v1/syncs` | 经 `sourceId` |
| `/v1/schedules` | `orgId`（create 已戳） |

---

## 3. 表设计（摘要）

| 表 | PK | 要点 |
|----|-----|------|
| `meta_source` | `id` | type, status, plugin_id, org_id, project_id, props jsonb |
| `meta_pipeline` | `id` | source_id, dataset_rid, last_build jsonb, object_type_hint, name |
| `meta_dataset` | `rid` | name, pipeline_id, source_id, status, object_type_hint, display_name |
| `meta_sync` | `id` | source_id, status, rows_synced, started_at, finished_at |
| `meta_schedule` | `id` | cron, pipeline_id, enabled, name, ingest jsonb, last_run jsonb |
| `meta_dataset_history` | bigserial | dataset_rid, payload jsonb |

凭据不入库（继续 env / 请求体覆盖）。

---

## 4. 工程落点

| 文件 | 变更 |
|------|------|
| `aos_api/data_os_store.py` | schema / load / persist / boot |
| `aos_api/routers/wave_ext.py` | 写穿；去 list 自动 demo seed；`clear_demo_data_surface` |
| `aos_api/main.py` | lifespan 调 `boot_data_os` |
| 测试 | 重启型或 persist roundtrip；demo story `force=True` |

---

## 5. 与清理刀衔接

本刀编码前已执行：修 `org-qyh` 名；删 `org-a`/`org-b`；废止 A/B 种子；停用默认 demo 播种。

---

## 6. 验收

- [x] 无 `AOS_DEMO_DATA_SEED` 时产品面无 `demo-file-wo`（boot 清 surface + 默认 skip seed）  
- [x] create Source/Pipeline/Sync/Schedule/Dataset 写穿 PG（`_persist_safe`）  
- [x] `org-qyh` →「栖月汇」；产品种子废止 org-a/org-b  
- [x] 重启 API 后自建 Source 仍在（`src-restart-probe` 验收）  
- [x] pytest：`test_data_os_store_185` · `test_twa9` · `test_twa10`（13 passed）  
- [x] list 按 orgId 过滤（`src-qyh-jdbc` 仅 org-qyh 可见；单测 `test_sources_list_filtered_by_org`）  
- [x] qyh_bootstrap_e2e 写入持久化 Data OS；重启后 Source/14 Pipeline 仍在  

---

## 7. 修订

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-07-20 | 初版：Data OS 元数据 PG 化 |
| v1.1 | 2026-07-20 | 写穿完成；测试夹具补种 A/B；删临时修名脚本 |
| v1.2 | 2026-07-20 | list Source/Pipeline/Dataset/Sync/Schedule 按 orgId 过滤 |

*v1.2 · w1 · 租户 list 过滤*

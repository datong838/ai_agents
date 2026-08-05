# 2026-08-05 · TI-5 C2-B wave_ext Dataset/Media 隔离证据

## 结论

`m1@b249a2d` 完成 TI-5 C2-B：主实现 `4e5d069` 将 `wave_ext` 的 `_datasets` / `_dataset_history` / `_media` / `_media_bytes` 统一使用 `(org_id, project_id, rid)` scoped key；analytics lookup、demo seed、purge、parser/docintel 均显式 TenantScope，`b249a2d` 补齐 Parser 直接单测的 ContextVar scope。`GET /v1/datasets` 运行时真源为 wave_ext Data OS；Phase5 同名 GET 为 `NOT_REACHABLE_DUPLICATE`。C2 总门 GREEN。

## 代码边界

- `services/aos-api/aos_api/routers/wave_ext.py`
- `services/aos-api/aos_api/routers/analytics.py`
- `services/aos-api/aos_api/data_os_store.py`
- `services/aos-api/aos_api/demo/demo_story.py`
- `services/aos-api/aos_api/routers/phase5_datasets.py`（仅文档化 NOT_REACHABLE_DUPLICATE）
- `services/aos-api/tests/tenant_isolation/test_ti5_c2b_wave_ext_scope.py`
- 既有相关回归：`test_analytics_ta4_113.py`、`test_vector_index_104.py`、`test_data_os_store_185.py`、`test_demo_story.py`
- Parser scope 回归：`test_file_parsers.py`

## 验证

| 门 | 结果 |
|---|---|
| C2-B 相关回归（含 analytics/vector/data_os/demo/media） | 80 passed / 1 skipped |
| Parser 专项 | 7 passed |
| Tenant Isolation 累计 | 211 passed / 8 skipped |
| 全量测试收集 | 9,204 collected，零错误 |
| Alembic head | `228ti5b1models`（本波无新迁移） |
| 五工作树 | 本地/远端同 HEAD `b249a2d` / tree `b3f4ddda21a2921122b49223b888cb195aa017a0` |

## 冻结判定

- 同 RID 双 scope Dataset/History/Media bytes 共存，跨 scope 404 / list 不可见。
- parser 读 `mediaRid` 前必须命中本 scope metadata；禁止全局 rid 命中后再过滤。
- demo seed 必须显式 `TenantScope`；内存 demo 写入后标记 `_data_os_loaded_scopes`，避免 hydrate 清掉未落库 demo。
- Phase5 GET `/v1/datasets` 不作为绕过路径；API 去重需单独兼容性评审，本波不改 manifest/operationId。
- `test_domain_router_manifest` runtime baseline `4047 != 4048` 在干净 `a302544` 已失败，与本波无关，登记但不阻断 C2-B。

## 下一门

TI-5 C3：缓存/队列/离线 envelope 与剩余 mutable finding 分类表。

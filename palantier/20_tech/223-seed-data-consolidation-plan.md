# 种子数据统一收敛与去 Mock 化方案

> 版本：v2.3  
> 日期：2026-07-26  
> 状态：🟡 Phase 1-5 完成 / Phase 6 进行中

## 修订记录

- **v2.3 (2026-07-26)**：新增 Phase 6 —— 删除测试专用死代码 + 解耦生产代码对 demo 清理函数的反向依赖
- **v2.2 (2026-07-26)**：新增 Phase 5 —— 适配 14 处 demo 接口调用残留（5 测试文件 + 2 前端文件）
- **v2.1 (2026-07-25)**：明确 `dev-org` / `dev-project` / 默认人员本身是**测试数据**，不在系统启动时创建
- v2.0：初版方案

## Phase 6：测试专用死代码清理 + 生产代码反 demo 解耦（2026-07-26）

### 背景

Phase 5 把测试从 `/v1/demo/*` HTTP 路由切到 Python 函数后，仍残留：
- 2 个无人引用的 shim 文件
- `mock_data.py` 中 7 个无人调用的 CRUD 函数 + 1 个 `_OBJECTS` 列表
- **生产代码** `data_os_store.boot_data_os` 反向调用了 `wave_ext.clear_demo_data_surface`，破坏"线上不依赖 demo"的语义

### 全局盘点结论

| 类别 | 符号 | 引用数 | 处理决策 |
|------|------|--------|---------|
| 🟢 A1 | `aos_api/order_seed.py`（整个 shim） | 0 | 删除文件 |
| 🟢 A2 | `aos_api/demo_story.py`（整个 shim） | 0 | 删除文件 |
| 🟢 A3 | `aos_api/mock_data.py` 中 `list_modules` / `get_module` / `create_module` / `update_module` / `publish_module` / `module_runtime` / `query_objects` | 0 | 删除函数 |
| 🟢 A4 | `aos_api/mock_data.py` 中 `_OBJECTS` 列表 | 0 | 删除 |
| 🟡 B1 | `aos_api/mock_data.py::reset_mock_state` | 28（全为测试 setup） | **不动**（线上 0 引用，已核实） |
| 🟡 B2 | `wave_ext._demo_data_seed_enabled` / `ensure_demo_data_seed` | 测试 + demo_story | 保留 |
| 🔴 C1 | `data_os_store.boot_data_os` → `wave_ext.clear_demo_data_surface` | 1 生产 + 1 测试 | **重构**：把清理逻辑内联到 data_os_store |
| 🔴 C2 | `wave_ext.clear_demo_data_surface` | C1 + test_data_os_store_185 | **删除**（C1 重构后即可删） |

### 核实：reset_mock_state 线上不走

- 32 个引用文件全部位于 `tests/` 或 `aos_api/mock_data.py`（自身定义）
- `aos_api/` 内（生产代码）**0 引用**
- `main.py` 启动流程不调用
- 结论：**纯测试辅助，线上业务 100% 不走**

### 改动清单

#### A. 删除文件（2 个）

| 文件 | 操作 |
|------|------|
| `aos_api/order_seed.py` | 物理删除 |
| `aos_api/demo_story.py` | 物理删除 |

#### B. 精简 `aos_api/mock_data.py`

删除 7 个函数：`list_modules` / `get_module` / `create_module` / `update_module` / `publish_module` / `module_runtime` / `query_objects`  
删除数据：`_OBJECTS` 列表  
保留：`_MODULES` 列表（`reset_mock_state` 维护）、`reset_mock_state` 函数（28 测试 setup 用）  
同时清理 `from copy import deepcopy` 等仅服务于已删函数的 import。

#### C. 重构 `aos_api/data_os_store.py`

| 操作 | 内容 |
|------|------|
| 新增模块常量 | `DEMO_SURFACE_IDS: dict[str, tuple[str, ...]]` —— 已知 demo id 清单（sources/pipelines/datasets/syncs/schedules） |
| 新增 public 函数 | `purge_demo_surface(wave_ext_module) -> dict[str, list[str]]` —— 从 wave_ext 内存 map 删除 demo 条目，返回 removed 清单（替代原 `wave_ext.clear_demo_data_surface`） |
| 修改 `boot_data_os` | 把对 `wave_ext_module.clear_demo_data_surface()` 的调用改为 `_purge_demo_surface(wave_ext_module)`（或 public 入口），其余 PG 删除逻辑不变 |

#### D. 精简 `aos_api/routers/wave_ext.py`

| 操作 | 内容 |
|------|------|
| 删除函数 | `clear_demo_data_surface()` |
| 保留 | `_demo_data_seed_enabled` / `ensure_demo_data_seed`（仍有测试 + demo_story 依赖） |

#### E. 适配测试（1 个）

| 文件 | 改动 |
|------|------|
| `tests/test_data_os_store_185.py` | `wave_ext.clear_demo_data_surface()` → `dos.purge_demo_surface(wave_ext)`（或直接 `data_os_store.purge_demo_surface`） |

### 验证计划

1. `pytest services/aos-api/tests/` 全量回归（重点：test_data_os_store_185、test_vector_index_104、所有 setup 用 reset_mock_state 的测试）
2. 启动后端验证 `/v1/health` 200 + 启动日志无报错
3. `boot_data_os` 仍能正常清理 demo 条目（test_product_surface_has_no_demo_source 验证）

### 验证结果（2026-07-26）

| 验证项 | 结果 |
|--------|------|
| 全局 grep 残留引用（`clear_demo_data_surface` / shim / mock_data CRUD） | ✅ 0 处代码引用（仅余 1 处 docstring 说明） |
| 全量 pytest 回归 | ✅ **7550 passed, 2 skipped**（用时 7 分 13 秒） |
| 运行时验证 `purge_demo_surface` 清理效果 | ✅ 5 类 demo id + 1 dlq 全部清除，wave_ext 内置 map 清空 |
| `wave_ext.clear_demo_data_surface` 已不存在 | ✅ `hasattr False` |
| `mock_data.list_modules` / `_OBJECTS` 已不存在 | ✅ `hasattr False` |
| `mock_data.reset_mock_state` 保留可用 | ✅ `hasattr True` |

### 风险评估

| 风险 | 缓解 |
|------|------|
| `purge_demo_surface` 行为与原 `clear_demo_data_surface` 不一致 | 严格保留原 5 类 id（sources/pipelines/datasets/syncs/schedules）+ dlq 前缀匹配逻辑 |
| `boot_data_os` 启动失败导致服务起不来 | 重构后用单元测试 + 启动验证双重保险 |
| 漏删某处对 shim 的引用导致 ImportError | 已全局 grep 确认 0 引用，删除后再跑一次 grep 校验 |
| mock_data 删函数后影响 reset_mock_state | `reset_mock_state` 仅维护 `_MODULES`，与 `_OBJECTS` 和 7 个 CRUD 函数无依赖，不影响 |

---



## Phase 5：Demo 接口下线后的残留适配（2026-07-26）

### 背景

Phase 2 删除了 6 个 `/v1/demo/*` HTTP 路由，但仍有 **14 处调用残留**没适配：
- 5 个测试文件 14 处直接调用 `/v1/demo/*`（pytest 失败）
- 2 个前端文件 2 处调用 `/v1/demo/*`（被 allSettled/try-catch 兜底，不崩溃但有 404 噪音）

### 核实结论：线上业务逻辑不依赖

- 后端 `aos_api/` 内 `from aos_api ... mock_data|demo_story|order_seed` 返回 **No matches**
- `/v1/demo/*` 全部 404
- `wave_ext.py` 内部残留的 `ensure_demo_data_seed` / `clear_demo_data_surface` / `_demo_data_seed_enabled` 是**内部 Python 函数**（无 HTTP 路由暴露），仅被测试 setup 调用，操作的是 wave_ext 模块级内存状态（`_connectors` / `_pipelines` 等），与"线上接口纯净"不冲突
- 前端两处调用都有兜底，浏览器不崩溃，只是控制台 404 + 对应指标显示 0

### 改动清单

#### A. 新增辅助函数（1 文件）

| 文件 | 改动 |
|------|------|
| `aos_api/demo/demo_story.py` | 新增 `ensure_demo_seed_full()` —— 组合 `seed_test_org()` + `wave_ext.ensure_demo_data_seed(force=True)`，返回与原 `/v1/demo/ensure-seed` HTTP 接口**结构兼容**的 payload（含 `snapshot.dataSurface.{datasets,dlq,syncs,sources,pipelines,builds}`） |

#### B. 测试基础设施（1 文件）

| 文件 | 改动 |
|------|------|
| `tests/conftest.py` | 新增非 autouse 的 `dev_principal` fixture，与 `Bearer dev` + dev-org/dev-project header 解析出的 Principal 完全等价（subject=`user:dev`，roles=`[developer,admin]`，markings=`[public,restricted]`，token_kind=`dev`） |

#### C. 测试改造（5 文件，18 处调用替换）

| 文件 | 测试数 | 改动 |
|------|--------|------|
| `tests/test_demo_story.py` | 4 | `ensure-seed → ensure_demo_seed_full()`；`story → demo_story_payload()`；`run-story → run_writeback_story(p)`；`governance → governance_probe(p)`；`run-capability → run_capability_mirror(p)` |
| `tests/test_analytics_ta7_116.py` | 3 | `ensure-seed → ensure_demo_seed_full()`；`run-analytics-story → run_analytics_story(p)`；`story → demo_story_payload()` |
| `tests/test_analytics_ta8_117.py` | 4 | `ensure-seed → seed_test_org()`；`run-analytics-story → run_analytics_story(p)`；`story → demo_story_payload()` |
| `tests/test_bi_subset_159.py` | 3 | `ensure-seed → seed_test_org()` |
| `tests/test_vector_index_104.py` | 4 | `ensure-seed → seed_test_org()`；`wave_ext.ensure_demo_data_seed(force=True)` 保留不变 |

#### D. 前端清理（2 文件）

| 文件 | 改动 |
|------|------|
| `apps/web/src/overviewMetrics.ts` | 移除 `apiGet("/v1/demo/story")`；`workOrders / pendingDrafts / objectTypePublished` 保持默认 0/false，加 TODO 注释（后续走 `/v1/object-sets/query` 或 `/v1/object-types/WorkOrder` 真实接口） |
| `apps/web/src/pages/s2/aip.tsx` | `loadGovernance()` 函数体替换为静态用户提示「治理探针已迁移到 scripts/demo 脚本」+ TODO 注释，不再发起 HTTP 请求 |

#### E. 不改动项（已知遗留，标 P1）

- `wave_ext.py` 内部 `ensure_demo_data_seed` / `clear_demo_data_surface` / `_demo_data_seed_enabled` 三个函数：**保留**，因为它们操作的是 wave_ext 模块级内存状态，搬迁会破坏现有内存接口的数据来源。后续持久化改造时一并清理。
- `scripts/demo/*.sh` / `*.ps1` / `CUSTOMER-DEMO.md`：会失败但属于辅助脚本，不在本次范围。

### 验证结果（2026-07-26）

| 验证项 | 结果 |
|--------|------|
| 5 个改造测试文件单独跑 | ✅ 18/18 PASSED |
| 全测试套件按 `analytics/demo/bi_subset/vector_index/governance` 关键字过滤跑 | ✅ 81/81 PASSED |
| 全局 grep `/v1/demo/` 实际调用 | ✅ 0 处（仅余注释/docstring/用户提示字符串） |
| 前端 typecheck | ⚠️ 本环境无 node，已做静态类型审查（索引重排、字面量赋值、签名保留）均无 TS 报错风险 |

### 风险评估

| 风险 | 缓解 |
|------|------|
| `ensure_demo_seed_full` 返回结构与原 HTTP 不一致导致测试断言失败 | 严格按原 payload schema 组合（含 dataSurface 嵌套），18 测试 PASSED 证实 |
| Principal 缺少 markings 导致 governance_probe 行为变化 | 显式传入 `markings=["public","restricted"]`，与原 `Bearer dev` 完全等价 |
| 前端指标永久显示 0 | 加 TODO 注释，明确后续走真实接口；不破坏现有 UI 渲染（`EMPTY` 默认就是 0） |

---



## 落地验证（2026-07-25）

执行 `clear_test_org()` → 重启后端 → 执行 `seed_test_org()`，验证结果：

| 验证项 | 结果 |
|--------|------|
| 启动后干净空壳（无 dev-org / 工单 / 订单） | ✅ |
| 启动日志含 `ensure_system_meta_done` | ✅ |
| 启动日志**不**含 `db_seed_workorder_done` / `order_seed` | ✅ |
| `/v1/demo/*` 全部返回 404 | ✅ |
| `/v1/object-sets/query` 无 `source=mock` 参数 | ✅（`source: pg`） |
| `seed_test_org()` 灌入 9 个成员 / 5 条工单 / 20 条订单 / 3 个模块 / 3 个 Action | ✅ |
| `clear_test_org()` 完整清空测试组织数据 | ✅ |
| 前端 SPA 路由 200 | ✅（9/9 路由全部 200） |

## 实施记录（2026-07-25）

### 新增文件

| 文件 | 用途 |
|------|------|
| `aos_api/demo/__init__.py` | 导出 `seed_test_org` / `clear_test_org` |
| `aos_api/demo/seed.py` | 总调度 + 清空逻辑 |
| `aos_api/demo/org_seed.py` | dev-org / dev-project / 人员 |
| `aos_api/demo/workorder_seed.py` | WorkOrder ObjectType + 5 样例 + 关联 + wiki + FGA |
| `aos_api/demo/order_seed.py` | Order + 20 订单 + OrderItem + LinkType |
| `aos_api/demo/module_seed.py` | Workshop 模块 |
| `aos_api/demo/action_seed.py` | Action 模板 |
| `aos_api/demo/demo_story.py` | 演示故事线（仅测试调用，不暴露 HTTP） |
| `scripts/demo/seed-test-org.sh` | 灌入测试组织数据 |
| `scripts/demo/clear-test-org.sh` | 清空测试组织数据 |

### 修改文件

| 文件 | 改动要点 |
|------|---------|
| `aos_api/db.py` | 新增 `ensure_system_meta()`；`seed_if_empty()` 改为兼容入口；`ensure_inherit_openfga_seed` 去掉测试实例数据 |
| `aos_api/main.py` | 启动调 `ensure_system_meta` 替代 `seed_if_empty`；去掉启动期 `seed_modules_if_empty` |
| `aos_api/tenant_catalog.py` | `boot_tenant_catalogs` 只 load，不再灌 dev-org |
| `aos_api/person_identity.py` | 删除模块加载时自动执行的 `seed_dev_persons()` |
| `aos_api/routers/wave_ext.py` | 删除 6 个 `/v1/demo/*` 路由；顶部加 `TODO(持久化改造)` 标记 |
| `aos_api/routers/object_sets.py` | 移除 `source=mock` 参数和 pg 失败 fallback |
| `aos_api/vector_index.py` | 移除 mock fallback，PG 不可用时返回空 + TODO |
| `aos_api/tool_runtime.py` | `query.objects` 改为真实 PG，PG 异常直接 502 + TODO |
| `aos_api/mock_data.py` | 降级为"测试辅助"模块，保留 `reset_mock_state` 供 27+ 单测 setup 调用 |
| `aos_api/order_seed.py` | 改为兼容 shim，委托给 `aos_api.demo.order_seed.seed_orders` |
| `aos_api/demo_story.py` | 改为兼容 shim，re-export `aos_api.demo.demo_story` |

### 已知遗留（待后续迭代）

1. `mock_data.py` 暂未删除：因为 27+ 单测在 setup 调用 `reset_mock_state`；建议后续把单测 setup 改为 `clear_test_org()`，最终删除该文件。
2. `wave_ext.py` 内存存储接口仍存在：保留接口契约（路径和线上一致），加 `# TODO(持久化改造)` 注释，后续迭代补齐数据库持久化。
3. 全量 pytest 未跑：本次只做了启动 + 核心 API + 前端验证，单测可能有因 `mock_data` 降级或 `/v1/demo/*` 下线而失败的 case，需要后续适配。

---

## 一、背景与目标

### 1.1 现状问题

当前系统中存在大量分散的演示/测试数据和 Mock 逻辑，分布在 10+ 个文件中，主要问题：

1. **Demo 接口暴露到线上**：`/v1/demo/*` 共 6 个接口，线上环境不应存在
2. **Mock 数据造假**：`mock_data.py` 内存数据 + `object_sets.py` 的 pg 失败 fallback 到 mock，逻辑和线上不一致
3. **内存假数据面**：`wave_ext.py` 里用全局变量存 connectors/pipelines/datasets/syncs/media 等，重启就丢，不是真实持久化
4. **种子数据分散**：工单、订单、组织、工作区、人员、模块等种子数据散落在各处，没有统一入口
5. **系统启动耦合测试数据**：启动时自动灌测试数据，企业上线后会看到 dev-org 默认数据，体验不好

### 1.2 核心原则

| 原则 | 说明 |
|------|------|
| **零测试专用接口** | 所有 HTTP 接口和线上完全一致，不允许 `/v1/demo/*` 这种测试专用路由 |
| **零 Mock 逻辑** | 业务查询只走真实数据库，不允许 pg 失败 fallback 到内存 mock |
| **数据按组织隔离** | 测试数据只存在于 `dev-org` / `dev-project` 下，和正式数据物理隔离 |
| **启动与测试数据解耦** | 系统启动后是干净空壳（无组织/无工作区/无人员）；测试组织、测试工作区、测试人员、测试业务数据全部由独立脚本灌入 |
| **最小改动** | 不重构架构，只搬迁和清理，确保现有功能不受影响 |

### 1.3 系统必需 vs 测试数据（明确边界）

| 类别 | 内容 | 在哪 |
|------|------|------|
| **系统元数据**（启动时自动创建） | main/sandbox 分支、默认 link type、field marking、openfga 继承、apollo catalog、funnel_status | `db.py` 的 `ensure_system_meta()` |
| **测试数据**（手动脚本灌入） | dev-org 组织、dev-project 工作区、默认人员/成员、WorkOrder、Order、模块列表、动作模板、演示故事线 | `aos_api/demo/` 的 `seed_test_org()` |

---

## 二、wave_ext.py 接口分类盘点

`wave_ext.py` 是最大的"混合体"，里面既有真实业务接口，也有 demo/mock 接口。分类如下：

### 2.1 ❌ 必须删除的 Demo 接口（6 个）

| 接口 | 位置 | 原因 |
|------|------|------|
| `GET /v1/demo/story` | L61 | Demo 叙事接口，线上不需要 |
| `POST /v1/demo/ensure-seed` | L70 | 种子注入接口，线上不需要 |
| `POST /v1/demo/run-story` | L79 | Demo 写回故事，线上不需要 |
| `POST /v1/demo/run-analytics-story` | L87 | Demo 分析故事，线上不需要 |
| `GET /v1/demo/governance` | L98 | Demo 治理探针，线上不需要 |
| `POST /v1/demo/run-capability` | L106 | Demo 能力演示，线上不需要 |

### 2.2 ⚠️ 内存假数据支撑的接口（需改造）

这些接口目前用全局变量存数据，不是持久化的，需要标记 TODO 或改造：

| 接口 | 数据存储 | 状态 |
|------|---------|------|
| `GET/POST /v1/sources` | `_connectors` 全局 dict | ⚠️ 内存存储，需标记 TODO |
| `GET/POST /v1/syncs` | `_syncs` 全局 dict | ⚠️ 内存存储，需标记 TODO |
| `GET/POST /v1/pipelines` | `_pipelines` 全局 dict | ⚠️ 内存存储，需标记 TODO |
| `GET /v1/datasets`、`PATCH /v1/datasets/{rid}` | `_datasets` 全局 dict | ⚠️ 内存存储，需标记 TODO |
| `GET/POST /v1/media-sets` | `_media`、`_media_bytes` 全局 dict | ⚠️ 内存存储（有 MinIO 可选），需标记 TODO |
| `POST /v1/aip/capabilities`、`GET /v1/aip/capabilities` | `_capabilities` 全局 dict | ⚠️ 内存存储，需标记 TODO |
| `POST /v1/aip/capabilities/{cap_id}/submit`、`/invoke` | `_jobs` 全局 dict | ⚠️ 内存存储，需标记 TODO |
| `GET /v1/aip/tools` | `_tools` 全局 list | ⚠️ 内存存储，需标记 TODO |
| `GET /v1/aip/evals/status`、`/set` | `_evals_green` 全局变量 | ⚠️ 内存存储，需标记 TODO |
| `POST /v1/aip/circuit/trip`、`/reset` | `_circuit` 全局 dict | ⚠️ 内存存储，需标记 TODO |

### 2.3 ✅ 真实业务接口（保留）

| 接口 | 说明 |
|------|------|
| `POST/GET/DELETE /v1/actions/webhooks` | Webhook 注册，调用 `channel_runtime` |
| `GET /v1/channels/outbox`、`/retry` | 通道发件箱，调用 `channel_runtime` |
| `POST /v1/channels/{plugin_id}/send`、`/health` | 通道投递，调用 `channel_runtime` |
| `POST /v1/functions/invoke` | 函数运行（虽然是 echo 占位，但接口是正式的） |
| `POST /v1/aip/tools/{tool_id}/invoke` | 工具调用，调用 `tool_runtime` |
| `GET /v1/plugins` | 插件目录，聚合各 registry |
| `GET /v1/aip/providers`、`/models` | LLM 模型，调用 `llm_gateway` |
| `GET/PUT /v1/aip/gateway-default` | 默认网关配置，调用 `gateway_default` |
| `GET/PUT /v1/aip/model-routes`、`/circuit-drill` | 模型路由，调用 `aip_kv_store` |
| `GET/PUT /v1/aip/tools/config` | 工具配置，调用 `aip_kv_store` |
| `GET/POST /v1/aip/llm-provider-plugins`、`/install` 等 | LLM Provider 插件管理 |
| `POST /v1/aip/chat` | AIP 聊天，调用 `llm_gateway` |
| `GET /v1/aip/models/warmup` | 预热状态，调用 `llm_gateway` |
| `POST /v1/aip/logic/run` | Logic 运行（dryRun 是正式设计） |
| `PUT /v1/wiki/{object_type}/{object_id}` | Wiki 写拦截（返回 409 是正式设计） |
| 各种 plugin 目录接口（connector/parser/widget/channel/embedding/action） | 插件管理，调用各 registry |
| `POST /v1/embeddings/{plugin_id}/embed`、`/rerank`、`/health` | Embedding 运行时 |
| `GET /v1/object-store/health` | 对象存储健康检查 |
| `POST /v1/parsers/extract` | 文件解析，调用 `file_parsers` |

### 2.4 处理策略

- **Demo 接口**：直接删除路由，逻辑移到 `demo/` 包供测试调用
- **内存存储接口**：接口保留（路径和线上一致），但在代码里加 `# TODO: 持久化改造` 注释，数据仍然用内存存储（避免空着报错），但明确标记为待改造项
- **真实业务接口**：不动

---

## 三、mock_data.py 相关改造

### 3.1 影响范围

`mock_data.py` 被 3 个地方引用：

| 文件 | 用途 | 处理方式 |
|------|------|---------|
| `routers/object_sets.py` | `source=mock` 参数 + pg 失败 fallback | 移除 mock 分支，只走 pg |
| `vector_index.py` | 向量查询用 mock 数据兜底 | 加 TODO，移除 mock，无数据时返回空 |
| `tool_runtime.py` | `query.objects` 工具用 mock | 加 TODO，移除 mock，改用真实数据库查询 |

### 3.2 风险

- `object_sets.py` 移除 mock fallback 后，如果 pg 连接失败会直接报错，而不是降级返回 mock 数据
- **这是正确的行为**：线上环境 pg 挂了就是挂了，不能返回假数据

---

## 四、目标目录结构

```
aos_api/
├── demo/                          # 新建：所有测试/演示数据统一入口
│   ├── __init__.py
│   ├── seed.py                    # 总入口：seed_test_org() / clear_test_org()
│   ├── org_seed.py                # dev-org / dev-project / 默认人员
│   ├── workorder_seed.py          # 工单 ObjectType + 样例工单 + wiki + 关联
│   ├── order_seed.py              # 订单 ObjectType + 20 条订单
│   ├── module_seed.py             # 模块列表种子
│   ├── action_seed.py             # 动作类型模板
│   └── demo_story.py              # 演示故事线（供测试调用，不暴露 HTTP）
│
├── db.py                          # 只保留 schema 初始化 + 系统必需元数据
├── mock_data.py                   # 删除
├── order_seed.py                  # 删除（迁入 demo/）
├── demo_story.py                  # 删除（迁入 demo/）
└── routers/
    ├── wave_ext.py                # 删除 /v1/demo/* 路由，保留真实接口
    └── object_sets.py             # 移除 mock fallback
```

---

## 五、具体改动清单

### 5.1 新建 `aos_api/demo/` 包

| 文件 | 内容 |
|------|------|
| `demo/__init__.py` | 导出 `seed_test_org()`、`clear_test_org()` |
| `demo/seed.py` | 总调度，按顺序调用各子模块 seed |
| `demo/org_seed.py` | 从 `orgs.py`、`workspaces_catalog.py`、`membership.py`、`person_identity.py` 里的 `seed_dev_*` 搬过来 |
| `demo/workorder_seed.py` | 从 `db.py` 里的 WorkOrder seed 部分搬迁 |
| `demo/order_seed.py` | 从 `order_seed.py` 整体搬迁 |
| `demo/module_seed.py` | 从 `module_store.py` 的 `seed_modules_if_empty()` 搬迁 |
| `demo/action_seed.py` | 从 `action_template_registry.py` 的 `seed_installed_action_types()` 搬迁 |
| `demo/demo_story.py` | 从 `demo_story.py` 整体搬迁 |

**所有 seed 函数都明确操作 `org_id='dev-org'`、`project_id='dev-project'` 的数据。**

### 5.2 修改 `db.py`

- 删除 `seed_if_empty()` 里的 WorkOrder 种子代码（迁到 `demo/workorder_seed.py`）
- `seed_if_empty()` 改名为 `ensure_system_meta()`，只保留：
  - main/sandbox 分支
  - 默认 link type（lt-related-to）
  - field marking seed
  - openfga inherit seed
  - apollo catalog seed
  - funnel_status seed
- `main.py` 启动时调用 `ensure_system_meta()` 替代 `seed_if_empty()`

### 5.3 删除文件

- `aos_api/mock_data.py`
- `aos_api/order_seed.py`
- `aos_api/demo_story.py`

### 5.4 修改 `routers/wave_ext.py`

- 删除 6 个 `/v1/demo/*` 路由
- 删除 `_demo_data_seed_enabled()`、`clear_demo_data_surface()`、`ensure_demo_data_seed()` 三个 demo 专用函数
- 内存存储的接口保留，但在文件顶部加 `# TODO(持久化改造): 以下接口使用内存存储，需改为数据库持久化` 统一注释
- 删除 `_connectors`、`_pipelines`、`_schedules`、`_dlq`、`_syncs`、`_datasets`、`_dataset_history` 等里面的 demo 专用数据初始化（demo-file-wo、demo-pipe-wo 等）

### 5.5 修改 `routers/object_sets.py`

- 移除 `from aos_api import mock_data`
- 移除 `source: str = "pg"` 参数
- 移除 `if body.source == "mock"` 分支
- 移除 pg 异常时 fallback 到 mock 的逻辑
- 只保留 `_query_pg()` 真实查询

### 5.6 修改 `vector_index.py`

- 移除 mock_data 引用
- 无数据时返回空结果，加 `# TODO: 向量索引持久化实现` 注释

### 5.7 修改 `tool_runtime.py`

- 移除 mock_data 引用
- `query.objects` 工具改为真实数据库查询
- 如果实现复杂，先返回空 + TODO 注释

### 5.8 测试脚本

新建 `scripts/demo/seed-test-org.sh`：
```bash
#!/usr/bin/env bash
# 灌入测试组织数据（开发/测试用）
python -c "from aos_api.demo import seed_test_org; seed_test_org()"
```

新建 `scripts/demo/clear-test-org.sh`：
```bash
#!/usr/bin/env bash
# 清理测试组织数据（回归测试完清理用）
python -c "from aos_api.demo import clear_test_org; clear_test_org()"
```

---

## 六、启动流程变化

### 之前

```
main.py 启动
  └─ init_schema()          # 建表
  └─ seed_if_empty()        # 灌 WorkOrder + Order + 组织 + 分支 + ...（全混在一起）
```

### 之后

```
main.py 启动
  └─ init_schema()          # 建表
  └─ ensure_system_meta()   # 系统必需元数据（分支、link type、apollo 目录等）
  └─ [没有测试数据]          # 默认不灌 dev-org 数据

# 开发/测试时手动执行：
python -m aos_api.demo.seed   # 灌入 dev-org 测试数据
```

---

## 七、风险与影响

| 风险 | 影响范围 | 缓解措施 |
|------|---------|---------|
| 前端代码调了 `/v1/demo/*` | 前端 | 搜索前端代码，移除 demo 接口调用 |
| 单测依赖 mock_data | 测试 | 单测改为用真实数据库 + seed_test_org() |
| 单测依赖 `/v1/demo/ensure-seed` | 测试 | 单测直接 import `demo.seed_test_org()` 调用 |
| `object_sets` 移除 mock fallback 后 pg 挂了会报错 | API | 正常行为，线上就是这样 |
| 内存存储接口的数据重启丢失 | 功能体验 | 加 TODO 标记，后续迭代改造，不影响接口契约 |

---

## 八、验证方式

1. **启动验证**：启动服务 → `/v1/health` 返回 200 → 数据库里没有 dev-org 数据
2. **种子验证**：执行 `seed_test_org()` → dev-org 下有工单、订单、wiki、模块等数据
3. **接口验证**：`/v1/demo/*` 全部返回 404
4. **Mock 验证**：`object-sets/query` 不再返回 `source: mock` 或 `source: mock-fallback`
5. **前端验证**：前端页面正常访问，数据来自真实数据库
6. **清理验证**：执行 `clear_test_org()` → dev-org 数据被清空
7. **单测验证**：运行 `pytest`，所有测试通过

---

## 九、分阶段实施建议

| 阶段 | 内容 | 工作量 |
|------|------|--------|
| Phase 1 | 新建 `demo/` 包 + 搬迁种子数据 + 删除 `order_seed.py`、`demo_story.py` | 中 |
| Phase 2 | 删除 `/v1/demo/*` 路由 + 清理 wave_ext.py demo 代码 | 小 |
| Phase 3 | 删除 `mock_data.py` + 移除各 mock fallback | 中 |
| Phase 4 | 单测适配 + 验证脚本 | 中 |

建议按 Phase 1 → Phase 2 → Phase 3 → Phase 4 顺序实施，每阶段独立验证。

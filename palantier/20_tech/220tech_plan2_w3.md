# 220tech plan2 — W3 核心平台补强（23 项）

> **分支**：feature/220plan2
> **工作目录**：aos-platform-220plan2/
> **波次**：W3 / P0 核心补强
> **原则**：先方案再编码 → TDD（RED→GREEN→REFACTOR）→ 每模块必有单元测试 → 波次完成回归测试

---

## 代码库现有模式（严格遵循）

```
services/aos-api/aos_api/
  ├── <module>.py              ← 引擎层：Pydantic Model + Engine 单例 + threading.Lock
  └── routers/<module>.py      ← 路由层：FastAPI APIRouter 包装引擎

services/aos-api/tests/
  └── test_<module>.py         ← 测试层：pytest class + setup_method
```

**引擎层模式**：
- `Pydantic BaseModel` 做数据模型
- `Engine` 类用 `_instance` + `_instance_lock` 做线程安全单例
- ID 生成：`f"{prefix}-{uuid.uuid4().hex[:8]}"`
- 容量限制：`_MAX_XXX = 200`，超限 LRU 淘汰
- 自定义 `Error(Exception)` 带 `code` + `message`

**路由层模式**：
- `APIRouter(prefix="/xxx", tags=["xxx"])`
- 每个 CRUD 操作一个 `@router.xxx` 端点
- 引擎通过 `get_xxx_engine()` 获取

**测试层模式**：
- `class TestXxx: def setup_method(self)`
- 先 `eng._items = {}` 清空
- 测试覆盖：CRUD + 校验 + 边界 + 过滤

---

## W3 任务分解（23 项 × 8 模块）

### 模块 1: [DC] 数据连接补强（3 项）

#### Task 1.1 — `dc_completion_strategy.py`：完成策略引擎
- **220w**: L156 完成策略（ON_SUCCESS / ON_FAILURE / ALWAYS / NEVER 四种触发策略）
- **文件**:
  - `aos_api/dc_completion_strategy.py` — CompletionStrategy Model + Engine
  - `aos_api/routers/dc_completion_strategy.py` — Router
  - `tests/test_dc_completion_strategy.py` — 测试
- **接口**:
  ```python
  class CompletionStrategy(BaseModel):
      strategy_id: str
      name: str
      trigger: str  # ON_SUCCESS | ON_FAILURE | ALWAYS | NEVER
      downstream_task_ids: list[str]
      cooldown_seconds: int = 0
      max_retries: int = 3
      enabled: bool = True

  class CompletionStrategyEngine:
      def register(strategy) -> CompletionStrategy
      def get(strategy_id) -> CompletionStrategy
      def list(filter by trigger / enabled) -> list[CompletionStrategy]
      def update(strategy_id, patch) -> CompletionStrategy
      def delete(strategy_id) -> None
      def evaluate(task_result) -> list[str]  # 返回应触发的下游任务ID
  ```
- **测试用例**（≥8）: register / get / list / list_filter / update / delete / evaluate_on_success / evaluate_cooldown
- **main.py**: `application.include_router(dc_completion_strategy.router)`

#### Task 1.2 — `dc_stream_mgmt.py`：Stream 创建与管理
- **220w**: L182 Stream 创建与管理（创建/暂停/恢复/监控/分区策略）
- **文件**:
  - `aos_api/dc_stream_mgmt.py`
  - `aos_api/routers/dc_stream_mgmt.py`
  - `tests/test_dc_stream_mgmt.py`
- **接口**: Stream Model（stream_id, name, source_connection_id, partition_strategy, status）+ Engine（create/pause/resume/get/list/stats）

#### Task 1.3 — `dc_erp_crm.py`：ERP/CRM 连接器
- **220w**: L2225 ERP/CRM 连接器（SAP/Oracle/Salesforce/HubSpot 模板）
- **文件**:
  - `aos_api/dc_erp_crm.py`
  - `aos_api/routers/dc_erp_crm.py`
  - `tests/test_dc_erp_crm.py`
- **接口**: ErpCrmConnector Model + ConnectorTemplate + Engine（register/test_connection/sync/discover_schema）

---

### 模块 2: [DI] 数据集成（2 项）

#### Task 2.1 — `di_view_lineage.py`：视图血缘图
- **220w**: L788 视图血缘图（从 Dataset 到 View 的列级血缘可视化数据）
- **文件**:
  - `aos_api/di_view_lineage.py`
  - `aos_api/routers/di_view_lineage.py`
  - `tests/test_di_view_lineage.py`
- **接口**: ViewLineageEdge Model + Engine（build_graph / get_upstream / get_downstream / column_level_trace）

#### Task 2.2 — `di_task_debug.py`：任务调试
- **220w**: L2079 任务调试（任务运行时日志、参数快照、错误定位）
- **文件**:
  - `aos_api/di_task_debug.py`
  - `aos_api/routers/di_task_debug.py`
  - `tests/test_di_task_debug.py`
- **接口**: DebugSession Model + Engine（start / add_log / get_snapshot / trace_error / close）

---

### 模块 3: [DL] 数据血缘增强（4 项）

#### Task 3.1 — `dl_build_strategy.py`：三种搭建策略
- **220w**: L591 全量搭建 / 增量搭建 / 选择性搭建
- **文件**: `aos_api/dl_build_strategy.py` + router + test
- **接口**: BuildStrategy Model（FULL / INCREMENTAL / SELECTIVE）+ Engine（create / preview / execute / compare）

#### Task 3.2 — `dl_build_preview.py`：搭建预览
- **220w**: L592 搭建前预览影响范围（受影响数据集数、预估时间、资源消耗）
- **文件**: `aos_api/dl_build_preview.py` + router + test
- **接口**: BuildPreview Model + Engine（preview / estimate / dry_run / cancel）

#### Task 3.3 — `dl_dep_order.py`：依赖顺序搭建
- **220w**: L594 拓扑排序后的自动依赖链搭建
- **文件**: `aos_api/dl_dep_order.py` + router + test
- **接口**: DependencyGraph + Engine（add_dependency / topological_sort / validate_no_cycle / build_plan）

#### Task 3.4 — `dl_stale_diagnosis.py`：过时数据集诊断
- **220w**: L652 检测过时数据集（上游更新但下游未同步）
- **文件**: `aos_api/dl_stale_diagnosis.py` + router + test
- **接口**: StaleDiagnosis Model + Engine（scan / diagnose / get_stale_chain / suggest_rebuild）

---

### 模块 4: [DS] Dataset Preview（1 项）

#### Task 4.1 — `ds_context_menu.py`：数据集操作菜单
- **220w**: L1537 Contour/搭建/探索/变换/管理 五大操作入口
- **文件**: `aos_api/ds_context_menu.py` + router + test
- **接口**: DatasetAction Model（action_type: CONTOUR/BUILD/EXPLORE/TRANSFORM/MANAGE）+ Engine（get_actions / execute / validate_permission）

---

### 模块 5: [PP+PB] 管道编排（5 项）

#### Task 5.1 — `pp_toolbar_settings.py`：顶部工具栏-搭建设置
- **220w**: L1005
- **文件**: `aos_api/pp_toolbar_settings.py` + router + test

#### Task 5.2 — `pb_build_vs_deploy.py`：部署 vs 搭建分离
- **220w**: L1213
- **文件**: `aos_api/pb_build_vs_deploy.py` + router + test

#### Task 5.3 — `pb_build_profiles.py`：搭建设置（9种批处理+6种流式计算配置文件）
- **220w**: L1236
- **文件**: `aos_api/pb_build_profiles.py` + router + test

#### Task 5.4 — `pb_task_groups.py`：任务组（输出分配/计算配置文件/权限继承）
- **220w**: L1242
- **文件**: `aos_api/pb_task_groups.py` + router + test

#### Task 5.5 — `pb_health_checks.py`：健康检查配置（任务级/搭建级/新鲜度）
- **220w**: L1265
- **文件**: `aos_api/pb_health_checks.py` + router + test

---

### 模块 6: [CR] 代码仓库（2 项）

#### Task 6.1 — `cr_branch_menu.py`：分支操作菜单
- **220w**: L1813
- **文件**: `aos_api/cr_branch_menu.py` + router + test

#### Task 6.2 — `cr_pipeline_review.py`：流水线审查
- **220w**: L1824
- **文件**: `aos_api/cr_pipeline_review.py` + router + test

---

### 模块 7: [MS+OB+ES+ID] 其他（6 项）

#### Task 7.1 — `ms_header_extractor.py`：表格表头提取器
- **220w**: L1978
- **文件**: `aos_api/ms_header_extractor.py` + router + test

#### Task 7.2 — `ob_index_debug.py`：索引调试
- **220w**: L2565
- **文件**: `aos_api/ob_index_debug.py` + router + test

#### Task 7.3 — `es_sap_stream.py`：SAP 实时流
- **220w**: L2188
- **文件**: `aos_api/es_sap_stream.py` + router + test

#### Task 7.4 — `id_py_transform_preview.py`：Python Transform 预览
- **220w**: L3623
- **文件**: `aos_api/id_py_transform_preview.py` + router + test

#### Task 7.5 — `id_build_panel.py`：Build 面板（3种启动方式）
- **220w**: L3655
- **文件**: `aos_api/id_build_panel.py` + router + test

#### Task 7.6 — `id_build_status.py`：搭建状态监控
- **220w**: L3656
- **文件**: `aos_api/id_build_status.py` + router + test

---

## 执行顺序与依赖

```
批次 A（独立模块，可并行）:
  Task 1.1  dc_completion_strategy     ← 无依赖
  Task 1.2  dc_stream_mgmt             ← 无依赖
  Task 1.3  dc_erp_crm                 ← 无依赖
  Task 2.1  di_view_lineage            ← 无依赖
  Task 2.2  di_task_debug              ← 无依赖
  Task 4.1  ds_context_menu            ← 无依赖
  Task 7.1  ms_header_extractor        ← 无依赖
  Task 7.2  ob_index_debug             ← 无依赖
  Task 7.3  es_sap_stream              ← 无依赖

批次 B（DL 血缘有内部依赖）:
  Task 3.1  dl_build_strategy          ← 无依赖
  Task 3.2  dl_build_preview           ← 弱依赖 3.1（可独立）
  Task 3.3  dl_dep_order               ← 弱依赖 3.1
  Task 3.4  dl_stale_diagnosis         ← 弱依赖 3.3

批次 C（管道编排有内部依赖）:
  Task 5.1  pp_toolbar_settings        ← 无依赖
  Task 5.2  pb_build_vs_deploy         ← 无依赖
  Task 5.3  pb_build_profiles          ← 弱依赖 5.2
  Task 5.4  pb_task_groups             ← 弱依赖 5.3
  Task 5.5  pb_health_checks           ← 无依赖

批次 D:
  Task 6.1  cr_branch_menu             ← 无依赖
  Task 6.2  cr_pipeline_review         ← 无依赖
  Task 7.4  id_py_transform_preview    ← 无依赖
  Task 7.5  id_build_panel             ← 无依赖
  Task 7.6  id_build_status            ← 弱依赖 7.5
```

## 每个任务的 TDD 流程

```
1. RED:   写 test_<module>.py（8-15 个测试用例，全部 FAIL）
2. GREEN: 写 <module>.py 引擎 + routers/<module>.py 路由（测试全 PASS）
3. REFACTOR: 检查命名/DRY/边界（测试仍 PASS）
4. HOOKUP: main.py 注册 router
5. VERIFY: pytest tests/test_<module>.py -v → 0 failures
```

## 回归测试

完成全部 23 项后：
```bash
cd aos-platform-220plan2/services/aos-api
python -m pytest tests/ -v --tb=short  # 全量回归
```

## 文件清单（69 个新文件）

| 类型 | 文件数 |
|------|--------|
| 引擎 `aos_api/*.py` | 23 |
| 路由 `aos_api/routers/*.py` | 23 |
| 测试 `tests/test_*.py` | 23 |

每模块 3 文件 × 23 项 = 69 个新文件。

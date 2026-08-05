# 228-EC Pipeline 生产执行器与证据 Resolver 注册实施方案

> 版本：v1.0 · 2026-08-05
> 状态：**设计方案 · 待用户批准**
> 定位：[228-EC-Pipeline诚实执行与负向验收方案](./228-EC-Pipeline诚实执行与负向验收方案.md) v1.1 的直接续篇——填补该方案 §五明确标注的"生产执行器/resolver 仍未注册"空缺
> 上游：诚实执行方案 v1.1（已完成 fail-closed 语义 + executor 注册框架 + 56 tests）
> 下游解除：[228-微商城专项 §8 D1](./电商平台接入/微商城电商接入方案/228-微商城专项实施准备与FDE全链路规格.md) 的硬前置阻塞（Pipeline resolver/executor + Dataset sink）
> 边界：平台通用能力，不含微商城 P01-P08 配置（那是 D1 波次）；不重写已就绪的 fail-closed 链路

---

## 0. 使用的 Rules

1. 先方案后编码，本文件为方案，批准后按 TDD 实施
2. 不重写已就绪的 fail-closed 判定链路（`_preflight → _collect_dispatch → _evidence_from_result → _valid_ref`），只在其上叠加注册
3. 最小更改：复用 `ecom_consistency_store` BatchCommand 落地，不建第二套 OT writer
4. 不影响已有功能：诚实执行方案的 56 tests 必须继续 GREEN
5. 租户隔离：生产 executor 必须走 scope 守门，落 `ecom_object`/`meta_dataset` 时带 `(org_id, project_id)`
6. 完成前自测：新增 resolver/executor 必须有负向验收（缺失/异常时 fail-closed）

---

## 1. 目标

解除 [228-微商城专项 D1](./电商平台接入/微商城电商接入方案/228-微商城专项实施准备与FDE全链路规格.md) 的硬前置阻塞，使 `execution_mode="live"` 的 Pipeline 能够：

1. 真实执行节点链（Source → Transform/Filter → Sink），不再 preflight 即拒
2. Sink 产出落到 `meta_dataset` + `ecom_object`（通过 BatchCommand），evidence URI 可被 resolver 验证
3. 失败 run 自动入 Pipeline DLQ，可重试

**非目标**（明确排除）：
- 不实现 Join 节点（诚实执行方案已排除，维持）
- 不实现自定义 SQL 节点（诚实执行方案已排除，维持）
- 不做微商城 P01-P08 的具体配置（D1 波次）
- 不做 LLM 节点的生产执行（独立波次）
- 不重写 Pipeline Builder（W1-14 DAG 编辑器）

---

## 2. 现状基线（已完成，复用不重写）

| 能力 | 位置 | 状态 |
|---|---|---|
| executor 注册 API + 白名单 | `phase5_pipeline_engine.py:903-924` | ✅ |
| evidence resolver 注册 API（5 scheme） | `phase5_pipeline_engine.py:903-924` | ✅ |
| 节点类型 preflight 白名单 `{source,transform,filter,sink,llm}` | `phase5_pipeline_engine.py:1001` | ✅ |
| config SQL 黑名单（递归扫描） | `phase5_pipeline_engine.py:956-965` | ✅ |
| evidence URI 语法/敏感度校验 + fail-closed | `phase5_pipeline_engine.py:967-997` | ✅ |
| executor 异常脱敏 `_safe_error` | `phase5_pipeline_engine.py:948-953` | ✅ |
| 超时取消（cancel_event + deadline + 线程 join） | `phase5_pipeline_engine.py:1058-1095` | ✅ |
| 快照隔离（pipeline/nodes 深拷贝） | `phase5_pipeline_engine.py:1028-1029` | ✅ |
| OT 落地表 `ecom_object`/`ecom_link`/`ecom_sync_checkpoint`/`ecom_ingest_receipt` | `ecom_consistency_store.py` | ✅ |
| 增量一致性内核（复合游标/去重/tombstone/幂等收据/单事务） | `ecom_consistency_store.py` BatchCommand | ✅ |
| Data OS 元数据 CRUD（scope 守门） | `data_os_store.py:152-536` | ✅ |
| 诚实失败语义测试覆盖（13+ case） | `tests/test_ec_pipeline_honesty.py` | ✅ |

---

## 3. 空缺清单（本方案要补的）

| 编号 | 空缺 | 严重性 | 接入点 |
|---|---|---|---|
| **G1** | `_start_dispatch` 不把 `scope` 传给 executor kwargs | **P0 阻塞** | `phase5_pipeline_engine.py:1034-1046` |
| **G2** | 零个生产 executor 注册；main.py lifespan 无注册动作 | **P0 阻塞** | 新增模块 + `main.py` lifespan |
| **G3** | 零个 evidence resolver 注册（dataset/lineage/quality/object/artifact 全空） | **P0 阻塞** | 新增模块 + `main.py` lifespan |
| **G4** | DatasetSink：executor 输出 → `meta_dataset` + `DatasetBuild` 落地 | P1 | executor 内部调用 `data_os_store.persist_dataset` |
| **G5** | executor 输出 → `ecom_object`/`ecom_link`（OT 落地） | P1 | executor 内部调用 `ecom_consistency_store` BatchCommand |
| **G6** | Pipeline 专用 DLQ（失败 run 自动入队） | P2 | 复用 `wave_ext._dlq` 结构，新增执行器侧自动投递 |
| **G7** | `reset(scope=...)` 进程级清空 `_executors`/`_evidence_resolvers`（测试语义泄漏到生产） | P2 | `phase5_pipeline_engine.py:1273-1274` |
| **G8** | health check 硬编码假数据（`null_rate=0.02` 等，`synthetic=True`） | P3 | `phase5_pipeline_engine.py:888-900` |

**D1 解除阻塞的最小集合**：G1 + G2 + G3（P0 三项）。G4/G5 在 D1 波次随 P01-P08 配置一起做。G6-G8 可延后。

---

## 4. 架构设计

### 4.1 生产 executor 模型（G2）

**关键决策：单 executor 驱动整个 pipeline DAG**（与现有 kwargs 契约一致——传整个 nodes 列表）。

executor_id = `"ec-live-v1"`，注册一次，处理所有 `execution_mode="live"` 的电商管道。内部按节点 `node_type` 分发：

```text
ec_live_executor(pipeline, nodes, node_id, sample_input, execution_kind,
                 cancel_event, deadline, scope)   ← G1 新增 scope
  │
  ├─ 拓扑排序 nodes（按 edges）
  ├─ 逐节点执行：
  │    ├─ source  → SourceAdapter 读源（MySQL 只读 / 合成 fixture）
  │    ├─ transform → Map/Project/Normalize（纯函数，行级）
  │    ├─ filter  → 谓词过滤
  │    └─ sink    → DatasetSink(G4) + OTWriter(G5)
  ├─ 产出 evidence dict:
  │    { output_ref, rows_read, rows_written, output_rows,
  │      lineage_ref, quality_ref }
  └─ 全程 scope 守门（落库带 org_id/project_id）
```

**SourceAdapter 职责**（读 MySQL，D1 波次实例化为 Niushop 只读源）：
- 从 `node.config` 取 `source_id` → 查 `meta_source` 拿连接配置
- 用只读事务（`SET SESSION TRANSACTION READ ONLY`，复用 `qyh_discover_readonly.py` 模式）
- 按 `node.config.cursor` 做增量游标读取（复用 `ecom_consistency_store` 的复合游标语义）

### 4.2 evidence resolver 注册（G3）

5 类 resolver，各自职责：

| scheme | resolver 实现 | 查询目标 |
|---|---|---|
| `dataset` | `dataset_resolver(ref)` | 解析 `dataset://catalog/<rid>` → 查 `meta_dataset` WHERE rid 匹配 AND scope 匹配 |
| `object` | `object_resolver(ref)` | 解析 `object://<ot>/<external_id>` → 查 `ecom_object` WHERE ot+external_id 匹配 AND scope 匹配 |
| `lineage` | `lineage_resolver(ref)` | 解析 `lineage://<run_id>/<node_id>` → 查 `PipelineHistory` 或专用 lineage 表（延后） |
| `quality` | `quality_resolver(ref)` | 解析 `quality://<run_id>/<check_id>` → 查质量评估记录（延后，先返回存在性占位） |
| `artifact` | `artifact_resolver(ref)` | 解析 `artifact://<type>/<id>` → 查 artifact registry（延后） |

**D1 最小集合**：只注册 `dataset` + `object` 两类 resolver（lineage/quality/artifact 返回 fail-closed，等对应存储就绪后再注册）。

**关键约束**（来自调查报告风险提示）：
- resolver 必须在 `main.py` lifespan 启动阶段注册，否则成功执行会被 `_valid_ref` 误判 `PIPELINE_EVIDENCE_INVALID`
- resolver 签名 `Callable[[str], bool]`，必须返回 `is True`（不是真值）
- resolver 抛异常 → `_valid_ref` 捕获视作 `False`（fail-closed，已有保障）

### 4.3 scope 注入修复（G1）

`_start_dispatch.invoke()` 的 kwargs 契约扩展（向后兼容）：

```python
# phase5_pipeline_engine.py:1034-1046 现状
executor(
    pipeline=pipeline_snapshot,
    nodes=nodes_snapshot,
    node_id=node_id,
    sample_input=...,
    execution_kind=execution_kind,
    cancel_event=cancel_event,
    deadline=deadline,
)
# 改为（新增 scope 参数）
executor(
    ...,
    scope=scope,   # ← 新增：TenantScope，executor 落库必需
)
```

**向后兼容**：合成测试 executor（`synthetic-test` 等）的签名用 `**kwargs` 或新增 `scope=None` 默认值，不破坏诚实执行方案的 56 tests。

### 4.4 DatasetSink（G4）+ OTWriter（G5）

executor 的 sink 节点处理：

```text
sink 节点输入: rows (transform 后的行流)
  │
  ├─ G4 DatasetSink:
  │    ├─ data_os_store.persist_dataset(scope, rid=gen_rid(), ...)
  │    ├─ data_os_store.persist_dataset_history(scope, ...)
  │    └─ engine.add_build(scope, dataset_id, DatasetBuild(...))
  │    → 产出 output_ref = "dataset://catalog/<rid>"
  │
  └─ G5 OTWriter:
       ├─ ecom_consistency_store.batch_upsert(scope, platform, objects=[...], links=[...])
       │    （复用 BatchCommand 单事务：upsert→link→checkpoint→receipt）
       └─ 产出 object_ref = "object://<ot>/<external_id>" （供 object resolver 验证）
```

**G4/G5 在 D1 波次实施**（随 P01-P08 配置），本方案只提供 executor 内部的 sink 调用框架。

---

## 5. 实施分解（TDD）

### Step 0：前置——修复 reset 副作用（G7）

| 动作 | 文件 |
|---|---|
| 把 `_executors.clear()` / `_evidence_resolvers.clear()` 从 `reset(scope=...)` 移到 `reset_all_for_tests()` | `phase5_pipeline_engine.py:1273-1274` |
| 负向测试：`reset(scope=X)` 后生产 executor 仍注册 | `tests/test_ec_pipeline_honesty.py` 新增 |

**理由**：G7 是隐患——若生产中调用 `reset(scope=...)`（租户注销场景）会把全局 executor 清空，所有管道立刻不可用。必须在 G1-G3 之前修，否则生产 executor 注册后这个隐患更危险。

### Step 1：scope 注入（G1）—— RED

| 动作 | 文件 |
|---|---|
| 新增测试：合成 executor 能收到 `scope` kwarg | `tests/test_ec_pipeline_honesty.py` |
| 测试合成 executor 把 scope.org_id 写入 evidence，验证可追溯 | 同上 |

### Step 2：scope 注入（G1）—— GREEN

| 动作 | 文件 |
|---|---|
| `_start_dispatch.invoke()` kwargs 增加 `scope=scope` | `phase5_pipeline_engine.py:1034-1046` |
| 合成测试 executor 签名加 `scope=None` | `tests/test_ec_pipeline_honesty.py` fixture |

### Step 3：evidence resolver 注册（G3）—— RED

| 动作 | 文件 |
|---|---|
| 新增 `tests/test_ec_pipeline_resolvers.py` | 新文件 |
| 测试 `dataset_resolver` 对存在/不存在的 rid 返回 True/False | 同上 |
| 测试 `object_resolver` 对存在/不存在的 ecom_object 返回 True/False | 同上 |
| 测试 scope 不匹配时返回 False（跨租户拒绝） | 同上 |
| 测试 resolver 异常时返回 False（fail-closed） | 同上 |

### Step 4：evidence resolver 注册（G3）—— GREEN

| 动作 | 文件 |
|---|---|
| 新增 `aos_api/ec_pipeline_resolvers.py`（dataset_resolver + object_resolver） | 新文件 |
| `main.py` lifespan 注册 `register_evidence_resolver("dataset", ...)` + `("object", ...)` | `aos_api/main.py:46-84` |

### Step 5：生产 executor 骨架（G2）—— RED

| 动作 | 文件 |
|---|---|
| 新增 `tests/test_ec_live_executor.py` | 新文件 |
| 测试：注册 `ec-live-v1` executor 后，live pipeline 能 preflight 通过（不再 EXECUTOR_MISSING） | 同上 |
| 测试：source→transform→sink 合成链路产出合法 evidence（output_ref/rows_read/rows_written） | 同上 |
| 测试：executor 收到 scope 并在 evidence 中体现 org_id | 同上 |
| 测试：executor 超时 → PIPELINE_EXECUTOR_TIMEOUT | 同上 |
| 测试：executor 异常 → PIPELINE_EXECUTOR_FAILED + 脱敏 | 同上 |
| 负向：未注册 executor → 仍 PIPELINE_EXECUTOR_MISSING（诚实执行方案 test 不回归） | 同上 |

### Step 6：生产 executor 骨架（G2）—— GREEN

| 动作 | 文件 |
|---|---|
| 新增 `aos_api/ec_live_executor.py`（ec_live_executor 函数 + 节点分发器） | 新文件 |
| `main.py` lifespan `register_executor("ec-live-v1", ec_live_executor)` | `aos_api/main.py` |
| SourceAdapter：D1 波次前用合成 fixture（不直连 MySQL）；D1 波次加 Niushop 只读源 | 同上 |

### Step 7：回归验证

| 动作 | 命令 |
|---|---|
| 诚实执行方案 56 tests 全 GREEN | `python -m pytest tests/test_ec_pipeline_honesty.py -v` |
| 新增 resolver/executor tests 全 GREEN | `python -m pytest tests/test_ec_pipeline_resolvers.py tests/test_ec_live_executor.py -v` |
| 全量回归无回归 | `bash scripts/ci.sh quick` |
| OpenAPI 契约确定性（若 router 变化） | `bash scripts/ci.sh wave` |

---

## 6. 独占文件清单

**新增**：
- `aos_api/ec_pipeline_resolvers.py`（dataset + object resolver）
- `aos_api/ec_live_executor.py`（生产 executor 骨架）
- `tests/test_ec_pipeline_resolvers.py`
- `tests/test_ec_live_executor.py`

**修改**：
- `aos_api/phase5_pipeline_engine.py`（G1 scope 注入 + G7 reset 修复）
- `aos_api/main.py`（lifespan 注册 executor + resolver）
- `tests/test_ec_pipeline_honesty.py`（合成 executor 签名加 scope=None，新增 reset 副作用负向测试）

**不改**：
- `aos_api/phase5_pipeline_engine.py` 的 fail-closed 判定逻辑（`_preflight`/`_evidence_from_result`/`_valid_ref`）
- `aos_api/ecom_consistency_store.py`（BatchCommand 接口已有，复用）
- `aos_api/data_os_store.py`（CRUD 已有，复用）
- Pipeline Builder（W1-14 DAG 编辑器）
- Connector / OAuth / OpenAPI 生成物 / CI

---

## 7. 风险与规避

| 风险 | 严重性 | 规避 |
|---|---|---|
| G7 reset 副作用：生产租户注销清空全局 executor | 高 | Step 0 前置修复 |
| resolver 注册晚于 executor 首次执行 → 误判 EVIDENCE_INVALID | 高 | lifespan 顺序：先 resolver 后 executor；加启动后自检 |
| scope 注入破坏合成 executor 的 56 tests | 中 | `scope=None` 默认值 + `**kwargs` 兼容 |
| DatasetSink 生成的 output_ref 不满足 URI 语法约束（无 netloc/有 query） | 中 | 强制格式 `dataset://catalog/<rid>`，无 query/fragment；加格式测试 |
| 生产 executor 连真实 MySQL 时 scope 守门绕过 | 高 | SourceAdapter 强制走 `meta_source` 查连接配置，不接 config 直传连接串 |
| lineage/quality/artifact resolver 延后注册 → 对应 evidence 永远 fail-closed | 中 | D1 波次 P01-P08 的 evidence 只用 dataset + object 两类；lineage/quality 延后到 D2 |

---

## 8. 验收标准

### 8.1 D1 阻塞解除验收（本方案核心交付）

| AC | 验证方式 |
|---|---|
| AC-1：`execution_mode="live"` 的 pipeline 不再因 EXECUTOR_MISSING 被 preflight 拒绝 | Step 5 测试 |
| AC-2：executor 收到 scope，evidence 可追溯 org_id | Step 1/5 测试 |
| AC-3：dataset/object resolver 注册后，`_valid_ref` 对真实落地的 dataset/object 返回 True | Step 3 测试 |
| AC-4：诚实执行方案 56 tests 零回归 | Step 7 |
| AC-5：reset(scope=...) 不清空全局 executor | Step 0 测试 |

### 8.2 D1 就绪声明（本方案通过后）

本方案 AC-1~AC-5 全部 GREEN 后，[228-微商城专项 D1](./电商平台接入/微商城电商接入方案/228-微商城专项实施准备与FDE全链路规格.md) 的硬前置"Pipeline resolver/executor"**解除阻塞**。D1 波次可启动 P01-P08 配置 + G4/G5（DatasetSink + OTWriter 实例化）。

---

## 9. 与微商城专项 D1 的衔接

本方案（平台通用执行链）通过后，D1 波次的工作变为：

| D1 工作 | 依赖本方案的哪一项 |
|---|---|
| P01-P08 pipeline 配置（frozen/02 manifest 实例化） | G2 ec-live-v1 executor |
| SourceAdapter 实例化为 Niushop 只读源 | G2 SourceAdapter 框架 |
| Sink 节点落 `meta_dataset` | G4 DatasetSink 框架 |
| Sink 节点落 `ecom_object`/`ecom_link`（7 OT 孪生） | G5 OTWriter（调 ecom_consistency_store BatchCommand） |
| evidence 用 dataset + object 两类 | G3 dataset/object resolver |
| §5.4.1 派生指标（quality_score/risk_score/overdue_hours）落地 | G2 transform 节点的 Normalize/QualityGate 子步 |

**D1 不依赖**：lineage/quality/artifact resolver（延后）、Pipeline DLQ（G6 延后）、health check 真实化（G8 延后）。

---

## 10. 开放问题

| 编号 | 问题 | 处置 |
|---|---|---|
| Q1 | SourceAdapter 在本方案用合成 fixture，D1 波次才接 Niushop 只读源——本方案的"生产 executor"是否算真正生产？ | 算：本方案交付的是**执行链注册与 evidence 闭环**，SourceAdapter 的真实数据源是 D1 波次的配置项。合成 fixture 足以验证执行链正确性。 |
| Q2 | lineage/quality resolver 延后，D1 的 PipelineHistory 能否作为 lineage evidence？ | 暂不接入 lineage evidence；D1 的 evidence 只用 dataset + object。lineage 等专用 lineage 表设计后补。 |
| Q3 | G7 reset 修复是否影响 wave_ext 的租户注销流程？ | 需核实 wave_ext 是否调用 `engine.reset(scope=...)`；若调用，需同步改为只清 scope 级数据。Step 0 实施时排查。 |
| Q4 | Python 3.11+ 环境在当前机器不可见——实施前必须解决 | 实施前确认 Python 3.11+ 路径，或指导安装 |

---

*本方案为 228-EC-Pipeline诚实执行方案 v1.1 的续篇，填补"生产执行器/resolver 仍未注册"空缺，解除微商城 D1 硬前置阻塞。批准后按 Step 0-7 TDD 实施。*

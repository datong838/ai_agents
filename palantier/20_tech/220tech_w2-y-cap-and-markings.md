# 220tech · W2-Y · 契约与安全标记组（#88 / #99 / #100）

> **版本**：v1.0 · 2026-07-22
> **状态**：✅ 方案定稿 · 可编码
> **对齐**：
> - 差距分析 [220w](./220w-与目标系统差距对照分析.md) §6.5 #88（CAP-01~07）· §3.5 #99（stop_propagating/stop_requiring）· §3.5 #100（filter-in/filter-out）
> - 产品方案 [07b](../07b-Capability-Adapter重能力接入.md) §4 CAP-01~07 · [07a](../07a-AIP引擎产品设计线框图.md)
> - 技术方案 [T07](./T07-AIP人工智能平台详细技术方案.md) §5.3（Capability Adapter）
> - 上游 W2-X CapabilityAdapterEngine（#87 已交付）· W2-U EgressPolicyEngine（#74 安全标记基础）
> **范围**：W2-Y 收口契约执行与安全标记传播三件 — CAP 约束引擎（7 项硬约束执行）· 安全标记传播控制（stop_propagating/stop_requiring）· 标记移除策略（filter-in/filter-out）
> **不替换底层**：本组是契约执行层与标记传播层，不重写 CapabilityAdapterEngine/EgressPolicyEngine

---

## 0. 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文回答 | 文档与代码注释均中文 |
| 先方案后编码 | 本文先定稿，再写引擎/路由/测试 |
| 最小更改 | 仅新增 `aos_api/cap_and_markings.py` + `aos_api/routers/cap_and_markings.py` + `tests/test_cap_and_markings.py`；`main.py` 加 2 行 |
| 不影响已有功能 | CAP 约束只增校验；标记传播只增配置；不破坏 W2-X/W2-U 既有逻辑 |
| 自测验证 | 单测全绿 + 全量回归 + 方案对照 |
| 符合方案军规 | CAP-01~07 字段与 07b §4 一致；stop_propagating/stop_requiring 与 220w §3.5 一致；filter-in/filter-out 与 Foundry remove-markings 一致 |

---

## 1. 背景与边界

### 1.1 现状

| 能力 | 现状 | 缺口 |
| --- | --- | --- |
| CAP 约束 | W2-X 已有 CapabilityAdapterEngine 但无 CAP-01~07 约束执行 | 🔴 缺 |
| 安全标记传播控制 | W2-U EgressPolicyEngine 有 security_label 但无传播配置 | 🔴 缺 |
| 标记移除策略 | 无 filter-in/filter-out 移除策略 | 🔴 缺 |

### 1.2 边界

- ✅ 本组做：
  - #88 CAP 约束引擎：7 项硬约束（CAP-01~07）的注册/校验/违规记录
  - #99 安全标记传播控制：stop_propagating/stop_requiring 配置 + 传播算法
  - #100 标记移除策略：filter-in/filter-out 移除策略 + 输出标记清理
- ❌ 本组不做：
  - Capability Marketplace（CAP-07 已禁）
  - 实际 Vault 接入（CAP-04 仅记录 ref，不接 Vault）
  - 实际回调验签（CAP-05 仅记录验签状态）
  - 跨组织传播（仅项目内传播）

---

## 2. 数据模型

### 2.1 #88 CAP 约束

```python
class CapRule(BaseModel):
    """CAP 约束规则。"""
    code: str                          # CAP-01 ~ CAP-07
    title: str
    description: str
    severity: str = "error"            # error / warning
    enabled: bool = True
    enforcement: str = "block"         # block / audit / dry_run


class CapViolation(BaseModel):
    """CAP 违规记录。"""
    id: str
    code: str                          # CAP-01 ~ CAP-07
    timestamp: float
    actor: str
    target_type: str                   # function / capability / logic_run / action
    target_id: str
    detail: dict[str, Any] = {}
    severity: str = "error"
    resolution: str = "blocked"        # blocked / audited / dry_run_passed
```

### 2.2 #99 安全标记传播

```python
class MarkingPropagationConfig(BaseModel):
    """标记传播配置（per project/object_type）。"""
    project_id: str
    object_type: str
    stop_propagating: bool = False     # 停止向下游传播
    stop_requiring: bool = False       # 不再要求下游继承
    inherit_from_parent: bool = True   # 从父项目继承
    expand_input_inheritance: bool = False  # 展开输入继承


class MarkingRecord(BaseModel):
    """标记记录。"""
    id: str
    project_id: str
    object_type: str
    object_id: str
    security_label: str                # public/internal/sensitive/restricted
    propagated_from: str = ""          # 来源 object_id（继承自）
    is_inherited: bool = False
    created_at: float = 0.0
```

### 2.3 #100 标记移除策略

```python
class MarkingRemovalPolicy(BaseModel):
    """标记移除策略。"""
    id: str
    project_id: str
    pipeline_id: str = ""
    output_object_type: str
    strategy: str                      # filter_in / filter_out
    removed_labels: list[str] = []     # 要移除的标记列表
    keep_labels: list[str] = []        # 仅保留的标记列表（filter_in 用）
    apply_to_inherited: bool = True    # 是否对继承标记也生效
    enabled: bool = True


class MarkingRemovalResult(BaseModel):
    """标记移除执行结果。"""
    id: str
    policy_id: str
    timestamp: float
    object_id: str
    original_labels: list[str]
    removed_labels: list[str]
    final_labels: list[str]
    skipped_inherited: int = 0
```

---

## 3. 引擎设计

文件：`aos_api/cap_and_markings.py`（新增，3 个引擎）

### 3.1 CapConstraintEngine（#88）

```python
class CapConstraintEngine:
    def get_rule(self, code: str) -> CapRule: ...
    def list_rules(self, enabled_only: bool = False) -> list[CapRule]: ...
    def update_rule(self, code: str, updates: dict[str, Any]) -> CapRule: ...
    def check(
        self, code: str, actor: str, target_type: str, target_id: str,
        detail: dict[str, Any] | None = None,
    ) -> CapViolation: ...
    """执行约束校验：返回 CapViolation（resolution=blocked/audited/dry_run_passed）"""
    def list_violations(
        self, code: str | None = None, target_type: str | None = None,
        limit: int = 50,
    ) -> list[CapViolation]: ...
    def get_violation(self, violation_id: str) -> CapViolation: ...
```

**check 流程**：
1. 取 rule，若 disabled 或 enforcement=dry_run → resolution=dry_run_passed
2. 若 enforcement=audit → resolution=audited（不阻塞）
3. 若 enforcement=block → resolution=blocked
4. 写入 CapViolation 记录

### 3.2 MarkingPropagationEngine（#99）

```python
class MarkingPropagationEngine:
    def set_config(self, cfg: MarkingPropagationConfig) -> MarkingPropagationConfig: ...
    def get_config(self, project_id: str, object_type: str) -> MarkingPropagationConfig: ...
    def list_configs(self, project_id: str | None = None) -> list[MarkingPropagationConfig]: ...
    def record_marking(self, rec: MarkingRecord) -> MarkingRecord: ...
    def get_marking(self, project_id: str, object_type: str, object_id: str) -> MarkingRecord: ...
    def list_markings(
        self, project_id: str, object_type: str | None = None,
        security_label: str | None = None, limit: int = 50,
    ) -> list[MarkingRecord]: ...
    def propagate(
        self, project_id: str, source_object_type: str, source_object_id: str,
        downstream_object_type: str, downstream_object_id: str,
    ) -> MarkingRecord: ...
    """传播标记：若 stop_propagating=True 则不传播；否则复制 source 的 security_label"""
```

### 3.3 MarkingRemovalEngine（#100）

```python
class MarkingRemovalEngine:
    def register_policy(self, policy: MarkingRemovalPolicy) -> MarkingRemovalPolicy: ...
    def get_policy(self, policy_id: str) -> MarkingRemovalPolicy: ...
    def list_policies(
        self, project_id: str | None = None, output_object_type: str | None = None,
        enabled_only: bool = False,
    ) -> list[MarkingRemovalPolicy]: ...
    def update_policy(self, policy_id: str, updates: dict[str, Any]) -> MarkingRemovalPolicy: ...
    def delete_policy(self, policy_id: str) -> bool: ...
    def apply(
        self, policy_id: str, object_id: str,
        original_labels: list[str], inherited_labels: list[str] | None = None,
    ) -> MarkingRemovalResult: ...
    """执行移除：filter_in 仅保留 keep_labels；filter_out 移除 removed_labels"""
    def list_results(
        self, policy_id: str | None = None, limit: int = 50,
    ) -> list[MarkingRemovalResult]: ...
```

**apply 流程**：
1. 取 policy，若 disabled → 抛 POLICY_DISABLED
2. filter_in：final = original ∩ keep_labels（其他全移除）
3. filter_out：final = original - removed_labels
4. 若 apply_to_inherited=False，inherited_labels 不参与移除
5. 记录 MarkingRemovalResult

### 3.4 单例与持久化

- 3 个引擎均用**双重检查锁单例**
- 内存态为主，200 条上限（violations/markings/results）

---

## 4. API 设计

文件：`aos_api/routers/cap_and_markings.py`（新增）

### 4.1 #88 CAP 约束

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/v1/aip/cap-constraints/rules` | 列出约束规则 |
| GET | `/v1/aip/cap-constraints/rules/{code}` | 单条规则 |
| PUT | `/v1/aip/cap-constraints/rules/{code}` | 更新规则 |
| POST | `/v1/aip/cap-constraints/check` | 执行约束校验 |
| GET | `/v1/aip/cap-constraints/violations` | 违规列表 |
| GET | `/v1/aip/cap-constraints/violations/{violation_id}` | 单条违规 |

### 4.2 #99 安全标记传播

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/aip/markings/propagation-configs` | 设置传播配置 |
| GET | `/v1/aip/markings/propagation-configs` | 列表 |
| GET | `/v1/aip/markings/propagation-configs/{project_id}/{object_type}` | 单条 |
| POST | `/v1/aip/markings/records` | 记录标记 |
| GET | `/v1/aip/markings/records` | 标记列表 |
| GET | `/v1/aip/markings/records/{project_id}/{object_type}/{object_id}` | 单条标记 |
| POST | `/v1/aip/markings/propagate` | 执行传播 |

### 4.3 #100 标记移除策略

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/aip/markings/removal-policies` | 注册策略 |
| GET | `/v1/aip/markings/removal-policies` | 列表 |
| GET | `/v1/aip/markings/removal-policies/{policy_id}` | 单条 |
| PUT | `/v1/aip/markings/removal-policies/{policy_id}` | 更新 |
| DELETE | `/v1/aip/markings/removal-policies/{policy_id}` | 删除 |
| POST | `/v1/aip/markings/removal-policies/{policy_id}/apply` | 执行移除 |
| GET | `/v1/aip/markings/removal-results` | 移除结果列表 |

---

## 5. 集成点

### 5.1 main.py（最小更改）

```python
from aos_api.routers import (..., cap_and_markings, ...)
application.include_router(cap_and_markings.router)
```

### 5.2 与 W2-X/W2-U 协同

- `CapConstraintEngine.check(CAP-01)` 可在 `CapabilityAdapterEngine.register` 前调用（校验超 FUNC-03 须 Capability）
- `MarkingPropagationEngine.record_marking` 可消费 W2-U `EgressPolicyEngine` 的 security_label
- `MarkingRemovalEngine.apply` 可作为 Pipeline 输出阶段的标记清理钩子

### 5.3 与 07b §4 对齐

- CAP-01~07 全部 7 个约束作为默认规则注册（DEFAULT_RULES）
- enforcement 默认 block（CAP-01/03/04/05）/ audit（CAP-02/06/07）

---

## 6. 测试计划

文件：`tests/test_cap_and_markings.py`（新增，约 45 个用例）

### 6.1 CapConstraintEngine（15）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | list_rules 默认 | 返回 7 条 CAP-01~07 |
| 2 | get_rule CAP-01 | 返回带 code/title |
| 3 | get_rule 未找到 | NOT_FOUND |
| 4 | update_rule | 修改后 get 返回新值 |
| 5 | list_rules enabled_only | 过滤禁用 |
| 6 | check CAP-01 block | resolution=blocked |
| 7 | check CAP-02 audit | resolution=audited |
| 8 | check CAP-07 dry_run | resolution=dry_run_passed |
| 9 | check disabled rule | resolution=dry_run_passed |
| 10 | list_violations 默认 | 列表 |
| 11 | list_violations 按 code 过滤 | 仅返回匹配 |
| 12 | list_violations 按 target_type 过滤 | 仅返回匹配 |
| 13 | get_violation 单条 | 返回详情 |
| 14 | get_violation 未找到 | NOT_FOUND |
| 15 | 200 条上限 | 旧记录被淘汰 |

### 6.2 MarkingPropagationEngine（15）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | set_config | 返回带 project_id+object_type |
| 2 | get_config | 返回配置 |
| 3 | get_config 默认回退 | stop_propagating=False |
| 4 | list_configs | 列表 |
| 5 | list_configs 按 project_id 过滤 | 仅返回匹配 |
| 6 | record_marking | 返回带 id |
| 7 | get_marking | 返回详情 |
| 8 | get_marking 未找到 | NOT_FOUND |
| 9 | list_markings 默认 | 列表 |
| 10 | list_markings 按 security_label 过滤 | 仅返回匹配 |
| 11 | propagate 正常 | 下游继承 source 标记 |
| 12 | propagate stop_propagating=True | 下游 is_inherited=False |
| 13 | propagate 默认配置 | 下游继承 |
| 14 | propagate source 未找到 | NOT_FOUND |
| 15 | 200 条上限 | 旧记录被淘汰 |

### 6.3 MarkingRemovalEngine（15）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register_policy | 返回带 id |
| 2 | get_policy | 返回详情 |
| 3 | get_policy 未找到 | NOT_FOUND |
| 4 | list_policies 默认 | 列表 |
| 5 | list_policies 按 project_id 过滤 | 仅返回匹配 |
| 6 | list_policies enabled_only | 过滤禁用 |
| 7 | update_policy | 修改后 get 返回新值 |
| 8 | delete_policy | 删除成功 |
| 9 | apply filter_in | 仅保留 keep_labels |
| 10 | apply filter_out | 移除 removed_labels |
| 11 | apply apply_to_inherited=False | 跳过 inherited |
| 12 | apply 禁用策略 | 抛 POLICY_DISABLED |
| 13 | apply 未知策略 | NOT_FOUND |
| 14 | list_results | 结果列表 |
| 15 | 200 条上限 | 旧记录被淘汰 |

---

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| CAP 校验阻塞正常调用 | enforcement=audit/dry_run 可降级 |
| 标记传播死循环 | propagate 仅支持 source→downstream 单跳，不递归 |
| 移除策略误删 | apply_to_inherited 默认 True 但可关闭；filter_in 需显式 keep_labels |
| 默认 enforcement 过严 | CAP-02/06/07 默认 audit，不阻塞 |

---

## 8. 交付物清单

| 路径 | 状态 | 说明 |
| --- | --- | --- |
| `docs/palantier/20_tech/220tech_w2-y-cap-and-markings.md` | 新建 | 本文档 |
| `aos-platform/services/aos-api/aos_api/cap_and_markings.py` | 新建 | 3 引擎 + 单例 |
| `aos-platform/services/aos-api/aos_api/routers/cap_and_markings.py` | 新建 | ~20 个端点 |
| `aos-platform/services/aos-api/tests/test_cap_and_markings.py` | 新建 | ~45 测试 |
| `aos-platform/services/aos-api/aos_api/main.py` | 修改 2 行 | import + include_router |
| `docs/palantier/20_tech/220plan-分阶段开发与里程碑计划.md` | 更新 | v3.7 → v3.8，标记 #88/#99/#100 ✅ |

---

## 9. 验收标准

1. ✅ 所有 ~45 个单测全绿
2. ✅ 全量回归无新增失败（pre-existing wiki flaky 不计）
3. ✅ `main.py` 启动无报错，新路由 `/v1/aip/cap-constraints/*` `/v1/aip/markings/*` 可访问
4. ✅ 方案文档与代码字段一致
5. ✅ 看板进度从 56/166 → 59/166，全局 102 → 105 / 259

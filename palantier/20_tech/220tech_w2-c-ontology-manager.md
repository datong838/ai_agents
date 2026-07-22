# 220tech · W2-C 第三批 Ontology Manager / OE（5 项）

> **版本**：v1.0 · 2026-07-22 · **关联**：220plan §1.2.3 W2+ #12/#13/#14/#15/#16
> **前置**：W2-3 Ontology Output · W1-3 Action 写回 · W2-B Functions 运行时
> **依赖**：ontology_output store · widget_registry · functions_runtime

## 1. 范围与目标

本批交付 Ontology Manager / Object Explorer 5 项后端能力。遵循「独立内存 store + 不污染已稳定 DB 表」原则，#14/#15/#16 Action 规则系列使用独立 store，避免触碰 `meta_action_type` 的 seed 流程。

| 编号 | 差距项 | 核心交付 | 主文件 |
|------|--------|----------|--------|
| W2-#13 | Object Views 微件系统 | 10+ 种微件 + 可视化编辑器 + 视图 CRUD | `object_views.py` |
| W2-#12 | OE 探索图表可视化 | 7 种图表 + 拖拽排序 + 撤销重做 + 保存设计 | `object_explorer.py` |
| W2-#14 | Action 规则可视化 | 规则引擎（create/modify/delete/link） + CRUD | `action_rules.py` |
| W2-#15 | Action 函数规则 | 引用 Functions 运行时的 Function 作为规则动作 | `action_rules.py`（同模块扩展） |
| W2-#16 | Action 可视化编辑器 | 参数 schema → 表单 spec + 创建向导 + 实时预览 | `action_visual_editor.py` |

## 2. 数据模型

### 2.1 Object Views（#13）

```python
WidgetKind = Literal[
    "property_table", "property_list", "object_card", "timeline",
    "bar_chart", "line_chart", "pie_chart", "scatter_plot",
    "map_view", "media_gallery", "link_list", "rich_text",
]  # 12 种微件

class ViewWidget(BaseModel):
    id: str
    kind: WidgetKind
    title: str = ""
    bound_field: str = ""        # 绑定的 OTD 字段
    config: dict[str, Any] = {}  # 微件自有配置（如 chart 的 groupBy）

class ObjectView(BaseModel):
    id: str
    name: str
    otd_id: str                  # 关联的对象类型
    widgets: list[ViewWidget]    # 微件列表（有序）
    is_default: bool = False

class ObjectViewStore:
    def create/get/list_by_otd/update/delete/reorder_widgets
```

### 2.2 OE 探索图表（#12）

```python
ChartKind = Literal[
    "bar", "line", "pie", "scatter", "heatmap", "histogram", "table",
]  # 7 种图表

class ExplorerDesign(BaseModel):
    id: str
    name: str
    otd_id: str
    chart_kind: ChartKind
    group_by: str = ""
    metrics: list[dict] = []     # [{field, agg: "count"|"sum"|"avg"}]
    filters: list[dict] = []
    sort_order: int = 0
    saved_at: str

class DesignHistory(BaseModel):
    design_id: str
    undo_stack: list[ExplorerDesign]
    redo_stack: list[ExplorerDesign]

class ObjectExplorerStore:
    def create/get/list/update/delete
    def save_design / undo / redo  # 撤销重做
    def render(design_id, rows) -> dict   # 渲染图表数据
```

### 2.3 Action 规则（#14）

```python
RuleKind = Literal[
    "create", "modify", "delete", "link",
]  # 4 种规则动作

class ActionRule(BaseModel):
    id: str
    name: str
    action_type_id: str          # 关联的 Action Type
    kind: RuleKind
    condition: str = ""          # DSL 表达式（复用 function_engine）
    target_otd_id: str = ""
    enabled: bool = True
    priority: int = 0

class ActionRuleStore:
    def create/get/list_by_action/update/delete
    def evaluate(rule_id, context: dict) -> bool   # 用 function_engine 求值 condition
    def list_rules_for_action(action_type_id) -> list[ActionRule]
```

### 2.4 Action 函数规则（#15）

```python
class FunctionRule(BaseModel):
    id: str
    name: str
    action_type_id: str
    function_id: str             # 引用 functions_runtime.RuntimeFunction
    trigger: Literal["before", "after", "instead"] = "before"
    condition: str = ""
    enabled: bool = True

class FunctionRuleStore:
    def create/get/list_by_action/update/delete
    def resolve(function_rule_id) -> RuntimeFunction  # 经 functions_runtime 查找
    def execute(function_rule_id, payload) -> Any     # 调用 Function
```

### 2.5 Action 可视化编辑器（#16）

```python
class FormFieldSpec(BaseModel):
    key: str
    label: str
    widget: Literal["text", "number", "select", "multiselect",
                    "toggle", "date", "object_ref", "expression"]
    required: bool = False
    default: Any = None
    options: list[str] = []      # select/multiselect 选项
    bound_otd: str = ""          # object_ref 绑定的对象类型

class ActionFormSpec(BaseModel):
    action_type_id: str
    fields: list[FormFieldSpec]
    wizard_steps: list[dict] = []   # 创建向导分步
    preview_template: str = ""      # 实时预览模板

class ActionVisualEditor:
    def generate_form_spec(action_type_id) -> ActionFormSpec  # 从 parameters JSONB 推导
    def validate_payload(form_spec, payload) -> list[str]
    def preview(action_type_id, payload) -> dict
```

## 3. 算法与接缝点

### 3.1 探索图表渲染（#12）

```
render(design, rows):
    filtered = [r for r in rows if 设计的 filters 都通过]
    if group_by:
        buckets = 按 group_by 字段分桶
        for metric in metrics: 按 agg 聚合
    return {chart_kind, series: [...], chartHint: design.chart_kind}
```
filters 复用 `function_engine.evaluate(parse(expr), row)`。

### 3.2 规则求值（#14/#15）

condition 是 DSL 表达式，复用 W1-1 `function_engine.parse + evaluate`：
```
evaluate(rule_id, context):
    rule = store.get(rule_id)
    if not rule.condition: return True
    return bool(evaluate(parse(rule.condition), context))
```

### 3.3 form-spec 推导（#16）

从 Action Type 的 `parameters` JSONB 推导表单：
```
for param in parameters:
    widget = _infer_widget(param)   # string→text, number→number, enum→select
    fields.append(FormFieldSpec(key=param.name, widget=widget, ...))
```
type 映射表内置于 action_visual_editor。

## 4. 测试矩阵

| 模块 | 测试文件 | 用例数 | 关键用例 |
|------|----------|--------|----------|
| Object Views | `test_object_views.py` | 12 | 12 种 widget kind、视图 CRUD、reorder、按 OTD 查询、默认视图 |
| OE 探索图表 | `test_object_explorer.py` | 12 | 7 种 chart kind、group_by 聚合、undo/redo、render、filters |
| Action 规则 | `test_action_rules.py` | 12 | 4 种 kind、condition 求值、按 action 查询、enable/disable、优先级 |
| Action 函数规则 | `test_action_function_rules.py` | 10 | 引用 Function、before/after/instead 触发、execute、condition |
| Action 可视化编辑器 | `test_action_visual_editor.py` | 10 | form-spec 推导、validate payload、preview、wizard steps |

合计 56 用例。

## 5. 文件清单

**新增**：
- `aos_api/object_views.py` + `aos_api/routers/object_views.py`
- `aos_api/object_explorer.py` + `aos_api/routers/object_explorer.py`
- `aos_api/action_rules.py` + `aos_api/routers/action_rules.py`
- `aos_api/action_visual_editor.py` + `aos_api/routers/action_visual_editor.py`
- `tests/test_object_views.py`
- `tests/test_object_explorer.py`
- `tests/test_action_rules.py`
- `tests/test_action_function_rules.py`
- `tests/test_action_visual_editor.py`

**修改（最小增量）**：
- `aos_api/main.py`：注册 4 个新 router（**串行编辑，非并行**）

**不修改**（避免污染已稳定模块）：
- `aos_api/routers/actions.py`（DB 表 meta_action_type 不动）
- `aos_api/submission.py`（criteria DSL 不动）
- `aos_api/ontology_output.py`（OTD 不加字段，视图独立 store）

## 6. 风险与对策

| 风险 | 对策 |
|------|------|
| 内存 store 进程重启丢失 | 与 W2-A/W2-B 一致的内存模型，生产化在后置 Phase |
| 规则 condition DSL 越界 | 复用 function_engine（已沙箱化），禁裸 eval |
| Function 引用悬空 | resolve 时检查 functions_runtime.get，未找到抛 NOT_FOUND |
| form-spec 与 parameters 不一致 | generate 时严格按 parameters 推导，不引入额外字段 |
| 同文件并行编辑覆盖 | main.py 注册一律串行单次编辑 |

# 220tech · W1-3 Funnel 可视化映射编辑器

> **版本**：v1.0 · 2026-07-22
> **关联**：220plan §1.2.2 W1-3 · Phase 3 · 中优先级
> **依赖**：W1-1 function_engine（映射表达式求值）、W1-5 funnel_engine（四阶段管道的映射阶段）
> **范围**：源 Schema 侧栏 + 映射表格 + 自动映射 + Lint 门控 + 行业模板

---

## 1. 目标与差距

| 维度 | 当前 | 目标 |
| --- | --- | --- |
| 源 Schema | 无结构化展示 | SchemaField 列表（name + type + nullable） |
| 映射表格 | 无 | MappingRule（source → target + 表达式 + 默认值） |
| 自动映射 | 无 | 按名称 + 类型兼容自动匹配 |
| Lint 门控 | 无 | 检查未映射/类型不匹配/重复 |
| 行业模板 | 无 | 电商/制造/金融预设 |

## 2. 数据模型

```python
class SchemaField(BaseModel):
    name: str
    type: Literal["string", "number", "boolean", "date"]
    nullable: bool = True

class MappingRule(BaseModel):
    source_field: str | None              # None 表示常量/default 填充
    target_field: str
    transform_expr: str | None = None     # 可选：W1-1 表达式变换
    default: Any = None                   # source 为空时的默认值

class MappingSpec(BaseModel):
    id: str
    name: str
    source_schema: list[SchemaField]
    target_schema: list[SchemaField]
    rules: list[MappingRule] = []
    template: str | None = None

class LintResult(BaseModel):
    passed: bool
    errors: list[str]
    warnings: list[str]
    unmapped_targets: list[str]
    type_mismatches: list[str]
```

## 3. 类型兼容矩阵

| target ↓ \ source → | string | number | boolean | date |
| --- | --- | --- | --- | --- |
| string | ✓ | ✓（toString） | ✓ | ✓ |
| number | ✗ | ✓ | ✗ | ✗ |
| boolean | ✗ | ✗ | ✓ | ✗ |
| date | ✗ | ✗ | ✗ | ✓ |

## 4. FunnelMappingEditor

```python
class FunnelMappingEditor:
    def create(name, source_schema, target_schema) -> MappingSpec
    def add_rule(spec_id, rule) -> MappingSpec
    def remove_rule(spec_id, target_field) -> MappingSpec
    def auto_map(spec_id) -> MappingSpec           # 按名称匹配 + 类型兼容
    def lint(spec_id) -> LintResult
    def apply_template(spec_id, template_name) -> MappingSpec
    def preview(spec_id, source_rows) -> list[dict]  # 按映射转换
```

### 4.1 auto_map 算法

```
for target_field in target_schema:
    if target_field.name in source_field_names:
        source = find by name
        if type_compatible(source.type, target.type):
            add rule(source.name, target.name)
        else:
            warning("类型不兼容，跳过")
```

### 4.2 lint 规则

| 规则 | 级别 |
| --- | --- |
| 目标字段未映射 | error |
| 重复映射同一目标字段 | error |
| 类型不兼容 | error |
| source_field 不在 source_schema | error |
| target nullable=False 但无 default | warning |

### 4.3 preview 算法

```
for row in source_rows:
    out = {}
    for rule in rules:
        if rule.source_field and rule.source_field in row:
            val = row[rule.source_field]
            if rule.transform_expr:
                val = evaluate(parse(rule.transform_expr), {rule.source_field: val, "row": row})
        else:
            val = rule.default
        out[rule.target_field] = val
    result.append(out)
```

## 5. 行业模板

```python
TEMPLATES = {
    "ecommerce": {
        "target_schema": [order_id, customer_id, product_id, quantity, price, total],
        "rules": [  # 名称模糊匹配
            {"source_pattern": "order", "target": "order_id"},
            ...
        ]
    },
    "manufacturing": {...},
    "finance": {...},
}
```

## 6. REST API

> 命名空间 `/v1/funnel-mappings`。

| 方法 | 路径 | 功能 |
| --- | --- | --- |
| POST | `/v1/funnel-mappings` | 创建 |
| GET | `/v1/funnel-mappings` | 列表 |
| GET | `/v1/funnel-mappings/{id}` | 详情 |
| POST | `/v1/funnel-mappings/{id}/rules` | 添加规则 |
| DELETE | `/v1/funnel-mappings/{id}/rules/{target}` | 删除规则 |
| POST | `/v1/funnel-mappings/{id}/auto-map` | 自动映射 |
| POST | `/v1/funnel-mappings/{id}/lint` | Lint 检查 |
| POST | `/v1/funnel-mappings/{id}/apply-template` | 套用模板 |
| POST | `/v1/funnel-mappings/{id}/preview` | 预览转换 |
| GET | `/v1/funnel-mappings/templates` | 列出模板 |

## 7. 测试用例（≥ 16）

引擎：create/add_rule/remove_rule/auto_map/lint（passed/未映射/类型不匹配/重复）/apply_template/preview（含表达式/默认值）/get_404 等 ≥ 10
API：create/list/rules/auto-map/lint/preview/templates/404 等 ≥ 6

## 8. 文件清单

| 路径 | 类型 |
| --- | --- |
| `aos_api/funnel_mapping.py` | 新增 |
| `aos_api/routers/funnel_mappings.py` | 新增 |
| `aos_api/main.py` | 修改 |
| `tests/test_funnel_mapping.py` | 新增 |

## 9. 不做的事

- ❌ 前端可视化拖拽（后续前端 Phase）
- ❌ 多源 Join 映射（W2+ Pipeline Builder 多数据源）
- ❌ 模板 CRUD（本期预设 3 个，自定义在 Phase 6）

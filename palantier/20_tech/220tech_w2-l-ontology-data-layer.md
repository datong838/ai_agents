# W2-L · Object 数据层增强组微规格（#33 / #29 / #30）

> **版本**：v1.0 · 2026-07-22
> **所属 Wave**：W2+ 中优先级
> **关联差距**：#33 Shared Property / #29 Type Coherence / #30 多源异构解法 A/C

---

## 1. 范围与目标

| 编号 | 差距项 | 当前状态 | 本批目标 |
|------|--------|----------|----------|
| #33 | Shared Property | 无 | 跨 OT 复用属性 / 集中管理 / 引用绑定 |
| #29 | Type Coherence | 无 | L1/L2 Schema 冲突检测 + 告警 |
| #30 | 多源异构解法 A/C | 仅解法 B | 解法 A（L1 Join 宽表）+ 解法 C（Function 派生） |

---

## 2. #33 Shared Property

### 2.1 模型

```python
class SharedProperty(BaseModel):
    id: str
    name: str
    data_type: str
    description: str = ""
    backing_column: str = ""
    nullable: bool = True
    referenced_by: list[str] = []  # Object Type IDs that reference this
```

### 2.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/ontology/shared-properties` | 列出共享属性 |
| POST | `/v1/ontology/shared-properties` | 创建共享属性 |
| GET/PUT/DELETE | `/v1/ontology/shared-properties/{id}` | CRUD |
| POST | `/v1/ontology/shared-properties/{id}/attach` | 绑定到 Object Type |
| POST | `/v1/ontology/shared-properties/{id}/detach` | 从 OT 解绑 |

---

## 3. #29 Type Coherence

### 3.1 冲突类型

| 冲突码 | 说明 |
|--------|------|
| `TC-01` | 属性类型不匹配（OT 声明 string vs dataset 列 int） |
| `TC-02` | 缺失列（OT 引用的 backing_column 在 dataset 中不存在） |
| `TC-03` | 多余列（dataset 有列但 OT 未声明） |
| `TC-04` | 可空性冲突（OT 声明 nullable=false 但 dataset 列允许 null） |

### 3.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/v1/ontology/type-coherence/check` | 检查指定 OT 与其 backing dataset 的 Schema 一致性 |
| GET | `/v1/ontology/type-coherence/conflicts` | 列出所有已知冲突 |

---

## 4. #30 多源异构解法 A/C

### 4.1 解法 A：L1 Join 宽表

将多个 dataset 通过 join key 合并为一个宽表，作为 OT 的 backing dataset。

```python
class L1JoinConfig(BaseModel):
    id: str
    object_type: str
    primary_dataset: str           # 主表 RID
    primary_key: str               # 主表 join key
    joins: list[JoinSpec] = []     # join 配置列表

class JoinSpec(BaseModel):
    dataset: str                   # 被join表 RID
    join_type: str = "left"        # left/inner/outer
    left_key: str                  # 主表 key
    right_key: str                 # 被join表 key
    columns: list[str] = []        # 需要引入的列（空=全部）
```

### 4.2 解法 C：Computed Property + Function

通过 Function 派生属性值。

```python
class ComputedProperty(BaseModel):
    id: str
    object_type: str
    property_name: str
    function_name: str             # 引用的 Function 名称
    input_mapping: dict = {}       # 输入参数 → OT 属性映射
    output_type: str = "string"
```

### 4.3 API

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/v1/ontology/l1-joins` | 创建 L1 Join 配置 |
| GET | `/v1/ontology/l1-joins` | 列出 L1 Join 配置 |
| GET | `/v1/ontology/l1-joins/{id}` | 获取 L1 Join 详情 |
| POST | `/v1/ontology/l1-joins/{id}/preview` | 预览 join 结果列 |
| POST | `/v1/ontology/computed-properties` | 创建计算属性 |
| GET | `/v1/ontology/computed-properties` | 列出计算属性 |
| GET | `/v1/ontology/computed-properties/{id}` | 获取计算属性详情 |

---

## 5. 实现计划

### 5.1 新增文件

| 文件 | 用途 |
|------|------|
| `aos_api/ontology_data_layer.py` | 核心引擎 |
| `aos_api/routers/ontology_data_layer.py` | API 路由 |
| `tests/test_ontology_data_layer.py` | 单元测试 |

### 5.2 修改文件

| 文件 | 修改内容 |
|------|----------|
| `aos_api/main.py` | 注册新路由 |

### 5.3 测试计划

| 测试类 | 用例数 |
|--------|--------|
| Shared Property | ~8 |
| Type Coherence | ~8 |
| L1 Join + Computed Property | ~8 |
| 合计 | ~24 |

# W2-O · 类型系统与视图配置组微规格（#51 / #52 / #53）

> **版本**：v1.0 · 2026-07-22
> **所属 Wave**：W2+ 中优先级
> **关联差距**：#51 Object Views 配置文件 / #52 完整类型系统 / #53 值类型与条件格式化

---

## 1. 范围与目标

| 编号 | 差距项 | 当前状态 | 本批目标 |
|------|--------|----------|----------|
| #51 | Object Views 配置文件 | 无 | 不同用户组不同标签页/可切换 |
| #52 | 完整类型系统（20+ 基础类型） | string/number/bool | Timestamp/Vector/Attachment/TimeSeries/MediaReference/Cipher |
| #53 | 值类型/条件格式化/类型类 | 无 | 语义约束/标准比较规则/30+ 类型类/渲染提示 |

---

## 2. #51 Object Views 配置文件

### 2.1 模型

```python
class ViewProfile(BaseModel):
    id: str
    name: str
    object_type: str
    user_groups: list[str]       # 适用用户组
    tabs: list[ViewTab]           # 标签页配置
    is_default: bool = False

class ViewTab(BaseModel):
    id: str
    name: str
    widgets: list[str]            # 微件 ID 列表
    visible: bool = True
```

### 2.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/ontology/view-profiles` | 列出视图配置 |
| POST | `/v1/ontology/view-profiles` | 创建视图配置 |
| GET/PUT/DELETE | `/v1/ontology/view-profiles/{id}` | CRUD |
| POST | `/v1/ontology/view-profiles/{id}/activate` | 为用户组激活配置 |

---

## 3. #52 完整类型系统

### 3.1 基础类型（20+）

| 类别 | 类型 |
|------|------|
| 标量 | String, Text, Integer, Long, Float, Double, Decimal, Boolean |
| 时间 | Date, Time, Timestamp, Interval |
| 二进制 | Byte, ByteArray, Attachment, MediaReference |
| 复合 | Vector, TimeSeries, JSON, Geopoint, Geoshape |
| 安全 | Cipher, Hash |

### 3.2 类型验证

每种类型提供 `validate(value) -> bool` 和 `coerce(value) -> Any` 方法。

---

## 4. #53 值类型/条件格式化/类型类

### 4.1 类型类（30+）

类型类是对基础类型的语义分组，如：
- `currency` → Decimal + 货币符号渲染
- `percentage` → Float + 百分比渲染
- `url` → String + 链接渲染
- `email` → String + 邮件渲染

### 4.2 条件格式化

```python
class ConditionalFormat(BaseModel):
    id: str
    field: str
    condition: str        # 表达式
    style: dict           # {color, background, icon, ...}
```

---

## 5. 实现计划

### 5.1 新增文件

| 文件 | 用途 |
|------|------|
| `aos_api/type_system.py` | 核心引擎（TypeSystem + ViewProfileEngine + FormatEngine） |
| `aos_api/routers/type_system.py` | API 路由 |
| `tests/test_type_system.py` | 单元测试 |

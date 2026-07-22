# W2-K · Ontology 管理增强组微规格（#36 / #37 / #32）

> **版本**：v1.0 · 2026-07-22
> **所属 Wave**：W2+ 中优先级
> **关联差距**：#36 OMA 编辑历史/恢复 / #37 Ontology 清理工具 / #32 Ontology Interface

---

## 1. 范围与目标

| 编号 | 差距项 | 当前状态 | 本批目标 |
|------|--------|----------|----------|
| #36 | OMA 编辑历史/恢复 | 无 | 全局时间线 + 按作者合并 + 逐条回退 |
| #37 | Ontology 清理工具 | 无 | 延迟/弃用/删除三级 + 6 种清理标记 + 正则筛选 |
| #32 | Ontology Interface | 无 | 接口类型 CRUD + extend/implement 多态 |

---

## 2. #36 编辑历史/恢复

### 2.1 数据模型

```python
class EditEvent(BaseModel):
    id: str
    target_type: str        # object_type / link_type / property / interface
    target_id: str
    action: str             # create / update / delete / publish
    author: str
    timestamp: str
    before: dict = {}       # 变更前快照
    after: dict = {}        # 变更后快照
    description: str = ""
    rolled_back: bool = False
```

### 2.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/ontology/edit-history` | 全局时间线（可按 target_type/author 过滤） |
| GET | `/v1/ontology/edit-history/{event_id}` | 获取事件详情 |
| POST | `/v1/ontology/edit-history/{event_id}/rollback` | 回退单个事件 |
| POST | `/v1/ontology/edit-history/rollback-by-author` | 按作者批量回退 |

---

## 3. #37 清理工具

### 3.1 三级操作

| 级别 | 操作 | 效果 |
|------|------|------|
| 1 | `delay` | 延迟（标记为待清理，不立即执行） |
| 2 | `deprecate` | 弃用（标记 deprecated，只读） |
| 3 | `delete` | 删除 |

### 3.2 六种清理标记

| 标记 | 自动检测条件 |
|------|-------------|
| `deprecated_date_passed` | 弃用日期已过 |
| `recycle_bin_source` | 数据源标记为回收站 |
| `long_no_update` | 长时间未更新（>90 天） |
| `missing_description` | 缺少描述 |
| `name_matches_regex` | 名称匹配正则 `[test\|deprecated]` |
| `unindexed` | 取消索引 |

### 3.3 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/ontology/cleanup/scan` | 扫描并返回带清理标记的资源 |
| POST | `/v1/ontology/cleanup/apply` | 对指定资源执行延迟/弃用/删除 |
| POST | `/v1/ontology/cleanup/batch` | 批量操作（按标记筛选） |

---

## 4. #32 Ontology Interface

### 4.1 数据模型

```python
class OntologyInterface(BaseModel):
    id: str
    name: str
    description: str = ""
    properties: list[dict] = []       # 接口定义的属性签名
    extends: list[str] = []           # 继承的父接口 ID
    implemented_by: list[str] = []    # 实现该接口的 Object Type ID
    version: int = 1
    owner: str = ""
    created_at: str
    updated_at: str
```

### 4.2 API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/ontology/interfaces` | 列出接口 |
| POST | `/v1/ontology/interfaces` | 创建接口 |
| GET | `/v1/ontology/interfaces/{interface_id}` | 获取接口详情 |
| PUT | `/v1/ontology/interfaces/{interface_id}` | 更新接口 |
| DELETE | `/v1/ontology/interfaces/{interface_id}` | 删除接口 |
| POST | `/v1/ontology/interfaces/{interface_id}/implement` | Object Type 声明实现接口 |
| GET | `/v1/ontology/interfaces/{interface_id}/implementors` | 列出实现者 |

---

## 5. 实现计划

### 5.1 新增文件

| 文件 | 用途 |
|------|------|
| `aos_api/ontology_management.py` | 核心引擎：EditHistoryEngine + CleanupEngine + InterfaceEngine |
| `aos_api/routers/ontology_management.py` | API 路由 |
| `tests/test_ontology_management.py` | 单元测试 |

### 5.2 修改文件

| 文件 | 修改内容 |
|------|----------|
| `aos_api/main.py` | 注册新路由 |

### 5.3 测试计划

| 测试类 | 用例数 |
|--------|--------|
| Edit History | ~8 |
| Cleanup | ~8 |
| Interface | ~8 |
| 合计 | ~24 |

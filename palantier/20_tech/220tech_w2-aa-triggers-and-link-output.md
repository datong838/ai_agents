# 220tech · W2-AA · 触发器与 Ontology 链接输出组（#97 / #98 / #91）

> **版本**：v1.0 · 2026-07-22
> **状态**：✅ 方案定稿 · 可编码
> **对齐**：
> - 差距分析 [220w](./220w-与目标系统差距对照分析.md) §4.2 #97/#98 + §3.2 #91 链接类型输出
> - 产品方案 [06](../06-数据管道Pipeline-Builder产品方案.md) §5（触发器）· [06b](../06b-Pipeline输出与Ontology产品方案.md) §2（Ontology 输出）
> - 技术方案 [T06](./T06-数据管道详细技术方案.md) §5（触发器）· §6（Ontology 输出）
> - 上游 W1-5 Pipeline 四阶段 · W2-3 OntologyOutputStore（对象类型输出）· W2-Z PipelineTypeEngine
> **范围**：W2-AA 收口 Pipeline 触发机制与 Ontology 链接类型输出三件 — Event Trigger（事件触发器）/ Composite Trigger（AND/OR 复合触发器）/ LinkType Output（Ontology 链接类型输出）
> **不替换底层**：本组是触发器与链接输出层，不重写 OntologyOutputStore（对象类型）/ SchedulingEngine

---

## 0. 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文回答 | 文档与代码注释均中文 |
| 先方案后编码 | 本文先定稿，再写引擎/路由/测试 |
| 最小更改 | 仅新增 `aos_api/triggers_and_link_output.py` + `aos_api/routers/triggers_and_link_output.py` + `tests/test_triggers_and_link_output.py`；`main.py` 加 2 行 |
| 不影响已有功能 | 三引擎纯新增；OntologyOutputStore 对象类型输出保留，仅新增链接类型 |
| 自测验证 | 单测全绿 + 全量回归 + 方案对照 |
| 符合方案军规 | 事件触发器与 220w §4.2 一致；复合触发器 AND/OR 与 triggers-reference 一致；链接类型基数与 outputs-add-ontology-output 一致 |

---

## 1. 背景与边界

### 1.1 现状

| 能力 | 现状 | 缺口 |
| --- | --- | --- |
| Event Trigger | 无事件触发器；仅 Cron 调度 | 🔴 缺 |
| Composite Trigger | 无 AND/OR 复合触发器 | 🔴 缺 |
| LinkType Output | 对象类型输出已有；链接类型输出缺 | 🔴 缺 |

### 1.2 边界

- ✅ 本组做：
  - #97 Event Trigger：dataset_updated/pipeline_built/schedule/manual 4 种事件源 + register/get/list/delete + fire 评估 + TriggerFire 记录
  - #98 Composite Trigger：AND/OR 逻辑组合 + 子触发器引用 + evaluate 评估 + fire
  - #91 LinkType Output：LinkTypeDefinition（一对多/多对多基数、主键/外键/显示名称）+ CRUD + infer_from_objects
- ❌ 本组不做：
  - 实际调度执行（属 SchedulingEngine）
  - 对象类型输出（已有 OntologyOutputStore）
  - 链接类型实际写回 Ontology 图谱

---

## 2. 数据模型

### 2.1 #97 Event Trigger

```python
class EventTrigger(BaseModel):
    """事件触发器。"""
    id: str
    name: str
    event_source: str             # dataset_updated / pipeline_built / schedule / manual
    target_pipeline_id: str       # 触发的目标管道
    source_ref: str = ""          # 事件源引用（dataset rid / pipeline id / cron expr）
    condition: str = ""           # 可选条件表达式
    enabled: bool = True
    cooldown_seconds: float = 0.0
    last_fired_at: float = 0.0
    fire_count: int = 0
    created_at: float = 0.0


class TriggerFire(BaseModel):
    """触发器点火记录。"""
    id: str
    trigger_id: str
    trigger_name: str
    event_source: str
    target_pipeline_id: str
    event_payload: dict[str, Any] = {}
    status: str = "fired"         # fired / skipped / cooldown
    fired_at: float = 0.0


_VALID_EVENT_SOURCES = {"dataset_updated", "pipeline_built", "schedule", "manual"}
```

### 2.2 #98 Composite Trigger

```python
class CompositeTrigger(BaseModel):
    """复合触发器。"""
    id: str
    name: str
    logic: str                    # and / or
    child_trigger_ids: list[str]  # 子触发器引用
    target_pipeline_id: str
    enabled: bool = True
    cooldown_seconds: float = 0.0
    last_fired_at: float = 0.0
    fire_count: int = 0
    created_at: float = 0.0


_VALID_COMPOSITE_LOGICS = {"and", "or"}
```

### 2.3 #91 LinkType Output

```python
class LinkTypeDefinition(BaseModel):
    """Ontology 链接类型输出定义。"""
    id: str
    name: str
    display_name: str = ""
    cardinality: str              # one_to_many / many_to_one / many_to_many
    source_object_type: str       # 主键对象类型
    target_object_type: str       # 外键对象类型
    source_pk_field: str          # 主键字段
    target_fk_field: str          # 外键字段
    display_field: str = ""       # 显示名称字段
    source_pipeline_id: str = ""
    description: str = ""
    created_at: float = 0.0


_VALID_CARDINALITIES = {"one_to_many", "many_to_one", "many_to_many"}
```

---

## 3. 引擎设计

文件：`aos_api/triggers_and_link_output.py`（新增，3 个引擎）

### 3.1 EventTriggerEngine（#97）

```python
class EventTriggerEngine:
    def register(self, trigger: EventTrigger) -> EventTrigger: ...
    def get(self, trigger_id: str) -> EventTrigger: ...
    def list(self, event_source: str | None = None, enabled_only: bool = False) -> list[EventTrigger]: ...
    def update(self, trigger_id: str, updates: dict[str, Any]) -> EventTrigger: ...
    def delete(self, trigger_id: str) -> bool: ...
    def fire(self, trigger_id: str, event_payload: dict[str, Any] | None = None) -> TriggerFire: ...
    """点火：检查 enabled → 检查 cooldown → 记录 TriggerFire → 推进 last_fired_at/fire_count"""
    def list_fires(self, trigger_id: str | None = None, limit: int = 50) -> list[TriggerFire]: ...
```

**fire 流程**：
1. 取 trigger，校验 enabled，否则 status=skipped
2. 检查 cooldown（now - last_fired_at < cooldown_seconds → status=cooldown）
3. status=fired，推进 last_fired_at + fire_count++
4. 200 条 TriggerFire 上限

### 3.2 CompositeTriggerEngine（#98）

```python
class CompositeTriggerEngine:
    def register(self, trigger: CompositeTrigger) -> CompositeTrigger: ...
    def get(self, trigger_id: str) -> CompositeTrigger: ...
    def list(self, enabled_only: bool = False) -> list[CompositeTrigger]: ...
    def update(self, trigger_id: str, updates: dict[str, Any]) -> CompositeTrigger: ...
    def delete(self, trigger_id: str) -> bool: ...
    def evaluate(self, trigger_id: str, child_fires: dict[str, bool]) -> dict[str, Any]: ...
    """评估：AND=全 True / OR=任一 True；返回 fired=bool + detail"""
    def fire(self, trigger_id: str, child_fires: dict[str, bool]) -> TriggerFire: ...
    """复合点火：evaluate 通过则点火"""
```

**evaluate 流程**：
1. AND：所有 child_trigger_ids 在 child_fires 中为 True 才 fired=True
2. OR：任一 child 为 True 即 fired=True
3. child_fires 缺失的子视为 False

### 3.3 LinkTypeOutputEngine（#91）

```python
class LinkTypeOutputEngine:
    def register(self, link: LinkTypeDefinition) -> LinkTypeDefinition: ...
    def get(self, link_id: str) -> LinkTypeDefinition: ...
    def get_by_name(self, name: str) -> LinkTypeDefinition | None: ...
    def list(self, source_object_type: str | None = None, target_object_type: str | None = None) -> list[LinkTypeDefinition]: ...
    def update(self, link_id: str, updates: dict[str, Any]) -> LinkTypeDefinition: ...
    def delete(self, link_id: str) -> bool: ...
    def infer_from_objects(
        self, source_ot: str, target_ot: str, rows: list[dict[str, Any]],
        fk_field: str, display_field: str = "",
    ) -> LinkTypeDefinition: ...
    """从对象数据推断链接类型（默认 many_to_one）"""
    def preview_links(
        self, link_id: str, rows: list[dict[str, Any]], limit: int = 100,
    ) -> list[dict[str, Any]]: ...
    """预览链接实例"""
```

### 3.4 单例与持久化

- 3 个引擎均用**双重检查锁单例**
- 内存态为主，各 200 条上限（triggers/fires/links）

---

## 4. API 设计

文件：`aos_api/routers/triggers_and_link_output.py`（新增）

### 4.1 #97 Event Trigger

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/pipeline-triggers/events` | 注册事件触发器 |
| GET | `/v1/pipeline-triggers/events` | 列表 |
| GET | `/v1/pipeline-triggers/events/{trigger_id}` | 单条 |
| PUT | `/v1/pipeline-triggers/events/{trigger_id}` | 更新 |
| DELETE | `/v1/pipeline-triggers/events/{trigger_id}` | 删除 |
| POST | `/v1/pipeline-triggers/events/{trigger_id}/fire` | 点火 |
| GET | `/v1/pipeline-triggers/events/fires` | 点火记录 |

### 4.2 #98 Composite Trigger

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/pipeline-triggers/composites` | 注册复合触发器 |
| GET | `/v1/pipeline-triggers/composites` | 列表 |
| GET | `/v1/pipeline-triggers/composites/{trigger_id}` | 单条 |
| PUT | `/v1/pipeline-triggers/composites/{trigger_id}` | 更新 |
| DELETE | `/v1/pipeline-triggers/composites/{trigger_id}` | 删除 |
| POST | `/v1/pipeline-triggers/composites/{trigger_id}/evaluate` | 评估 |
| POST | `/v1/pipeline-triggers/composites/{trigger_id}/fire` | 复合点火 |

### 4.3 #91 LinkType Output

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/pipeline-outputs/link-types` | 注册链接类型 |
| GET | `/v1/pipeline-outputs/link-types` | 列表 |
| GET | `/v1/pipeline-outputs/link-types/{link_id}` | 单条 |
| PUT | `/v1/pipeline-outputs/link-types/{link_id}` | 更新 |
| DELETE | `/v1/pipeline-outputs/link-types/{link_id}` | 删除 |
| POST | `/v1/pipeline-outputs/link-types/infer` | 从对象推断 |
| POST | `/v1/pipeline-outputs/link-types/{link_id}/preview` | 预览链接实例 |

---

## 5. 集成点

### 5.1 main.py（最小更改）

```python
from aos_api.routers import (..., triggers_and_link_output, ...)
application.include_router(triggers_and_link_output.router)
```

### 5.2 与 W2-Z/W2-3 协同

- `EventTriggerEngine.fire` 可触发 W2-Z `PipelineTypeEngine.validate_run`
- `LinkTypeOutputEngine.register` 可关联 W2-3 `OntologyOutputStore` 的对象类型
- `infer_from_objects` 可消费 Pipeline 输出的 rows

---

## 6. 测试计划

文件：`tests/test_triggers_and_link_output.py`（新增，约 42 个用例）

### 6.1 EventTriggerEngine（15）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 未知 event_source | INVALID_EVENT_SOURCE |
| 3 | get 未找到 | NOT_FOUND |
| 4 | list 默认 | 列表 |
| 5 | list 按 event_source 过滤 | 仅匹配 |
| 6 | list enabled_only | 过滤禁用 |
| 7 | update | 修改后 get 返回新值 |
| 8 | delete | 删除成功 |
| 9 | fire 成功 | status=fired + fire_count++ |
| 10 | fire 禁用 | status=skipped |
| 11 | fire cooldown | status=cooldown |
| 12 | list_fires | 列表 |
| 13 | list_fires 按 trigger_id | 过滤 |
| 14 | register 缺 name | MISSING_NAME |
| 15 | 200 条 fire 上限 | 旧记录淘汰 |

### 6.2 CompositeTriggerEngine（14）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 未知 logic | INVALID_LOGIC |
| 3 | register 空 child | EMPTY_CHILDREN |
| 4 | get 未找到 | NOT_FOUND |
| 5 | list 默认 | 列表 |
| 6 | list enabled_only | 过滤 |
| 7 | update | 修改后返回新值 |
| 8 | delete | 删除成功 |
| 9 | evaluate AND 全 True | fired=True |
| 10 | evaluate AND 部分False | fired=False |
| 11 | evaluate OR 任一 True | fired=True |
| 12 | evaluate OR 全 False | fired=False |
| 13 | fire 通过 | status=fired |
| 14 | fire 未通过 | status=skipped |

### 6.3 LinkTypeOutputEngine（13）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 未知 cardinality | INVALID_CARDINALITY |
| 3 | register 缺 name | MISSING_NAME |
| 4 | get 未找到 | NOT_FOUND |
| 5 | get_by_name | 返回匹配 |
| 6 | list 默认 | 列表 |
| 7 | list 按 source_ot 过滤 | 仅匹配 |
| 8 | list 按 target_ot 过滤 | 仅匹配 |
| 9 | update | 修改后返回新值 |
| 10 | delete | 删除成功 |
| 11 | infer_from_objects | 返回 many_to_one |
| 12 | preview_links | 返回链接实例 |
| 13 | register 重名 | NAME_DUPLICATE |

---

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 触发器频繁点火 | cooldown_seconds 冷却期 + 200 条 fire 上限 |
| 复合触发器子引用缺失 | child_fires 缺失视为 False；evaluate 不抛错 |
| 链接类型基数误配 | cardinality 白名单校验 |
| infer_from_objects 误判 | 默认 many_to_one；调用方可 update 修正 |
| 链接类型重名 | register 检查 NAME_DUPLICATE |

---

## 8. 交付物清单

| 路径 | 状态 | 说明 |
| --- | --- | --- |
| `docs/palantier/20_tech/220tech_w2-aa-triggers-and-link-output.md` | ✅ 本文件 | 微规约 |
| `aos_api/triggers_and_link_output.py` | ⬜ 待编码 | 3 引擎 |
| `aos_api/routers/triggers_and_link_output.py` | ⬜ 待编码 | ~21 端点 |
| `tests/test_triggers_and_link_output.py` | ⬜ 待编码 | ~42 用例 |
| `aos_api/main.py` | ⬜ +2 行 | import + include_router |

---

*v1.0 · w2-aa*

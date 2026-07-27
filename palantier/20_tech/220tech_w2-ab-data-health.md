# 220tech · W2-AB · Data Health 检查组（#133 / #134 / #135）

> **版本**：v1.0 · 2026-07-22
> **状态**：✅ 方案定稿 · 可编码
> **对齐**：
> - 差距分析 [220w](./220w-与目标系统差距对照分析.md) §11 #133/#134/#135 Data Health 检查类型/计划/组
> - 产品方案 [08](../08-数据治理DataHealth产品方案.md)（如有）
> - 上游 W2-3 Ontology 输出 · W2-Z Pipeline 类型语义
> **范围**：W2-AB 收口 Data Health 检查能力三件 — Check Type（检查类型定义）/ Check Schedule（检查计划 auto+manual）/ Check Group（检查分组+通知+监控）
> **不替换底层**：本组是检查层，不重写 Pipeline 输出或 Ontology 对象存储

---

## 0. 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文回答 | 文档与代码注释均中文 |
| 先方案后编码 | 本文先定稿，再写引擎/路由/测试 |
| 最小更改 | 仅新增 `aos_api/data_health.py` + `aos_api/routers/data_health.py` + `tests/test_data_health.py`；`main.py` 加 2 行 |
| 不影响已有功能 | 三引擎纯新增 |
| 自测验证 | 单测全绿 + 全量回归 + 方案对照 |
| 符合方案军规 | 5 种检查类型与 220w §11 一致；auto/manual 计划与 foundry data-health 一致；检查组通知与 foundry health-checks 一致 |

---

## 1. 背景与边界

### 1.1 现状

| 能力 | 现状 | 缺口 |
| --- | --- | --- |
| Data Health 检查类型 | 无 | 🔴 缺 5 种检查 |
| Data Health 检查计划 | 无 auto/manual | 🔴 缺 |
| Data Health 检查组 | 无分组/通知 | 🔴 缺 |

### 1.2 边界

- ✅ 本组做：
  - #133 Check Type：freshness/freshness_duration/volume/schema/content 5 种检查类型 + register/get/list/delete + run 执行
  - #134 Check Schedule：auto（数据集更新触发）+ manual（cron 定时）双模式 + enable/disable + next_run 计算
  - #135 Check Group：检查分组 CRUD + attach/detach 检查到组 + 通知配置 + 监控概览
- ❌ 本组不做：
  - 实际数据扫描执行（属 Pipeline/Build 引擎）
  - Issues 集成（#139 后续）
  - 数据集健康 Tab（#140 后续）

---

## 2. 数据模型

### 2.1 #133 Check Type

```python
class HealthCheckType(BaseModel):
    """检查类型定义。"""
    id: str
    name: str
    check_kind: str           # freshness / freshness_duration / volume / schema / content
    target_dataset_rid: str
    configuration: dict[str, Any] = {}   # 类型特定配置（如 threshold/cron/columns）
    severity: str = "warning"             # error / warning / info
    enabled: bool = True
    created_at: float = 0.0


class HealthCheckResult(BaseModel):
    """检查执行结果。"""
    id: str
    check_id: str
    check_kind: str
    status: str               # passed / failed / errored / skipped
    message: str = ""
    measured_value: Any | None = None
    threshold: Any | None = None
    executed_at: float = 0.0


_VALID_CHECK_KINDS = {"freshness", "freshness_duration", "volume", "schema", "content"}
_VALID_SEVERITIES = {"error", "warning", "info"}
_VALID_RESULT_STATUSES = {"passed", "failed", "errored", "skipped"}
```

### 2.2 #134 Check Schedule

```python
class HealthSchedule(BaseModel):
    """检查计划。"""
    id: str
    check_id: str
    mode: str                 # auto / manual
    cron_expression: str = "" # manual 模式 cron
    trigger_dataset_rid: str = ""  # auto 模式触发数据集
    enabled: bool = True
    last_run_at: float = 0.0
    next_run_at: float = 0.0
    run_count: int = 0
    created_at: float = 0.0


_VALID_SCHEDULE_MODES = {"auto", "manual"}
```

### 2.3 #135 Check Group

```python
class HealthCheckGroup(BaseModel):
    """检查分组。"""
    id: str
    name: str
    description: str = ""
    check_ids: list[str] = []
    notification_config: dict[str, Any] = {}  # email/webhook/severity_filter
    enabled: bool = True
    created_at: float = 0.0


class GroupMonitorSummary(BaseModel):
    """分组监控概览。"""
    group_id: str
    total_checks: int
    enabled_checks: int
    last_results: dict[str, str] = {}  # check_id -> last status
    pass_rate: float = 0.0
```

---

## 3. 引擎设计

文件：`aos_api/data_health.py`（新增，3 个引擎）

### 3.1 HealthCheckTypeEngine（#133）

```python
class HealthCheckTypeEngine:
    def register(self, check: HealthCheckType) -> HealthCheckType: ...
    def get(self, check_id: str) -> HealthCheckType: ...
    def list(self, check_kind: str | None = None, enabled_only: bool = False) -> list[HealthCheckType]: ...
    def update(self, check_id: str, updates: dict[str, Any]) -> HealthCheckType: ...
    def delete(self, check_id: str) -> bool: ...
    def run(self, check_id: str, measured_value: Any | None = None) -> HealthCheckResult: ...
    """执行检查：根据 check_kind + configuration + measured_value 判定 passed/failed"""
    def list_results(self, check_id: str | None = None, status: str | None = None, limit: int = 50) -> list[HealthCheckResult]: ...
```

**run 流程**：
1. 取 check，校验 enabled，否则 status=skipped
2. 根据 check_kind 评估：
   - freshness：measured_value（时间戳秒）与 threshold（最大延迟秒）比，now-measured <= threshold → passed
   - freshness_duration：同 freshness，但 threshold 单位为小时
   - volume：measured_value（行数）与 threshold（最小行数）比，>= → passed
   - schema：measured_value（列名列表）与 configuration["expected_columns"] 比，完全匹配 → passed
   - content：measured_value（dict）与 configuration["rules"] 比，全部满足 → passed
3. 200 条 result 上限

### 3.2 HealthScheduleEngine（#134）

```python
class HealthScheduleEngine:
    def register(self, schedule: HealthSchedule) -> HealthSchedule: ...
    def get(self, schedule_id: str) -> HealthSchedule: ...
    def list(self, check_id: str | None = None, mode: str | None = None, enabled_only: bool = False) -> list[HealthSchedule]: ...
    def update(self, schedule_id: str, updates: dict[str, Any]) -> HealthSchedule: ...
    def delete(self, schedule_id: str) -> bool: ...
    def trigger(self, schedule_id: str) -> dict[str, Any]: ...
    """触发执行：auto 检查 trigger_dataset_rid 更新事件 / manual 按 cron 推进 next_run_at"""
    def compute_next_run(self, schedule_id: str) -> float: ...
    """计算下次运行时间"""
```

**trigger 流程**：
1. 取 schedule，校验 enabled
2. 推进 last_run_at + run_count++
3. auto 模式：next_run_at 不变（事件驱动）；manual 模式：next_run_at = now + cron 间隔（简化：cron 解析为秒数）
4. 返回 {schedule_id, triggered: True, next_run_at}

### 3.3 HealthCheckGroupEngine（#135）

```python
class HealthCheckGroupEngine:
    def register(self, group: HealthCheckGroup) -> HealthCheckGroup: ...
    def get(self, group_id: str) -> HealthCheckGroup: ...
    def list(self, enabled_only: bool = False) -> list[HealthCheckGroup]: ...
    def update(self, group_id: str, updates: dict[str, Any]) -> HealthCheckGroup: ...
    def delete(self, group_id: str) -> bool: ...
    def attach_check(self, group_id: str, check_id: str) -> HealthCheckGroup: ...
    def detach_check(self, group_id: str, check_id: str) -> HealthCheckGroup: ...
    def monitor(self, group_id: str) -> GroupMonitorSummary: ...
    """汇总分组监控：total_checks/enabled_checks/last_results/pass_rate"""
    def send_notification(self, group_id: str, event: dict[str, Any]) -> dict[str, Any]: ...
    """发送通知（基于 notification_config）"""
```

### 3.4 单例与持久化

- 3 个引擎均用**双重检查锁单例**
- 内存态为主，各 200 条上限

---

## 4. API 设计

文件：`aos_api/routers/data_health.py`（新增）

### 4.1 #133 Check Type

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/data-health/checks` | 注册检查 |
| GET | `/v1/data-health/checks` | 列表 |
| GET | `/v1/data-health/checks/{check_id}` | 单条 |
| PUT | `/v1/data-health/checks/{check_id}` | 更新 |
| DELETE | `/v1/data-health/checks/{check_id}` | 删除 |
| POST | `/v1/data-health/checks/{check_id}/run` | 执行检查 |
| GET | `/v1/data-health/check-results` | 结果列表 |

### 4.2 #134 Check Schedule

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/data-health/schedules` | 注册计划 |
| GET | `/v1/data-health/schedules` | 列表 |
| GET | `/v1/data-health/schedules/{schedule_id}` | 单条 |
| PUT | `/v1/data-health/schedules/{schedule_id}` | 更新 |
| DELETE | `/v1/data-health/schedules/{schedule_id}` | 删除 |
| POST | `/v1/data-health/schedules/{schedule_id}/trigger` | 触发执行 |
| GET | `/v1/data-health/schedules/{schedule_id}/next-run` | 下次运行时间 |

### 4.3 #135 Check Group

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/data-health/groups` | 注册分组 |
| GET | `/v1/data-health/groups` | 列表 |
| GET | `/v1/data-health/groups/{group_id}` | 单条 |
| PUT | `/v1/data-health/groups/{group_id}` | 更新 |
| DELETE | `/v1/data-health/groups/{group_id}` | 删除 |
| POST | `/v1/data-health/groups/{group_id}/attach/{check_id}` | 挂载检查 |
| POST | `/v1/data-health/groups/{group_id}/detach/{check_id}` | 卸载检查 |
| GET | `/v1/data-health/groups/{group_id}/monitor` | 监控概览 |
| POST | `/v1/data-health/groups/{group_id}/notify` | 发送通知 |

---

## 5. 集成点

### 5.1 main.py（最小更改）

```python
from aos_api.routers import (..., data_health, ...)
application.include_router(data_health.router)
```

### 5.2 与 W2-AA/W2-Z 协同

- `HealthScheduleEngine.trigger` 可调用 `HealthCheckTypeEngine.run`
- `HealthCheckGroupEngine.monitor` 可聚合 `HealthCheckTypeEngine.list_results`
- auto 模式 trigger_dataset_rid 可关联 W2-Z Pipeline 输出 dataset

---

## 6. 测试计划

文件：`tests/test_data_health.py`（新增，约 42 个用例）

### 6.1 HealthCheckTypeEngine（15）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 未知 check_kind | INVALID_CHECK_KIND |
| 3 | register 缺 name | MISSING_NAME |
| 4 | register 未知 severity | INVALID_SEVERITY |
| 5 | get 未找到 | NOT_FOUND |
| 6 | list 默认 | 列表 |
| 7 | list 按 check_kind 过滤 | 仅匹配 |
| 8 | list enabled_only | 过滤禁用 |
| 9 | update | 修改后返回新值 |
| 10 | delete | 删除成功 |
| 11 | run freshness passed | status=passed |
| 12 | run freshness failed | status=failed |
| 13 | run disabled | status=skipped |
| 14 | list_results | 列表 |
| 15 | 200 条 result 上限 | 旧记录淘汰 |

### 6.2 HealthScheduleEngine（14）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register auto | 返回带 id |
| 2 | register manual | 返回带 id |
| 3 | register 未知 mode | INVALID_MODE |
| 4 | register auto 缺 trigger_dataset | MISSING_TRIGGER_DATASET |
| 5 | register manual 缺 cron | MISSING_CRON |
| 6 | get 未找到 | NOT_FOUND |
| 7 | list 默认 | 列表 |
| 8 | list 按 mode 过滤 | 仅匹配 |
| 9 | list enabled_only | 过滤禁用 |
| 10 | update | 修改后返回新值 |
| 11 | delete | 删除成功 |
| 12 | trigger auto | triggered=True + run_count++ |
| 13 | trigger manual | next_run_at 推进 |
| 14 | trigger disabled | 触发失败 |

### 6.3 HealthCheckGroupEngine（13）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 缺 name | MISSING_NAME |
| 3 | register 重名 | NAME_DUPLICATE |
| 4 | get 未找到 | NOT_FOUND |
| 5 | list 默认 | 列表 |
| 6 | list enabled_only | 过滤 |
| 7 | update | 修改后返回新值 |
| 8 | delete | 删除成功 |
| 9 | attach_check | check_ids 增长 |
| 10 | detach_check | check_ids 减少 |
| 11 | attach 重复 | 幂等无变化 |
| 12 | monitor | 返回 GroupMonitorSummary |
| 13 | send_notification | 返回派发结果 |

---

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 检查类型配置误配 | check_kind 白名单 + severity 白名单 |
| 计划频繁触发 | enabled 开关 + run_count 计数 |
| 分组检查引用缺失 | monitor 容忍缺失检查 |
| 通知配置错误 | notification_config 透传不强制校验 |
| 分组重名 | register 检查 NAME_DUPLICATE |

---

## 8. 交付物清单

| 路径 | 状态 | 说明 |
| --- | --- | --- |
| `docs/palantier/20_tech/220tech_w2-ab-data-health.md` | ✅ 本文件 | 微规约 |
| `aos_api/data_health.py` | ⬜ 待编码 | 3 引擎 |
| `aos_api/routers/data_health.py` | ⬜ 待编码 | ~22 端点 |
| `tests/test_data_health.py` | ⬜ 待编码 | ~42 用例 |
| `aos_api/main.py` | ⬜ +2 行 | import + include_router |

---

*v1.0 · w2-ab*

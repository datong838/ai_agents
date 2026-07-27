# W2-AK · Data Connection 安全治理组（#125 #126 #127）

> 所属阶段：W2+ 中优先级 · Phase 8+
> 批次代码：W2-AK
> 依赖：W2-AJ Webhook Pipeline / Output

---

## 批次范围

| # | 差距项 | 引擎 | 模块文件 |
| --- | --- | --- | --- |
| 125 | Data Connection Webhooks 执行策略 | WebhookExecutionPolicyEngine | `data_connection_security.py` |
| 126 | Data Connection Egress policies | EgressPolicyEngine | `data_connection_security.py` |
| 127 | Data Connection Exportable markings | ExportableMarkingEngine | `data_connection_security.py` |

路由：`routers/data_connection_security.py`
测试：`tests/test_data_connection_security.py`

---

## 1. #125 · Webhook Execution Policy（Webhook 执行策略）

### 1.1 数据模型

**WebhookExecutionPolicy**（执行策略）
- `policy_id: str` — 策略 ID
- `name: str` — 名称
- `webhook_id: str` — 关联 webhook
- `max_concurrent: int` — 最大并发数（默认 5）
- `rate_limit_per_minute: int` — 每分钟速率限制（默认 60）
- `timeout_ms: int` — 超时毫秒（默认 30000）
- `max_retries: int` — 最大重试次数（默认 3）
- `retry_backoff_ms: int` — 重试退避基数毫秒（默认 1000）
- `retry_on_status: list[int]` — 触发重试的 HTTP 状态码（默认 [429, 500, 502, 503, 504]）
- `circuit_breaker_enabled: bool` — 熔断开关（默认 True）
- `circuit_failure_threshold: float` — 熔断失败率阈值 0-1（默认 0.5）
- `circuit_cooldown_ms: int` — 熔断冷却毫秒（默认 60000）
- `status: str` — `active|disabled`（默认 `active`）
- `created_at: str` — ISO 时间
- `updated_at: str` — ISO 时间

**ExecutionState**（执行状态）
- `state_id: str` — 状态 ID
- `policy_id: str` — 策略 ID
- `current_concurrent: int` — 当前并发数
- `window_start: str` — 速率窗口起始
- `window_count: int` — 窗口内请求数
- `circuit_state: str` — `closed|open|half_open`
- `circuit_failure_count: int` — 失败计数
- `circuit_total_count: int` — 总计数
- `circuit_opened_at: str | None` — 熔断打开时间

**ExecutionAttempt**（执行尝试记录）
- `attempt_id: str` — 尝试 ID
- `policy_id: str` — 策略 ID
- `webhook_call_id: str` — webhook 调用 ID
- `attempt_number: int` — 第几次尝试
- `status: str` — `pending|success|failed|rate_limited|concurrency_limited|circuit_open`
- `http_status: int | None` — HTTP 状态码
- `duration_ms: int` — 耗时毫秒
- `started_at: str` — ISO 时间
- `finished_at: str | None` — ISO 时间
- `error_message: str | None` — 错误消息

### 1.2 引擎接口：WebhookExecutionPolicyEngine

#### CRUD
- `register(policy: WebhookExecutionPolicy) -> WebhookExecutionPolicy` — 注册策略；校验 name/webhook_id 必填，max_concurrent/rate_limit/timeout/max_retries 正整数，circuit_failure_threshold 0-1
- `get(policy_id: str) -> WebhookExecutionPolicy` — 获取
- `list(webhook_id: str | None = None, status: str | None = None) -> list[WebhookExecutionPolicy]` — 列表，可按 webhook_id/status 过滤
- `update(policy_id: str, updates: dict) -> WebhookExecutionPolicy` — 更新
- `delete(policy_id: str) -> bool` — 删除

#### 执行控制
- `acquire_slot(policy_id: str, call_id: str) -> ExecutionAttempt` — 申请执行槽位：检查并发数<max_concurrent、速率窗口内<rate_limit、熔断器非 open；成功则 current_concurrent+1、window_count+1、创建 attempt=pending
- `release_slot(policy_id: str, call_id: str, success: bool, http_status: int | None, duration_ms: int, error_message: str | None = None) -> ExecutionAttempt` — 释放槽位：current_concurrent-1，更新 attempt=success/failed，推进熔断器计数
- `record_retry(policy_id: str, call_id: str, attempt_number: int, next_attempt_at: str, error_message: str | None = None) -> ExecutionAttempt` — 记录重试，推进 attempt_number，计算下次时间（指数退避 backoff * 2^(n-1)）
- `get_execution_state(policy_id: str) -> ExecutionState` — 获取执行状态
- `reset_state(policy_id: str) -> ExecutionState` — 重置执行状态（清空计数、熔断器 closed）
- `list_attempts(policy_id: str, limit: int = 50) -> list[ExecutionAttempt]` — 倒序列出尝试记录

#### 熔断
- `_update_circuit(state: ExecutionState, success: bool) -> None` — 内部方法：更新熔断器计数，失败率达到阈值→open；half_open 成功→closed 失败→open
- `trip_circuit(policy_id: str) -> ExecutionState` — 手动触发熔断（演练）
- `reset_circuit(policy_id: str) -> ExecutionState` — 手动重置熔断器

### 1.3 错误码
- `MISSING_NAME` — 缺少名称
- `MISSING_WEBHOOK` — 缺少 webhook_id
- `INVALID_CONCURRENCY` — 并发数无效
- `INVALID_RATE_LIMIT` — 速率限制无效
- `INVALID_TIMEOUT` — 超时无效
- `INVALID_RETRY_COUNT` — 重试次数无效
- `INVALID_THRESHOLD` — 阈值无效（0-1 范围外）
- `NOT_FOUND` — 策略不存在
- `CONCURRENCY_EXCEEDED` — 并发数超限
- `RATE_LIMIT_EXCEEDED` — 速率超限
- `CIRCUIT_OPEN` — 熔断器打开
- `ATTEMPT_NOT_FOUND` — 尝试记录不存在

### 1.4 存储与上限
- 策略：200 条上限，FIFO 淘汰
- 执行状态：与策略一一对应
- 尝试记录：每个策略 200 条上限，FIFO 淘汰

---

## 2. #126 · Egress Policy（出站策略）

### 2.1 数据模型

**EgressPolicy**（出站策略）
- `policy_id: str` — 策略 ID
- `name: str` — 名称
- `description: str | None` — 描述
- `effect: str` — `allow|deny`（默认 `allow`）
- `cidr_blocks: list[str]` — CIDR 白名单/黑名单
- `ports: list[int]` — 端口列表
- `domains: list[str]` — 域名列表
- `protocols: list[str]` — 协议列表 `http|https|tcp|udp`
- `priority: int` — 优先级（数值越小越高，默认 100）
- `status: str` — `active|disabled`（默认 `active`）
- `created_at: str` — ISO 时间
- `updated_at: str` — ISO 时间

**EgressEvaluation**（评估结果）
- `eval_id: str` — 评估 ID
- `policy_id: str | None` — 命中策略 ID（None 表示无匹配）
- `destination: str` — 目标地址（IP 或域名）
- `port: int` — 目标端口
- `protocol: str` — 协议
- `decision: str` — `allowed|denied`
- `matched_rules: list[str]` — 匹配的规则类型（cidr/port/domain/protocol）
- `reason: str` — 原因说明
- `evaluated_at: str` — ISO 时间

### 2.2 引擎接口：EgressPolicyEngine

#### CRUD
- `register(policy: EgressPolicy) -> EgressPolicy` — 注册策略；校验 name 必填，effect 合法，cidr/ports/domains/protocols 至少一个非空，priority 正整数
- `get(policy_id: str) -> EgressPolicy` — 获取
- `list(effect: str | None = None, status: str | None = None) -> list[EgressPolicy]` — 列表，可按 effect/status 过滤，按 priority 升序
- `update(policy_id: str, updates: dict) -> EgressPolicy` — 更新
- `delete(policy_id: str) -> bool` — 删除

#### 评估
- `evaluate(destination: str, port: int, protocol: str, source_context: dict | None = None) -> EgressEvaluation` — 评估出站请求：按 priority 升序遍历 active 策略，逐条匹配 cidr/port/domain/protocol，匹配到则返回 effect=allow/deny；全部不匹配则默认 deny（安全默认）
- `evaluate_batch(requests: list[dict]) -> list[EgressEvaluation]` — 批量评估
- `check_allowed(destination: str, port: int, protocol: str) -> bool` — 简化版：是否允许
- `list_evaluations(policy_id: str | None = None, limit: int = 50) -> list[EgressEvaluation]` — 列出评估记录，可按策略过滤

#### 工具
- `add_cidr(policy_id: str, cidr: str) -> EgressPolicy` — 追加 CIDR
- `remove_cidr(policy_id: str, cidr: str) -> EgressPolicy` — 移除 CIDR
- `add_domain(policy_id: str, domain: str) -> EgressPolicy` — 追加域名
- `remove_domain(policy_id: str, domain: str) -> EgressPolicy` — 移除域名

### 2.3 匹配规则
- **CIDR**：支持 IPv4 CIDR（如 `192.168.1.0/24`），单 IP 自动视为 /32
- **端口**：精确匹配
- **域名**：精确匹配 + 子域名通配（`*.example.com` 匹配 `api.example.com`）
- **协议**：精确匹配
- **匹配逻辑**：策略中所有非空条件全部匹配才算命中（AND 关系）

### 2.4 错误码
- `MISSING_NAME` — 缺少名称
- `INVALID_EFFECT` — effect 不合法
- `EMPTY_RULES` — 没有任何规则（cidr/ports/domains/protocols 全空）
- `INVALID_CIDR` — CIDR 格式无效
- `INVALID_PORT` — 端口无效（1-65535）
- `INVALID_PROTOCOL` — 协议不合法
- `INVALID_PRIORITY` — 优先级无效
- `NOT_FOUND` — 策略不存在

### 2.5 存储与上限
- 策略：200 条上限，FIFO 淘汰
- 评估记录：全局 200 条上限，FIFO 淘汰

---

## 3. #127 · Exportable Marking（可导出标记控制）

### 3.1 数据模型

**ExportableMarkingPolicy**（可导出标记策略）
- `policy_id: str` — 策略 ID
- `name: str` — 名称
- `connection_id: str` — 关联数据连接
- `marking_level: str` — 标记级别 `public|internal|restricted|confidential`
- `export_action: str` — 导出动作 `allow|deny|mask|redact`（默认 `deny`）
- `mask_character: str` — 掩码字符（默认 `*`）
- `redact_text: str` — 替换文本（默认 `[REDACTED]`）
- `affected_columns: list[str]` — 影响的列（空=全部列）
- `affected_markings: list[str]` — 影响的具体标记标签
- `priority: int` — 优先级（数值越小越高，默认 100）
- `status: str` — `active|disabled`（默认 `active`）
- `created_at: str` — ISO 时间
- `updated_at: str` — ISO 时间

**MarkingEvaluation**（标记评估结果）
- `eval_id: str` — 评估 ID
- `policy_id: str | None` — 命中策略 ID
- `connection_id: str` — 连接 ID
- `column_name: str | None` — 列名
- `markings: list[str]` — 数据标记列表
- `decision: str` — `allowed|denied|masked|redacted`
- `masked_value: str | None` — 掩码/替换后的值
- `reason: str` — 原因说明
- `evaluated_at: str` — ISO 时间

### 3.2 引擎接口：ExportableMarkingEngine

#### CRUD
- `register(policy: ExportableMarkingPolicy) -> ExportableMarkingPolicy` — 注册策略；校验 name/connection_id 必填，marking_level 合法，export_action 合法，priority 正整数
- `get(policy_id: str) -> ExportableMarkingPolicy` — 获取
- `list(connection_id: str | None = None, status: str | None = None, marking_level: str | None = None) -> list[ExportableMarkingPolicy]` — 列表，可按 connection_id/status/marking_level 过滤
- `update(policy_id: str, updates: dict) -> ExportableMarkingPolicy` — 更新
- `delete(policy_id: str) -> bool` — 删除

#### 评估
- `evaluate(connection_id: str, column_name: str | None, markings: list[str], value: str | None = None) -> MarkingEvaluation` — 评估可导出性：按 priority 升序匹配 connection_id+marking_level/affected_markings，返回最高优先级策略的决策
  - `allow` → decision=allowed
  - `deny` → decision=denied
  - `mask` → decision=masked, masked_value = mask_character 填充
  - `redact` → decision=redacted, masked_value = redact_text
- `evaluate_row(connection_id: str, columns: list[dict]) -> list[MarkingEvaluation]` — 批量评估行内多列
- `can_export(connection_id: str, markings: list[str]) -> bool` — 简化版：整行是否允许导出（任何 deny 策略命中则返回 False）
- `list_evaluations(policy_id: str | None = None, limit: int = 50) -> list[MarkingEvaluation]` — 列出评估记录

#### 工具
- `add_affected_column(policy_id: str, column: str) -> ExportableMarkingPolicy` — 添加影响列
- `remove_affected_column(policy_id: str, column: str) -> ExportableMarkingPolicy` — 移除影响列
- `add_affected_marking(policy_id: str, marking: str) -> ExportableMarkingPolicy` — 添加影响标记
- `remove_affected_marking(policy_id: str, marking: str) -> ExportableMarkingPolicy` — 移除影响标记

### 3.3 错误码
- `MISSING_NAME` — 缺少名称
- `MISSING_CONNECTION` — 缺少 connection_id
- `INVALID_MARKING_LEVEL` — 标记级别不合法
- `INVALID_EXPORT_ACTION` — 导出动作不合法
- `INVALID_PRIORITY` — 优先级无效
- `NOT_FOUND` — 策略不存在

### 3.4 存储与上限
- 策略：200 条上限，FIFO 淘汰
- 评估记录：全局 200 条上限，FIFO 淘汰

---

## 4. API 端点概览

### 4.1 Webhook Execution Policy（~16 端点）
- POST `/v1/webhook-execution-policies` — 注册
- GET `/v1/webhook-execution-policies` — 列表
- GET `/v1/webhook-execution-policies/{policy_id}` — 获取
- PATCH `/v1/webhook-execution-policies/{policy_id}` — 更新
- DELETE `/v1/webhook-execution-policies/{policy_id}` — 删除
- POST `/v1/webhook-execution-policies/{policy_id}/acquire` — 申请槽位
- POST `/v1/webhook-execution-policies/{policy_id}/release` — 释放槽位
- POST `/v1/webhook-execution-policies/{policy_id}/retry` — 记录重试
- GET `/v1/webhook-execution-policies/{policy_id}/state` — 获取执行状态
- POST `/v1/webhook-execution-policies/{policy_id}/reset-state` — 重置状态
- GET `/v1/webhook-execution-policies/{policy_id}/attempts` — 尝试记录列表
- POST `/v1/webhook-execution-policies/{policy_id}/trip-circuit` — 手动熔断
- POST `/v1/webhook-execution-policies/{policy_id}/reset-circuit` — 重置熔断器

### 4.2 Egress Policy（~15 端点）
- POST `/v1/egress-policies` — 注册
- GET `/v1/egress-policies` — 列表
- GET `/v1/egress-policies/{policy_id}` — 获取
- PATCH `/v1/egress-policies/{policy_id}` — 更新
- DELETE `/v1/egress-policies/{policy_id}` — 删除
- POST `/v1/egress-policies/evaluate` — 评估出站请求
- POST `/v1/egress-policies/evaluate-batch` — 批量评估
- GET `/v1/egress-policies/check-allowed` — 简化检查
- GET `/v1/egress-policies/evaluations` — 评估记录列表
- POST `/v1/egress-policies/{policy_id}/cidrs` — 追加 CIDR
- DELETE `/v1/egress-policies/{policy_id}/cidrs` — 移除 CIDR
- POST `/v1/egress-policies/{policy_id}/domains` — 追加域名
- DELETE `/v1/egress-policies/{policy_id}/domains` — 移除域名

### 4.3 Exportable Marking（~15 端点）
- POST `/v1/exportable-markings` — 注册
- GET `/v1/exportable-markings` — 列表
- GET `/v1/exportable-markings/{policy_id}` — 获取
- PATCH `/v1/exportable-markings/{policy_id}` — 更新
- DELETE `/v1/exportable-markings/{policy_id}` — 删除
- POST `/v1/exportable-markings/evaluate` — 评估
- POST `/v1/exportable-markings/evaluate-row` — 批量评估行
- GET `/v1/exportable-markings/can-export` — 简化检查
- GET `/v1/exportable-markings/evaluations` — 评估记录列表
- POST `/v1/exportable-markings/{policy_id}/columns` — 添加影响列
- DELETE `/v1/exportable-markings/{policy_id}/columns` — 移除影响列
- POST `/v1/exportable-markings/{policy_id}/markings` — 添加影响标记
- DELETE `/v1/exportable-markings/{policy_id}/markings` — 移除影响标记

合计 ~46 端点

---

## 5. 测试计划

### 5.1 WebhookExecutionPolicyEngine（~20 测试）
- CRUD 5 项：register 成功 + 校验失败 + get/list + update + delete
- 执行控制 8 项：acquire 成功 + 并发超限 + 速率超限 + release 成功 + 重试退避 + 获取状态 + 重置状态 + 尝试记录列表
- 熔断 4 项：失败触发熔断 + 熔断打开拒绝 + 手动熔断演练 + 重置熔断器
- 边界 2 项：FIFO 淘汰 + 多策略独立状态
- 单例 1 项

### 5.2 EgressPolicyEngine（~17 测试）
- CRUD 5 项：register 成功 + 校验失败 + get/list + update + delete
- 评估 6 项：CIDR 匹配 + 端口匹配 + 域名匹配（含通配）+ 多条件 AND + 默认 deny + priority 顺序
- 批量 2 项：evaluate_batch + check_allowed
- 工具 3 项：add/remove cidr + add/remove domain + 评估记录列表
- 边界 1 项：FIFO 淘汰

### 5.3 ExportableMarkingEngine（~17 测试）
- CRUD 5 项：register 成功 + 校验失败 + get/list + update + delete
- 评估 6 项：allow + deny + mask + redact + 列级匹配 + priority 顺序
- 行级 2 项：evaluate_row + can_export
- 工具 3 项：add/remove column + add/remove marking + 评估记录列表
- 边界 1 项：FIFO 淘汰

合计 ~54 测试

---

## 6. 进度影响

- W2+ 中优先级：94/166 → **97/166**
- 总差距：140/259 → **143/259**

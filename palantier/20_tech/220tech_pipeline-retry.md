# 220tech · W1-11 Pipeline 重试机制

> **版本**：v1.0 · 2026-07-22 · **关联**：220plan §1.2.2 W1-11 · Phase 6 · 中优先级
> **依赖**：W1-4 Build 引擎（`aos_api/jobs/build_engine.py`）
> **范围**：自动重试 + 指数退避 + 死信队列（DLQ）+ 手动重试

## 1. 目标
- Build Job 失败后自动重试（默认 3 次）
- 指数退避：1s → 2s → 4s
- 超过最大重试次数 → 标记 FAILED + 进入死信队列
- 手动重试：用户可在 UI 触发（复用现有 `/v1/builds/{job_id}/retry`）
- DLQ 查询：`GET /v1/builds/dlq`

## 2. 设计原则
- **最小更改**：扩展 `build_engine.py` 的 `_execute`，不重写
- **可测试**：`sleeper` 参数可注入，测试中传 `lambda _: None` 跳过真实 sleep
- **步骤级失败注入**：`JobStep.config["_fail_n"]` 控制模拟失败次数，每次执行递减
- **DLQ 独立**：新文件 `jobs/retry.py`，不与 `wave_ext.py` 的数据同步 DLQ 混用

## 3. 数据模型变更

### 3.1 Job 扩展（build_engine.py）
```python
class Job(BaseModel):
    # ... 既有字段 ...
    retry_count: int = 0       # 已重试次数
    max_retries: int = 3       # 最大重试次数
```

### 3.2 新增模型（jobs/retry.py）
```python
class DeadLetterEntry(BaseModel):
    id: str                    # dlq-{hex}
    job_id: str
    spec_name: str
    error: str
    retry_count: int
    pushed_at: str

class RetryPolicy:
    max_retries: int = 3
    base_delay: float = 1.0
    def should_retry(attempt) -> bool      # attempt < max_retries
    def compute_backoff(attempt) -> float  # base_delay * 2^attempt

class DeadLetterQueue:
    def push(job) -> DeadLetterEntry
    def list() -> list[DeadLetterEntry]
    def count() -> int
    def get(entry_id) -> DeadLetterEntry | None
    def remove(entry_id) -> bool
```

## 4. 重试算法（_execute 扩展）
```
for attempt in range(job.max_retries + 1):   # 0..max_retries（共 max_retries+1 次执行）
    locked = []
    try:
        acquire locks
        job.status = RUNNING
        run steps（检查 _fail_n 注入）
        job.status = SUCCEEDED
        return                                  # 成功退出
    except JobError as exc:
        job.retry_count = attempt
        if attempt < job.max_retries:
            backoff = policy.compute_backoff(attempt)   # 1s/2s/4s
            log WARN "第 {attempt+1} 次失败，{backoff}s 后重试"
            sleeper(backoff)
            # 循环继续
        else:
            job.status = FAILED
            job.error = exc.message
            dlq.push(job)
            log ERROR "超过最大重试次数，进入死信队列"
            return
    finally:
        release locks
```

### 4.1 退避计算
| attempt | backoff |
|---------|---------|
| 0 | 1.0s |
| 1 | 2.0s |
| 2 | 4.0s |
| ≥3 | 不重试，进 DLQ |

### 4.2 步骤级失败注入（仅测试用）
```python
JobStep(name="transform", config={"_fail_n": 2})
# 第 1 次执行：_fail_n=2>0 → 递减为 1 → raise STEP_FAILED
# 第 2 次执行（重试）：_fail_n=1>0 → 递减为 0 → raise STEP_FAILED
# 第 3 次执行（重试）：_fail_n=0 → 正常通过
```

## 5. BuildEngine 构造函数变更
```python
class BuildEngine:
    def __init__(self, sleeper=time.sleep):
        self._sleeper = sleeper
        self._dlq = DeadLetterQueue()
        # ... 既有 ...
```
- 生产：`BuildEngine()` → 真实 `time.sleep`
- 测试：`BuildEngine(sleeper=lambda _: None)` → 跳过 sleep

## 6. REST API 扩展（builds.py）
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/v1/builds/dlq` | 列出死信队列 |
| GET | `/v1/builds/dlq/{entry_id}` | 查看死信条目 |
| DELETE | `/v1/builds/dlq/{entry_id}` | 从 DLQ 移除 |
| POST | `/v1/builds/{job_id}/retry` | 手动重试（既有，不变） |

## 7. 测试矩阵（≥ 10）
| 测试 | 说明 |
|------|------|
| `test_auto_retry_on_failure` | 步骤失败 → 自动重试 |
| `test_exponential_backoff` | 退避时间 1/2/4s |
| `test_max_retry_exceeded` | 超过 max_retries → FAILED |
| `test_manual_retry` | 手动 retry_job → 新 Job SUCCEEDED |
| `test_dlq_on_max_retry` | 超过重试 → DLQ 有条目 |
| `test_retry_success_within_limit` | 重试内成功 → SUCCEEDED，retry_count>0 |
| `test_dlq_count` | DLQ count 方法 |
| `test_dlq_remove` | 从 DLQ 移除条目 |
| `test_no_retry_when_zero` | max_retries=0 → 直接 FAILED |
| `test_dlq_visible_via_api` | GET /v1/builds/dlq 返回条目 |
| `test_retry_resets_on_manual` | 手动重试 → retry_count=0 |

## 8. 文件清单
| 文件 | 动作 |
|------|------|
| `aos_api/jobs/retry.py` | 新增 |
| `aos_api/jobs/build_engine.py` | 修改（Job 扩展 + _execute 重试循环） |
| `aos_api/routers/builds.py` | 修改（DLQ 端点） |
| `tests/test_build_engine.py` | 修改（3 个现有失败测试加 sleeper） |
| `tests/test_job_retry.py` | 新增 |

## 9. 不做的事
- ❌ 真实异步线程池重试（后续项）
- ❌ 持久化 DLQ（内存即可，Phase 7 接 DB）
- ❌ UI 前端重试徽章（前端独立交付）
- ❌ 与 wave_ext.py `/v1/dlq` 合并（语义不同：Build Job DLQ vs 数据同步 DLQ）

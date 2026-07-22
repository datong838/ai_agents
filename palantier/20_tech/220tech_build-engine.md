# 220tech · W1-4 Build 引擎 · 微观实现方案

> **版本**：v1.0 · 2026-07-22
> **关联宏观方案**：[220plan](./220plan-分阶段开发与里程碑计划.md) §3.2（W1-4）
> **状态**：⬜ 方案 → 开发 → 测试

---

## 1. 功能边界

| 子功能 | 本期 |
| --- | --- |
| Job/JobSpec 模型（输入数据集+变换步骤+输出目标） | ✅ |
| 状态机 PENDING→RUNNING→SUCCEEDED/FAILED/CANCELLED | ✅ |
| 事务锁定（输出数据集级互斥，防并发写） | ✅ |
| Job 执行器（顺序执行变换步骤） | ✅（同步模拟，非真异步） |
| 结构化日志收集（时间戳+级别+消息，内存 ring buffer） | ✅ |
| 手动重试（失败后创建新 Job） | ✅ |

**不做**：自动重试退避（W1-11）、Freshness 检测跳过（后置）、Force Build 全量重算（后置）、真异步线程池（本期同步执行器）。

## 2. 数据模型

```python
class JobStep(BaseModel):
    name: str                              # 步骤名
    type: str = "transform"                # "transform"|"source"|"sink"
    config: dict[str, Any] = {}            # 步骤配置

class JobSpec(BaseModel):
    inputs: list[str]                      # 输入数据集 RID
    steps: list[JobStep]                   # 变换步骤序列
    outputs: list[str]                     # 输出数据集 RID
    name: str = "untitled-build"           # Job 名称

class LogEntry(BaseModel):
    timestamp: str                         # ISO8601
    level: str                             # INFO|WARN|ERROR
    message: str

class Job(BaseModel):
    id: str                                # UUID
    spec: JobSpec
    status: str                            # PENDING|RUNNING|SUCCEEDED|FAILED|CANCELLED
    created_at: str                        # ISO8601
    started_at: str | None = None
    finished_at: str | None = None
    logs: list[LogEntry] = []
    error: str | None = None
```

## 3. API 契约

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/builds` | 创建 Job（body=JobSpec），同步执行，返回 Job |
| GET | `/v1/builds` | 列出全部 Job |
| GET | `/v1/builds/{id}` | 单个 Job 详情含日志 |
| POST | `/v1/builds/{id}/cancel` | 取消 RUNNING 的 Job |
| POST | `/v1/builds/{id}/retry` | 失败后创建新 Job |

## 4. 核心类设计

```python
class BuildEngine:
    _jobs: dict[str, Job]                  # 内存存储
    _locks: dict[str, str]                 # dataset_rid → job_id（事务锁）

    def create_job(spec: JobSpec) -> Job          # 创建+执行
    def _execute(job: Job) -> None                # 获取锁→执行步骤→收集日志→释放锁
    def get_job(id) -> Job | None
    def list_jobs() -> list[Job]
    def cancel_job(id) -> Job                     # RUNNING→CANCELLED
    def retry_job(id) -> Job                      # 用同 spec 创建新 Job
    def _acquire_lock(dataset, job_id) -> bool    # 返回 False=已被锁
    def _release_lock(dataset) -> None
```

## 5. 接缝点

| 动作 | 文件 |
| --- | --- |
| 🆕 新建 | `aos_api/jobs/build_engine.py` |
| 🆕 新建 | `aos_api/routers/builds.py` |
| ✏️ 改 | `aos_api/main.py`（注册 router 2 行） |
| 🆕 新建 | `tests/test_build_engine.py` |

## 6. 测试细化（13 用例）

| 用例 | 断言 |
| --- | --- |
| test_create_job_pending | 初始 PENDING |
| test_job_lifecycle_success | PENDING→RUNNING→SUCCEEDED |
| test_job_lifecycle_failure | →FAILED |
| test_job_lifecycle_cancelled | →CANCELLED |
| test_transaction_lock_concurrent | 同输出并发→第二个 lock 失败 |
| test_lock_released_on_completion | 完成后锁释放 |
| test_job_log_collection | 日志按时间戳排列 |
| test_jobspec_validation_no_inputs | 空 inputs→400 |
| test_jobspec_validation_no_outputs | 空 outputs→400 |
| test_job_retry_after_failure | retry→新 Job |
| test_create_build_endpoint | POST /v1/builds |
| test_list_builds_endpoint | GET /v1/builds |
| test_get_build_detail_with_logs | GET 含 logs |
| test_cancel_build_endpoint | POST cancel |
| test_build_not_found_404 | 404 |
| test_retry_build_endpoint | POST retry→新 Job |

# 220tech · W2-AH · Data Connection 文件处理组（#116 / #117 / #118）

> **版本**：v1.0 · 2026-07-22
> **状态**：✅ 方案定稿 · 可编码
> **对齐**：
> - 差距分析 [220w](./220w-与目标系统差距分析.md) §11 #116/#117/#118
> - 220plan v4.6 已交付 85/166，本批收口 3 项 → 88/166
> **范围**：W2-AH 收口 DC 文件处理三件 — 文件筛选 + 文件变换 + Streaming Sync
> **设计原则**：最小新增、单例引擎 + 200 条 FIFO、内存态

---

## 0. 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文回答 | 文档与代码注释均中文 |
| 先方案后编码 | 本文先定稿，再写引擎/路由/测试 |
| 最小更改 | 仅新增 `aos_api/file_processing.py` + 路由 + 测试；`main.py` 加 2 行 |
| 不影响已有功能 | 纯新增，不修改任何现有模块 |
| 自测验证 | 单测全绿 + 全量回归 + 方案对照 |
| 编码前复习方案 | 已核对 W2-AG 引擎模式（单例 + 200 条 FIFO） |

---

## 1. 背景与边界

### 1.1 现状

| 能力 | 现状 | 缺口 |
| --- | --- | --- |
| 文件筛选 | 无 | 🔴 缺 |
| 文件变换 | 无 | 🔴 缺 |
| Streaming Sync | 无 | 🔴 缺 |

### 1.2 边界

- ✅ 本组做：
  - #116 文件筛选：FileFilterEngine（path_pattern/mtime/size/exclude_synced + apply_filter）
  - #117 文件变换：FileTransformEngine（gzip/merge/rename/pgp_decrypt/add_timestamp + apply_transform）
  - #118 Streaming Sync：StreamingSyncEngine（Kafka/Kinesis/PubSub 三源 + consumer + offset 管理 + sync 记录）
- ❌ 本组不做：
  - 真实文件 I/O（模拟返回结果）
  - 真实 Kafka/Kinesis/PubSub 连接（内存模拟）
  - 真实 PGP 加解密（简化模拟）

---

## 2. 数据模型

### 2.1 #116 FileFilter

```python
class FileEntry(BaseModel):
    """文件条目（筛选输入/输出）。"""
    path: str
    size_bytes: int = 0
    modified_at: float = 0.0
    is_synced: bool = False


class FileFilterRule(BaseModel):
    """文件筛选规则。"""
    id: str
    name: str
    path_pattern: str = ""           # 正则
    min_size_bytes: int = 0
    max_size_bytes: int = 0          # 0 表示不限
    modified_after: float = 0.0      # 时间戳，0 表示不限
    modified_before: float = 0.0     # 时间戳，0 表示不限
    exclude_synced: bool = False
    created_at: float = 0.0


class FilterResult(BaseModel):
    """筛选结果。"""
    filter_id: str
    total_files: int = 0
    matched_files: int = 0
    files: list[FileEntry] = []
    applied_at: float = 0.0


_VALID_FILTER_SORTS = {"path", "size", "mtime"}
```

### 2.2 #117 FileTransform

```python
class FileTransform(BaseModel):
    """文件变换配置。"""
    id: str
    name: str
    transform_type: str           # gzip / merge / rename / pgp_decrypt / add_timestamp
    config: dict[str, Any] = Field(default_factory=dict)
    created_at: float = 0.0


class TransformResult(BaseModel):
    """变换结果。"""
    transform_id: str
    input_files: list[str] = []
    output_files: list[str] = []
    status: str = "success"       # success / failed / skipped
    error_message: str = ""
    transformed_at: float = 0.0


_VALID_TRANSFORM_TYPES = {"gzip", "merge", "rename", "pgp_decrypt", "add_timestamp"}
```

### 2.3 #118 StreamingSync

```python
class StreamEvent(BaseModel):
    """流事件。"""
    key: str
    value: str
    timestamp: float
    partition: int = 0
    offset: int = 0


class StreamingSync(BaseModel):
    """Streaming Sync 配置。"""
    id: str
    name: str
    source_type: str              # kafka / kinesis / pubsub
    source_config: dict[str, Any] = Field(default_factory=dict)
    target_stream: str = ""
    status: str = "stopped"       # running / stopped / error
    offset: int = 0
    last_consumed_at: float = 0.0
    created_at: float = 0.0


class SyncRecord(BaseModel):
    """同步记录。"""
    sync_id: str
    event_key: str
    status: str = "synced"        # synced / failed / retry
    error_message: str = ""
    synced_at: float = 0.0


_VALID_SOURCE_TYPES = {"kafka", "kinesis", "pubsub"}
_VALID_SYNC_STATUSES = {"running", "stopped", "error"}
_VALID_RECORD_STATUSES = {"synced", "failed", "retry"}
```

---

## 3. 引擎设计

文件：`aos_api/file_processing.py`（新增，3 个引擎）

### 3.1 FileFilterEngine（#116）

```python
class FileFilterEngine:
    def register(self, rule: FileFilterRule) -> FileFilterRule: ...
    def get(self, rule_id: str) -> FileFilterRule: ...
    def list(self) -> list[FileFilterRule]: ...
    def update(self, rule_id: str, updates: dict) -> FileFilterRule: ...
    def delete(self, rule_id: str) -> bool: ...
    def apply_filter(self, rule_id: str, files: list[FileEntry]) -> FilterResult: ...
    """按规则筛选文件：path_pattern 正则 + size 范围 + mtime 范围 + exclude_synced"""
```

**apply_filter 流程**：
1. 对每个 FileEntry 依次检查：
   - path_pattern：re.match（非空时）
   - size：min_size_bytes ≤ size_bytes ≤ max_size_bytes（max 为 0 时跳过上限）
   - mtime：modified_after ≤ modified_at ≤ modified_before（0 时跳过对应边界）
   - exclude_synced：若 True 则 is_synced=True 的排除
2. 返回 FilterResult（total/matched/files）

### 3.2 FileTransformEngine（#117）

```python
class FileTransformEngine:
    def register(self, transform: FileTransform) -> FileTransform: ...
    def get(self, transform_id: str) -> FileTransform: ...
    def list(self) -> list[FileTransform]: ...
    def update(self, transform_id: str, updates: dict) -> FileTransform: ...
    def delete(self, transform_id: str) -> bool: ...
    def apply_transform(self, transform_id: str, input_files: list[str]) -> TransformResult: ...
    """按类型模拟变换：gzip 加 .gz 后缀；merge 输出 merged_*.dat；rename 用 config.pattern；pgp_decrypt 加 .decrypted；add_timestamp 加时间戳前缀"""
```

**apply_transform 简化模拟**：
- `gzip`：每个输入文件 → `{file}.gz`
- `merge`：所有输入合并为 `merged_{transform_id[:8]}.dat`
- `rename`：使用 `config.pattern`（如 `renamed_{name}`）生成新名
- `pgp_decrypt`：每个输入 → `{file}.decrypted`
- `add_timestamp`：每个输入 → `{ts}_{file}`（ts=当前时间戳）

### 3.3 StreamingSyncEngine（#118）

```python
class StreamingSyncEngine:
    def register(self, sync: StreamingSync) -> StreamingSync: ...
    def get(self, sync_id: str) -> StreamingSync: ...
    def list(self) -> list[StreamingSync]: ...
    def update(self, sync_id: str, updates: dict) -> StreamingSync: ...
    def delete(self, sync_id: str) -> bool: ...
    def start(self, sync_id: str) -> StreamingSync: ...
    """status = running"""
    def stop(self, sync_id: str) -> StreamingSync: ...
    """status = stopped"""
    def consume(self, sync_id: str, events: list[StreamEvent]) -> list[SyncRecord]: ...
    """消费事件：推进 offset + 生成 SyncRecord + 写入记录列表"""
    def list_records(self, sync_id: str, limit: int = 50) -> list[SyncRecord]: ...
    """返回同步记录"""
```

**consume 流程**：
1. 校验 status=running（否则 NOT_RUNNING）
2. 对每个 event 生成 SyncRecord，默认 synced
3. 推进 offset 到最大 event.offset
4. 推进 last_consumed_at
5. 记录写入 _records 列表（按 sync_id 分组，200 条上限）

### 3.4 单例与持久化

- 3 个引擎均用**双重检查锁单例**
- 内存态为主，各 200 条上限（records 200 条滚动）

---

## 4. API 设计

文件：`aos_api/routers/file_processing.py`（新增）

### 4.1 #116 File Filter

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/file-filters` | 注册筛选规则 |
| GET | `/v1/file-filters` | 列表 |
| GET | `/v1/file-filters/{filter_id}` | 单条 |
| PUT | `/v1/file-filters/{filter_id}` | 更新 |
| DELETE | `/v1/file-filters/{filter_id}` | 删除 |
| POST | `/v1/file-filters/{filter_id}/apply` | 应用筛选 |

### 4.2 #117 File Transform

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/file-transforms` | 注册变换 |
| GET | `/v1/file-transforms` | 列表 |
| GET | `/v1/file-transforms/{transform_id}` | 单条 |
| PUT | `/v1/file-transforms/{transform_id}` | 更新 |
| DELETE | `/v1/file-transforms/{transform_id}` | 删除 |
| POST | `/v1/file-transforms/{transform_id}/apply` | 应用变换 |

### 4.3 #118 Streaming Sync

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| POST | `/v1/streaming-syncs` | 注册同步 |
| GET | `/v1/streaming-syncs` | 列表 |
| GET | `/v1/streaming-syncs/{sync_id}` | 单条 |
| PUT | `/v1/streaming-syncs/{sync_id}` | 更新 |
| DELETE | `/v1/streaming-syncs/{sync_id}` | 删除 |
| POST | `/v1/streaming-syncs/{sync_id}/start` | 启动 |
| POST | `/v1/streaming-syncs/{sync_id}/stop` | 停止 |
| POST | `/v1/streaming-syncs/{sync_id}/consume` | 消费事件 |
| GET | `/v1/streaming-syncs/{sync_id}/records` | 同步记录列表 |

---

## 5. 集成点

### 5.1 main.py（最小更改）

```python
from aos_api.routers import (..., file_processing, ...)
application.include_router(file_processing.router)
```

---

## 6. 测试计划

文件：`tests/test_file_processing.py`（新增，约 45 个用例）

### 6.1 FileFilterEngine（15）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 缺 name | MISSING_NAME |
| 3 | get 未找到 | NOT_FOUND |
| 4 | list 默认 | 列表 |
| 5 | update | 修改后返回新值 |
| 6 | delete | 删除成功 |
| 7 | apply_filter path_pattern | 仅匹配正则的文件 |
| 8 | apply_filter size 范围 | min/max 内的文件 |
| 9 | apply_filter mtime 范围 | modified_after/before 内 |
| 10 | apply_filter exclude_synced | 排除已同步文件 |
| 11 | apply_filter 多条件组合 | 所有条件同时生效 |
| 12 | apply_filter 空输入 | matched=0 |
| 13 | apply_filter 无匹配 | matched=0 |
| 14 | 200 条上限 | 旧记录淘汰 |
| 15 | filter 单例 | 同一实例 |

### 6.2 FileTransformEngine（14）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 缺 name | MISSING_NAME |
| 3 | register 未知 type | INVALID_TRANSFORM_TYPE |
| 4 | get 未找到 | NOT_FOUND |
| 5 | list 默认 | 列表 |
| 6 | update | 修改后返回新值 |
| 7 | delete | 删除成功 |
| 8 | apply_transform gzip | 输出 .gz 后缀 |
| 9 | apply_transform merge | 输出 merged_*.dat |
| 10 | apply_transform rename | 按 pattern 重命名 |
| 11 | apply_transform pgp_decrypt | 输出 .decrypted 后缀 |
| 12 | apply_transform add_timestamp | 加时间戳前缀 |
| 13 | apply_transform 空输入 | output_files=[] |
| 14 | transform 单例 | 同一实例 |

### 6.3 StreamingSyncEngine（17）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register | 返回带 id |
| 2 | register 缺 name | MISSING_NAME |
| 3 | register 未知 source_type | INVALID_SOURCE_TYPE |
| 4 | get 未找到 | NOT_FOUND |
| 5 | list 默认 | 列表 |
| 6 | update | 修改后返回新值 |
| 7 | delete | 删除成功 |
| 8 | start | status=running |
| 9 | stop | status=stopped |
| 10 | consume 正常 | 生成 SyncRecord + offset 推进 |
| 11 | consume 未启动 | NOT_RUNNING |
| 12 | consume 多条 | 多条记录 + offset 最大 |
| 13 | list_records | 返回记录列表 |
| 14 | list_records limit | 前 N 条 |
| 15 | 200 条 sync 上限 | 旧记录淘汰 |
| 16 | 200 条 record 滚动 | 旧记录淘汰 |
| 17 | streaming 单例 | 同一实例 |

---

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 文件筛选组合条件遗漏 | 逐项检查，测试覆盖组合场景 |
| 变换类型扩展 | 使用 VALID_TRANSFORM_TYPES 枚举，register 即校验 |
| Streaming sync offset 错乱 | consume 原子推进，用最大值更新 |
| 记录膨胀 | 200 条 FIFO 滚动上限 |

---

## 8. 交付物清单

| 路径 | 状态 | 说明 |
| --- | --- | --- |
| `docs/palantier/20_tech/220tech_w2-ah-file-processing.md` | ✅ 本文件 | 微规约 |
| `aos_api/file_processing.py` | ⬜ 待编码 | FileFilterEngine + FileTransformEngine + StreamingSyncEngine |
| `aos_api/routers/file_processing.py` | ⬜ 待编码 | ~20 端点 |
| `tests/test_file_processing.py` | ⬜ 待编码 | ~46 用例 |
| `aos_api/main.py` | ⬜ +2 行 | 1 import + 1 include_router |

---

*v1.0 · w2-ah*

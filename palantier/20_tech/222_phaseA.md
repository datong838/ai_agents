# 222 Phase A 技术方案 · 模型供应商与凭据管理

> **版本**：v1.0 · 2026-07-25
> **关联**：[222plan-分阶段开发与里程碑计划.md](222plan-分阶段开发与里程碑计划.md)
> **对应章节**：222 第 23 章 · 222 第 9.6 节
> **目标**：实现模型供应商详情页的 4 Tab（凭据管理/模型列表/安全策略/调用日志）+ 后端 API
> **状态**：✅ 已完成

---

## 一、现有架构分析

经过深入代码审计，模型供应商模块的现有架构是：

```
plugins/llm-providers/{41个供应商}/manifest.json  ← 磁盘内置插件
                          ↓
llm_provider_registry.py ← 核心：插件注册/安装/配置/凭据（418行）
  ├── KEY_INSTALLS  (已安装列表)     → PostgreSQL meta_aip_kv
  ├── KEY_READY     (已就绪列表)     → PostgreSQL meta_aip_kv
  ├── KEY_CONFIGS   (配置 baseUrl等) → PostgreSQL meta_aip_kv
  ├── KEY_CUSTOM    (自定义插件)     → PostgreSQL meta_aip_kv
  └── KEY_SECRETS   (API Key 明文!)  → PostgreSQL meta_aip_kv  ← 问题1：明文存储
      ├── put_plugin_secret(id, key)  → 直接存明文
      ├── has_plugin_secret(id)       → 检查存在
      └── resolve_plugin_api_key(id)  → 读取明文返回
                          ↓
llm_gateway.py ← 网关层：统一调用出口（521行）
  └── chat() → resolve_plugin_api_key() → 拿到明文 key → 调供应商 API
                          ↓
routers/wave_ext.py ← 路由层（2377行）
  ├── GET  /v1/aip/providers          → 供应商列表
  ├── GET  /v1/aip/llm-provider-plugins → 插件目录
  └── PUT  /v1/aip/llm-provider-plugins/{id}/config → 保存配置（含写入凭据）
```

**前端现状**：
```
apps/web/src/pages/s2/aip.tsx → ProvidersPage（565-1608行，约1000行）
  ├── view="list"       → 供应商卡片列表（已有）
  ├── view="configure"  → 配置表单（已有：baseUrl/modelId/secretRef）
  ├── view="credentials"→ 凭据管理（已有：但只是简单的 key 输入框）
  └── view="studio"     → 插件工作室（已有）
  ❌ 没有独立的详情页路由 /models/providers/:providerId
  ❌ 凭据管理没有加密状态、轮换策略、轮换历史、连接测试
```

## 二、缺失项精确定位

| # | 缺失 | 影响 | 解决方案 |
|---|------|------|---------|
| 1 | **API Key 明文存储** | 安全风险 | 新建 `kms_crypto.py`，AES-256-GCM 加解密；改造 `put_plugin_secret`/`resolve_plugin_api_key` 透明加解密 |
| 2 | **无凭据 CRUD API** | 222文档要求 `/api/models/providers/{id}/credentials` | 新建 `model_provider_credential_router.py`，prefix `/api/models/providers` |
| 3 | **无连接测试 API** | 222文档要求 `/api/models/providers/{id}/test-connection` | 在新 router 中实现，用 httpx 向供应商 `/v1/models` 发 GET |
| 4 | **无密钥轮换** | 222文档要求 30/90天自动轮换 | 新建 `key_rotation_scheduler.py`，记录轮换历史 |
| 5 | **无安全策略 API** | 222文档要求 IP白名单/QPS限制/审计 | 新建 `provider_security_router.py` |
| 6 | **无调用日志 API** | 222文档要求调用历史 | 新建 `provider_call_log_router.py`，从 FailoverEngine.CallRecord 提取 |
| 7 | **无供应商详情页** | 前端只有列表页，缺详情页 | 改造 `aip.tsx` ProvidersPage，增加 `detail` view + 4 Tab |

## 三、实施策略

**不破坏现有 3772 条路由**——采用增量添加方式：

```
新增文件（6个）：
  services/aos-api/aos_api/kms_crypto.py                    ← AES-256-GCM 加解密
  services/aos-api/aos_api/model_provider_credential.py     ← 凭据引擎
  services/aos-api/aos_api/model_provider_credential_router.py ← 凭据路由
  services/aos-api/aos_api/provider_security.py             ← 安全策略引擎
  services/aos-api/aos_api/provider_security_router.py      ← 安全策略路由
  services/aos-api/aos_api/provider_call_log.py             ← 调用日志引擎
  services/aos-api/aos_api/provider_call_log_router.py      ← 调用日志路由

改造文件（2个）：
  services/aos-api/aos_api/llm_provider_registry.py  ← 透明加解密改造
  services/aos-api/aos_api/main.py                   ← 注册新路由

前端改造（1个）：
  apps/web/src/pages/s2/aip.tsx  ← ProvidersPage 增加 detail view + 4 Tab
  apps/web/src/pages/s2/routes.tsx ← 增加 /aip/model-providers/:providerId 路由

测试文件（1个）：
  services/aos-api/tests/test_phase_a_provider_credentials.py
```

## 四、数据模型设计

```python
# kms_crypto.py
class KMSCrypto:
    """AES-256-GCM 透明加解密"""
    _master_key: bytes  # 来自环境变量 AOS_KMS_MASTER_KEY 或自动生成
    @classmethod
    def encrypt(cls, plaintext: str) -> str:  # → "enc:v1:{base64_nonce+ciphertext+tag}"
    @classmethod
    def decrypt(cls, token: str) -> str:      # ← "enc:v1:..." → plaintext
    @classmethod
    def is_encrypted(cls, val: str) -> bool   # 检查是否有 enc:v1: 前缀

# model_provider_credential.py
class ProviderCredential(BaseModel):
    key_id: str               # 凭据 ID（自动生成）
    provider_id: str          # 供应商 ID
    key_masked: str           # 掩码显示 "...sk-xxxx"
    encrypted_key: str        # 加密后的 API Key
    label: str                # 凭据标签（"生产"/"测试"/"开发"）
    rotation_policy: str      # "manual" / "30d" / "90d"
    last_rotated_at: str      # ISO datetime
    next_rotation_at: str     # 计算得出
    rotation_history: list    # [{date, operator, old_key_tail}]
    created_at: str

class ProviderCredentialEngine:
    """Singleton + threading.Lock"""
    _store: dict[str, list[ProviderCredential]]  # by provider_id

# provider_security.py
class ProviderSecurity(BaseModel):
    provider_id: str
    content_filter: bool = True
    max_tokens: int = 4096
    qps_limit: int = 100
    ip_allowlist: list[str] = []
    audit_log: bool = True
    data_residency: str = "provider"  # provider/local_cache/no_cache

# provider_call_log.py
class ProviderCallLog(BaseModel):
    log_id: str
    provider_id: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: int
    cost_usd: float
    status: str             # success/failed/timeout
    trace_id: str
    created_at: str
```

## 五、API 端点设计

| 方法 | 路径 | 说明 | 对应222文档 |
|------|------|------|------------|
| POST | `/api/models/providers/{id}/credentials` | 创建凭据 | 23.3 |
| GET | `/api/models/providers/{id}/credentials` | 列出凭据 | 23.3 |
| PUT | `/api/models/providers/{id}/credentials/{key_id}` | 更新凭据 | 23.3 |
| DELETE | `/api/models/providers/{id}/credentials/{key_id}` | 删除凭据 | 23.3 |
| POST | `/api/models/providers/{id}/test-connection` | 测试连接 | 23.3 |
| GET | `/api/models/providers/{id}/logs` | 调用日志（分页） | 23.6 |
| GET | `/api/models/providers/{id}/security` | 安全策略 | 23.5 |
| PUT | `/api/models/providers/{id}/security` | 更新安全策略 | 23.5 |

## 六、编码顺序（4 批）

| 批次 | 内容 | 文件 |
|------|------|------|
| **A-1** | KMS 加密 + 凭据引擎 + 凭据 CRUD API + 测试 | kms_crypto.py, model_provider_credential.py, model_provider_credential_router.py, test |
| **A-2** | 连接测试 + 安全策略 + 调用日志 API + 测试 | provider_security.py(+router), provider_call_log.py(+router), test |
| **A-3** | 透明加解密改造 llm_provider_registry.py + 测试 | llm_provider_registry.py 改造, test |
| **A-4** | 前端供应商详情页 4 Tab | aip.tsx, routes.tsx |

## 七、验收标准

- [x] 凭据 CRUD API 支持 4 种操作
- [x] API Key 存储 AES-256-GCM 加密
- [x] 透明加解密不影响现有 llm_gateway 调用
- [x] 安全策略可配置 QPS/IP白名单/审计
- [x] 调用日志可分页查询
- [x] 前端详情页 4 Tab 完整
- [x] 22 个单元测试全部 PASS

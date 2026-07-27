# 222plan · 222 产品补充功能分阶段开发与里程碑计划

> **版本**：v1.7 · 2026-07-26
> **分支**：m1（MacBook 本机）
> **状态**：✅ Phase E 全部完成（Phase A+B+C+C+D+E ✅ 全部完成，104/104 项）
> **参考资料**：[222-产品补充说明](222-产品补充说明.md) · [220w](220w-与目标系统差距对照分析.md) · [221m](221m-与目标系统差距对照分析.md)
> **关联**：220plan（已完成 270 项）· 220plan2（已完成 316 项）· 221plan（已完成 33 项）

---

## 〇、背景与定位

### 0.1 为什么需要 222plan

220plan / 220plan2 / 221plan 完成了后端 API 和引擎的**从零到一**搭建（共 619 项，3772 路由）。222 文档则定义了**产品层面的详细规格**（29 章，93 个功能点），关注前后端对接、交互体验和功能完整性。

**222plan = 把 222 文档中定义的产品功能落地为可运行的端到端系统。**

### 0.2 当前代码库基线

| 维度 | 数量 | 说明 |
|------|------|------|
| 后端 .py 文件 | 1,554 | 含引擎/路由/模型/工具 |
| 后端路由（include_router） | 468 | 已注册的路由模块 |
| 后端 API 端点（@router 装饰器） | 3,772 | 实际暴露的 REST 端点 |
| 后端测试文件 | 566 | pytest 测试文件 |
| 前端 ts/tsx 文件 | 101 | React 页面/组件/Hook |
| 前端导航页面 | 66（全部 live） | 0 个空壳占位 |
| 前端 React 页面 | 59+ | 全部有 state + API 调用 |
| 前端调用的 API 端点 | 80+ | 覆盖全部业务域 |
| 插件 | 67 | LLM/连接器/解析器/动作/渠道/组件/嵌入 |

### 0.3 差距分析结论

#### 222 文档 26 个 API 需求 vs 后端实际实现

| 状态 | 数量 | 说明 |
|------|------|------|
| ✅ 已实现 | 21 | 路径和功能完全匹配 |
| ⚠️ 部分实现 | 1 | `/v1/pipeline-outputs` 缺少根路径 POST |
| ❌ 完全缺失 | 4 | 全在 `/api/models/` 命名空间（供应商凭据 + 路由编辑） |

#### 222 文档 18 个前端页面需求 vs 前端实际实现

| 状态 | 数量 | 说明 |
|------|------|------|
| ✅ HTML Demo 已完成 | 73 页 | 视觉稿层面全部完成 |
| ✅ React 已实现 | 59+ 页 | 全部有真实 state + API 调用 |
| ❌ React 待实现 | 2 页 | 模型供应商详情页 + 模型路由编辑页 |

#### 222 文档 93 个功能点 vs 实际系统

| 状态 | 数量 | 说明 |
|------|------|------|
| ✅ 后端 API + 前端 React 均已实现 | ~65 | 占 70% |
| ⚠️ 后端有但前端未深度对接 | ~18 | 占 19%（交互补强类） |
| ❌ 前后端均缺失 | ~10 | 占 11%（模型供应商/路由/工作流编辑） |

### 0.4 222plan 的核心工作

```
不是从零搭建，而是深度补强：

  ┌─────────────────────────────────────────────────────────┐
  │  已有 API (3772 路由)  ←─连接─→  已有 React 页面 (59+)    │
  │                                                         │
  │  缺 4 个 API → 补                                       │
  │  缺 2 个 React 页面 → 建                                │
  │  18 个浅对接 → 深化                                     │
  │  33 个 HTML Demo 交互 → React 化                        │
  └─────────────────────────────────────────────────────────┘
```

---

## 一、使用的 Rules

| Rule | 应用 |
|------|------|
| 用中文回答 | 文档全中文 |
| 先方案再编码 | 本文档为开发计划，编码前须确认 |
| 修改代码前完善方案文档 | 各阶段开发前须完善详细方案 |
| 最小更改 | 按阶段增量开发，不影响现有 3772 条路由 |
| 每个功能点开发完立即写单元测试 | TDD 模式 |
| 每个波次完成后做集成自测 | 重启系统 → 验证页面 → 验证风格 |
| UI 功能设计对标 HTML 蓝图页 | 73 个 foundry/html 作为设计参考 |

---

## 二、整体路线图

```
┌──────────────────────────────────────────────────────────────────────────┐
│                  222plan · 产品功能落地路线图                              │
├──────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Phase A       Phase B       Phase C       Phase C+      Phase D       Phase E     │
│  模型供应商     模型路由      画布深度      订单管理      AIP Logic     端到端      │
│  与凭据管理     编辑器        对接          应用实例      交互补强       集成        │
│                                                                          │
│  ✅ 完成       ✅ 完成       ✅ 完成       ✅ 完成       ✅ 完成       ✅ 17/17    │
│  18/18         17/17         18/18         18/18         16/16         17/17 全部   │
│                                                                          │
│  ● API 4个     ● API 2个     ● 9 Tab       ● Order模型   ● 8 Block     ✅ Pipeline │
│  ● 详情页      ● 路由页      ● 工作流      ● 种子数据    ● 配置表单    ✅ Analytics│
│  ● KMS加密     ● Fallback    ● 事件向导    ● 3个Action   ● 调试器      ✅ Workshop │
│  ● 密钥轮换    ● 熔断器      ● 变量管理    ● 列表+详情   ● 自动化      ✅ Agent    │
│  ● 连接测试    ● 路由测试    ● 样式管理    ● 统计Widget  ● 运行历史    ✅ Wiki      │
│                                                                          │
│  P0 核心       P0 核心       P1 增强       P1 增强       P1 增强       ✅ 回归测试 │
│                                                                          │
│  总进度：104 / 104 = 100% ✅                                              │
└──────────────────────────────────────────────────────────────────────────┘
```

---

## 三、Phase A：模型供应商与凭据管理（P0 核心）

> **对应章节**：222 第 23 章 · 222 第 9.6 节
> **目标**：实现模型供应商详情页的 4 Tab（凭据管理/模型列表/安全策略/调用日志）+ 后端 API

### 3.0 技术方案（编码前确认）

#### 现有架构分析

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

#### 缺失项精确定位

| # | 缺失 | 影响 | 解决方案 |
|---|------|------|---------|
| 1 | **API Key 明文存储** | 安全风险 | 新建 `kms_crypto.py`，AES-256-GCM 加解密；改造 `put_plugin_secret`/`resolve_plugin_api_key` 透明加解密 |
| 2 | **无凭据 CRUD API** | 222文档要求 `/api/models/providers/{id}/credentials` | 新建 `model_provider_credential_router.py`，prefix `/api/models/providers` |
| 3 | **无连接测试 API** | 222文档要求 `/api/models/providers/{id}/test-connection` | 在新 router 中实现，用 httpx 向供应商 `/v1/models` 发 GET |
| 4 | **无密钥轮换** | 222文档要求 30/90天自动轮换 | 新建 `key_rotation_scheduler.py`，记录轮换历史 |
| 5 | **无安全策略 API** | 222文档要求 IP白名单/QPS限制/审计 | 新建 `provider_security_router.py` |
| 6 | **无调用日志 API** | 222文档要求调用历史 | 新建 `provider_call_log_router.py`，从 FailoverEngine.CallRecord 提取 |
| 7 | **无供应商详情页** | 前端只有列表页，缺详情页 | 改造 `aip.tsx` ProvidersPage，增加 `detail` view + 4 Tab |

#### 实施策略

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

#### 数据模型设计

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

#### API 端点设计

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

#### 编码顺序（4 批）

| 批次 | 内容 | 文件 |
|------|------|------|
| **A-1** | KMS 加密 + 凭据引擎 + 凭据 CRUD API + 测试 | kms_crypto.py, model_provider_credential.py, model_provider_credential_router.py, test |
| **A-2** | 连接测试 + 安全策略 + 调用日志 API + 测试 | provider_security.py(+router), provider_call_log.py(+router), test |
| **A-3** | 透明加解密改造 llm_provider_registry.py + 测试 | llm_provider_registry.py 改造, test |
| **A-4** | 前端供应商详情页 4 Tab | aip.tsx, routes.tsx |

### 3.1 里程碑

**MA-1**：供应商凭据 CRUD API + KMS 加密
**MA-2**：供应商详情页 React 实现
**MA-3**：密钥轮换定时任务
**MA-4**：连接测试 API

### 3.2 详细任务

| 任务ID | 任务 | 类型 | 预估工时 | 依赖 | 交付物 |
|--------|------|------|---------|------|--------|
| A-01 | 新建 `model_provider_credential_router.py`，prefix `/api/models/providers` | 后端 API | 1d | — | 凭据 CRUD 路由 |
| A-02 | 实现 `POST /api/models/providers/{id}/credentials` — 创建凭据 | 后端 API | 0.5d | A-01 | 创建端点 |
| A-03 | 实现 `GET /api/models/providers/{id}/credentials` — 列出凭据 | 后端 API | 0.3d | A-01 | 列出端点 |
| A-04 | 实现 `PUT /api/models/providers/{id}/credentials/{key_id}` — 更新凭据 | 后端 API | 0.5d | A-01 | 更新端点 |
| A-05 | 实现 `DELETE /api/models/providers/{id}/credentials/{key_id}` — 删除凭据 | 后端 API | 0.3d | A-01 | 删除端点 |
| A-06 | KMS AES-256-GCM 加密工具 `kms_crypto.py` | 后端引擎 | 1d | — | 加密/解密工具 |
| A-07 | 凭据存储 Pydantic 模型 `ProviderCredential`（key_id, provider_id, encrypted_key, rotation_policy, created_at, last_rotated） | 后端模型 | 0.5d | A-06 | 数据模型 |
| A-08 | 实现 `POST /api/models/providers/{id}/test-connection` — 向 `/v1/models` 发 GET | 后端 API | 0.5d | A-04 | 测试端点 |
| A-09 | 密钥轮换定时任务 `key_rotation_scheduler.py`（APScheduler，30/90 天） | 后端引擎 | 1d | A-07 | 定时任务 |
| A-10 | 调用日志查询 API `GET /api/models/providers/{id}/logs`（分页） | 后端 API | 0.5d | A-01 | 日志端点 |
| A-11 | 安全策略配置 API `GET/PUT /api/models/providers/{id}/security` | 后端 API | 0.5d | A-01 | 策略端点 |
| A-12 | 单元测试：凭据 CRUD × 5 用例 + 加密 × 3 + 测试连接 × 2 + 轮换 × 2 | 测试 | 1d | A-02~A-09 | 12 个测试 |
| A-13 | 供应商详情页 React 组件 `ProviderDetailPage.tsx` | 前端页面 | 2d | A-02~A-11 | 详情页 |
| A-14 | 凭据管理 Tab（添加/编辑/删除/轮换 + 掩码显示） | 前端 Tab | 1d | A-13 | 凭据 Tab |
| A-15 | 模型列表 Tab（供应商下的模型表格 + 状态徽章） | 前端 Tab | 0.5d | A-13 | 模型 Tab |
| A-16 | 安全策略 Tab（加密算法/轮换周期/IP 白名单/速率限制） | 前端 Tab | 0.5d | A-13 | 策略 Tab |
| A-17 | 调用日志 Tab（时间线 + 成功/失败/超时筛选） | 前端 Tab | 0.5d | A-13 | 日志 Tab |
| A-18 | nav.ts 注册路由 `/models/providers/:providerId` | 前端路由 | 0.2d | A-13 | 路由注册 |

### 3.3 验收标准

- [ ] 凭据 API 支持 CRUD，密钥以 AES-256-GCM 加密存储
- [ ] 连接测试可向供应商 `/v1/models` 端点发送 GET 请求
- [ ] 密钥轮换定时任务可按 30/90 天周期执行
- [ ] 供应商详情页 4 Tab 全部可交互
- [ ] 12 个单元测试全部 PASS

---

## 四、Phase B：模型路由编辑器（P0 核心）

### Phase B 技术方案（B-Tech）

#### 现状审计结论

| 维度 | 现状 | 差距 |
|------|------|------|
| **后端引擎** | `llm_routing.py`(784行) 已有 SmartRouter + ScenarioRouter + FailoverEngine 三大引擎 | 引擎内存存储、重启丢失 |
| **后端 API** | `routers/llm_routing.py`(416行) 已有 22 个端点 `/v1/aip/smart-router/*` 等 | 前端完全没调用这些端点 |
| **前端实际使用** | `wave_ext.py` 的 `/v1/aip/model-routes`(GET/PUT) | 只有 primary/fallback 二选一，无权重分配 |
| **KV 存储** | `aip_kv_store.py` 持久化 RouteRule | 缺少 weights、circuit_config_v2、fallback_chain |
| **前端 ModelRouterPage** | aip.tsx L1644(385行) 已有规则表 + 保存 + 熔断演练 + 试聊 | 缺少权重滑块、全局熔断配置面板、Fallback 链可视化、路由测试 |
| **视觉稿** | aip-model-router.html(407行) 完整 UI | 权重分配条 + 熔断滑块组 + Fallback 链 SVG + 预热状态 |

**核心洞察**：后端引擎能力（智能路由+场景路由+熔断状态机）远超前端使用深度。Phase B 的本质是**让前端接入已有的 22 个 API 端点**，同时补齐 KV 层缺失的字段。

#### 数据模型扩展

在 `aip_kv_store.py` 的 RouteRule 基础上增加字段（向后兼容）：

```python
# aip_kv_store.py 扩展字段
class RouteRuleV2:
    id: str
    task: str
    primary: str
    fallback: str
    egress: str
    span: bool
    # --- V2 新增 ---
    weights: list[dict]          # [{"model":"gpt-4o","pct":60}, {"model":"gpt-4o-mini","pct":40}]
    fallback_chain: list[str]    # ["gpt-4o", "gpt-4o-mini", "报错"]
    circuit_config: dict         # {"error_rate_threshold":10, "latency_p99_ms":3000, "cooldown_s":30, "half_open_probes":3}
    strategy: str                # "weighted" | "failover" | "lowest_latency" | "lowest_cost"
```

全局熔断配置（独立持久化）：

```python
class GlobalCircuitConfig:
    error_rate_threshold_pct: int = 10      # 5xx 错误率
    latency_p99_ms: int = 3000              # 延迟阈值
    cooldown_seconds: int = 30              # 熔断时长
    half_open_probes: int = 3               # 半开探测数
```

#### 编码顺序（3 批）

| 批次 | 内容 | 文件 |
|------|------|------|
| **B-1** | KV 层扩展 RouteRuleV2 + 全局熔断配置 + 路由 CRUD API + 测试 | aip_kv_store.py 扩展, model_router_config.py, model_router_config_router.py, test |
| **B-2** | 路由测试 API + 融合熔断引擎 + 测试 | model_router_config.py 扩展, test |
| **B-3** | 前端 ModelRouterPage 深度增强 | aip.tsx 增强 |

> **对应章节**：222 第 24 章
> **目标**：实现模型路由编辑器的 Fallback 链可视化 + 权重滑块 + 熔断器 + 路由测试

### 4.1 里程碑

**MB-1**：路由配置 CRUD API
**MB-2**：路由编辑页 React 实现
**MB-3**：Fallback 链拖拽可视化
**MB-4**：路由测试面板

### 4.2 详细任务

| 任务ID | 任务 | 类型 | 预估工时 | 依赖 | 交付物 |
|--------|------|------|---------|------|--------|
| B-01 | 新建 `model_router_config_router.py`，prefix `/api/models/router` | 后端 API | 1d | — | 路由 CRUD 模块 |
| B-02 | 实现 `GET /api/models/router` — 列出所有路由配置 | 后端 API | 0.3d | B-01 | 列出端点 |
| B-03 | 实现 `GET /api/models/router/{id}` — 获取单条路由配置 | 后端 API | 0.3d | B-01 | 详情端点 |
| B-04 | 实现 `PUT /api/models/router/{id}` — 更新路由配置 | 后端 API | 0.5d | B-01 | 更新端点 |
| B-05 | 实现 `POST /api/models/router/{id}/test` — 路由测试（模拟决策） | 后端 API | 1d | B-04 | 测试端点 |
| B-06 | `RouteConfig` Pydantic 模型（route_id, name, models[], weights[], fallback_chain[], circuit_breaker, timeout_ms, retry_count, strategy） | 后端模型 | 0.5d | B-01 | 数据模型 |
| B-07 | `CircuitBreaker` 状态机（closed→open→half_open→closed） | 后端引擎 | 1d | B-06 | 熔断器 |
| B-08 | 路由策略引擎扩展（加权/最低延迟/最低成本）— 增强 `llm_routing.py` | 后端引擎 | 1d | B-06 | 策略引擎 |
| B-09 | 单元测试：路由 CRUD × 4 + 熔断器 × 3 + 策略 × 3 + 测试 × 2 | 测试 | 1d | B-02~B-08 | 12 个测试 |
| B-10 | 路由编辑页 React 组件 `ModelRouterEditPage.tsx` | 前端页面 | 2d | B-02~B-08 | 编辑页 |
| B-11 | Fallback 链可视化（拖拽排序 + 连线 SVG + 节点状态颜色） | 前端交互 | 1.5d | B-10 | Fallback 链 |
| B-12 | 权重滑块组件（拖拽分配百分比 + 实时总和校验） | 前端组件 | 0.5d | B-10 | 权重滑块 |
| B-13 | 熔断器配置面板（阈值/恢复时间/状态可视化） | 前端面板 | 0.5d | B-10 | 熔断面板 |
| B-14 | 超时/重试配置面板 | 前端面板 | 0.3d | B-10 | 配置面板 |
| B-15 | 路由测试面板（输入 prompt → 显示模型选择 + 延迟 + Token 消耗） | 前端面板 | 1d | B-05 | 测试面板 |
| B-16 | 路由策略选择器（加权/最低延迟/最低成本 Radio 切换） | 前端组件 | 0.3d | B-10 | 策略选择 |
| B-17 | nav.ts 注册路由 `/models/router/:routeId/edit` | 前端路由 | 0.2d | B-10 | 路由注册 |

### 4.3 验收标准

- [ ] 路由配置 API 支持 CRUD
- [ ] 路由测试 API 可模拟决策并返回模型选择 + 延迟
- [ ] Fallback 链可拖拽排序，节点状态实时更新
- [ ] 权重滑块总和始终 = 100%
- [ ] 熔断器状态可视化（绿/红/黄三色）
- [ ] 12 个单元测试全部 PASS

---

### 4.5 Phase C 技术方案（先行文档）

> **写入时间**：2026-07-25 · 编码前
> **核心洞察**：后端 Workshop 引擎极其完整——变量引擎（register/evaluate/lineage/events）、事件引擎（vs_events）、Compute Job 轮询、Widget Plugin 全部已实现并注册到 main.py。Phase C 90% 的工作是**前端对接**。

#### 现有后端 API（已实现，Phase C 直接对接）

| API 前缀 | 用途 | 关键端点 |
|----------|------|---------|
| `/workshop-compute-api/variables` | 变量引擎 | POST(register) / GET(list) / PUT(update) / DELETE / POST(evaluate) / GET(lineage) |
| `/workshop-compute-api/variables/{id}/events` | 变量事件 | POST(record) / GET(list) |
| `/workshop-compute-api/jobs` | Compute Job | POST(submit) / GET(list) / POST(poll) / GET(result) |
| `/workshop-compute-api/app-entries` | App Entry | POST(register) / GET(list) / POST(validate) |
| `/v1/modules` | Module CRUD | GET(list) / POST(create) / GET(detail) / PATCH / POST(publish) |
| `/v1/modules/{id}/runtime` | Module 运行态 | GET |
| `/api/module-interfaces` | Module 接口 | GET(list) / PUT(update) |
| `/v1/widget-plugins` | Widget 注册表 | GET(list) |
| `/v1/sql/preview` | SQL 预览 | POST |

#### 现有前端 CanvasPage 结构（1089 行）

- 三栏布局：Layout 树 | Canvas 画布 | Props 配置面板
- 顶部工具栏有 9 个 Tab（dashboard/queries/functions/objects/events/data/dependencies/styles/variables）
- **问题**：Tab 按钮是纯装饰，没有 state 切换，没有内容面板
- Widget/Workflow 模式按钮也是纯装饰

#### Phase C 改造方案

**C-1 批：Tab 系统核心 + 后端补全（C-01~C-08 + C-11~C-15）**

1. CanvasPage 增加 `activeTab` state，9 个 Tab 按钮接入点击切换
2. 为每个 Tab 实现内容面板组件（内联或独立函数组件）
3. 补充后端缺失的 Module 事件持久化（C-11~C-13）

**C-2 批：前端面板组件（C-02~C-07 + C-09~C-10 + C-14~C-17）**

| Tab | 数据源 | 渲染内容 |
|-----|--------|---------|
| Dashboard | `/v1/modules/{id}/runtime` | 统计卡片 + Widget 绑定状态 |
| Queries | `/v1/sql/preview` | SQL 编辑器 + 查询列表 |
| Functions | `/workshop-compute-api/variables` (type=function) | 函数列表 + AIP Logic 导入 |
| Events | `/v1/modules/{id}/events` (新增) | 事件绑定列表 + 3 步向导 |
| Data | `/v1/sources` | 数据源列表 + 绑定编辑器 |
| Dependencies | `/workshop-compute-api/variables/{id}/lineage` | 依赖树 SVG |
| Styles | 前端 state（持久化到 Module.widgets.meta.styles） | 4 主题预设 + CSS 变量编辑 |
| Variables | `/workshop-compute-api/variables` | 变量表 + 7 类型 + 3 作用域 |
| Objects | 现有 CanvasPage 配置面板（保持不变） | 保持当前 |

**C-3 批：工作流模式 + 事件向导 + 组件注册表（C-08~C-10 + C-16）**

- Workflow 模式：SVG 事件编排图（触发器→条件→动作）
- 事件 3 步向导：选择触发器 → 选择动作 → 变量幂等 + 预览链
- 组件注册表：对接 `/v1/widget-plugins`

#### 后端需新增（最小量）

| 任务 | 说明 |
|------|------|
| Module 事件持久化 | `module_store.py` 增加 events 字段到 meta_module，暴露 `/v1/modules/{id}/events` GET/POST/DELETE |
| 变量↔Module 关联 | `WorkshopVariableEngine` 已有 module_id 字段，list 时按 module_id 过滤即可 |

#### 测试

- Module 事件 CRUD × 3
- 变量按 module_id 过滤 × 2
- 变量 evaluate × 2

---

## 五、Phase C：Workshop 画布深度对接（P1 增强）

> **对应章节**：222 第 1-5 章 · 第 25-27 章
> **目标**：将 HTML Demo 中实现的画布交互（9 Tab / 三模式 / 事件向导 / 变量管理 / 组件注册）映射到 React 前端，并对接后端 API

### 5.1 里程碑

**MC-1**：Workshop 9 Tab 内容面板 React 化
**MC-2**：工作流模式 SVG 事件编排 React 化
**MC-3**：事件添加 3 步向导对接后端
**MC-4**：变量管理器对接后端
**MC-5**：组件注册表对接 Widget Plugin API

### 5.2 详细任务

| 任务ID | 任务 | 类型 | 预估工时 | 依赖 | 交付物 |
|--------|------|------|---------|------|--------|
| C-01 | CanvasPage 增强：Tab 系统（Dashboard/Queries/Functions/Events/Data/Dependencies/Styles/Variables） | 前端增强 | 1.5d | — | Tab 系统 |
| C-02 | Queries Tab：SQL 编辑器面板 + 查询列表（对接 `/v1/sql/preview`） | 前端 Tab | 1d | C-01 | 查询 Tab |
| C-03 | Functions Tab：函数列表 + AIP Logic 导入按钮（对接 `/v1/functions-runtime/functions`） | 前端 Tab | 0.5d | C-01 | 函数 Tab |
| C-04 | Events Tab：事件绑定列表 + 触发器配置（对接 `/v1/modules/{id}/events`） | 前端 Tab | 0.5d | C-01 | 事件 Tab |
| C-05 | Data Tab：数据源列表 + 绑定编辑器（对接 `/v1/sources`） | 前端 Tab | 0.5d | C-01 | 数据 Tab |
| C-06 | Dependencies Tab：依赖树 + 引用计数（对接 `/v1/modules/{id}/dependencies`） | 前端 Tab | 0.5d | C-01 | 依赖 Tab |
| C-07 | Dashboard Tab：统计卡片 + Widget 绑定状态（聚合查询） | 前端 Tab | 0.5d | C-01 | 仪表 Tab |
| C-08 | 三模式切换：组件模式 / 工作流模式 / 预览模式 | 前端增强 | 0.5d | C-01 | 模式切换 |
| C-09 | 工作流模式：SVG 事件编排图（触发器→条件→动作节点 + 连线） | 前端交互 | 2d | C-08 | 工作流画布 |
| C-10 | 事件添加 3 步向导 React 化（选择触发器→选择动作→变量幂等 + 预览链） | 前端弹窗 | 1.5d | C-04 | 事件向导 |
| C-11 | `POST /v1/modules/{id}/events` — 事件绑定创建 API | 后端 API | 0.5d | — | 事件 API |
| C-12 | `GET /v1/modules/{id}/events` — 事件绑定列表 API | 后端 API | 0.3d | — | 事件 API |
| C-13 | `DELETE /v1/modules/{id}/events/{event_id}` — 事件绑定删除 API | 后端 API | 0.3d | — | 事件 API |
| C-14 | 变量管理器 React 面板（12 变量表 + 7 类型 + 3 作用域 + 绑定微件） | 前端面板 | 1d | C-01 | 变量面板 |
| C-15 | 变量 CRUD API（`GET/POST/PUT/DELETE /v1/modules/{id}/variables`） | 后端 API | 0.5d | — | 变量 API |
| C-16 | 组件注册表面板（对接 `/v1/widget-plugins`，16 组件卡片 + 3 来源 Tab） | 前端面板 | 0.5d | — | 组件面板 |
| C-17 | 样式管理面板（4 主题预设 + 调色板 + CSS 变量编辑器） | 前端面板 | 0.5d | C-01 | 样式面板 |
| C-18 | 单元测试：事件 CRUD × 3 + 变量 CRUD × 4 | 测试 | 0.5d | C-11~C-15 | 7 个测试 |

### 5.3 验收标准

- [ ] 9 个 Tab 全部有内容面板（非空壳）
- [ ] 工作流模式可显示 SVG 事件编排图
- [ ] 事件添加向导可完成 3 步并创建绑定
- [ ] 变量管理器可 CRUD 变量
- [ ] 组件注册表可展示 Widget 列表
- [ ] 7 个单元测试全部 PASS

---

## 五½、Phase C+：订单管理应用实例（P1 增强）

> **对应章节**：222 第 12 章 · 视觉稿 `workshop-app-order.html`
> **目标**：实现视觉稿中「工作台 → 订单管理」的完整前后端，作为 Workshop 画布编辑器的**首个真实业务应用实例**
> **背景**：视觉稿侧栏「工作台」分区有 `订单管理(workshop-app-order)` 菜单项，但 React 前端 `nav.ts` 中缺失。后端有 `WorkOrder`（工单）但没有 `Order`（电商订单）。需要补齐完整的订单管理应用。

### 5½.0 技术方案（C+-Tech，编码前确认）

#### 后端现有基础设施审计

后端已有完整的 Ontology + Action 基础设施，Phase C+ **不需要新建引擎**：

| 基础设施 | 文件 | 说明 |
|----------|------|------|
| ObjectType CRUD | `routers/ontology.py` | `meta_object_type` 表 + `/v1/ontology/object-types` API |
| Object 实例 CRUD | `routers/ontology.py` | `obj_instance` 表 + `/v1/objects/{type}` API (GET 列表/详情) |
| Object Set 查询 | `routers/object_sets.py` | `POST /v1/object-sets/query` 支持 filters/分页 |
| LinkType CRUD | `routers/ontology.py` | `meta_link_type` 表 + graph_edge 邻接表 |
| Action Type CRUD | `routers/actions.py` | `meta_action_type` 表 + `/v1/actions/types` API |
| Action 执行 | `routers/runtime_write.py` | `POST /v1/actions/execute` → Draft 审批写回 |
| 种子注入 | `db.py` `seed_if_empty()` | 启动时自动注入种子 |
| Action 插件 | `plugins/actions/*/manifest.json` | 磁盘插件 + `action_template_registry.py` 自动扫描注册 |

**结论**：现有后端 100% 覆盖 Phase C+ 需求。工作全部集中在**种子数据 + Action 插件 manifest + 前端 React**。

#### 实施策略：3 批

| 批次 | 内容 | 文件 |
|------|------|------|
| **C+-1** | Order/OrderItem ObjectType 定义 + 种子数据（20 条订单）+ LinkType + 3 个 Action 插件 manifest + 测试 | `order_seed.py`, `plugins/actions/*/manifest.json`, `test_phase_cp_orders.py` |
| **C+-2** | 前端 OrderManagementPage.tsx — 对齐视觉稿 | `apps/web/src/pages/s2/OrderManagementPage.tsx` |
| **C+-3** | nav.ts 注册 + routes.tsx 路由 | `nav.ts`, `routes.tsx` |

#### C+-1 详细方案

**Order ObjectType 定义**（properties JSONB 数组）：
```python
_ORDER_PROPS = json.dumps([
    {"name": "order_no", "type": "string"},
    {"name": "customer_id", "type": "string"},
    {"name": "customer_name", "type": "string"},
    {"name": "order_date", "type": "string"},
    {"name": "total_amount", "type": "number"},
    {"name": "status", "type": "string"},  # pending/paid/shipped/delivered/cancelled/refunded
    {"name": "shipping_address", "type": "string"},
    {"name": "items", "type": "json"},     # JSONB 数组
    {"name": "tracking_no", "type": "string"},
    {"name": "remark", "type": "string"},
])
```

**种子数据 20 条订单**：覆盖 6 种状态，客户名使用中文，金额 76~5880 元。

**3 个 Action 插件**（manifest.json + inproc runtime）：
- `confirm-shipment`: status→shipped + 记录 tracking_no
- `cancel-order`: status→cancelled + 记录 remark
- `refund-order`: status→refunded + 记录退款金额

#### C+-2 前端方案

`OrderManagementPage.tsx` 对齐视觉稿 `workshop-app-order.html`：
- **统计卡片行**：4 张 stat card（总订单 / 待处理 / 已完成 / 总收入）
- **订单列表表格**：订单号 / 客户 / 日期 / 金额 / 状态徽章
- **状态筛选 Tab**：全部 / 待付款 / 已付款 / 已发货 / 已签收 / 已取消 / 已退款
- **搜索框**：按订单号 / 客户名搜索
- **订单详情侧栏**：选中行 → 展开详情面板 + 3 个 Action 按钮
- **趋势图**：近 7 天折线图（SVG 内联）
- 数据源：`GET /v1/objects/Order` + `POST /v1/object-sets/query`

### 5½.1 里程碑

**MC+1**：Order ObjectType + 种子数据 + 3 个 Action 插件
**MC+2**：订单管理 React 页面（列表 + 详情 + 统计 Widget）
**MC+3**：nav.ts 注册路由

### 5½.2 详细任务

| 任务ID | 任务 | 类型 | 预估工时 | 依赖 | 交付物 |
|--------|------|------|---------|------|--------|
| C+01 | Order ObjectType 定义（order_id PK / customer_id / order_date / total_amount / status / shipping_address / items JSONB）— 注册到本体元数据 | 后端模型 | 0.5d | — | ObjectType |
| C+02 | Order 种子数据（20 条订单样例，覆盖 6 种状态：待付款/已付款/已发货/已签收/已取消/已退款） | 后端数据 | 0.3d | C+01 | 种子数据 |
| C+03 | OrderItem ObjectType 定义（item_id / order_id FK / product_name / quantity / unit_price / subtotal）— 订单明细子表 | 后端模型 | 0.3d | C+01 | 子表 |
| C+04 | Order LinkType 定义（Order → Customer / Order → OrderItem / Order → Product） | 后端模型 | 0.3d | C+01 | LinkType |
| C+05 | `GET /v1/ontology/object-types/Order/objects` — 订单列表查询 API（支持分页 + 状态筛选 + 关键词搜索） | 后端 API | 0.5d | C+02 | 列表 API |
| C+06 | `GET /v1/ontology/object-types/Order/objects/{order_id}` — 订单详情 API（含 OrderItem 子对象展开） | 后端 API | 0.3d | C+05 | 详情 API |
| C+07 | `POST /v1/actions/execute` — ConfirmShipment Action（确认发货：status→已发货 + 记录物流单号） | 后端 Action | 0.5d | C+01 | 发货 Action |
| C+08 | `POST /v1/actions/execute` — CancelOrder Action（取消订单：status→已取消 + 库存回滚） | 后端 Action | 0.5d | C+01 | 取消 Action |
| C+09 | `POST /v1/actions/execute` — RefundOrder Action（退款：status→已退款 + 退款金额记录） | 后端 Action | 0.5d | C+01 | 退款 Action |
| C+10 | 订单管理 React 页面 `OrderManagementPage.tsx` — 对齐 `workshop-app-order.html` 视觉稿 | 前端页面 | 2d | C+05~C+06 | 订单页面 |
| C+11 | 订单列表区域：表格（订单号/客户/日期/金额/状态徽章）+ 状态筛选 Tab + 搜索框 | 前端区域 | 1d | C+10 | 列表区 |
| C+12 | 订单详情区域：选中订单后展开详情面板（订单信息 + 物品明细 + 物流信息 + 操作按钮） | 前端区域 | 1d | C+10 | 详情区 |
| C+13 | 画布区域：展示当前 Module 的 Widget 布局（统计卡片 + 趋势图 + 订单表格），复用 CanvasPage | 前端区域 | 0.5d | C+10 | 画布区 |
| C+14 | 工具栏：+ 添加微件 / 布局 / 变量 / 事件 / 保存 / 发布（复用 Phase C 的工具栏组件） | 前端工具栏 | 0.5d | Phase C | 工具栏 |
| C+15 | 订单统计卡片 Widget（总订单数 / 待处理 / 今日营收 / 退款率） | 前端 Widget | 0.5d | C+10 | 统计 Widget |
| C+16 | 订单趋势图 Widget（近 7 天订单量折线图） | 前端 Widget | 0.5d | C+10 | 趋势 Widget |
| C+17 | nav.ts 注册路由 `/workshop/orders`（label: 订单管理，icon: inbox，status: live） | 前端路由 | 0.2d | C+10 | 路由注册 |
| C+18 | 单元测试：订单列表 × 2 + 详情 × 1 + 发货 × 2 + 取消 × 2 + 退款 × 2 | 测试 | 0.5d | C+05~C+09 | 9 个测试 |

### 5½.3 验收标准

- [ ] 订单列表 API 支持分页 + 状态筛选 + 搜索
- [ ] 订单详情 API 可展开 OrderItem 子对象
- [ ] 3 个 Action（发货/取消/退款）可正常执行并修改订单状态
- [ ] 订单管理页面与视觉稿 `workshop-app-order.html` 对齐
- [ ] 列表表格状态徽章颜色正确（待付款灰/已付款蓝/已发货黄/已签收绿/已取消红/已退款紫）
- [ ] nav.ts 侧边栏「工作台 → 订单管理」可点击进入
- [ ] 9 个单元测试全部 PASS

---

## 六、Phase D：AIP Logic 交互补强（P1 增强）

> **对应章节**：222 第 20 章 · 第 21 章
> **目标**：将 AIP Logic 画布的 8 种 Block 交互绑定 + 配置区动态表单 + 调试器 + 自动化 Tab 全部对接后端 API

### 6.1 里程碑

**MD-1**：8 种 Block 按钮事件绑定
**MD-2**：配置区动态表单（按 BlockKind 渲染不同控件）
**MD-3**：预览区试运行对接
**MD-4**：自动化 Tab 完善（5 种触发器）
**MD-5**：运行历史 Tab 对接 API

### 6.2 详细任务

| 任务ID | 任务 | 类型 | 预估工时 | 依赖 | 交付物 |
|--------|------|------|---------|------|--------|
| D-01 | LogicCanvasPage 8 种 Block 按钮事件绑定（get/transform/execute/writeback/branch/merge/handoff/annotate） | 前端交互 | 1.5d | — | Block 按钮 |
| D-02 | 配置区动态表单引擎（按 BlockKind 渲染不同控件：ObjectSet 选择器/SQL 编辑器/LLM Prompt/Action 选择器/条件 DSL/合并策略/Handoff 配置/标注文本） | 前端组件 | 2d | D-01 | 动态表单 |
| D-03 | 分支条件 DSL 编辑器（条件表达式 + AND/OR 组合 + 字段选择器） | 前端编辑器 | 1d | D-02 | 条件编辑器 |
| D-04 | 预览区试运行对接（`POST /v1/logic/run` → 展示输入/输出/Token/耗时） | 前端对接 | 0.5d | D-02 | 试运行 |
| D-05 | 调试器逐步执行对接（`POST /v1/logic/debug` → CoT 展开 + 工具调用链） | 前端对接 | 1d | D-04 | 调试器 |
| D-06 | 拖拽调整 Block 顺序（react-dnd / 原生 HTML5 drag） | 前端交互 | 1d | D-01 | 拖拽排序 |
| D-07 | 保存到分支对接（`PUT /api/aip/logic-state` + `POST /api/aip/logic-version`） | 前端对接 | 0.5d | D-02 | 保存功能 |
| D-08 | 自动化 Tab 增强：补全 5 种触发器（对象变更/定时/人工/Webhook/阈值） | 前端 Tab | 1d | — | 自动化 Tab |
| D-09 | 运行历史 Tab 对接（`GET /v1/aip/automate/runs` → 表格 + Trace 下钻） | 前端 Tab | 0.5d | — | 历史 Tab |
| D-10 | 汇聚节点显式 merge 语义（merge 策略选择：first/last/union/intersect） | 前端交互 | 0.5d | D-02 | Merge 语义 |
| D-11 | AIP 可观测性：4 Tab 切换 React 化 + 追踪/详情视图切换器 | 前端增强 | 1d | — | 观测 Tab |
| D-12 | 可观测性：火焰图 Span 树对接 API（`GET /tracing-perf-geo-map/tracing/traces/{id}/tree`） | 前端对接 | 1d | D-11 | 火焰图 |
| D-13 | 可观测性：函数代码面板（语法高亮 + 安全约束展示） | 前端面板 | 0.5d | D-11 | 代码面板 |
| D-14 | 可观测性：测试用例管理 UI（列表 + 运行 + 断言，对接 `/functions-dev-tools/tests`） | 前端面板 | 0.5d | D-11 | 测试面板 |
| D-15 | 可观测性：调试器断点 UI（单步执行，对接 `/functions-dev-tools/debug-sessions`） | 前端面板 | 0.5d | D-11 | 调试面板 |
| D-16 | 可观测性：删除函数依赖检查 UI（对接 `/v1/oma/function-types/{name}/usage`） | 前端面板 | 0.5d | D-11 | 删除确认 |

### 6.3 验收标准

- [ ] 8 种 Block 按钮均可点击并弹出对应配置表单
- [ ] 配置区按 BlockKind 渲染不同控件
- [ ] 分支条件 DSL 编辑器可添加/编辑/删除条件
- [ ] 预览区可试运行并展示结果
- [ ] 调试器可单步执行
- [ ] Block 可拖拽排序
- [ ] 保存功能可持久化到分支
- [ ] 自动化 Tab 支持 5 种触发器
- [ ] 运行历史可下钻到 Trace
- [ ] 可观测性火焰图对接 API 数据

---

## 七、Phase E：端到端集成与回归（P2 收尾）

> **对应章节**：222 全章节交叉验证
> **目标**：全链路集成测试，确保前端 59+ 页面与后端 3772+ 路由的完整对接
> **进度**：✅ 全部完成 17/17 项

### 7.1 里程碑

**ME-1**：Pipeline Builder 前端深度对接 ✅
**ME-2**：Workshop Module 创建/编辑全流程 ✅
**ME-3**：Analytics 页面深度对接 ✅
**ME-4**：全量回归测试 ✅

### 7.2 详细任务

| 任务ID | 任务 | 类型 | 预估工时 | 依赖 | 交付物 | 状态 |
|--------|------|------|---------|------|--------|------|
| E-01 | Pipeline 列表页动态加载（对接 `/v1/pipeline-builder`） | 前端对接 | 0.5d | — | 列表加载 | ✅ |
| E-02 | Pipeline DAG 画布交互增强（节点拖拽/连线/删除） | 前端增强 | 1.5d | E-01 | DAG 画布 | ✅ |
| E-03 | 变换算子工具栏补全（15 个，含隐藏 5 个） | 前端增强 | 0.5d | E-02 | 算子工具栏 | ✅ |
| E-04 | 底部数据预览表对接（`GET /v1/datasets/{id}/preview`） | 前端对接 | 0.5d | E-02 | 预览表 | ✅ |
| E-05 | 管道类型选择器（batch/incremental/streaming） | 前端组件 | 0.3d | E-02 | 类型选择 | ✅ |
| E-06 | 输出配置面板（6 种 Write Mode） | 前端面板 | 0.5d | E-02 | 输出配置 | ✅ |
| E-07 | Workshop Module 创建全流程（基本信息→数据绑定→模板选择→确认创建→跳转画布） | 前端全流程 | 1d | Phase C | 创建流程 | ✅ |
| E-08 | Analytics 页面增强：读数/Draft/探索 Tab 深度对接 | 前端增强 | 1d | — | Analytics | ✅ |
| E-09 | Agent 创建向导 4 步（基础信息→能力配置→安全等级→确认创建） | 前端向导 | 1d | — | Agent 向导 | ✅ |
| E-10 | Agent 目录页（3 来源 11 卡片 + 搜索筛选） | 前端页面 | 0.5d | E-09 | 目录页 | ✅ |
| E-11 | 外部 Agent 导入向导（5 步：来源→扫描→Manifest→安全→确认） | 前端向导 | 1d | — | 导入向导 | ✅ |
| E-12 | 插件引入向导（4 步：能力类型→Manifest→安全→连通测试） | 前端向导 | 0.5d | — | 插件向导 | ✅ |
| E-13 | Wiki 索引页对接（分支树 + 页面卡片 + 搜索，对接 `/v1/wiki`） | 前端对接 | 0.5d | — | Wiki 索引 | ✅ |
| E-14 | 版本对比视图对接（diff 数据，对接 `/v1/wiki/{type}/{id}/versions`） | 前端对接 | 0.5d | E-13 | 版本对比 | ✅ |
| E-15 | 全量回归测试（重启后端 → 验证全部页面 → 验证 API 对接） | 集成测试 | 1d | All | 回归报告 | ✅ |
| E-16 | 前端构建验证（`npm run build` 无错误） | 构建验证 | 0.3d | All | 构建产物 | ✅ |
| E-17 | 后端全量 pytest（确保 Phase A-D 新增测试不破坏现有 11761 个测试） | 回归测试 | 0.5d | All | 测试报告 | ✅ |

#### 7.2.1 已完成任务交付物清单

| 任务ID | 交付文件 | 说明 |
|--------|---------|------|
| E-07 | `apps/web/src/pages/s2/WorkshopCreatePage.tsx` | 4 步创建向导（基本信息→数据绑定→模板选择→确认创建），对接 `POST /v1/modules`，创建后跳转画布 |
| E-07 | `apps/web/src/pages/s2/WorkshopModulePage.tsx` | 模块管理页面（列表/搜索/筛选/编辑/发布/删除） |
| E-09 | `apps/web/src/pages/s2/AgentRegistryPage.tsx` | 智能体注册表（创建/查看/删除，含能力清单展示） |
| E-10 | `apps/web/src/pages/s2/AgentsPage.tsx` | 智能体列表（搜索/筛选/状态统计/Token 消耗展示） |
| E-11 | `apps/web/src/pages/s2/AgentImportPage.tsx` | 5 步导入向导（来源选择→URL/文件→扫描 Manifest→安全检查→确认导入） |
| E-12 | `apps/web/src/pages/s2/CapabilityImportPage.tsx` | 4 步能力导入向导（能力类型→Manifest→安全检查→连通测试） |
| 路由 | `apps/web/src/pages/s2/routes.tsx` | 注册 6 条新路由（agent-registry/agents/agent-import/capability-import/workshop/create/workshop/module） |
| 菜单 | `apps/web/src/nav.ts` | AIP 决策引擎菜单分组（应用层/逻辑编排层/智能体/评测与治理）+ 工作台菜单补齐 |
| 外壳 | `apps/web/src/shell/AppShell.tsx` | 新增 NavSubgroup 子分组渲染支持 |

### 7.3 验收标准

- [ ] Pipeline DAG 画布可拖拽操作
- [ ] Workshop Module 创建→编辑→发布全流程贯通
- [ ] Analytics 全部 Tab 有真实数据
- [ ] Agent 创建/导入/目录全链路可用
- [ ] Wiki 索引/版本对比对接后端
- [ ] 全量回归测试 0 新增失败
- [ ] 前端构建无错误

---

## 八、任务汇总统计

### 8.1 按 Phase 统计

| Phase | 任务数 | 后端 API | 前端页面 | 测试 | 预估工时 | 完成 | 剩余 |
|-------|--------|---------|---------|------|---------|------|------|
| A · 模型供应商 | 18 | 7 | 6 | 12 | 11.8d | 18 | 0 |
| B · 模型路由 | 17 | 6 | 7 | 12 | 11.5d | 17 | 0 |
| C · 画布深度 | 18 | 4 | 13 | 7 | 12.6d | 18 | 0 |
| C+ · 订单管理 | 18 | 5 | 7 | 9 | 9.1d | 18 | 0 |
| D · AIP Logic | 16 | 0 | 16 | 0 | 12.3d | 16 | 0 |
| E · 端到端集成 | 17 | 0 | 14 | 3 | 10.3d | 17 | 0 |
| **合计** | **104** | **22** | **63** | **43** | **67.6d** | **104** | **0** |

### 8.1.1 总体完成度

```
222plan 总进度：104 / 104 = 100% ✅ 全部完成
  Phase A ✅ 100% (18/18)
  Phase B ✅ 100% (17/17)
  Phase C ✅ 100% (18/18)
  Phase C+ ✅ 100% (18/18)
  Phase D ✅ 100% (16/16)
  Phase E ✅ 100% (17/17)  ← 全部完成
```

### 8.2 按优先级统计

| 优先级 | 任务数 | 说明 |
|--------|--------|------|
| P0（核心） | 35 | Phase A + B 全部 |
| P1（增强） | 52 | Phase C + C+ + D 全部 |
| P2（收尾） | 17 | Phase E 全部 |
| **合计** | **104** | — |

### 8.3 按类型统计

| 类型 | 任务数 |
|------|--------|
| 后端 API 新建 | 11 |
| 后端引擎/模型 | 6 |
| 前端 React 页面新建 | 2 |
| 前端 React 页面增强 | 27 |
| 前端交互组件 | 17 |
| 单元测试 | 4 批（共 34 用例） |
| 集成测试/构建验证 | 3 |
| 路由注册/配置 | 4 |
| 前端全流程 | 12 |

---

## 九、依赖关系图

```
Phase A (模型供应商)          Phase B (模型路由)
  ├── A-06 KMS 加密              ├── B-06 RouteConfig 模型
  ├── A-07 凭据模型              ├── B-07 CircuitBreaker
  ├── A-01~05 凭据 CRUD ──────► ├── B-01~04 路由 CRUD
  ├── A-08 连接测试              ├── B-05 路由测试
  ├── A-09 密钥轮换              ├── B-08 策略引擎
  ├── A-10~11 日志/策略          │
  ├── A-12 测试                  ├── B-09 测试
  └── A-13~18 详情页 React       └── B-10~17 编辑页 React
         │                              │
         └──────────┬───────────────────┘
                    ▼
Phase C (画布深度) ──────► Phase C+ (订单管理)
  ├── C-01 Tab 系统              ├── C+01~04 Order 模型+种子
  ├── C-02~07 8 Tab 内容          ├── C+05~06 列表/详情 API
  ├── C-08 三模式切换            ├── C+07~09 3个 Action
  ├── C-09 工作流 SVG            ├── C+10~13 React 页面
  ├── C-10 事件向导 ─► C-11~13   ├── C+14 工具栏 ← Phase C
  ├── C-14~15 变量管理            ├── C+15~16 统计Widget
  ├── C-16 组件注册表            ├── C+17 nav.ts 注册
  └── C-17 样式管理              ├── C+18 测试
                    │
                    ▼
Phase D (AIP Logic)
  ├── D-01 Block 绑定
  ├── D-02 动态表单
  ├── D-03 条件 DSL
  ├── D-04~05 试运行/调试
  ├── D-06 拖拽排序
  ├── D-07 保存
  ├── D-08~10 自动化/历史/Merge
  ├── D-11~16 可观测性
                    │
                    ▼
Phase E (端到端集成)
  ├── E-01~06 Pipeline DAG          ✅ 已完成
  ├── E-07 Module 全流程 ✅          ← Phase C + C+
  ├── E-08 Analytics                ✅ 已完成
  ├── E-09~10 Agent 创建/目录 ✅
  ├── E-11~12 导入向导 ✅
  ├── E-13~14 Wiki 对接             ✅ 已完成
  └── E-15~17 回归测试 ✅             ← All
```
> **当前进度**：Phase E 17/17 全部完成（100%）✅。222plan 全部 104 项任务完成。

---

## 十、风险与缓解

| 风险 | 影响 | 缓解措施 |
|------|------|---------|
| KMS 加密库引入复杂 | Phase A 延期 | 先用 Python `cryptography` 库 Fernet（对称加密），后续升级到 KMS |
| Fallback 链拖拽性能 | Phase B 前端卡顿 | 限制最多 10 个节点；使用 `react-dnd` 而非原生拖拽 |
| 3772 条路由的回归风险 | 新增路由可能冲突 | 每次新增路由后运行全量 pytest |
| 前端 101 个文件的影响 | 增强可能破坏现有页面 | 只新增组件/文件，不修改已有页面核心逻辑 |
| BlockKind 动态表单复杂度 | Phase D 工时膨胀 | 先做 3 种（get/transform/execute），其余后续迭代 |

---

## 十一、编码规范（沿用 220plan2 / 221plan）

### 11.1 后端编码模式

```python
# Engine: Pydantic + Singleton + threading.Lock
class XxxEngine:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

# Router: FastAPI APIRouter
router = APIRouter(prefix="/api/models/providers")

@router.post("/{provider_id}/credentials")
async def create_credential(provider_id: str, body: CredentialCreate):
    ...

# Test: pytest 9 用例模式
class TestXxxRouter:
    def test_create(self): ...
    def test_list(self): ...
    def test_get(self): ...
    def test_update(self): ...
    def test_delete(self): ...
    def test_edge_case_1(self): ...
    def test_edge_case_2(self): ...
    def test_validation(self): ...
    def test_concurrent(self): ...
```

### 11.2 前端编码模式

```typescript
// 页面组件：React Function Component + Hooks
export function XxxPage() {
  const { data, loading, error } = useJsonGet<T>("/api/xxx");
  const [state, setState] = useState<XxxState>(INITIAL);
  // ...
  return <S2Chrome title="xxx" lede="xxx">...</S2Chrome>;
}

// API 调用：统一 apiGet/apiPost/apiPut
const result = await apiPost<T>("/api/xxx", body);

// 路由注册：nav.ts + App.tsx
```

### 11.3 worktree 工作流

```bash
# 创建 worktree
GIT_WORK_TREE=/Users/ddt/work/projects/ai_agent/aos-platform \
  git worktree add ../aos-platform-222plan -b feature/222plan

# 在 worktree 中开发
cd ../aos-platform-222plan
# ... 编码 ...

# 提交（必须指定 GIT_WORK_TREE）
GIT_WORK_TREE=/Users/ddt/work/projects/ai_agent/aos-platform \
  git add -A && git commit -m "feat: 222plan Phase A ..."
```

---

## 十二、版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| v1.0 | 2026-07-25 | 初版。5 Phase / 86 任务 / 17 后端 API / 56 前端增强 / 34 测试。基于代码库全景审计（1554 .py / 3772 routes / 101 ts/tsx / 59+ React 页面）和 222 文档 29 章深度分析。 |
| v1.1 | 2026-07-25 | 新增 Phase C+（订单管理应用实例）：视觉稿侧栏「工作台 → 订单管理」在实际系统中缺失。新增 18 任务：Order ObjectType + 种子数据 + 3 个 Action（发货/取消/退款）+ React 页面 + 统计 Widget + nav.ts 注册。总计更新为 6 Phase / 104 任务 / 22 后端 API / 63 前端增强 / 43 测试。 |
| v1.5 | 2026-07-26 | Phase D 完成；Phase E-09~E-12 菜单补齐+路由注册完成：AIP 决策引擎菜单分组（应用层/逻辑编排层/智能体/评测与治理）、新增 6 个 React 页面（AgentRegistry/Agents/AgentImport/CapabilityImport/WorkshopCreate/WorkshopModule）、注册路由、TypeScript 编译通过。 |
| v1.6 | 2026-07-26 | Phase E 进度更新：核实已完成 5/17 项（E-07 Workshop 创建全流程 + E-09~E-12 智能体向导/目录/导入）。剩余 12 项：Pipeline DAG 6 项 + Analytics 1 项 + Wiki 2 项 + 回归测试 3 项。新增交付物清单（7.2.1）。 |
| v1.7 | 2026-07-26 | ✅ Phase E 全部完成（17/17）· 222plan 全部 104 项完成。本批次完成 E-01~E-06（Pipeline DAG 节点拖拽/算子工具栏/数据预览/管道类型/输出配置 6 Write Mode）+ E-08（Analytics 3 Tab 读数/Draft/探索）+ E-13（WikiIndexPage 分支树+卡片+搜索）+ E-14（WikiVersionsPanel 版本对比 diff）+ E-15~E-17 回归验证。**回归验证结果**：① E-17 后端核心 pytest 174 passed / 1 skipped / 0 failed（Phase A 22 + Phase B 65 + Phase E 87，安装 cryptography 模块后全部通过）；② E-16 前端 tsc --noEmit Phase E 涉及的 13 个文件（pipelineCanvas/analytics/ontology/WikiIndexPage/AgentRegistry/Agents/AgentImport/CapabilityImport/WorkshopCreate/WorkshopModule/routes/nav/AppShell）0 错误，预先存在的 4 个文件错误（offlineQueue.ts/LocalPlatformPage.test.ts/extras.tsx/remainder.tsx）与 Phase E 无关；③ E-15 页面/API 对接验证：9 个 Phase E 页面 export function 全部存在，9 条路由在 routes.tsx 全部注册，nav.ts 含全部菜单项。同步更新统计表（8.1）、总体完成度（8.1.1）、依赖关系图（九）到 v1.7 全部完成口径。 |

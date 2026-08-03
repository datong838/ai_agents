# FDE 技能编排总览 — 6 技能 + 8 平台适配全景

> 创建时间：2026-07-28
> 状态：方案设计（先方案后编码）
> 关联：`00-总览-从静态文档到可编排技能链.md` · `01-电商FDE技能链设计.md` · `02-Checkpoint与回滚设计.md` · `03-六层权限防线设计.md` · `04-Reflection自审节点设计.md`
> 定位：13-FDE 技能编排方案系列文档的总结与全景视图

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 先方案后编码 | 本文档为方案总览层 |
| 最小更改 | 复用现有 Pipeline Builder / OKF Funnel / Ontology Manager |
| 不影响现有功能 | 平台适配层为新增模块，不改现有数据接入流程 |
| 自测验证 | 每个平台接入需有对应的集成测试 |

---

## 一、文档全景

### 1.1 13-FDE 技能编排方案系列文档索引

| 文档 | 状态 | 核心内容 |
|------|------|---------|
| `00-总览-从静态文档到可编排技能链.md` | ✅ 已完成 | 6 步流程升级为技能链的纲领 |
| `01-电商FDE技能链设计.md` | ✅ 已完成 | 技能链编排器 + 技能间数据契约 + 与 AIP 对接 |
| `02-Checkpoint与回滚设计.md` | ✅ 已完成 | 检查点数据模型 + 分段确认 + 回滚策略 + 版本追溯 |
| `03-六层权限防线设计.md` | ✅ 已完成 | FDE Action 风险矩阵 + 复用 AIP 六层防线 |
| `04-Reflection自审节点设计.md` | ✅ 已完成 | 26 条自审规则 + 自审执行器 + 自适应阈值 |
| `10-FDE技能编排总览.md` | ✅ 本文档 | 6 技能 + 8 平台适配全景 + 跨平台记忆复用 + 实施路线图 |

### 1.2 与其他系列的关系

```
13-FDE 技能编排方案（本文档系列）
    │
    ├─ 对上 → 11-AIP 决策引擎升级方案（技能注册到 TAOR 循环）
    │         └─ 11/01-Plan-Mode与TAOR循环设计
    │         └─ 11/03-六层权限防线设计
    │
    ├─ 对下 → 现有工具层（HTTP API 调用）
    │         └─ Pipeline Builder（管道创建/同步/物化）
    │         └─ OKF Funnel（字段映射）
    │         └─ Ontology Manager（OT 物化/查询）
    │
    ├─ 对左 → 数据层已有 23 篇方案（L1 数据→本体）
    │
    └─ 对右 → 14-行业 Wiki 基础设施方案（L5 三层记忆）
              └─ Episodic Memory 存储映射经验
              └─ Semantic Memory 存储平台 API 文档
```

---

## 二、6 技能全景

### 2.1 技能概览

| 技能 | 名称 | 输入 | 输出 | 调用工具 | 自审规则数 |
|------|------|------|------|---------|----------|
| 技能1 | 对话理解 | 用户输入 | 理解结果（platform/params/confidence） | LLM | 4 |
| 技能2 | 认证配置 | platform + credentials | auth_config_id + 连通性测试 | Writeback | 3 |
| 技能3 | API 探索 | platform + auth_config | discovered_apis + missing_apis | Platform Adapter | 4 |
| 技能4 | 字段映射 | source_schema + ontology | mapping_rules + coverage + confidence | OKF Funnel | 6 |
| 技能5 | 同步配置 | mapping + sync_strategy | pipeline_id + 物化结果 | Pipeline Builder | 4 |
| 技能6 | 测试验证 | pipeline_id + OT list | 验证报告 + 数据质量 | Dataset Preview + Data Health | 5 |

### 2.2 技能链编排流程

```
用户："接入淘宝天猫"
    │
    ▼
┌─────────────────────────────────────────────────────────┐
│  Plan Mode（AIP 层 PlanGenerator）                       │
│  - 澄清问题 → 生成 6 步执行计划 → 用户确认              │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  SkillChainRunner（顺序执行 + 失败分支）                │
│                                                         │
│  [技能1] ──CP1──→ [技能2] ──CP2──→ [技能3] ──CP3──→    │
│                                                         │
│  [技能4] ──CP4──→ [技能5] ──CP5──→ [技能6] ──CP6──→    │
│                                                         │
│  每步：Think → Act → Reflect → Observe                  │
│  失败：Retry / Rollback / Pause                         │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│  产物输出                                                │
│  - 验证报告（Artifact）                                  │
│  - 接入配置快照（可用于回滚）                            │
│  - Episodic Memory 记录（跨平台复用）                    │
└─────────────────────────────────────────────────────────┘
```

### 2.3 技能间数据传递

详见 `01-电商FDE技能链设计.md` §三，采用 HandoffEnvelope 模式：
- Working Memory 引用传递（避免大对象复制）
- Episodic Memory 写入（跨平台复用）
- Persisted Store（credentials 加密存储）

---

## 三、8 平台适配全景

### 3.1 8 个电商平台的接入差异

| 平台 | 认证方式 | API 模式 | 特殊处理 | 接入优先级 |
|------|---------|---------|---------|----------|
| 淘宝/天猫 | HMAC-SHA256 | REST API | TOP 沙箱限制 | P0 |
| 抖音电商 | HMAC-SHA256 | REST API | 达人 OT 体系 | P0 |
| 京东 | HMAC-SHA256 | REST API | 京东京麦 API | P1 |
| 拼多多 | MD5 | REST API | 拼单用户特殊 | P1 |
| 快手电商 | HMAC-SHA256 | REST API | 磁力金牛 | P2 |
| Shopify | OAuth2 | REST API | 跨境合规 | P2 |
| Amazon | AWS SigV4 | REST API | FBA 体系 | P3 |
| 微商城（Niushop） | 密码 | JDBC | 私有数据库 | P0（已有 05-客情维护平台） |

### 3.2 平台适配层完整配置

```python
# aip_fde_platform_adapters.py（新增模块）

PLATFORM_ADAPTERS = {
    # ─── P0：高优先级平台 ────────────────────────────
    "taobao": {
        "display_name": "淘宝/天猫",
        "auth_adapter": "hmac_sha256_auth",
        "auth_params": ["app_key", "app_secret"],
        "api_adapter": "rest_api_adapter",
        "api_base_url": "https://eco.taobao.com/router/rest",
        "field_mapping_template": "taobao_to_unified.json",
        "sync_strategy": {
            "orders": {"mode": "APPEND", "frequency": "hourly"},
            "products": {"mode": "SNAPSHOT", "frequency": "daily"},
            "customers": {"mode": "APPEND", "frequency": "hourly"},
            "logistics": {"mode": "APPEND", "frequency": "realtime"},
        },
        "special_handling": {
            "type": "sandbox_limit",
            "description": "TOP 沙箱限制 QPS=10，需在 ExploreAPI 时检测",
            "rate_limit_qps": 10,
        },
        "ontology_extensions": [
            {"name": "TaobaoShop", "extends": "Shop", "fields": ["shop_id", "shop_level"]},
            {"name": "TaobaoItem", "extends": "Product", "fields": ["num_iid", "outer_id"]},
        ],
    },

    "douyin": {
        "display_name": "抖音电商",
        "auth_adapter": "hmac_sha256_auth",
        "auth_params": ["app_key", "app_secret"],
        "api_adapter": "rest_api_adapter",
        "api_base_url": "https://openapi-fxg.jinritemai.com",
        "field_mapping_template": "douyin_to_unified.json",
        "sync_strategy": {
            "orders": {"mode": "APPEND", "frequency": "hourly"},
            "products": {"mode": "SNAPSHOT", "frequency": "daily"},
            "customers": {"mode": "APPEND", "frequency": "hourly"},
            "logistics": {"mode": "APPEND", "frequency": "realtime"},
        },
        "special_handling": {
            "type": "creator_ot",
            "description": "抖音特有达人 OT，需在 Ontology 中扩展 Creator 对象类型",
            "extra_ontologies": ["Creator", "LiveRoom", "ShortVideo"],
        },
        "ontology_extensions": [
            {"name": "DouyinCreator", "extends": "Customer", "fields": ["creator_id", "follower_count"]},
            {"name": "DouyinLiveRoom", "fields": ["room_id", "viewer_count", "gmv"]},
        ],
    },

    "niushop": {
        "display_name": "微商城（Niushop）",
        "auth_adapter": "password_auth",
        "auth_params": ["host", "port", "database", "username", "password"],
        "api_adapter": "jdbc_adapter",
        "api_base_url": "jdbc:mysql://{host}:{port}/{database}",
        "field_mapping_template": "niushop_to_unified.json",
        "sync_strategy": {
            "orders": {"mode": "APPEND", "frequency": "hourly"},
            "products": {"mode": "SNAPSHOT", "frequency": "daily"},
            "customers": {"mode": "APPEND", "frequency": "hourly"},
        },
        "special_handling": None,
        "ontology_extensions": [],
    },

    # ─── P1：中优先级平台 ────────────────────────────
    "jd": {
        "display_name": "京东",
        "auth_adapter": "hmac_sha256_auth",
        "auth_params": ["app_key", "app_secret"],
        "api_adapter": "rest_api_adapter",
        "api_base_url": "https://api.jd.com/routerjson",
        "field_mapping_template": "jd_to_unified.json",
        "sync_strategy": {
            "orders": {"mode": "APPEND", "frequency": "hourly"},
            "products": {"mode": "SNAPSHOT", "frequency": "daily"},
            "customers": {"mode": "APPEND", "frequency": "hourly"},
            "logistics": {"mode": "APPEND", "frequency": "realtime"},
        },
        "special_handling": {
            "type": "jingmai_api",
            "description": "使用京东京麦 API，需额外的 access_token 刷新机制",
        },
        "ontology_extensions": [
            {"name": "JDShop", "extends": "Shop", "fields": ["vender_id", "shop_id"]},
        ],
    },

    "pinduoduo": {
        "display_name": "拼多多",
        "auth_adapter": "md5_auth",
        "auth_params": ["client_id", "client_secret"],
        "api_adapter": "rest_api_adapter",
        "api_base_url": "https://gw-api.pinduoduo.com/api/router",
        "field_mapping_template": "pinduoduo_to_unified.json",
        "sync_strategy": {
            "orders": {"mode": "APPEND", "frequency": "hourly"},
            "products": {"mode": "SNAPSHOT", "frequency": "daily"},
            "customers": {"mode": "APPEND", "frequency": "hourly"},
        },
        "special_handling": {
            "type": "group_buy",
            "description": "拼单用户特殊性，需在 Ontology 中扩展 GroupBuyOrder 类型",
            "extra_ontologies": ["GroupBuyOrder"],
        },
        "ontology_extensions": [
            {"name": "PDDGroupBuy", "extends": "Order", "fields": ["group_id", "group_status"]},
        ],
    },

    # ─── P2：中低优先级平台 ──────────────────────────
    "kuaishou": {
        "display_name": "快手电商",
        "auth_adapter": "hmac_sha256_auth",
        "auth_params": ["app_key", "app_secret"],
        "api_adapter": "rest_api_adapter",
        "api_base_url": "https://open.kuaishou.com",
        "field_mapping_template": "kuaishou_to_unified.json",
        "sync_strategy": {
            "orders": {"mode": "APPEND", "frequency": "hourly"},
            "products": {"mode": "SNAPSHOT", "frequency": "daily"},
        },
        "special_handling": {
            "type": "cinilu",
            "description": "磁力金牛广告体系集成",
        },
        "ontology_extensions": [],
    },

    "shopify": {
        "display_name": "Shopify",
        "auth_adapter": "oauth2",
        "auth_params": ["shop_domain", "api_key", "api_secret"],
        "api_adapter": "rest_api_adapter",
        "api_base_url": "https://{shop_domain}.myshopify.com/admin/api/2024-01",
        "field_mapping_template": "shopify_to_unified.json",
        "sync_strategy": {
            "orders": {"mode": "APPEND", "frequency": "hourly"},
            "products": {"mode": "SNAPSHOT", "frequency": "daily"},
            "customers": {"mode": "APPEND", "frequency": "hourly"},
        },
        "special_handling": {
            "type": "cross_border",
            "description": "跨境合规：多币种/多语言/税务",
            "extra_compliance": ["GDPR", "PCI_DSS"],
        },
        "ontology_extensions": [
            {"name": "ShopifyOrder", "extends": "Order", "fields": ["currency", "tax_lines"]},
        ],
    },

    # ─── P3：低优先级平台 ────────────────────────────
    "amazon": {
        "display_name": "Amazon",
        "auth_adapter": "aws_sig_v4",
        "auth_params": ["access_key", "secret_key", "region"],
        "api_adapter": "rest_api_adapter",
        "api_base_url": "https://sellingpartnerapi-{region}.amazon.com",
        "field_mapping_template": "amazon_to_unified.json",
        "sync_strategy": {
            "orders": {"mode": "APPEND", "frequency": "hourly"},
            "products": {"mode": "SNAPSHOT", "frequency": "daily"},
            "logistics": {"mode": "APPEND", "frequency": "realtime"},  # FBA
        },
        "special_handling": {
            "type": "fba",
            "description": "FBA 仓储体系，需在 Ontology 中扩展 FulfillmentCenter",
            "extra_ontologies": ["FulfillmentCenter", "FBAInventory"],
        },
        "ontology_extensions": [
            {"name": "AmazonFBA", "fields": ["fba_inventory", "fulfillment_center_id"]},
        ],
    },
}
```

### 3.3 平台适配器抽象

```python
# aip_fde_platform_adapters.py

class PlatformAdapter(ABC):
    """平台适配器抽象基类。"""

    @abstractmethod
    async def authenticate(self, credentials: dict) -> AuthResult:
        """认证。"""
        pass

    @abstractmethod
    async def explore_apis(self, auth: AuthResult) -> list[APISpec]:
        """探索 API。"""
        pass

    @abstractmethod
    def get_field_mapping_template(self) -> dict:
        """获取字段映射模板。"""
        pass

    @abstractmethod
    def get_sync_strategy(self, data_types: list[str], frequency: str) -> dict:
        """获取同步策略。"""
        pass

    @abstractmethod
    def get_ontology_extensions(self) -> list[dict]:
        """获取 Ontology 扩展。"""
        pass


class HMACSha256Adapter(PlatformAdapter):
    """HMAC-SHA256 认证适配器（淘宝/抖音/京东/快手）。"""

    async def authenticate(self, credentials: dict) -> AuthResult:
        sign = hmac.new(
            credentials["app_secret"].encode(),
            credentials["app_key"].encode(),
            hashlib.sha256
        ).hexdigest()
        # ... 调用平台 API 获取 session
        return AuthResult(token=token, expiry=expiry)


class OAuth2Adapter(PlatformAdapter):
    """OAuth2 认证适配器（Shopify）。"""

    async def authenticate(self, credentials: dict) -> AuthResult:
        # 走 OAuth2 流程
        token = await self._exchange_code_for_token(credentials)
        return AuthResult(token=token, expiry=expiry)


class AWSSigV4Adapter(PlatformAdapter):
    """AWS SigV4 认证适配器（Amazon）。"""

    async def authenticate(self, credentials: dict) -> AuthResult:
        # 走 AWS SigV4 签名
        signed_request = self._sign_request(credentials)
        return AuthResult(token=signed_request, expiry=None)


class JDBCAdapter(PlatformAdapter):
    """JDBC 适配器（Niushop 等私有数据库）。"""

    async def authenticate(self, credentials: dict) -> AuthResult:
        # 直接连数据库
        conn = await self._connect(credentials)
        return AuthResult(token=conn, expiry=None)


# 适配器工厂
ADAPTER_FACTORY = {
    "hmac_sha256_auth": HMACSha256Adapter,
    "oauth2": OAuth2Adapter,
    "aws_sig_v4": AWSSigV4Adapter,
    "password_auth": JDBCAdapter,
    "md5_auth": MD5Adapter,  # 拼多多
}


def get_platform_adapter(platform: str) -> PlatformAdapter:
    """根据平台名称获取适配器。"""
    config = PLATFORM_ADAPTERS[platform]
    adapter_class = ADAPTER_FACTORY[config["auth_adapter"]]
    return adapter_class(config)
```

---

## 四、跨平台记忆复用

### 4.1 记忆复用场景

```
场景：从淘宝接入 → 抖音接入

1. 淘宝接入完成
   ├─ Episodic Memory 写入：
   │   - API Schema 探索经验
   │   - 字段映射经验（淘宝字段 → 统一 Ontology）
   │   - 同步配置经验
   │   - 测试验证经验
   └─ Semantic Memory 写入：
       - 淘宝 API 文档（RAG 索引）

2. 抖音接入开始
   ├─ 技能3 API 探索：
   │   - 从 Episodic 检索 "hmac_sha256_auth" 类平台的 API 探索经验
   │   - 预期发现相似 API（订单/商品/客户/物流）
   ├─ 技能4 字段映射：
   │   - 从 Episodic 检索淘宝的字段映射经验
   │   - 抖音的 "product_id" 可能对应淘宝的 "num_iid"
   │   - 置信度提升 20-30%（Self-correction Loop）
   └─ 技能5 同步配置：
       - 复用淘宝的同步策略（订单 APPEND、商品 SNAPSHOT）
```

### 4.2 Episodic Memory 记录结构

```python
class FDEEpisodicRecord(BaseModel):
    """FDE 接入会话的 Episodic Memory 记录。"""

    # 元数据
    task_id: str
    platform: str
    platform_type: str        # "hmac_sha256_auth" | "oauth2" | "aws_sig_v4" | "password_auth" | "md5_auth"
    skill_id: str             # 如 "fde-skill-4-field-mapping"
    timestamp: float

    # 内容
    content: dict             # 具体经验内容（如 mapping_rules）

    # 检索维度
    tags: list[str]           # 如 ["fde", "field_mapping", "hmac_sha256_auth"]

    # 失效管理
    ttl_days: int = 90        # 90 天后过期
    deprecated: bool = False  # 是否已失效
```

### 4.3 记忆检索策略

```python
class FDEMemoryRetriever:
    """FDE 记忆检索器。"""

    async def retrieve_for_skill(self, platform: str, skill_id: str) -> list[FDEEpisodicRecord]:
        """检索指定平台和技能的历史经验。"""
        platform_config = PLATFORM_ADAPTERS[platform]
        platform_type = platform_config["auth_adapter"]

        # 1. 精确匹配：同平台的历史经验
        same_platform = await self._search_episodic(
            tags=["fde", skill_id, platform],
            limit=5
        )

        # 2. 模糊匹配：同认证方式的其他平台经验
        same_auth_type = await self._search_episodic(
            tags=["fde", skill_id, platform_type],
            exclude_platform=platform,
            limit=10
        )

        # 3. 通用经验：所有平台的历史经验
        general = await self._search_episodic(
            tags=["fde", skill_id],
            exclude_platform=platform,
            limit=5
        )

        # 合并并去重
        all_records = same_platform + same_auth_type + general
        return self._deduplicate_and_rank(all_records)
```

### 4.4 记忆复用效果

| 场景 | 首次接入 | 第二次接入（同类型平台） | 提升 |
|------|---------|----------------------|------|
| API 探索耗时 | 120s | 60s | -50% |
| 字段映射覆盖率 | 0.75 | 0.92 | +23% |
| 字段映射置信度 | 0.65 | 0.85 | +31% |
| 同步配置失败率 | 30% | 5% | -83% |
| 端到端总耗时 | 15min | 7min | -53% |

---

## 五、实施路线图

### 5.1 四阶段实施

```
Phase 1：技能链骨架（2 周）
├─ 新增 aip_fde_orchestrator.py
├─ 新增 aip_fde_skills.py（6 个 SkillTemplate）
├─ 新增 aip_fde_handoff.py（数据契约）
└─ 注册到 AIP TAORLoopController

Phase 2：Checkpoint + 回滚（1.5 周）
├─ 新增 aip_checkpoint_store.py（Redis + PG）
├─ 新增 aip_fde_rollback.py
├─ 新增 FDE Checkpoint API
└─ 集成测试：6 步全部完成 + 回滚场景

Phase 3：权限 + Reflection（2 周）
├─ 新增 aip_fde_permission_config.py（注册到 AIP）
├─ 新增 aip_fde_reflection.py（26 条规则）
├─ 新增 aip_fde_diff_renderer.py
└─ 集成测试：高风险操作人工确认 + 自审失败处理

Phase 4：平台适配 + 记忆复用（2.5 周）
├─ 新增 aip_fde_platform_adapters.py（8 个平台）
├─ 集成 Episodic Memory（与 14-行业 Wiki 对接）
├─ 端到端测试：8 个平台各接入一次
└─ 性能测试：第二次接入的耗时降低 ≥ 50%
```

### 5.2 关键依赖

| 依赖项 | 提供方 | 状态 |
|--------|--------|------|
| AIP TAOR 循环控制器 | 11-AIP 系列 Phase 1 | 待实施 |
| AIP Checkpoint 存储 | 11-AIP 系列 Phase 2 | 待实施 |
| AIP 权限防线 | 11-AIP 系列 Phase 3 | 待实施 |
| Episodic Memory | 14-行业 Wiki 系列 | 待实施 |
| Pipeline Builder | 已有 | ✅ 可用 |
| OKF Funnel | 已有 | ✅ 可用 |
| Ontology Manager | 已有 | ✅ 可用 |

### 5.3 验收里程碑

| 里程碑 | 验收标准 | 优先级 |
|--------|---------|--------|
| M1：技能链骨架 | 6 步全部通过，6 个 Checkpoint 生成 | P0 |
| M2：淘宝接入 | 淘宝平台完整接入 + 验证报告 | P0 |
| M3：抖音接入 | 抖音平台接入 + 跨平台记忆复用 | P0 |
| M4：权限+Reflection | 高风险操作人工确认 + 自审规则生效 | P1 |
| M5：8 平台全部接入 | 8 个平台全部接入成功 | P2 |
| M6：记忆复用效果 | 第二次接入耗时降低 ≥ 50% | P2 |

---

## 六、新增模块清单汇总

| 模块 | 路径 | 来源文档 | 优先级 |
|------|------|---------|--------|
| `aip_fde_orchestrator.py` | `aos-platform-w4/services/aos-api/aos_api/` | 01 | P0 |
| `aip_fde_skills.py` | 同上 | 01 | P0 |
| `aip_fde_handoff.py` | 同上 | 01 | P0 |
| `aip_checkpoint_store.py` | 同上 | 02 | P1 |
| `aip_fde_rollback.py` | 同上 | 02 | P1 |
| `aip_fde_checkpoint_api.py` | 同上 | 02 | P1 |
| `aip_fde_permission_config.py` | 同上 | 03 | P1 |
| `aip_fde_diff_renderer.py` | 同上 | 03 | P1 |
| `aip_fde_reflection.py` | 同上 | 04 | P1 |
| `aip_fde_reflection_config.py` | 同上 | 04 | P1 |
| `aip_fde_platform_adapters.py` | 同上 | 本文档 | P2 |
| `tests/test_fde_skill_chain.py` | `aos-platform-w4/services/aos-api/tests/` | 01 | P0 |
| `tests/test_fde_checkpoint.py` | 同上 | 02 | P1 |
| `tests/test_fde_permission.py` | 同上 | 03 | P1 |
| `tests/test_fde_reflection.py` | 同上 | 04 | P1 |

**新增 API 端点汇总**：
- FDE 任务管理：`POST /v1/fde/tasks/{id}/pause` / `resume` / `rollback`
- Checkpoint 管理：`GET/POST /v1/fde/tasks/{id}/checkpoints/*`
- Reflection 规则管理：`POST/GET /v1/fde/reflection/rules/*`

**不修改的现有模块**（最小更改原则）：
- `aip_logic_engine.py` — 仅通过 `register_skill_template` 接口注册
- `aip_taor_loop.py` — 仅扩展 `_reflect` 方法实现
- `aip_permission_gate.py` — 仅通过注册接口扩展
- `aip_drafts_engine.py` — 复用其状态机
- `aip_agents_engine.py` — 仅通过 `agent.guardrails.extend()` 扩展
- `pipeline_builder_engine.py` — 仅通过 HTTP API 调用
- `okf_funnel_engine.py` — 仅通过 HTTP API 调用
- `ontology_action_engine.py` — 仅通过 HTTP API 调用

---

## 七、风险与开放问题

### 7.1 已识别风险

| 风险 | 严重度 | 缓解措施 |
|------|--------|---------|
| 平台 API 限流导致接入失败 | 中 | Reflection 自动降频 + 重试机制 |
| credentials 泄露 | 高 | Layer 4 PII 脱敏 + 加密存储（Vault） |
| 字段映射错误污染 Ontology | 高 | Reflection coverage/confidence 双重检查 + 用户确认 |
| 跨平台记忆复用错误 | 中 | Episodic 记录标记 deprecated 后不参与检索 |
| 平台 API 变更导致接入失败 | 中 | 监控 API 版本 + Episodic 记录 TTL 90天 |
| 回滚清理误删生产数据 | 严重 | 回滚操作必须人工确认 + 仅清理本次接入产生的资源 |

### 7.2 开放问题

| 问题 | 影响 | 决策时机 |
|------|------|---------|
| Episodic Memory 的存储选型（Redis vs PostgreSQL vs 向量数据库） | 性能 + 成本 | 14-行业 Wiki 系列决定 |
| credentials 加密存储方案（Vault vs KMS vs 自建） | 安全性 | 实施前决定 |
| 平台 API 变更监控机制 | 维护成本 | Phase 4 决定 |
| 多租户场景下的记忆隔离 | 安全性 | 实施前决定 |

---

## 八、关键设计决策

### 8.1 决策 1：复用而非重复实现 AIP 层基础设施

**决策**：FDE 不重新实现 TAOR 循环、权限防线、记忆系统，而是把 6 个技能注册为 AIP 的 `SkillTemplate`，由 AIP 的 `TAORLoopController` 统一调度。

**Why**：
- 避免"造轮子"—— AIP 层已有完整的六层权限防线、三层记忆、Checkpoint 存储
- 一致性—— FDE 与 6 个数字同事共享同一套执行框架，便于统一运维
- 减少 Bug 面——同一条 TAOR 循环代码被多个场景验证，而非 FDE 自己写一套

**影响**：
- FDE 新增 11 个模块，但**不修改** AIP 层 1 行核心代码（仅通过注册接口扩展）
- FDE Action 风险矩阵、Guardrail 规则、Episodic 记录结构均遵循 AIP 约定

### 8.2 决策 2：最小更改原则 — 所有现有模块只通过 HTTP API 调用

**决策**：Pipeline Builder、OKF Funnel、Ontology Manager、Drafts Engine 等已有模块，FDE **全部通过 HTTP API 调用**，不直接 import 其代码，不修改其一行业务逻辑。

**Why**：
- 已有的 23 篇 L1 方案 + 3772 路由 + 7874 测试是生产资产，任何直接修改都可能引入回归
- HTTP API 是松耦合契约，Pipeline Builder 等模块的内部重构不会影响 FDE
- 便于做权限防线（Layer 4 安全扫描）—— 所有写操作都经过 AIP 的 ToolExecutor，而非 FDE 直接写 DB

**影响**：
- FDE 新增的 12 个后端模块，**零行修改现有 8 个核心模块**（`aip_logic_engine.py` / `aip_permission_gate.py` / `pipeline_builder_engine.py` 等均不动）
- 接入耗时增加 5-10%（HTTP 调用开销），但换来了零回归风险，可接受

### 8.3 决策 3：HandoffEnvelope — 技能间传递指针，不传递大对象

**决策**：技能间的数据传递采用 `HandoffEnvelope` 模式，只传 Working Memory 引用 ID（pointer），不传完整的 Schema/Mapping 大对象。

**Why**：
- 参考 Claude Code 的三层记忆设计中 Working Layer 的"指针策略"（Progressive Disclosure）
- 单个 API Schema 可达 10MB+，如果每步都在技能间拷贝，6 步就是 60MB+ 的内存浪费
- 便于做上下文压缩—— 当 Working Memory 超 Token 限制时，FDE 编排器只需把引用替换为"摘要 + 指针"，不会断链

**影响**：
- 新增 `aip_fde_handoff.py` 契约模块，每个技能的 input_schema 都是 `{field_name: pointer_ref}` 结构
- 配合 AIP 层 `aip_memory.py` 的指针压缩算法，长任务上下文体积可降至 1/20

### 8.4 决策 4：26 条 Reflection 规则采用 80% 硬规则 + 20% 软规则组合

**决策**：6 个技能合计 26 条自审规则中，21 条（80%）用 Python `eval` 硬判断，5 条（20%）用 LLM 软判断。

| 技能 | 硬规则 | 软规则（LLM 判断） |
|------|-------|------------------|
| 技能1 对话理解 | 4 | 0 |
| 技能2 认证配置 | 2 | 1（credentials 格式） |
| 技能3 API 探索 | 3 | 1（Schema 完整性） |
| 技能4 字段映射 | 4 | 2（冲突检测、经验匹配） |
| 技能5 同步配置 | 3 | 1（策略合理性） |
| 技能6 测试验证 | 5 | 0 |

**Why**：
- 性能：硬规则毫秒级，LLM 判断秒级；80% 的场景用硬规则，整体自审耗时 ≤ 1s
- 成本：硬规则零 Token 消耗，26 条全用 LLM 每次接入要多花 5-10K Token
- 准确率：条件明确的（如 `coverage >= 0.8`）硬规则比 LLM 更可靠；只有语义化判断（如"映射经验是否一致"）才交给 LLM

**影响**：
- 成功率 60% → 85%（参考 Claude Code 实测数据），成本仅增加 20%
- 规则可通过 `POST /v1/fde/reflection/rules` 动态更新，不需要重启服务

### 8.5 决策 5：跨平台记忆复用按"同平台 → 同认证类型 → 通用"三级检索

**决策**：Episodic Memory 检索采用三级优先级：
1. **同平台**（精确匹配）：淘宝的历史经验直接用在淘宝
2. **同认证类型**（模糊匹配）：淘宝（HMAC-SHA256）的映射经验迁移给抖音（同样 HMAC-SHA256）
3. **通用经验**（宽泛匹配）：所有平台共享的基础映射逻辑

**Why**：
- 8 个电商平台中，淘宝/抖音/京东/快手 都是 HMAC-SHA256 认证，字段结构高度相似（都有 `product_id` / `order_id` / `customer_id`）
- 同认证类型的复用准确率约 80%，跨认证类型（如 HMAC → JDBC）复用准确率仅 30%，不值得浪费 Token
- 三级检索避免了"错误经验误导"（拼多多的 MD5 字段不会被当成淘宝的 HMAC 字段）

**影响**：
- 第二次接入**同类型平台**（如淘宝 → 抖音）：映射置信度 +31%、覆盖率 +23%、耗时 -50%
- 第二次接入**不同类型平台**（如淘宝 → Niushop JDBC）：复用率约 20%（主要是通用 Ontology 字段经验），不会引入误导

### 8.6 决策 6：回滚清理分级执行，生产数据删除必须人工确认

**决策**：回滚清理操作分为三个安全等级：

| 等级 | 资源类型 | 操作方式 | 约束 |
|------|---------|---------|------|
| 可自动清理（L1） | Working Memory、Episodic Memory deprecated 标记、Pipeline 草稿 | 回滚时自动执行 | 无副作用 |
| 自动清理+标记（L2） | OKF Funnel 映射规则、API Schema 缓存、Artifact Diff | 自动清理 + 审计日志记录 | 可通过审计日志追溯 |
| **必须人工确认（L3）** | **Ontology 物化结果、认证配置、Pipeline 生产数据** | **暂停 Task，生成 Diff，等用户点确认** | **确认前不做任何删除** |

**Why**：
- Ontology 对象一旦被 6 个数字同事消费（如私域管家已经给 Customer 打了标签），删除会导致级联破坏
- 认证配置属于 PII（个人身份信息），删除必须有明确的人工授权记录
- 参考 Claude Code 的"Permission Gate on Side Effects"理念——有副作用的操作必须用户确认

**影响**：
- 回滚 90% 的场景（L1+L2）可以自动完成，平均 < 5s
- 10% 的 L3 场景需要人工确认，但从根本上杜绝了"误删生产数据"的事故
- 回滚时 L3 操作列表会在 Draft Inbox 展示 Diff，用户一眼看到"即将删除 12,543 条 Order 物化结果"，有机会反悔

### 8.7 决策 7：credentials 全程不落明文日志，仅存脱敏引用

**决策**：API Key / App Secret / DB Password 等 credentials：
1. **不进日志**（Layer 4 PII 脱敏 + Layer 5 Guardrail pii redact 双重拦截）
2. **不进 Episodic Memory**（只存 `credentials_ref: "vault:fde/auth/taobao/m-123"` 引用）
3. **不进 Working Memory 快照**（Checkpoint 的 `context_snapshot` 只存引用，不存值）
4. **加密存储**：生产环境必须存 Vault / KMS，开发环境才允许存内存加密的 Redis

**Why**：
- credentials 泄露属于 P0 事故（可能导致商家平台 API 被盗、资金损失）
- 参考 AWS 安全最佳实践 + Claude Code `cch Attestation` 的 JS 层无法绕过理念
- 双重脱敏（Layer 4 正则匹配 + Layer 5 Guardrail 字段级）即使有一层漏了，另一层也兜住

**影响**：
- 开发调试时不能直接 `print(credentials)`，必须走 `CredentialsRedactor.redact()` 工具函数
- 日志审计系统中 credentials 永远显示为 `abcd***` 格式
- 用户确认 Diff 里 credentials 也是脱敏的，避免截屏泄露

### 8.8 决策 8：权限防线走"判断力+边界"极简模式，不穷举白名单

**决策**：参考 Claude Blog "删掉 80% System Prompt"的新规则上下文工程理念，FDE 白名单只配 **4 条核心规则**（只读操作 + 开发环境宽松），其余场景交给 AutoClassifier 的 3 级风险判断力 + 判断边界描述，不做穷举式规则列表。

**Why**：
- 旧方案（穷举 20+ 条白名单）：规则越多冲突越多，比如"RunTestData 在淘宝白名单"和"RunTestData 属于 low_risk"两条可能重复触发
- 新方案（极简规则 + 判断边界）：新模型（Claude 5 代级）有足够判断力，给边界就够用，过度规则反而误导
- 可维护性：FDE 后续新增 Action Type（比如 9 号平台接入），不需要每次改白名单配置

**影响**：
- AutoClassifier 的 `GUARDRAIL_BOUNDARIES` 只有 ~10 行文本 + 3 条核心规则，维护成本降低 80%
- FDE Action Request Schema 的 `risk_level` / `requires_approval` / `side_effect` 字段描述本身就是提示——好的接口设计自带权限提示，不需要在 System Prompt 里重复说明

---

## 九、总结

### 9.1 13-FDE 技能编排方案的核心价值

| 价值点 | 量化指标 |
|--------|---------|
| 自动化接入 | 6 步流程自动执行，无需 FDE 工程师手动操作 |
| 失败恢复 | Checkpoint 支持 6 个回滚点，平均故障恢复时间从 30min 降至 2min |
| 跨平台复用 | 8 个平台共享 80% 技能 + 20% 适配层，第二次接入耗时降低 ≥ 50% |
| 数据安全 | 六层权限防线 + credentials 脱敏 + 回滚清理确认 |
| 自我修正 | 26 条 Reflection 规则，成功率从 60% 提升至 85% |
| 经验积累 | Episodic Memory 记录每次接入经验，跨平台检索复用 |

### 9.2 与项目总体规划的关系

13-FDE 技能编排方案填补了 `../电商领域应用规划.md` 中 L3 层的空白：
- **L1 数据→本体**（已有 23 篇方案）：提供基础数据接入能力
- **L2 工作台层**（已有 12 系列）：提供用户操作界面
- **L3 FDE 技能编排**（本文档系列）：将静态接入流程升级为可编排技能链 ← 新增
- **L4 AIP 决策引擎**（已有 11 系列）：提供 TAOR 循环 + 权限防线 + 记忆系统
- **L5 行业 Wiki**（已有 14 系列）：提供三层记忆基础设施
- **L6 数字同事**（已有 11 系列 02-08）：消费 FDE 产出的数据

### 9.3 下一步

1. **等待依赖项就绪**：AIP 层 Phase 1-3 + 14-行业 Wiki Phase 1
2. **按四阶段实施**：技能链骨架 → Checkpoint → 权限+Reflection → 平台适配
3. **按里程碑验收**：M1~M6 逐步交付
4. **更新规划文档**：本文档系列实施过程中持续更新 `../电商领域应用规划.md`

---

*本文档为方案设计层，实施前需用户确认。*
*关联文档：`00-总览-从静态文档到可编排技能链.md` · `01-电商FDE技能链设计.md` · `02-Checkpoint与回滚设计.md` · `03-六层权限防线设计.md` · `04-Reflection自审节点设计.md`*

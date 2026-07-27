# 220tech · W2-U · k-LLM 扩展能力组（#74 / #75 / #77）

> **版本**：v1.0 · 2026-07-22
> **状态**：✅ 方案定稿 · 可编码
> **对齐**：
> - 差距分析 [220w](./220w-与目标系统差距对照分析.md) §12 #74/#75/#77
> - 产品方案 [07](../07-AIP引擎k-LLM与AgentStudio产品方案.md) §2.4（数据出境策略）· §6.2（自定义 LLM 注册）· §4.3（Prompt 工程）
> - 上游 W2-T [220tech_w2-t-llm-routing.md](./220tech_w2-t-llm-routing.md)（RouteRule.egress 字段已对齐 5 枚举）
> - 底层 `aos_api/llm_gateway.py` · `aos_api/llm_provider_registry.py` · `aos_api/aip_kv_store.py`
> **范围**：W2-U 收口三件 — 数据出境策略（敏感标记强制私有路由）· 自定义 LLM 注册（Function Interfaces/Source/Webhook 三形态）· Prompt 工程（变量注入/Few-shot/版本）
> **不替换底层**：本组是策略层与元数据层；最终调用仍走 `llm_gateway.chat()`，自定义 LLM 注册作为元数据补充 `llm_provider_registry`（不重写 provider 插件扫描）

---

## 0. 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文回答 | 文档与代码注释均中文 |
| 先方案后编码 | 本文先定稿，再写引擎/路由/测试 |
| 最小更改 | 仅新增 `aos_api/llm_extras.py` + `aos_api/routers/llm_extras.py` + `tests/test_llm_extras.py`；`main.py` 加 2 行（import + include_router）；不动 `llm_gateway.py` / `llm_provider_registry.py` |
| 不影响已有功能 | 自定义 LLM 注册与 `llm_provider_registry.publish_custom_plugin` 互补不冲突；数据出境策略是 SmartRouter 之上的策略层；Prompt 工程是 chat 之前的模板层 |
| 自测验证 | 单测全绿 + 全量回归 + 方案对照 |
| 符合方案军规 | egress 枚举与 W2-T RouteRule.egress 对齐；自定义 LLM 三形态与 07 §6.2 一致 |

---

## 1. 背景与边界

### 1.1 现状

| 能力 | 现状 | 缺口 |
| --- | --- | --- |
| 数据出境 | W2-T RouteRule.egress 有枚举但无独立策略引擎；无敏感字段检测；无审计抽检 | 🔴 缺 |
| 自定义 LLM | `llm_provider_registry.publish_custom_plugin` 支持自定义 provider 插件（openai_compatible 形态） | 🔴 缺 Function Interfaces / Source / Webhook 三形态的元数据注册 |
| Prompt 工程 | `llm_gateway.chat(query, model)` 直接传 query；无变量注入；无 Few-shot 模板；无版本管理 | 🔴 缺 |

### 1.2 边界

- ✅ 本组做：
  - #74 数据出境策略：敏感字段标记 + 字段级 egress 评估 + 出境审计抽检
  - #75 自定义 LLM 注册：Function Interfaces / Source / Webhook 三形态元数据 CRUD（不替代 provider 插件扫描）
  - #77 Prompt 工程：模板 CRUD + 变量注入 + Few-shot + 版本管理 + 渲染
- ❌ 本组不做：
  - 跨境法律合规判定（属合规层）
  - 自定义 provider 的实际 HTTP 调用（仍走 `llm_gateway.chat`）
  - Prompt 评估与门控（属 #78 Modeling Objectives）

---

## 2. 数据模型

### 2.1 #74 数据出境策略

```python
class SensitiveField(BaseModel):
    """敏感字段标记。"""
    object_type: str
    field_path: str            # a.b.c 点路径
    sensitivity: Literal["public", "internal", "sensitive", "restricted"] = "sensitive"
    # restricted = 必须私有路由，禁公网
    pii: bool = False          # 是否个人身份信息
    mask_strategy: Literal["none", "hash", "redact", "substitute"] = "redact"
    description: str = ""


class EgressPolicy(BaseModel):
    """数据出境策略。"""
    id: str
    name: str
    security_label: Literal["public", "internal", "sensitive", "restricted"]
    allowed_egress: Literal["allow", "restricted", "forbidden"]
    # allow=可公网 / restricted=脱敏后可 / forbidden=仅私有
    mask_before_egress: bool = False   # 出境前是否强制脱敏
    audit_sample_rate: float = 0.0     # 0~1 审计抽检比例
    description: str = ""


class EgressDecision(BaseModel):
    """单次请求的出境决策。"""
    allowed: bool
    egress: Literal["allow", "restricted", "forbidden"]
    masked_fields: list[str] = []      # 需脱敏的字段路径列表
    audit_required: bool = False
    reason: str = ""


class EgressAuditRecord(BaseModel):
    """出境审计记录。"""
    id: str
    timestamp: float
    security_label: str
    decision: str                       # allow / restricted / forbidden
    masked_fields: list[str] = []
    model_id: str = ""
    query_snippet: str = ""             # 截断前 200 字符
    route_rule_id: str = ""
```

### 2.2 #75 自定义 LLM 注册

```python
class FunctionInterface(BaseModel):
    """Function Interfaces 形态 — 通过函数签名描述 LLM 能力。"""
    id: str
    name: str
    function_ref: str                   # 函数 id（与 functions 模块对齐）
    input_schema: dict[str, Any]        # JSON Schema 输入
    output_schema: dict[str, Any]       # JSON Schema 输出
    model_hint: str = ""                # 推荐模型
    description: str = ""


class LLMSource(BaseModel):
    """Source 形态 — 数据源型 LLM（如知识库+LLM 组合）。"""
    id: str
    name: str
    source_type: Literal["knowledge_base", "vector_index", "dataset", "media_set"]
    source_ref: str                     # 数据源 id
    model_id: str                       # 底层 LLM 模型 id
    retrieval_config: dict[str, Any] = {}  # top_k / similarity_threshold 等
    description: str = ""


class LLMWebhook(BaseModel):
    """Webhook 形态 — 通过外部 webhook 接入自定义 LLM。"""
    id: str
    name: str
    url: str
    method: Literal["GET", "POST"] = "POST"
    auth_type: Literal["none", "bearer", "basic", "hmac"] = "none"
    auth_secret_ref: str = ""           # vault ref 或 env var name
    request_template: str = ""          # {{query}} {{model}} 模板
    response_path: str = "answer"       # dot-path 提取响应
    description: str = ""
```

### 2.3 #77 Prompt 工程

```python
class PromptTemplate(BaseModel):
    """Prompt 模板。"""
    id: str
    name: str
    template: str                       # 含 {{var}} 占位符
    variables: list[str] = []           # 变量名列表
    few_shot_examples: list[dict[str, str]] = []
    # [{"user": "...", "assistant": "..."}]
    version: int = 1
    is_active: bool = False             # 同 name 仅一个 active
    description: str = ""
    created_at: float = 0.0


class PromptVersion(BaseModel):
    """Prompt 版本记录。"""
    template_id: str
    version: int
    template: str
    timestamp: float
    change_note: str = ""


class RenderResult(BaseModel):
    """渲染结果。"""
    rendered: str
    variables_used: dict[str, str] = {}
    few_shot_count: int = 0
    template_id: str
    version: int
```

---

## 3. 引擎设计

文件：`aos_api/llm_extras.py`（新增，3 个引擎 + 统一 facade）

### 3.1 EgressPolicyEngine（#74）

```python
class EgressPolicyEngine:
    def register_sensitive(self, sf: SensitiveField) -> SensitiveField: ...
    def list_sensitive(self, object_type: str | None = None) -> list[SensitiveField]: ...
    def delete_sensitive(self, object_type: str, field_path: str) -> bool: ...
    def upsert_policy(self, policy: EgressPolicy) -> EgressPolicy: ...
    def get_policy(self, policy_id: str) -> EgressPolicy: ...
    def list_policies(self) -> list[EgressPolicy]: ...
    def delete_policy(self, policy_id: str) -> bool: ...
    def evaluate(
        self,
        security_label: str,
        payload: dict[str, Any] | None = None,
        object_type: str | None = None,
    ) -> EgressDecision: ...
    def record_audit(self, record: EgressAuditRecord) -> EgressAuditRecord: ...
    def list_audit_records(
        self, model_id: str | None = None, limit: int = 50,
    ) -> list[EgressAuditRecord]: ...
```

**evaluate 流程**：
1. 根据 `security_label` 找匹配的 EgressPolicy（无则用默认：restricted→forbidden, sensitive→restricted, internal→allow, public→allow）
2. 若 `mask_before_egress=True` 且 `payload` 提供：扫描 payload 中匹配 `object_type` 的敏感字段，返回 `masked_fields`
3. 若 `audit_sample_rate > 0` 且 `random() < audit_sample_rate`：`audit_required=True`
4. `restricted` 等级且 `mask_before_egress=False` → `allowed=False`
5. `forbidden` 等级 → `allowed=False`
6. 返回 `EgressDecision`

### 3.2 CustomLLMRegistry（#75）

```python
class CustomLLMRegistry:
    def upsert_function_interface(self, fi: FunctionInterface) -> FunctionInterface: ...
    def get_function_interface(self, fi_id: str) -> FunctionInterface: ...
    def list_function_interfaces(self) -> list[FunctionInterface]: ...
    def delete_function_interface(self, fi_id: str) -> bool: ...

    def upsert_source(self, src: LLMSource) -> LLMSource: ...
    def get_source(self, src_id: str) -> LLMSource: ...
    def list_sources(self, source_type: str | None = None) -> list[LLMSource]: ...
    def delete_source(self, src_id: str) -> bool: ...

    def upsert_webhook(self, wh: LLMWebhook) -> LLMWebhook: ...
    def get_webhook(self, wh_id: str) -> LLMWebhook: ...
    def list_webhooks(self) -> list[LLMWebhook]: ...
    def delete_webhook(self, wh_id: str) -> bool: ...

    def list_all(self) -> dict[str, list[dict[str, Any]]]:
        """统一返回 {function_interfaces, sources, webhooks}"""
```

**与 `llm_provider_registry` 关系**：
- `llm_provider_registry.publish_custom_plugin` 是 openai_compatible 形态的 provider 插件注册（底层调用通道）
- `CustomLLMRegistry` 是更高层的元数据描述：Function Interfaces 描述"通过函数调用 LLM"、Source 描述"LLM+数据源组合"、Webhook 描述"通过 webhook 接入 LLM"
- 两者互补：CustomLLMRegistry 的 LLMSource.model_id 应能在 `llm_provider_registry.routable_models_from_plugins()` 找到

### 3.3 PromptEngine（#77）

```python
class PromptEngine:
    def create_template(self, tpl: PromptTemplate) -> PromptTemplate: ...
    def get_template(self, template_id: str) -> PromptTemplate: ...
    def list_templates(self, name: str | None = None) -> list[PromptTemplate]: ...
    def update_template(
        self, template_id: str, updates: dict[str, Any],
    ) -> PromptTemplate: ...
    def delete_template(self, template_id: str) -> bool: ...
    def activate_version(self, template_id: str, version: int) -> PromptTemplate: ...
    """激活指定版本（同 name 仅一个 active）"""
    def list_versions(self, template_id: str) -> list[PromptVersion]: ...
    def render(
        self,
        template_id: str,
        variables: dict[str, str] | None = None,
        few_shot_count: int = 0,
    ) -> RenderResult: ...
    def render_and_call(
        self,
        template_id: str,
        variables: dict[str, str] | None = None,
        model: str | None = None,
    ) -> dict[str, Any]:
        """渲染模板并调用 llm_gateway.chat."""
```

**render 流程**：
1. 取 `template_id` 对应模板（若 inactive，回退到同 name 的 active 版本）
2. 若 `few_shot_count > 0`，取前 N 个 `few_shot_examples` 拼接到模板前
3. 用 `{{var}}` 正则替换 `variables` 中的值
4. 未提供的变量保留为 `{{var}}` 原样（便于调试）
5. 返回 `RenderResult(rendered, variables_used, few_shot_count, template_id, version)`

**render_and_call 流程**：
1. 调用 `render(template_id, variables)`
2. 调用 `llm_gateway.chat(rendered, model=model)`
3. 返回 `{answer, model, template_id, version, rendered}`

### 3.4 单例与持久化

- 3 个引擎均用**双重检查锁单例**
- 持久化走 `aip_kv_store.put_payload / get_payload`，key 前缀：
  - `llm_extras_sensitive_fields`
  - `llm_extras_egress_policies`
  - `llm_extras_egress_audit`
  - `llm_extras_function_interfaces`
  - `llm_extras_llm_sources`
  - `llm_extras_llm_webhooks`
  - `llm_extras_prompt_templates`
  - `llm_extras_prompt_versions`

---

## 4. API 设计

文件：`aos_api/routers/llm_extras.py`（新增）

### 4.1 #74 数据出境策略

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/v1/aip/egress/sensitive-fields` | 列出敏感字段（可按 object_type 过滤） |
| POST | `/v1/aip/egress/sensitive-fields` | 注册敏感字段 |
| DELETE | `/v1/aip/egress/sensitive-fields/{object_type}/{field_path}` | 删除敏感字段 |
| GET | `/v1/aip/egress/policies` | 列出出境策略 |
| POST | `/v1/aip/egress/policies` | 新增/更新策略 |
| GET | `/v1/aip/egress/policies/{policy_id}` | 单条策略 |
| DELETE | `/v1/aip/egress/policies/{policy_id}` | 删除策略 |
| POST | `/v1/aip/egress/evaluate` | 评估请求出境决策 |
| GET | `/v1/aip/egress/audit-records` | 审计记录列表 |
| POST | `/v1/aip/egress/audit-records` | 手动追加审计记录 |

### 4.2 #75 自定义 LLM 注册

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/v1/aip/custom-llm/function-interfaces` | 列出 Function Interfaces |
| POST | `/v1/aip/custom-llm/function-interfaces` | 新增/更新 |
| GET | `/v1/aip/custom-llm/function-interfaces/{fi_id}` | 单条 |
| DELETE | `/v1/aip/custom-llm/function-interfaces/{fi_id}` | 删除 |
| GET | `/v1/aip/custom-llm/sources` | 列出 LLM Sources |
| POST | `/v1/aip/custom-llm/sources` | 新增/更新 |
| GET | `/v1/aip/custom-llm/sources/{src_id}` | 单条 |
| DELETE | `/v1/aip/custom-llm/sources/{src_id}` | 删除 |
| GET | `/v1/aip/custom-llm/webhooks` | 列出 Webhooks |
| POST | `/v1/aip/custom-llm/webhooks` | 新增/更新 |
| GET | `/v1/aip/custom-llm/webhooks/{wh_id}` | 单条 |
| DELETE | `/v1/aip/custom-llm/webhooks/{wh_id}` | 删除 |
| GET | `/v1/aip/custom-llm/all` | 统一返回三形态列表 |

### 4.3 #77 Prompt 工程

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/v1/aip/prompts/templates` | 列出模板（可按 name 过滤） |
| POST | `/v1/aip/prompts/templates` | 新增模板（version=1） |
| GET | `/v1/aip/prompts/templates/{template_id}` | 单条模板 |
| PUT | `/v1/aip/prompts/templates/{template_id}` | 更新模板（自动新增版本） |
| DELETE | `/v1/aip/prompts/templates/{template_id}` | 删除模板及其所有版本 |
| POST | `/v1/aip/prompts/templates/{template_id}/activate` | 激活指定版本（body={version}） |
| GET | `/v1/aip/prompts/templates/{template_id}/versions` | 模板版本历史 |
| POST | `/v1/aip/prompts/render` | 渲染模板（body={template_id, variables, few_shot_count}） |
| POST | `/v1/aip/prompts/render-and-call` | 渲染并调用 LLM |

---

## 5. 集成点

### 5.1 main.py（最小更改）

```python
from aos_api.routers import (..., llm_extras, ...)
application.include_router(llm_extras.router)
```

### 5.2 与 W2-T 协同

- `EgressPolicyEngine.evaluate` 的结果可作为 `SmartRouter.choose` 的硬过滤条件（`security_label=restricted` 且 `egress != forbidden` 的候选淘汰）
- `CustomLLMRegistry` 的 `LLMSource.model_id` 应在 `llm_provider_registry.routable_models_from_plugins()` 中可查

### 5.3 与底层网关协同

- `PromptEngine.render_and_call` 内部调用 `from aos_api.llm_gateway import chat`
- 调用签名 `chat(rendered, model=model)`

---

## 6. 测试计划

文件：`tests/test_llm_extras.py`（新增，约 40 个用例）

### 6.1 EgressPolicyEngine（14）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | register_sensitive | 返回带标记的敏感字段 |
| 2 | list_sensitive 过滤 | 按 object_type 过滤 |
| 3 | delete_sensitive | 删除后 list 不含 |
| 4 | upsert_policy 新增 | 返回带 id 的策略 |
| 5 | get_policy 未找到 | 抛 NOT_FOUND |
| 6 | list_policies | 全量列表 |
| 7 | delete_policy | 删除后 get 抛 NOT_FOUND |
| 8 | evaluate public → allow | allowed=True |
| 9 | evaluate restricted → forbidden | allowed=False |
| 10 | evaluate sensitive → restricted + mask | masked_fields 非空 |
| 11 | evaluate 无匹配策略 → 默认 | internal → allow |
| 12 | evaluate audit_sample_rate | 触发 audit_required |
| 13 | record_audit + list_audit_records | 审计记录可查 |
| 14 | evaluate restricted 无 mask_before_egress | allowed=False |

### 6.2 CustomLLMRegistry（13）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | upsert_function_interface 新增 | 返回带 id |
| 2 | get_function_interface 未找到 | 抛 NOT_FOUND |
| 3 | list_function_interfaces | 列表 |
| 4 | delete_function_interface | 删除后 get 抛 NOT_FOUND |
| 5 | upsert_source 新增 | 返回带 id |
| 6 | get_source 未找到 | 抛 NOT_FOUND |
| 7 | list_sources 按 source_type 过滤 | 仅返回匹配项 |
| 8 | delete_source | 删除成功 |
| 9 | upsert_webhook 新增 | 返回带 id |
| 10 | get_webhook 未找到 | 抛 NOT_FOUND |
| 11 | list_webhooks | 列表 |
| 12 | delete_webhook | 删除成功 |
| 13 | list_all | 返回三形态合并字典 |

### 6.3 PromptEngine（13）

| # | 用例 | 期望 |
| --- | --- | --- |
| 1 | create_template | version=1 |
| 2 | get_template 未找到 | 抛 NOT_FOUND |
| 3 | list_templates 按 name 过滤 | 仅返回匹配项 |
| 4 | update_template 新增版本 | version 递增，旧版本保留 |
| 5 | delete_template | 删除模板及所有版本 |
| 6 | activate_version | 同 name 仅一个 active |
| 7 | list_versions | 按版本号排序 |
| 8 | render 基础 | {{var}} 替换 |
| 9 | render 未提供变量 | 保留 {{var}} 原样 |
| 10 | render with few_shot | few_shot_count > 0 时拼接示例 |
| 11 | render few_shot_count 超过实际 | 仅拼接实际数量 |
| 12 | render inactive 模板 | 回退到 active 版本 |
| 13 | render_and_call 端到端 | 渲染 → 调用 → 返回 answer |

---

## 7. 风险与缓解

| 风险 | 缓解 |
| --- | --- |
| 数据出境策略与 W2-T egress 字段语义不一致 | egress 枚举严格对齐（allow/restricted/forbidden 与 W2-T RouteRule.egress 5 枚举映射） |
| 自定义 LLM 注册与 provider 插件重复 | CustomLLMRegistry 仅做元数据；实际调用走 llm_gateway |
| Prompt 模板版本爆炸 | 同 name 模板的非 active 版本可定期清理（暂不实现自动清理，留作扩展） |
| 敏感字段扫描性能 | 仅扫描 payload 顶层 + 一层嵌套；深层扫描留作扩展 |
| 审计抽检随机性 | 使用 random.random() < audit_sample_rate；测试时可注入确定性 random |

---

## 8. 交付物清单

| 路径 | 状态 | 说明 |
| --- | --- | --- |
| `docs/palantier/20_tech/220tech_w2-u-llm-extras.md` | 新建 | 本文档 |
| `aos-platform/services/aos-api/aos_api/llm_extras.py` | 新建 | 3 引擎 + 单例 |
| `aos-platform/services/aos-api/aos_api/routers/llm_extras.py` | 新建 | ~30 个端点 |
| `aos-platform/services/aos-api/tests/test_llm_extras.py` | 新建 | ~40 测试 |
| `aos-platform/services/aos-api/aos_api/main.py` | 修改 2 行 | import + include_router |
| `docs/palantier/20_tech/220plan-分阶段开发与里程碑计划.md` | 更新 | v3.3 → v3.4，标记 #74/#75/#77 ✅ |

---

## 9. 验收标准

1. ✅ 所有 ~40 个单测全绿
2. ✅ 全量回归无新增失败（pre-existing wiki flaky 不计）
3. ✅ `main.py` 启动无报错，新路由 `/v1/aip/egress/*` `/v1/aip/custom-llm/*` `/v1/aip/prompts/*` 可访问
4. ✅ 方案文档与代码字段一致
5. ✅ 看板进度从 44/166 → 47/166，全局 90 → 93 / 259

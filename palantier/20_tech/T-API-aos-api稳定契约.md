# T-API · aos-api 稳定契约（首版）

> **版本**：v1.0 · 2026-07-17  
> **状态**：✅ **方案完成**（实现按 T-EVO 里程碑落地）  
> **对齐**：[20 §3](20-AOS整体技术方案.md) · [T-EVO](T-EVO-v0.1到目标态替换阶梯.md) · [10 adapter](../10_v01/10-v0.1技术方案.md)  
> **原则**：UI / Desktop **只依赖本契约**；上游 Dify/LiteLLM/图库均藏在 Adapter 后

---

## 使用的 Rules

契约优先 · 版本化 · 禁止 UI 直连上游 · 与各 T0x API 摘要一致

---

## 1. 基线

| 项 | 值 |
| --- | --- |
| Base URL | `/v1` |
| 协议 | HTTPS · JSON · UTF-8 |
| 鉴权 | `Authorization: Bearer <OIDC access_token>`（见 T-CROSS） |
| 幂等 | 写接口支持头 `Idempotency-Key` |
| 错误 | `{ "code","message","details?","traceId" }` |
| 兼容 | 加字段兼容；破坏性变更走 `/v2` 或显式 deprecation ≥1 个次版本 |

**从 v0.1 继承：** `POST /v1/buddy/ask` **永久保留**（或 301 到 `/v1/aip/chat` 且保留字段映射），禁止打断桌面试用。

---

## 2. 资源一览（按域）

### 2.1 工作台 · T08

| Method | Path | 说明 |
| --- | --- | --- |
| GET/POST | `/v1/modules` | Module 列表/创建 |
| GET/PATCH | `/v1/modules/{id}` | 定义（Layout/Variables/Events） |
| GET | `/v1/modules/{id}/runtime` | 运行态 Schema |
| POST | `/v1/object-sets/query` | body: filters≤10 维 · page · pageSize≤1000 |
| POST | `/v1/actions/execute` | Idempotency-Key 必填（写路径） |
| POST | `/v1/modules/{id}/publish` | → Apollo Publish Adapter |

### 2.2 Ontology · T06

| Method | Path | 说明 |
| --- | --- | --- |
| CRUD | `/v1/ontology/object-types` | 发布门禁 HR-02 |
| CRUD | `/v1/ontology/link-types` | 含解法 B 规模校验 |
| GET | `/v1/objects/{type}` · `/v1/objects/{type}/{id}` | 实例 |
| GET/PUT | `/v1/wiki/{objectType}/{objectId}` | PUT 仅创建 Action 提议，不直写 |
| GET | `/v1/funnel/{objectType}/status` | 四阶段 |
| POST | `/v1/functions/{id}/invoke` | 只读默认；超时/内存由 Runtime 强制 |

### 2.3 AIP · T07

| Method | Path | 说明 |
| --- | --- | --- |
| POST | `/v1/aip/chat` | Buddy / Studio；兼容 buddy/ask |
| POST | `/v1/aip/logic/run` | dryRun=true 不落库 |
| GET/POST | `/v1/aip/models` · `/v1/aip/providers` | 插件汇总 |
| GET/POST | `/v1/aip/capabilities` · `/v1/aip/capabilities/{id}/invoke` · `/submit` · `/jobs/{jobId}` · `/sessions` | Capability Facade（07b）；UI 不直连厂商 |
| CRUD | `/v1/aip/drafts` | Draft Dataset |
| GET/POST | `/v1/aip/evals` | 门控 |
| GET | `/v1/aip/lineage/{id}` | 决策谱系 |

### 2.4 L1 · T05

| Method | Path | 说明 |
| --- | --- | --- |
| CRUD | `/v1/sources` · `/v1/syncs` | Connector |
| CRUD | `/v1/pipelines` · `/v1/builds` | Pipeline |
| CRUD | `/v1/schedules` | 计划 |
| GET | `/v1/datasets/{rid}` · `/history` | Dataset |
| GET | `/v1/media-sets/{rid}` | MediaSet |
| GET/POST | `/v1/dlq` · `/v1/dlq/{id}/retry` | 死信 |

### 2.5 Apollo · T09

| Method | Path | 说明 |
| --- | --- | --- |
| GET | `/v1/apollo/fleet` | Hub 舰队 |
| GET/POST | `/v1/apollo/channels` · `/promote` · `/recall` · `/hotfix` | 通道 |
| GET | `/v1/apollo/spokes/{id}` | Spoke / Lite |
| POST | `/v1/apollo/assets` · `/bind` | Asset Bundle |
| CRUD | `/v1/apollo/changes` | Change Mgmt |
| GET/PATCH | `/v1/apollo/config` | Override（禁密钥明文） |
| POST | `/v1/apollo/ferry/export` · `/import` | 气隙包 |

### 2.6 横切 · T-CROSS

| Method | Path | 说明 |
| --- | --- | --- |
| GET | `/v1/me` | 当前用户 · 角色 · Markings |
| GET | `/v1/health` · `/v1/ready` | 探活 |

---

## 3. 关键错误码（稳定）

| code | HTTP | 含义 |
| --- | --- | --- |
| `AUTH_REQUIRED` | 401 | 未登录 |
| `FORBIDDEN` | 403 | Marking/角色不足 |
| `VALIDATION` | 400 | 参数/维数超限等 |
| `IDEMPOTENT_REPLAY` | 200 | 幂等命中（返回首次结果） |
| `DRAFT_REQUIRED` | 409 | 须走 Draft |
| `EVAL_GATE` | 409 | L4 Eval 未绿 |
| `CIRCUIT_OPEN` | 503 | L4 熔断降级 |
| `BACKING_NOT_UNIQUE` | 422 | HR-02 |
| `LINK_SCALE_BLOCKED` | 422 | 解法 B>100万未 MDO |
| `SECRET_PLAINTEXT_REJECTED` | 400 | 明文密钥 |

---

## 4. OpenAPI 落点

```text
aos-platform/packages/contracts/openapi/v1.yaml
```

生成：`packages/contracts-client`（TS）· 可选 Python。  
CI：契约测试 + 禁止 apps 依赖上游 SDK（grep 门禁）。

---

## 5. 修订

| 版本 | 说明 |
| --- | --- |
| v1.0 | 首版资源全表；与 T05～T09 / T-UI / T-CROSS 对齐 |

---

*T-API v1.0 · docs/palantier/20_tech*

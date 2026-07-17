# 48 · Module 落 PG · JWKS 可插拔 · OpenAPI 深化方案

> **版本**：v1.0 · 2026-07-17  
> **前提**：**TX.4 最小引擎已 ✅**（[47](47-技术方案全面对齐补缺方案.md) G-ALIGN-07）；截图「仍未完成」为旧清单  
> **本刀**：Module 持久化 PG · Dev JWKS（自签 RSA，可换真 Keycloak URL）· OpenAPI 主表补全  
> **工程**：`aos-platform/services/aos-api` · `packages/contracts/openapi/v1.yaml`  
> **硬规则**：PG 不可用时测试 skip（同 ontology）；生产禁默认口令；不强迫起 Keycloak 集群

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文后改 |
| 最小更改 | modules 换存储；mock_data 仅作 seed 源/降级说明 |
| 不影响已有 | Bearer dev / HS256 仍可用 |

---

## 1. TX.4 状态（诚实）

| 项 | 状态 |
| --- | --- |
| `ensure_markings` → 403 `FORBIDDEN` | ✅ |
| modules 读/列表过滤 | ✅ |
| actions validate / execute 读 requiredMarkings | ✅ |
| 策略引擎 / 继承 / 字段级 Marking | **后置**（非本刀） |

→ 台账 TX.4 = **✅ MVP**；「完整企业 Marking 产品」另立后置，不挡主路径。

---

## 2. Module 落 PG

表 `meta_module`：id, name, status, description, object_type, markings jsonb, entry_path, widgets jsonb, buddy_bound, created_at。

- `modules.py` 读写 PG；启动 seed 三模块（ops/canvas/buddy）
- 幂等 / publish / patch 语义不变
- 单测走 PG（同 conftest）

---

## 3. JWKS 可插拔（缓解 B-TX3-01）

| 能力 | 行为 |
| --- | --- |
| `GET /v1/auth/jwks` | 返回 Dev RSA 公钥 JWKS（进程内生成或 env PEM） |
| `AOS_OIDC_JWKS_URL` | 指向外部 Keycloak **或** `http://127.0.0.1:8080/v1/auth/jwks` |
| `POST /v1/auth/token` | 支持 `alg=RS256`（默认仍 HS256）；RS256 签发可被 JWKS 验 |
| 真 Keycloak | 只改 env URL，不改代码 |

---

## 4. OpenAPI 深化

补 T-API 其余主 path（ontology/datasets/syncs/media-sets/pipelines/dlq/auth/…）为可发现条目；Ferry 标 `x-deferred: true`。

---

## 5. 自测

- [x] modules CRUD/publish 经 PG
- [x] RS256 token + `/v1/auth/jwks` 验签 → `/v1/me` oidc
- [x] OpenAPI 含 fleet/publish/jwks/ferry(deferred)
- [x] 既有 auth/module 测不回归（`test_module_pg_jwks` 3 passed）

---

*v1.0*

# 57 · Dev HA Keycloak（缓解关闭 B-TX3-01）方案

> **版本**：v1.0 · 2026-07-17  
> **任务**：台账下一刀 #1 — HA Keycloak（可选）  
> **对齐**：[50](50-Dev-Keycloak联调缓解B-TX3方案.md) · [41](41-TX.3-IdP-OIDC对接方案.md) · [24](24-AOS客户侧前置组件安装SOP.md)  
> **工程**：`deploy/dev` · `aos_api/oidc.py` · `scripts/ci`  
> **硬规则**：KC **不进客户包**；`oidc` / `oidc-ha` 互斥；生产真集群仍可由客户自备 IdP；本刀 = **Dev 双节点 + JWKS 故障切换**

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文后改 |
| 最小更改 | 扩 OIDC 多 URL；compose 新 profile；probe |
| 不影响主路径 | 无 profile / 单 JWKS 行为与现网一致 |
| 诚实 | 非生产级 Infinispan 深运维；Dev 共享 DB + LB 证明拓扑 |

---

## 1. 目标 / 非目标

| 目标（DoD） | 非目标 |
| --- | --- |
| `compose --profile oidc-ha`：KC DB + 双节点 + nginx `:8083` | 强制每人起 HA |
| `AOS_OIDC_JWKS_URLS` 多 URL **故障切换**（单测不依赖 Docker） | 改 UI 登录产品 |
| `AOS_OIDC_ISSUERS` 多 issuer 允许表 | 多 realm 产品 |
| probe-ha：未起 → SKIP | 客户包打入 Keycloak |
| **B-TX3-01**：Dev HA 路径 ✅；生产 = 换同构 URL / 客户 IdP | 现场机房 HA 验收单 |

---

## 2. 拓扑

```
                    :8083 nginx LB
                   /              \
          keycloak-a:8080    keycloak-b:8080
                   \              /
                    postgres (keycloak DB)
                    
aos-api: AOS_OIDC_JWKS_URLS=http://127.0.0.1:8083/.../certs[,fallback]
         AOS_OIDC_ISSUER=http://127.0.0.1:8083/realms/aos
```

| 服务 | 说明 |
| --- | --- |
| `aos-dev-kc-db` | 独立 PG（与 aos_meta 隔离） |
| `aos-dev-keycloak-a` | `start-dev --import-realm` |
| `aos-dev-keycloak-b` | `start-dev`（同 DB，不重复 import） |
| `aos-dev-keycloak-lb` | nginx upstream a/b · 宿主 **8083** |

与 [50] `profile oidc` **互斥**（同抢 8083）；文档写明先 `down` 再切 profile。

---

## 3. aos-api

| 变量 | 含义 |
| --- | --- |
| `AOS_OIDC_JWKS_URL` | 单 URL（兼容 [50]） |
| `AOS_OIDC_JWKS_URLS` | 逗号分隔；优先于单 URL；逐个尝试 |
| `AOS_OIDC_ISSUERS` | 可选；缺省 = `[AOS_OIDC_ISSUER]` |
| `GET /v1/auth/oidc` | `haMode` · `jwksUrls` |

验签：`PyJWKClient` 按 URL 列表故障切换；`issuer` 用允许表。

---

## 4. 落点

| 路径 | 变更 |
| --- | --- |
| `docs/.../57-*.md` | 本文 |
| `deploy/dev/docker-compose.yml` | profile `oidc-ha` 服务 |
| `deploy/dev/keycloak/nginx-ha.conf` | LB |
| `aos_api/oidc.py` | 多 JWKS / issuers |
| `scripts/ci/probe-keycloak-ha.ps1` | SKIP 友好 |
| `tests/test_jwks_failover.py` | 首 URL 挂 → 次 URL 成 |
| `.env.example` · 26/31/00/27 | 回写；关 B-TX3-01 Dev |

---

## 5. 自测

- [x] `test_jwks_failover`：坏 URL + 好 URL → verify OK
- [x] 单 `AOS_OIDC_JWKS_URL` 回归绿（`test_external_jwks`）
- [ ] （可选）`oidc-ha up` + probe-ha
- [x] compose `--profile oidc-ha config` 语法通过

---

## 6. 风险

| 风险 | 缓解 |
| --- | --- |
| 双 KC 内存大 | profile 可选；probe SKIP |
| a/b 同时 import 冲突 | 仅 a import-realm |
| iss host 漂移 | LB 统一 `KC_HOSTNAME=127.0.0.1` + port 8083 |

---

*v1.0*

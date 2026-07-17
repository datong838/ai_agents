# 50 · Dev Keycloak 联调（缓解 B-TX3-01）方案

> **版本**：v1.0 · 2026-07-17  
> **任务**：台账下一刀 #1 — 真 JWKS 联调路径；缓解 **B-TX3-01**  
> **对齐**：[41](41-TX.3-IdP-OIDC对接方案.md) · [48](48-Module落PG与JWKS及OpenAPI深化方案.md) · [24](24-AOS客户侧前置组件安装SOP.md) · [27](27-本机开发基础设施与工程门禁记录.md)  
> **工程**：`aos-platform/deploy/dev` · `services/aos-api` · `scripts/ci`  
> **硬规则**：生产禁默认口令；Keycloak **不进客户包**；默认 `compose up` **不起** IdP（profile）；UI 只打 aos-api

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文后改 |
| 最小更改 | 复用现有 JWKS 验签；只加 compose + password 代理 + probe |
| 不影响主路径 | 无 profile 时行为与现网一致（Dev JWT / Bearer dev） |
| 诚实 | **非** HA Keycloak 集群；本刀 = **可联调的单机 Dev IdP** |

---

## 1. 目标 / 非目标

| 目标（DoD） | 非目标 |
| --- | --- |
| `docker compose --profile oidc up` 起 Keycloak + realm `aos` | 生产 HA / 多 realm 运维 |
| `AOS_OIDC_JWKS_URL` 指向 KC certs → JWT 可 `/v1/me` | 改写 UI 登录产品页 |
| `POST /v1/auth/token` 支持 `grantType=password`（代理 KC，可选） | 存 client secret 进仓库 |
| probe 脚本可 skip（KC 未起） | 强制每人每天起 KC |
| 单测：外部 JWKS URL 验签路径绿 | 字段级 Marking / Ferry |

**B-TX3-01 处置：** Dev 单机路径 ✅；「现场/生产真集群」仍可选后置（换同构 URL 即可）。

---

## 2. 架构

```
[可选] Keycloak :8083  realm=aos  client=aos-api
        │  JWKS  /realms/aos/protocol/openid-connect/certs
        │  token /realms/aos/protocol/openid-connect/token
        ▼
aos-api
  AOS_OIDC_ISSUER=http://127.0.0.1:8083/realms/aos
  AOS_OIDC_AUDIENCE=aos-api
  AOS_OIDC_JWKS_URL=…/certs
  AOS_OIDC_TOKEN_URL=…/token   # password 代理用
        ▲
Client  POST /v1/auth/token  {grantType:password, username, password}
        Authorization: Bearer <kc-jwt> → /v1/me
```

---

## 3. 配置（Dev）

| 变量 | 示例 |
| --- | --- |
| `AOS_OIDC_ISSUER` | `http://127.0.0.1:8083/realms/aos` |
| `AOS_OIDC_AUDIENCE` | `aos-api` |
| `AOS_OIDC_JWKS_URL` | `http://127.0.0.1:8083/realms/aos/protocol/openid-connect/certs` |
| `AOS_OIDC_TOKEN_URL` | 同上路径 `…/token`（可选） |
| `AOS_OIDC_CLIENT_ID` | `aos-api`（password 代理；**非** secret） |
| KC Admin | `admin` / `aos_dev_only_change_me`（仅 compose；勿进客户包） |
| 用户 | `alice` / `aos_dev_only_change_me` · claims：`org_id`/`project_id`/`markings` |

---

## 4. 代码 / 落点

| 路径 | 变更 |
| --- | --- |
| `deploy/dev/docker-compose.yml` | `aos-dev-keycloak` · `profiles: [oidc]` |
| `deploy/dev/keycloak/aos-realm.json` | realm 导入 |
| `aos_api/oidc.py` | `password` grant 代理；`grantTypes` 声明 |
| `aos_api/routers/auth_oidc.py` | 接 password body |
| `scripts/ci/probe-keycloak-oidc.ps1` | 联调；未起则 skip |
| `tests/test_external_jwks.py` | 临时 HTTP JWKS 验签 |
| `.env.example` · 27 · 26/31/00 | 回写 |

---

## 5. 自测

- [ ] `pytest tests/test_external_jwks.py` 绿（不依赖 Docker）
- [ ] （可选）`compose --profile oidc up -d` + probe → `/v1/me` tokenKind=oidc
- [x] 无 profile 时既有 auth 测不回归（oidc+jwks 11 passed）

---

## 6. 风险

| 风险 | 缓解 |
| --- | --- |
| KC 镜像大 / 拉不动 | probe skip；单测不依赖 KC |
| issuer host 不一致（localhost vs 127.0.0.1） | compose 固定 `KC_HOSTNAME=127.0.0.1` + 文档写死 |
| 误把 KC 打进客户包 | compose 顶注释 + 23 refs 语义 |

---

*v1.0*

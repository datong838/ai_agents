# 60 · 生产 IdP 联调手册（客户自备 OIDC）

> **版本**：v1.0 · 2026-07-17  
> **任务**：台账下一刀 #1 — 生产 IdP 联调手册  
> **对齐**：[41](41-TX.3-IdP-OIDC对接方案.md) · [50](50-Dev-Keycloak联调缓解B-TX3方案.md) · [57](57-Dev-HA-Keycloak缓解B-TX3方案.md) · [24](24-AOS客户侧前置组件安装SOP.md) §3.4  
> **工程**：手册本文 · `scripts/ci/probe-prod-idp.ps1` · `aos_api/auth.py`（claim 别名）  
> **硬规则**：Keycloak/客户 IdP **不进客户包**；生产 `AOS_AUTH_ALLOW_DEV=0`；密钥只走 vault/env ref；UI 只打 aos-api

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文即手册 + 最小探针/别名 |
| 最小更改 | 不改登录产品页；仅 claim 兼容 + 探针 |
| 诚实 | Dev KC [50]/[57] ≠ 生产现场；本刀 = **换 URL 联调规程** |

---

## 1. 目标 / 非目标

| 目标（DoD） | 非目标 |
| --- | --- |
| 现场按清单把客户 IdP 接到 aos-api | 代客户安装 IdP HA |
| 环境变量与 claim 映射写清 | 改 UI SSO 产品壳 |
| `probe-prod-idp.ps1`：discovery/JWKS/（可选）token+/me | 强制 password grant（多数生产禁用） |
| 生产关闭 Dev token | 多租户 IdP 联邦产品 |

---

## 2. 架构（生产）

```
[客户 IdP]  Azure AD / Keycloak / Okta / …
     │  OIDC discovery + JWKS
     │  签发 access_token（RS256）
     ▼
aos-api
  AOS_AUTH_ALLOW_DEV=0
  AOS_OIDC_ISSUER / AOS_OIDC_ISSUERS
  AOS_OIDC_AUDIENCE=aos-api（或客户约定 aud）
  AOS_OIDC_JWKS_URL 或 AOS_OIDC_JWKS_URLS（HA）
     ▲
Client  Authorization: Bearer <IdP JWT> → /v1/me
```

**Dev 对照：** [50] 单机 · [57] 双节点；生产只需 **同构 URL**，不必起 AOS 自带 Keycloak。

---

## 3. 客户 IdP 侧准备（给集成商勾选）

| # | 项 | 说明 |
| --- | --- | --- |
| 1 | Issuer | 稳定 HTTPS；与 token `iss` **字节级一致**（含/不含尾 `/`） |
| 2 | Audience | access token `aud` 含 `aos-api`（或约定值，填入 `AOS_OIDC_AUDIENCE`） |
| 3 | JWKS | `.../protocol/openid-connect/certs` 或 `.../discovery/v2.0/keys` 可公网/专网达 aos-api |
| 4 | Client | 机密客户端密钥进 Vault；AOS 只存 `AOS_OIDC_CLIENT_ID_REF` |
| 5 | Claims | 见 §4；缺 claim 时用请求头兜底（org/project）但 **roles/markings 建议落 JWT** |
| 6 | 时钟 | NTP；时钟偏斜过大验签失败 |
| 7 | TLS | 企业根证书进 aos-api 信任链（如有 MITM 代理） |

### 3.1 Keycloak 示例

- Realm：`aos`（或客户名）
- Client：`aos-api`（confidential 或 public+PKCE，按前端）
- Audience mapper → `aos-api`
- Protocol mappers（建议）：

| Claim | Mapper 建议 |
| --- | --- |
| `org_id` | User attribute / hardcoded |
| `project_id` | User attribute |
| `roles` | Realm roles → claim **或** 使用默认 `realm_access.roles`（aos-api 已识别） |
| `markings` | 多值属性 → JSON array claim |

### 3.2 Azure AD / Entra 示例

- App registration → Expose API / App ID URI
- `aud` = Application ID URI 或 api://…
- Optional claims：扩展属性映射到 `org_id` / `roles`（或用 groups 后由网关转换——本刀不内置 groups→roles）

---

## 4. aos-api 环境变量（生产清单）

| 变量 | 生产要求 |
| --- | --- |
| `AOS_AUTH_ALLOW_DEV` | **`0`** |
| `AOS_OIDC_ISSUER` | 客户 issuer（与 JWT `iss` 一致） |
| `AOS_OIDC_ISSUERS` | 可选多 issuer（迁移/双活） |
| `AOS_OIDC_AUDIENCE` | 与 token `aud` 对齐 |
| `AOS_OIDC_JWKS_URL` | 单 JWKS |
| `AOS_OIDC_JWKS_URLS` | HA 故障切换（逗号分隔） |
| `AOS_OIDC_TOKEN_URL` | 仅当需要 Dev 形 password 代理；**生产通常不配** |
| `AOS_OIDC_CLIENT_ID` / `_REF` | 元数据/代理；secret 不进仓 |

重启 aos-api 后：`GET /v1/auth/oidc` 应显示 `jwksConfigured`、正确 `issuer`、`haMode`（若多 URL）。

---

## 5. JWT Claims（aos-api 识别）

| Claim | 必填 | 说明 |
| --- | --- | --- |
| `sub` | 是 | 主体 |
| `iss` / `aud` / `exp` | 是 | 标准验签 |
| `org_id` | 建议 | 别名：`orgId` · `organization_id`；否则用头 `X-Org-Id` |
| `project_id` | 建议 | 别名：`projectId`；否则 `X-Project-Id` |
| `roles` | 建议 | 或 Keycloak `realm_access.roles` |
| `markings` | 建议 | 缺省 `["public"]` |

---

## 6. 联调步骤（现场）

1. 向客户要：issuer、JWKS URL、测试账号拿到的 **access_token 样例**（可脱敏）。  
2. 配置 §4 变量，**关 Dev**，重启 aos-api。  
3. 跑探针：

```powershell
.\scripts\ci\probe-prod-idp.ps1 `
  -Issuer "https://idp.example.com/realms/aos" `
  -JwksUrl "https://idp.example.com/realms/aos/protocol/openid-connect/certs" `
  -Audience "aos-api"
# 有样例 token 时：
.\scripts\ci\probe-prod-idp.ps1 ... -AccessToken $tok -ApiBase http://aos-api:8080
```

4. 期望：discovery/JWKS **200**；带 token 时 `/v1/me` **200** 且 `tokenKind` 反映 OIDC。  
5. 失败对照 §8。

---

## 7. 落点

| 路径 | 变更 |
| --- | --- |
| `docs/.../60-*.md` | 本文 |
| `scripts/ci/probe-prod-idp.ps1` | 新建 |
| `aos_api/auth.py` | claim 别名 |
| `tests/test_idp_claim_aliases.py` | 别名单测 |
| [24] §3.4 | 挂接本文 |
| 26/31/00/27 | 回写 |

---

## 8. 故障速查

| 现象 | 排查 |
| --- | --- |
| 401 JWT | JWKS 不可达；`iss`/`aud` 不一致；时钟；算法非 RS256/ES256 |
| 403 marking | JWT 无 `markings`/`secret`；见 [52]/[55] |
| 仍接受 Bearer `dev` | `AOS_AUTH_ALLOW_DEV` 未关 |
| HA 单点挂 | 配 `AOS_OIDC_JWKS_URLS`（[57]） |

---

## 9. 自测

- [x] claim 别名单测绿  
- [x] 探针无参数时给出用法且可 SKIP  
- [x] 与 [41]/[50]/[57]/[24] 交叉引用  

---

*v1.0*

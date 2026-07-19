# 154 · 生产 IdP 真 JWT · Dev Keycloak 可复现演练（分轨）

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 方案定稿 · 已编码 · 已测试  
> **对齐**：[60](60-生产IdP联调手册.md) · [50](50-Dev-Keycloak联调缓解B-TX3方案.md) · [151](151-macOS打包清单与pack脚本方案.md) · probe-prod-idp.sh

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| 诚实 | **≠** 客户生产 IdP 现场；= 用 Dev KC 拿到 **真 OIDC JWT** 走 60 探针 |
| 分轨 | 不改 `probe-keycloak-oidc.ps1`；并列 `.sh` |
| 最小 | KC 未起 → SKIP exit 0；不起 Full Spoke |

## 1. DoD

| 项 | 验收 |
| --- | --- |
| `probe-keycloak-oidc.sh` | 对齐 ps1：JWKS → password grant → 可选 `/v1/me` |
| `drill-prod-idp-via-dev-kc.sh` | 取 token 后调 `probe-prod-idp.sh --token` |
| 无 KC | 两脚本 SKIP 绿 |
| 60 | 增补「Dev 演练」节 |

## 2. 非目标

- 代客户装生产 IdP  
- 强制 password grant 进生产包  
- 改登录 UI  

## 3. 落点

| 路径 | 改动 |
| --- | --- |
| `154-…` | 本文 |
| `scripts/ci/probe-keycloak-oidc.sh` | 新建 |
| `scripts/ci/drill-prod-idp-via-dev-kc.sh` | 新建 |
| `60` · `26` · `00` | 回写 |

## 4. 自测

```bash
bash scripts/ci/probe-keycloak-oidc.sh
bash scripts/ci/drill-prod-idp-via-dev-kc.sh
```

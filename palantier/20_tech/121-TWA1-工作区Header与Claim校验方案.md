# 121 · TWA.1 工作区 Header 与 Claim 校验（安全收紧）

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 已编码 · 已自测  
> **对齐**：[20a](20a-多用户与工作区整站隔离方案.md) R-ISO-01 · [26 §14 TWA.1](26-AOS目标态开发计划.md)  
> **范围**：仅鉴权绑定租户；不做 Membership / 切换器（TWA.2+）

## 1. 做了什么

| 项 | 实现 |
| --- | --- |
| Claim 优先 | JWT `org_id`/`project_id` 为租户真源 |
| Header 冲突 | 显式 `X-Org-Id`/`X-Project-Id` 与 claim 不一致 → **403 `AUTH_TENANT_MISMATCH`** |
| 生产禁纯 Header | `AOS_AUTH_ALLOW_DEV=0` 且 JWT 无租户 claim → **401 `AUTH_TENANT_CLAIM_REQUIRED`**（忽略伪造头） |
| Dev Bearer | 仍可用 Header（仅 `allow_dev`） |
| 中间件默认值 | **不**把 middleware 注入的 `dev-org` 当成客户端 Header |
| 日志 | `tenant_header_mismatch` / `tenant_bound` / `principal_resolved`（含 org/project） |

## 2. 文件

- `aos-platform/services/aos-api/aos_api/auth.py`
- `aos-platform/services/aos-api/tests/test_twa1_tenant_headers.py`

## 3. 自测

```bash
export PATH="$HOME/tools/micromamba-root/envs/aos/bin:$PATH"
cd aos-platform/services/aos-api
python -m pytest tests/test_twa1_tenant_headers.py -q
# 10 passed（本机无 PG 时不依赖 conftest client）
```

## 4. 风险

- 生产 IdP 必须在 access token 中带 `org_id`/`project_id`（或别名）；否则 401。
- Web 写死 Header 且 JWT claim 不同 → 会 403，由 **TWA.2** 去掉写死并改 `/v1/me` 注入。

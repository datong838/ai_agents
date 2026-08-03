# 228-EC REST/OAuth 最小真实链路方案

> 版本：v1.1 · 2026-08-01
> 状态：通用 REST/OAuth 内核已完成并合入 `m1`；具体平台授权和 endpoint 仍未接入
> 边界：纯通用协议能力，不含任何平台 endpoint、签名、GraphQL、Webhook 或业务写回

## 使用的 Rules

1. 先方案后编码；W2 只拥有本文件列出的新模块与测试。
2. 旧 REST env/mock 路径保持兼容，但必须显式标记 mock。
3. 凭据只存密文，日志/API/审计不得出现明文；生产缺 key 必须失败。
4. 测试使用可注入 transport/clock/sleep/random，不访问真实外网。

## 一、REST GET 最小真实能力

- 声明式请求与 `response_path`；支持 page、offset、cursor 三种分页。
- `max_pages`、`max_items`、重复 cursor 检测和确定性终止。
- workspace+connection 维度限流；429 支持 Retry-After 秒数和 HTTP-date。
- 仅 GET 对 408/429/500/502/503/504 进行有界指数退避+jitter；其他 4xx 不重试。
- 单次 timeout 与总 deadline 同时生效，错误分类稳定且不回显 URL query/header/body。
- 默认只允许 HTTPS；拒绝 loopback、private、link-local、metadata IP，重定向后再次校验。dev 例外必须显式 allowlist。
- 旧 `connector_runtime.py` 只做兼容适配，真实逻辑下沉；不再把单次 sample 伪装成完整同步。

## 二、OAuth Manager

- provider-neutral 支持 authorization_code、client_credentials、refresh_token。
- 唯一键：`(org_id, workspace_id, platform, external_account_id)`。
- `get_valid_access_token()` 在提前刷新窗口内 lazy refresh；`refresh_due()` 供调度器调用。
- refresh 使用 version/CAS 或租约防止惊群；rotation 原子保存新 refresh token。
- `invalid_grant` 进入 `reauth_required`；吊销后不可再取 token。
- 审计事件：exchange/refresh/revoke/reauth 的成功与失败，只记录作用域、token_id、平台、账户、状态、耗时和错误码。

## 三、加密与持久化

- AES-256-GCM，随机 nonce，AAD=`org|workspace|platform|token_id|field`。
- access_token、refresh_token、client_secret 全部密文；篡改、未知版本、错误 AAD、生产缺 key 均 fail-closed。
- 保留旧 KMS API 兼容语义，新增 strict API，避免影响模型供应商凭据。
- 新建专用 OAuth 表；不复用全局 KV 或内存 RefreshToken CRUD。
- `cryptography` 提升为运行时依赖；migration、Router manifest、OpenAPI 产物由总控单点接线。

## 四、独占实现范围

- 新增 `aos_api/rest_connector.py`、`oauth_token_manager.py`、`oauth_token_store.py`、`routers/ecommerce_connectors.py`。
- 修改 `connector_runtime.py`、`kms_crypto.py`、`plugins/connectors/rest-generic/manifest.json`。
- 新增 `tests/test_ec_rest_connector.py`、`test_ec_oauth_token_manager.py`、`test_ec_connector_security.py`。
- OAuth migration 与运行时依赖在 W2 commit 中提交，但总控审查并负责生成物更新。
- 禁止修改 `wave_ext.py`、Ontology、Pipeline、Web/Desktop。

## 五、验收门

必须覆盖三类分页、空页/重复 cursor、429 两种 Retry-After、重试白名单、deadline、SSRF/重定向、并发单次刷新、rotation、invalid_grant、吊销、两租户隔离、密文随机性/AAD/篡改、审计和日志零明文。旧 REST mock/health/probe、插件安装门与既有 credential 测试不得回归。

## 六、实施结果（2026-08-01）

`ab84d24`、`5707612` 已经总控合并为 `da0d83a`，并由 `1d5c4e3` 修正安全扫描夹具。专项 30 tests 连续 3 次通过；最终 full 12/12 通过。`oauth2` capability 在未完成真实 Router/平台接线前不做虚假声明。

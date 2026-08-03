# 2026-08-03 M3-1 专用 SDK Adapter 回归证据

## 1. 结论

M3-1 在 `aos-platform m1@89bbb98` 达到 GREEN。实现只映射既有 Registry、Composition、Installation 能力，没有修改生产页面、通用 API client、后端架构、数据库或状态机。允许进入 M3-2。

## 2. 基线与提交

- 开工基线：`m1@b400f16`
- W1 幂等：`0457cf0`
- W2 错误语义：`0110021`、`cb0ee4e`、`a4b61d5`
- W3 SDK：`cbaf5b9`、`fd30057`
- 总控契约测试：`89bbb98`
- 最终 tree：`1cf65e7c5948d4c5a85a29022500a37c12eebaa8`

## 3. 新增文件

- `apps/web/src/api/assetControl/client.ts`
- `apps/web/src/api/assetControl/client.test.ts`
- `apps/web/src/api/assetControl/idempotency.ts`
- `apps/web/src/api/assetControl/idempotency.test.ts`
- `apps/web/src/api/assetControl/errors.ts`
- `apps/web/src/api/assetControl/errors.test.ts`

## 4. 已验证能力

- Registry list/detail/version GET 使用真实失败关闭 parser。
- Composition resolve/get lock 路径、body、认证和 Idempotency-Key 正确。
- Installation create/list/get 及 submit/approve/reject/apply/verify/rollback 全覆盖。
- 同一命令重试复用相同幂等键，新命令使用新键；键只驻留内存。
- 六个 action 使用强 `If-Match: "etagVersion"`；安装响应 ETag 与 body 不一致时失败关闭。
- 400/401/403/404/409/412/428/500、网络异常和畸形响应结构化归一。
- 404 不区分不可见与不存在；409/412 要求刷新；500 与网络异常标记结果未知。
- 离线 mutation 在 fetch 前阻断，不进入通用离线写队列，并标记为明确未执行。

## 5. 回归结果

| 验证 | 结果 |
|---|---|
| Asset Control 六个测试文件 | 41 passed |
| Web 全量 | 119 files，1822 passed |
| TypeScript | GREEN |
| Web production build | GREEN |
| 后端 Registry/Composition/Installation/M3 OpenAPI | 77 passed，7 个既有 warning |
| `git diff --check` | GREEN |

## 6. 风险与后续门禁

- 幂等键依赖浏览器 Web Crypto `randomUUID`；不支持时明确失败，不降级为弱随机。
- SDK 对 Registry 执行运行时 parser；Composition/Installation 继续依赖冻结 DTO、OpenAPI 契约和 ETag 校验，M3-2 组件测试不得伪造新增字段。
- M3-2 只允许改造真实只读页面状态；不得提前接通 M3-3/M3-4 mutation UI。
- M3-2 必须移除生产路径的隐式 Mock fallback，并验证 loading/empty/error/403/404/分页与刷新回读。

## 7. 分支收口

`m1`、W1、W2、W3、W4 均指向 `89bbb98`，相互 ahead/behind 为 `0/0`，四个 Worker 工作区干净。

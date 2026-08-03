# 228-EC Wave2 总控集成与回归方案

> 版本：v1.1 · 2026-08-01
> 状态：通用平台能力实施、审查、合并与最终回归已完成
> 基线：`m1@e34c66e`

## 使用的 Rules

1. 四 Worker 先读各自 `228-EC-*` 方案再编码。
2. 文件所有权互斥；共享生成物、CI、主计划只由总控修改。
3. 每个 Worker 先专项测试，再由总控逐波合并并运行阶段回归。
4. 只做通用平台能力；所有具体电商平台适配继续阻塞。

## 一、分工

| Worker | 工作树/分支 | 独占任务 | 禁止越界 |
|---|---|---|---|
| W1 | `aos-platform-w1` / `feature/228-ec-w1-contracts` | 公共契约、TaskStatus、Error | Connector/OAuth/Ontology/Pipeline |
| W2 | `aos-platform-w2` / `feature/228-ec-w2-rest-oauth` | REST GET、OAuth、strict crypto | Ontology/Pipeline/具体平台 |
| W3 | `aos-platform-w3` / `feature/228-ec-w3-consistency` | 核心 7 OT、专用一致性 store | Connector/legacy Ontology/Pipeline |
| W4 | `aos-platform-w4` / `feature/228-ec-w4-pipeline` | Pipeline 执行证据与负向门 | Connector/OAuth/Ontology |

共享边界：W2/W3 的 migration 若同时新增，从不同 revision 串行 rebase/调整 down_revision；`pyproject.toml`、Router manifest、OpenAPI snapshot、CI 与主计划由总控审查接线。

## 二、合并顺序与阶段门

1. W1：公共契约专项 + AIP/错误回归；合并后跑 `scripts/ci.sh wave`。
2. W2：REST/OAuth/安全专项 + Connector/KMS 回归；合并后跑 wave。
3. W3：核心模型/一致性/migration 专项 + Ontology/增量回归；合并后跑 wave。
4. W4：Pipeline honesty + Phase5/Builder 回归；合并后跑 wave。
5. 总控统一更新 Router/OpenAPI/CI、文档状态，运行 `scripts/ci.sh full`。

任何阶段失败先修复当前阶段，不用后续阶段结果替代；最终 full 未全绿不得宣告 Wave2 完成。

## 三、完成与继续阻塞

完成只代表通用前置能力可用，不代表淘宝、拼多多、京东、抖音、Shopify、Amazon、微商城或快手已接入。真实平台 endpoint、签名、真实凭据、真实商家数据、GraphQL/Webhook/AWS4/解密/写回须另建新的 `228-` 专项方案。

## 四、最终证据（2026-08-01）

- 合并顺序：W1 `9299b74` → W2 `da0d83a` → W3 `36c4d96`/`a8ea840` → W4 `cda42f3`。
- W3、W4 合并后分别执行 `scripts/ci.sh wave`，均 10/10。
- 最终 `scripts/ci.sh full` 为 12/12：后端 8048 passed / 2 skipped / 2 subtests，Web 1557、Desktop 40、SDK 6，两端 build、Helm、OpenAPI、源码及产物扫描全绿，critical=0。
- 代码仅保存在本地 `m1`，未 push；具体平台能力继续阻塞。

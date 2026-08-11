# AIP-4 E1A 版本化 EvalPack Registry 对账

> 日期：2026-08-11
> 状态：`IMPLEMENTED_GREEN`
> 代码：`aos-platform/m1@134b7e8`
> 方案门：`docs/m1@834b3f2`

## 结果与边界

- 新增 tenant-scoped、RLS/FORCE RLS、append-only 的 `aip_eval_suite_revision`，真实库单 head 升至 `aip4_002`。
- Registry 只接受 exact target/dataset/judge revision+hash；Suite 写入前复验同租户 Dataset revision。
- Dataset manifest 是 metadata-only：必须包含真实 source reference/hash、字段 allowlist、脱敏 Receipt/hash 和 case count；拒绝 Mock/synthetic/demo 与内联业务行。
- 未生成六同事或 37 Logic 假目录；它们继续等待 AIP-6 的真实 Agent/Skill revision。

## 验证

- 契约、迁移、authority store、Registry：20 passed。
- Python compile、`git diff --check`：PASS；Ruff 未安装，不声明通过。
- `org-org/dev-project` Suite revisions=0；`dev-org/dev-project` Suite revisions=0。没有真实业务写入。
- E1A 没有 API/页面，不需要浏览器验收。

## 下一波

E1B 实现不可变 Eval Report 和 runner。报告不保存业务明文；逐项复验 suite/target/dataset/judge/artifact exact refs，漂移或 judge/解析失败必须使 Run failed，不能产出可过门报告。

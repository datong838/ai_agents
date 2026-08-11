# AIP-4 E1B 精确引用 Runner 与不可变 Report 对账

> 日期：2026-08-11
> 状态：`IMPLEMENTED_GREEN`
> 代码：`aos-platform/m1@7e255ed`

## 本波结果

- 新增 RLS/FORCE RLS、append-only `aip_eval_report_revision`，真实库单 head `aip4_003`。
- Runner 从版本化 Registry 读取 Suite；逐项复验 Artifact 引用与实际内容 hash、target exact ref、judge exact ref。
- Report 仅持久化 case/result hash、detail code、耗时、计数和 exact refs，不持久化输入、期望或输出业务明文。
- 任一引用/内容漂移使 Run 进入 failed，且不生成 Report；通过或未通过阈值的正常评测均是 succeeded Run，门控结论由不可变 Report 表达。

## 验证与诚实边界

- E0A～E1B 组合：28 passed；Python compile、`git diff --check` PASS；Ruff 未安装。
- `org-org/dev-project` suites=0/reports=0；`dev-org/dev-project` suites=0/reports=0；无业务写入。
- E1B 没有 API/页面，不做浏览器 UI 验收。
- 历史 `tests/test_evals_engine.py` 7 项 FORCE RLS 夹具 RED 尚未消除，明确归入 E1C；因此仍不宣称全后端 GREEN。

## 下一波

E1C 在不放松 RLS 的前提下修正旧 Logic Eval compatibility 测试夹具和生产边界，恢复或替代 7 项 RED，并标明旧 API 只读/兼容职责与新 Registry/Runner 写链。

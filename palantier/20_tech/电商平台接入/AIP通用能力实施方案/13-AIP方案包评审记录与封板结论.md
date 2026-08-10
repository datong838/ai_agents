# AIP 方案包评审记录与封板结论

> 状态：**评审通过 · v1.0**
> 日期：2026-08-10
> 范围：`00`～`12` 全部 AIP 通用能力方案；仅批准方案基线，不授权编码。

## 1. 评审方法

本轮执行三次审查：

1. 事实审查：对照 `aos-platform/m1`、API 回读和 19 个浏览器路由，区分真实、部分实现、静态、Mock 和空态。
2. 可执行性审查：逐份检查权威边界、canonical 模型、状态机、租户、RLS、幂等、并发、失败语义、回滚、文件边界和验收证据。
3. 交叉审查：核对 AIP-0～10 依赖、O1/M1～M5 复用、六数字同事、行业 Wiki、FDE、内容官和平台专项准入门。

## 2. 第一轮问题与整改

| 编号 | 问题 | 整改 |
|---|---|---|
| R01 | AIP-10 的 D4/D5 容易重开已封板 O1 | 改为 AIP-FDE EvidencePack 与 AIP 通用场景独立证据 |
| R02 | 阶段只有线性表，缺强依赖和可并行边界 | 增加 AIP-0～10 DAG 与公共契约 owner |
| R03 | 多份方案缺 RLS、迁移、并发和错误语义 | 补双租户、CAS/lease、expand/backfill/cutover、统一错误码 |
| R04 | Agent/Skill 导入和卸载生命周期不足 | 补 Template/Instance/ImportJob/Handoff 生命周期和卸载 Receipt |
| R05 | Action 超时、重复执行和补偿边界不足 | 补 unknown/reconcile、kill switch、职责分离和受控 compensation |
| R06 | Eval、观测和成本真值可能混用估算 | 补 measured/estimated 分离、迟到事件、AdjustmentEvent 和撤回语义 |
| R07 | 记忆共享、删除和向量索引 authority 不清 | 补三类 scope、删除最小留痕、索引非真源和 fail-closed |
| R08 | 工作台只描述布局，缺状态与可访问性 | 补七类状态、Focus Mode、SavedExploration、键盘和多视口门 |
| R09 | 内容官 C0～C5 与 Capability C0/C1/C2 冲突 | 重命名 Content-0～5，补 Job/Session/授权撤回语义 |
| R10 | 六同事场景缺职责矩阵和调度门 | 补覆盖矩阵、每小时调度条件、真实数据/新鲜度/证据要求 |
| R11 | `CustomerLite` 可能形成 Customer 平行模型 | 冻结为 canonical Customer 的字段受限读投影/兼容别名 |
| R12 | AIP-5/6 的并行起点早于审批/Eval 主链退出 | 调整为 AIP-4 后与 AIP-7 并行，AIP-8 等待三者共同退出 |

## 3. 第二轮交叉复审

| 检查门 | 结论 | 说明 |
|---|---|---|
| 架构唯一性 | PASS | 复用 O1、M1～M5，不建第二本体、Action、Wiki、Task 或 FDE 控制面 |
| 租户隔离 | PASS | 真实范围固定 `org-org/dev-project`；scope 取认证上下文；`dev-org` 仅负向 canary |
| 状态与并发 | PASS | Task、Agent、Action、Memory、Job 均定义状态/版本；CAS、lease、幂等和 unknown 已覆盖 |
| 安全与外部副作用 | PASS | R2+ 均需 Draft/Approval/Receipt；R4 默认禁止；超时先 reconcile |
| 真实数据原则 | PASS | 无数据为空，禁止 Mock/fallback 冒充；达人、控价首期只读/草稿 |
| 页面交互 | PASS | 状态时序、Focus Mode、多视口、可访问性、无静默 no-op 已进入验收门 |
| 证据与可观测 | PASS | revision/hash、source/freshness、Lineage、UsageReceipt 和 EvidencePack 已统一 |
| 回滚与删除 | PASS | 回滚只处理本 run 所有资源；历史 Receipt/Lineage 不被破坏；外部补偿是新 Action |
| 范围控制 | PASS | 不编码、不接具体平台、不重开 O1、不进入微商城工作台细分 |

## 4. 最终封板结论

`00`～`12` 方案在当前目标范围内评审通过，可作为后续 AIP-0 开发清单的上位基线。通过条件不包括代码、数据迁移或页面已经实现。

下一步只能是：生成并评审 `AIP-0-真值与公共契约冻结开发清单`，其中必须列出实际修改/新增文件、OpenAPI diff、迁移/回滚、测试矩阵、浏览器步骤、证据目录和单一 owner。该清单再次明确批准前，保持不编码。

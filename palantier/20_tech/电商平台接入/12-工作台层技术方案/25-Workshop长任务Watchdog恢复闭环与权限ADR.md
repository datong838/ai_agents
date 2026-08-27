# Workshop 长任务 Watchdog 恢复闭环与权限 ADR

> 日期：2026-08-14
> 状态：`V2.2_IMPLEMENTED_REVIEWED_AND_ACCEPTED_GREEN`
> Task：`workshop-watchdog-recovery-loop-20260814`
> 适用范围：仅 `aos-platform-w2-workshop` / `w2-workshop`，不改变 AIP Watchdog、业务能力、租户数据或 m1 CAS 边界。

## 1. 事故事实与根因

2026-08-14 的 Workshop 长任务在最后一次实质工作后约 5 小时 32 分钟未继续产生开发进展。Watchdog 在停用旧逻辑前共尝试恢复 50 次，但恢复 turn 处于 `workspace-write / network=false / approval=never`：无法写 linked worktree 实际位于主仓的 Git index、无法写共享 docs Receipt/方案目录，也无法连接本机 PostgreSQL。

同时，当前 transcript 的 assistant 终态实际使用 `phase="final_answer"`，旧实现只识别 `phase="final"`。因此即使恢复 turn 已产生完整 final，仍被误判为 `resume exited 0 without a visible final` 并持续重试。

只兼容 `final_answer` 仍不充分：退出码 0 + final 只能证明 Codex turn 结束，不能证明恢复后完成了状态审计、继续推进了任务，或基于真实门禁做了安全阻断。

## 2. 安全目标

完整闭环必须可独立证明：

```text
检测疑似断流
  → 防重入与静默期判定
  → 创建本次 recovery episode
  → 以 Workshop 专属最小权限唤醒同一 thread
  → 恢复 turn 回读 Git/Receipt/Lease/方案/依赖
  → 继续实际安全任务，或形成结构化 safe-blocked/completed/reentry-noop
  → 当前 episode 的结构化 Ack + 新 final_answer/final 同时出现
  → 标记 outcome 并停止该 episode 重试
```

任何旧 final、旧 Ack、旧 `last_recovered_at`、单独的退出码 0、自由文本“已恢复”或计划状态均不得判绿。

## 3. 状态机

### 3.1 检测态

- `idle`：最新用户消息已有更新的 `final` 或 `final_answer`；不恢复。
- `turn-running`：最新 `task_started` 尚无对应 `task_complete`；不并发恢复。
- `tool-running`：存在未完成工具调用且未超过静默阈值；不恢复。
- `live`：transcript 最近仍有活动；不恢复。
- `recover`：最新用户消息无终态、turn 已结束、无活跃工具且超过静默期。

### 3.2 Episode 结果态

- `resumed-progress`：恢复 turn 完成真实状态审计并产生可核验安全进展；停止本 episode 重试。
- `safe-blocked`：依赖、Lease、权限或安全门明确阻断；记录稳定 reason/fingerprint 并以 final 收口，停止重试，直到 transcript 出现新用户活动或配置 revision 变化。
- `completed`：长任务全部完成；禁用 Watchdog。
- `reentry-noop`：唤醒与正在运行的 turn/Lease 发生竞态；不做副作用并停止本 episode 重试。
- `transport-failed`：Codex 请求失败且没有当前 episode Ack/新 final；只做有上限退避，达到阈值转 `paused-failure`，禁止无限空转。
- `protocol-failed`：已有新 final 但 Ack 缺失、过期或错配；停止重试，等待协议修复，不能把自然语言 final 当成功。
- `outcome-uncertain`：已有当前 episode Ack，但没有新 final 或进程异常退出；停止盲重试，先 reconcile Ack 所列 evidence，防止重复副作用。
- `paused-failure`：环境或传输连续失败达到上限；保留现场并发出本地告警，等待用户活动或配置变化后创建新 episode。

## 4. 结构化 Recovery Ack

恢复 turn 必须为当前 `recovery_episode_id` 写入 mode-0600 的 sidecar Ack。Ack 至少包含：

- schema、episode、thread、project root、expected/actual branch；
- outcome：`resumed-progress|safe-blocked|completed|reentry-noop`；
- 权限自检：worktree、Git common dir、技术方案、Receipt、loopback network；
- authority revision、HEAD before/after、当前 Task、next Task；
- reason code、blocker fingerprint、evidence refs；
- 写入时间，必须晚于本 episode attempt。

Watchdog 只在以下条件同时成立时接受终态：命令退出 0；同一 transcript 出现比 attempt 前更新的 `final` 或 `final_answer`；Ack episode/thread/root 完全匹配；Ack 时间属于当前 attempt；outcome 与必填字段自洽。`resumed-progress/completed` 必须位于 expected branch；分支不一致只允许形成带 `BRANCH_MISMATCH` fingerprint 的 `safe-blocked/reentry-noop`，禁止执行副作用。

自由文本不参与成功判定。

## 5. 权限模型

恢复命令使用 `workspace-write`，通过明确 writable roots 授予：

1. `aos-platform-w2-workshop`；
2. 主仓 `.git`（仅由项目 Rules 限定为 w2 安全提交，禁止 reset/rebase/force push）；
3. `12-工作台层技术方案`；
4. Task/Delivery Receipt 与 memory events；
5. Workshop Watchdog 专属状态目录。

同时启用恢复 turn 的网络访问，以连接 ChatGPT/Codex、本机 loopback API、测试数据库和浏览器服务。authority、01/06、Prime 仍只允许 m1 串行 CAS；外部生产写、高风险业务动作、远端推送与正式发布不因本 ADR 自动开放。

`memory-status/validate` 会在 memory 根创建 `.memoryctl.lock`，而 Codex `--add-dir` 只能授权目录，不能单独授权锁文件。因此恢复 sandbox 的技术 writable root 包含 memory 根；业务授权仍严格限定为锁、Task/Delivery Receipt 与 events。`authority.json`、01/06、Prime 投影在 w2 保持禁止修改，只有 m1 串行 CAS 可推进。该边界同时由 AGENTS、resume prompt、Task Receipt 和交付审查约束。

## 6. 防重试风暴

1. 每次 launchd tick 只允许一次 `codex exec resume`，不在同一 tick 内连续请求 ChatGPT。
2. 纯 transport 失败按可配置序列渐进退避：5、10、15、30、60、120 分钟；序列耗尽后以 120 分钟为上限低频重试。
3. 第三次 transport 失败不得立即熔断；默认累计 12 次纯 transport 失败后才进入 `paused-failure`，其时间窗约覆盖 14 小时。新用户活动或配置 revision 变化可开启新 episode。
4. 有效 `safe-blocked`、`completed`、`reentry-noop`、`resumed-progress` 均清零 retry 并停止本 episode。
5. `paused-failure/protocol-failed/outcome-uncertain` 只有新用户消息或配置 revision 变化才允许创建新 episode；旧 Ack 不得复用。
6. LaunchAgent 可继续做轻量检测，但 paused/terminal 状态不得调用 `codex exec resume`。

## 7. 实施文件

- `scripts/long-task-watchdog/watchdog.py`：phase 兼容、episode/Ack、权限命令、失败上限、结果状态机。
- `scripts/long-task-watchdog/test_watchdog.py`：红测、状态机、权限命令、过期 Ack、重试停止、分支/数据保护。
- `scripts/long-task-watchdog/README.md`：运行协议、配置、故障处置。
- `~/.codex/long-task-watchdog-workshop/config.json`：Workshop 独立权限根、branch、Ack、失败上限与 prompt。
- `~/Library/LaunchAgents/com.aos.codex-long-task-watchdog-workshop.plist`：继续使用独立 config/state/lock/log，不与 AIP 共用。

## 8. 验收矩阵

### 必须 GREEN

1. `final` 与 `final_answer` 都能终结 active 判定；commentary 不能。
2. 退出 0 但无新 final、无 Ack、Ack 过期、episode/thread/root/branch 错配均不判恢复。
3. `resumed-progress`、`safe-blocked`、`completed`、`reentry-noop` 四 outcome 均停止当前 episode 重试。
4. transport 连续失败达到上限进入 `paused-failure`，后续 launchd tick 不再调用 runner。
5. 新用户活动或配置 revision 变化可解除旧 pause，但不得复用旧 Ack。
6. 恢复命令明确包含 Workshop cwd、workspace-write、必要 add-dir 与 network 配置，不包含 API Key 或 `--dangerously-bypass-approvals-and-sandbox`。
7. 活跃 turn、活跃工具、Lease/branch 不一致均 0 副作用。
8. 隔离端到端 fixture 完成两条完整链：`检测→唤醒→resumed-progress→停止重试` 与 `检测→唤醒→safe-blocked→停止重试`。
9. 对真实当前 thread 只执行 idle/turn-running no-op smoke，不故障注入、不创建并发恢复 turn。
10. 现有 `w2-workshop` HEAD、工作树和业务数据库在验收前后保持守恒；本波只允许 Watchdog 代码、方案、Receipt 与专属本机配置变化。

### 实现前复审

- R1：补充 Ack 已写但 final 丢失的 `outcome-uncertain`，禁止以 transport retry 重复可能已发生的提交或数据库动作；`CLOSED`。
- R2：第一条用户可见消息只允许声明“检测到中断，正在恢复核验”；只有 `resumed-progress/completed` 可在证据闭合后称“已恢复”，`safe-blocked` 必须称“已触发并安全阻断”；`CLOSED`。
- R3：分支错配不能简单进入 transport retry；允许结构化安全阻断但不允许进展态；`CLOSED`。

复审结论：`APPROVED_FOR_IMPLEMENTATION`。

## 9. 回滚

- 保留旧 config/state 备份的 hash 和路径；配置升级失败即恢复旧 LaunchAgent 但将 `enabled=false`，避免旧逻辑重试风暴。
- 代码回滚只回退本波 Watchdog 提交，不触碰 W1-A～D 提交。
- Ack 与 state 属本地可重建控制状态，不反写 authority，不删除历史 Delivery Receipt。

## 10. 编码门结论

本 ADR 通过实现前复审后，允许按 Red-Green-Refactor 修改第 7 节文件。正式完成必须同时具备代码测试、隔离闭环、真实 no-op smoke、LaunchAgent 回读、Delivery Receipt 和安全提交；缺任一项不得宣称“下次一定能恢复”。

## 11. 实现后复审与验收证据

### 11.1 第一轮实现后复审

- 已兼容 transcript 的 `final` 与 `final_answer`，并用 `post_final_activity` 防止旧恢复 turn 的终态污染正在工作的原 turn。
- 已引入 current-episode Recovery Ack；退出码 0、自由文本与旧 final/Ack 均不能独立判绿。
- 已限制恢复命令只能使用 `workspace-write`，拒绝 `danger-full-access`、文件系统根目录和用户主目录作为 writable root；命令不含 bypass sandbox 参数。
- 已将纯传输失败限制为三次；`safe-blocked/completed/reentry-noop/resumed-progress` 均终止当前 episode。

第一轮复审发现：`outcome-uncertain` 虽在单次调用中终止，但下一轮 tick 仍可能再次进入 recover，存在重复副作用风险。结论：`REMEDIATION_REQUIRED`。

### 11.2 第二轮整改与复审

- `outcome-uncertain` 与 `protocol-failed` 已和 `paused-failure` 一样形成稳定等待态；相同用户消息和配置 revision 下后续 tick 不再调用 runner。
- 新用户活动或配置 revision 变化才解除等待；新 episode 开始前删除旧 Ack，禁止跨 episode 复用。
- 旧 `state.json` 保留 50 次失败事故现场；LaunchAgent 改用独立 `state-v2.json`，新状态从 0 次尝试开始，未破坏历史证据。

第二轮复审结论：`ACCEPTED_GREEN`。

### 11.3 新鲜验证

1. 单元与状态机测试：27/27 GREEN，覆盖 `final_answer`、防重入、四类成功/安全 outcome、错 episode/thread/root/branch、无 Ack、Ack 无 final、失败上限与宽权限拒绝。
2. 子进程完整闭环：真实启动隔离 fake Codex 子进程，完成 `检测→受限唤醒→写 current Ack→final_answer→resumed-progress→下一 tick idle`；业务哨兵文件前后不变。
3. 真实 Codex 恢复权限探针：以与 Watchdog 相同的 `workspace-write + add-dir + network` 启动隔离 Codex，worktree、主仓 Git common dir、技术方案目录、memory 目录、专属状态目录和 loopback bind 全部 GREEN，实际分支为 `w2-workshop`。
4. LaunchAgent 回读：已加载 `state-v2.json`；连续真实 tick 为 `live/live/tool-running`，`total_attempts=0`，证明当前 turn 活跃时不会并发唤醒。
5. 配置/语法/一致性：JSON 与 plist 校验 GREEN，Python compile GREEN，`git diff --check` GREEN；`memory-validate=GREEN`，所有强一致投影 CURRENT。

验收边界：没有故意中断当前真实开发 turn，也没有连接或修改业务数据库；真实断流时是否能完成实际 W1 任务仍须由未来自然故障 episode 的 Ack、final 与 Delivery Receipt 共同证明，不能由本次测试预先承诺。

## 12. V2.1 长时服务故障退避整改

### 12.1 触发原因

V2 使用三次连续 transport 失败后立即 `paused-failure`。该策略能够抑制空转，但对 ChatGPT 服务端持续数十分钟乃至数小时的故障恢复窗口过短。用户裁决改为渐进衰减，不把第三次网络失败误判为需要永久人工介入。

### 12.2 决策

- `retryScheduleSeconds=[300,600,900,1800,3600,7200]`；第 N 次纯 transport 失败选择第 N 个延迟，超过序列长度后保持最后一个延迟。
- `maxTransportFailures=12`；第 12 次仍无 Ack/新 final 才转 `paused-failure`。按默认序列，从第一次失败到最终暂停约 14 小时。
- 每个 tick 最多发起一次恢复请求；取消旧版“首次 episode 立即重试两次”，避免服务端故障时突发双请求。
- 只有没有当前 Ack、没有新 final 的请求失败才累计 transport failure。`protocol-failed/outcome-uncertain` 立即停止盲重试；四类结构化终态立即停止本 episode。
- state 记录 `retry_delay_seconds/next_retry_at/consecutive_failures`，使重启后退避仍可回读，不靠内存计时。

### 12.3 实现门

先用红测证明 5/10/15/30/60/120 分钟顺序、第三次不熔断、封顶 120 分钟、12 次后暂停、成功/安全阻断即时停止，再最小修改状态机与 Workshop 专属配置。AIP Watchdog 不在本次范围。

### 12.4 实现后复审

- 红测先复现旧实现一次 tick 双请求和第三次熔断；整改后每 tick 恢复调用严格为 1。
- 29/29 测试 GREEN：精确验证 300/600/900/1800/3600/7200 秒序列、120 分钟封顶、第三次继续、配置上限暂停、无效 schedule 在调用 runner 前失败关闭，以及 V2 全部 Ack/final/分支/权限/数据保护回归。
- Workshop 本机配置已升级为 `workshop-watchdog-v2.1-20260814`、`maxTransportFailures=12`；LaunchAgent 连续 tick 仍为 `live`，`total_attempts=0`。
- 复审结论：唤醒事实与恢复 outcome 仍严格分离；长时 ChatGPT transport 故障改为渐进衰减，不会形成 5 分钟空转风暴，也不会在第三次过早永久熔断。`ACCEPTED_GREEN`。

## 13. V2.2 跨任务依赖 Lease 心跳

### 13.1 触发场景

Workshop 已用完并释放 Alembic migration Lease 后，AIP 随即取得 `aip-w2d1-migration-store-20260814`。此时 Workshop 后续任务若依赖 migration head 或 AIP 交付，应安全停在依赖门；但原 Watchdog 只识别“未完成 turn 的异常静默”，对“当前 turn 已正常收口、等待另一任务释放共享资源”只会返回 `idle`，无法在依赖解除后唤醒同一 thread。

### 13.2 设计裁决

1. 监控与执行分离：Watchdog 只读解析 `leases.json`，不抢 Lease、不执行迁移、不修改代码或真实租户数据。
2. 配置声明 `dependencyWatch`：精确 `leasesPath`、需等待的 scope token、忽略自身 task/owner；不扫描 w1-aip 工作树或未提交内容。
3. 发现匹配的活动 Lease 时记录稳定 fingerprint 与 `dependency_wait_armed=true`，返回 `dependency-blocked`；每 5 分钟继续只读检查，但不调用 Codex、不重复发消息。
4. 只有曾经 armed 且本轮匹配 Lease 变为 0 时才产生一次 `dependency-released` recovery episode。若 transcript 仍有 active turn、未完成 tool/task、Git/评审新冲突，则 no-op，保持 armed，待下一 tick 重核。
5. dependency release 唤醒后的第一条用户可见消息固定为：“依赖 Watchdog 检测到迁移 Lease 已释放，正在重新核验后继续”。该句只证明依赖变化触发了核验，不证明恢复成功。
6. 恢复 turn 必须重新读取 authority、01/06、Git、最近 Delivery Receipt、memory status/validate/gate 与全部 Lease，再按 `resumed-progress|safe-blocked|completed|reentry-noop` 写 current episode Ack。只有 `resumed-progress/completed` 才算有效续跑。
7. 一次 release episode 得到 Ack+新 final 后立即 disarm；`safe-blocked/reentry-noop` 同样停止该 episode，不因迁移 Lease 已释放而空转。若后续再次观察到新的匹配 Lease，才允许重新 arm。
8. LaunchAgent `StartInterval=300`。原断流检测仍保留自身 5/10/15/30/60/120 分钟退避；依赖阻断轮询不累计 transport failure。

### 13.3 红绿验收门

- 活动 migration Lease：连续 tick 均为 `dependency-blocked`，runner 调用 0，用户消息 0。
- Lease 释放但当前 turn/task/tool 仍运行：`turn-running/tool-running/live`，runner 调用 0，armed 不丢失。
- Lease 释放且当前对话 idle：只创建一次 dependency episode；prompt 精确包含固定首句与全量重核清单。
- 新活动 Lease 在 resume 前出现：恢复 turn 必须 `reentry-noop/safe-blocked`，不做副作用。
- Ack+新 final 后下一 tick 为 idle，不重复唤醒；无 Ack、错 final 或 transport failure 继续沿用 V2.1 安全状态机。
- 配置、状态和 LaunchAgent 回读为 ACTIVE/300 秒；worktree、Git common dir、业务数据库哨兵与对方 w1-aip 状态前后守恒。

实现前复审：该扩展只增加依赖检测输入与一次性唤醒触发，不授予任何共享资源或业务副作用权限；与原 episode Ack 终态协议正交，`APPROVED_FOR_IMPLEMENTATION`。

### 13.4 实现后复审

- 红测先稳定复现五个缺口：活动 Lease 未 arm、释放后 idle 不唤醒、空退避 schedule 不失败关闭、第四次延迟仍为 20 分钟、transport failure 达到上限不暂停。
- `dbbcc4d` 以精确 `scope_tokens` 只读匹配 `leases.json`，新增 `dependency-blocked/dependency-released` 触发、armed/fingerprint/task ids 状态和一次性 dependency episode；未新增 Lease acquire、迁移、Git 写或业务数据接口。
- dependency-release prompt 固定首句，并强制重新核验 authority、01/06、Git、Delivery Receipt、memory 三门和全部 Lease；当前 turn/tool/task 运行时保持 no-op。
- 同波恢复被合流覆盖的 V2.1：5/10/15/30/60/120 分钟退避与 12 次 transport failure 暂停门重新进入实现和测试，避免文档与线上代码漂移。
- 33/33 单元与隔离闭环 GREEN；包括连续 Lease 阻断 runner=0、释放时活跃 turn 不唤醒、idle 释放只唤醒一次、固定首句、Ack+final 后 disarm、非匹配 AIP Lease 不 arm、V2.1 全回归。
- Workshop 本机配置升级为 `workshop-watchdog-v2.2-20260814`；LaunchAgent 已重载，`StartInterval=300`、`last exit code=0`。真实现场只读识别 `aip-w2d1-migration-store-20260814`，状态 `dependency_wait_armed=true`、`last_decision=turn-running`、`total_attempts=0`，证明当前对话运行时未并发唤醒。
- 文件 SHA-256、测试、配置、LaunchAgent 与现场状态见 `.evidence/workshop/2026-08-14-watchdog-dependency-lease-heartbeat-v22-delivery-receipt.json`。

复审结论：`ACCEPTED_GREEN`。它只保证依赖释放后触发一次重新核验；未来真实 release episode 仍必须以当次 Ack+新 final+Delivery Receipt 证明有效续跑，不能提前承诺“必然恢复成功”。

## 14. V2.3 非 Lease 外部事实变化心跳

### 14.1 缺口

V2.2 只识别精确 Lease scope。Workshop 当前还会等待 Data/Adapter Delivery Receipt、AIP runtime-control API 合入和 authority CAS 等非 Lease 事实；若这些任务在两个 5 分钟 tick 之间完成并释放 Lease，单看当前 `leases.json` 可能无法知道阻塞事实已经变化。

### 14.2 设计裁决

1. 新增 `fact_watch`，只接受显式绝对路径；配置只放 authority、Delivery Receipt 目录等非秘密控制事实，禁止业务数据目录、`.env`、Token/Cookie 或 w1-aip 工作树。
2. 文件按内容 SHA-256；目录按“相对路径 + 文件内容 SHA-256”确定性聚合。只存最终 fingerprint，不把文件正文写入 state/log/prompt。
3. 首次检查只建立 baseline，不唤醒。当前 turn/tool/task 活跃时若事实变化，只更新 baseline，不创建并发恢复副本。
4. 仅当对话 idle/recover、没有精确阻塞 Lease，且 fingerprint 相对上一 baseline 发生变化时，创建一次 `dependency-fact-changed` episode；第一句固定为“依赖 Watchdog 检测到外部交付事实已变化，正在重新核验后继续”。
5. episode 创建前立即把 baseline 推进到新 fingerprint；无论最终 `resumed-progress/safe-blocked/completed/reentry-noop`，同一事实变化不重复唤醒。后续只有新的 fingerprint 才能再次触发。
6. 恢复协议仍必须全量核验 authority、01/06、Git、Delivery Receipt、memory 三门与全部 Lease；事实变化不是依赖已 GREEN 的证明。

### 14.3 红绿验收门

- 首次 baseline、内容不变、活跃 turn 变化、存在精确 Lease 时 runner=0；
- idle 且 authority/Receipt 内容变化时单次唤醒；prompt 固定首句；下一 tick 不重复；
- 目录 fingerprint 与文件创建、修改、删除均确定性相关，符号链接和不可读路径失败关闭；
- V2/V2.1/V2.2 全部 33 项回归继续 GREEN；本机配置、LaunchAgent 与真实 no-op 回读完成后才能标记实现通过。

实现前复审：该能力只观察控制事实变化，不判断依赖通过、不读取业务数据、不扩大恢复权限，`APPROVED_FOR_IMPLEMENTATION`。

## 15. V2.4 人工重入与恢复进程竞态收敛

### 15.1 现场缺口

2026-08-14 16:06，V2.3 真实检测到 AIP 迁移 Lease 释放并启动一次 `codex exec resume`。恢复进程尚未写入当次 Recovery Ack 或新 final 时，用户手工进入同一对话。旧状态机只能把被终止的恢复请求记为 `transport-failed`，不能证明后续 5 分钟 tick 一定会消费同一 release episode；存在人工已经接管、Watchdog 仍在稍后重复恢复的竞态。

### 15.2 设计裁决

1. transcript 解析只额外产生布尔事实 `latest_user_is_watchdog`，通过固定恢复协议标记识别 Watchdog 自己注入的 user prompt；不得把用户正文写入 state、log 或 Receipt。
2. 当 episode 为 `dependency-released` 或 `dependency-fact-changed`，状态为 `attempting/transport-failed`，且在 `last_attempt_at` 之后出现新的、非 Watchdog user message 时，判定 `manual-reentry`。
3. `manual-reentry` 是本地安全终态，不等于恢复成功：清零 transport retry，消费当前依赖变化事件，释放 `dependency_wait_armed`，记录时间与 episode，但不写 `last_recovered_at`、不伪造 Ack/final。
4. Watchdog 自己注入的恢复 prompt 不得触发 `manual-reentry`；纯 transport failure 仍按 V2.1 的 5/10/15 分钟序列重试。
5. 当前真实人工 turn 活跃时 runner 调用必须为 0；不得终止或修改用户当前工作，不得触碰 Git、迁移或真实租户数据。

### 15.3 红绿验收门

- dependency release 首次恢复失败后，人工 user message 使下一 tick 返回 `manual-reentry`，runner 不再调用，retry 清零且 release disarm；
- 相同路径若最新 user message 带固定恢复协议标记，则不作为人工接管，仍遵守原退避；
- 普通活跃 turn、无 episode、普通断流 episode均保持原语义；
- V2～V2.3 全量回归、Python compile、真实当前 thread no-op、LaunchAgent 300 秒回读全部 GREEN。

实现前复审：该整改只关闭重复恢复竞态，不扩大唤醒条件或执行权限，`APPROVED_FOR_IMPLEMENTATION`。

## 16. V2.5 `resumed-progress` 后受控连续续跑

### 16.1 现场缺口

V2.4 已在真实 episode `dependency-fact-1786765415359` 完成一次有效恢复：新提交、Delivery Receipt、current Ack 与 `final` 同时存在，Ack 为 `resumed-progress` 且 `next_task=W3-09`。然而状态机把四种 Ack outcome 都当作本 episode 的终点；下一 tick 看到 transcript 已有 final 后只返回 `idle`。这能停止重试，却错误地把“一个波次收口”当成“96 项长目标完成”，造成恢复一波后再次停滞。

### 16.2 设计裁决

1. `resumed-progress` 仍终止当前 episode 的 transport retry，但若 Ack 含非空 `next_task`，额外建立本地 `continuation_armed=true`，记录来源 episode、next task、Ack 时间和最早续跑时间。
2. continuation 默认等待一个 LaunchAgent 周期（300 秒）；等待期内如出现普通用户消息，视为人工接管并消费 continuation，runner=0。
3. 只有 transcript idle、无 turn/tool/task、无精确 dependency Lease blocker、分支与权限配置仍有效，且最早续跑时间已到，才创建一次全新的 `continuation` episode。
4. continuation prompt 第一条用户可见消息固定为“外部 Watchdog 检测到长任务仍有后续项，正在重新核验后继续。”；恢复 turn 必须和其他 trigger 一样回读 authority、01/06、Git、Receipt、memory gate 与全部 Lease。
5. 新 episode 仍必须形成 current Ack + 新 final。`resumed-progress` 可再次 arm 下一个 continuation；`completed`、`safe-blocked`、`reentry-noop`、`protocol-failed`、`outcome-uncertain` 和 `paused-failure` 全部 disarm，禁止空转。
6. `next_task` 只是导航提示，不是授权或依赖 GREEN 证明；每次恢复仍选首个真实依赖满足且 scope 不冲突的安全任务。若没有可执行任务，必须 `safe-blocked`，不能用方案占位伪造进展。
7. continuation 只恢复同一 thread、同一 `w2-workshop`，不创建新 thread，不抢 Lease，不读取 w1-aip 未提交内容，不扩大 sandbox、数据库、租户或外部副作用权限。

### 16.3 实现前两轮复审

- R1 发现直接把 `resumed-progress` 当成下一 tick 的 recover 会在 final 后每 5 分钟重复唤醒。整改：引入 source episode + one-shot armed + earliest-at，创建新 episode 时先消费旧 armed 状态。
- R2 发现用户在 300 秒窗口内人工继续时仍可能与 continuation 竞态。整改：记录 Ack final/user cutoff；出现更新的非 Watchdog user message即 `continuation-manual-reentry`，runner=0 并 disarm；active turn/tool/task 永远优先 no-op。

实现前复审结论：`APPROVED_FOR_RED_GREEN_IMPLEMENTATION`。必须先增加红测证明当前实现“resumed-progress 后永久 idle”，再最小修改状态机；真实当前 turn 只做 no-op smoke，不人为中断或并发恢复。

### 16.4 实现后两轮复审

- R1：红测稳定复现旧状态机未写 `continuation_armed`、用户重入仍返回 `live` 的缺口；实现后 `resumed-progress + next_task` 写 one-shot armed/ready-at/source episode，新 episode 创建前先消费旧 armed，`completed` 立即 disarm。
- R2：组合审查发现还必须证明精确 Lease 优先于 continuation。新增测试后，活动 migration Lease 返回 `dependency-blocked`、runner=0 且 continuation 保持 armed；普通用户消息返回 `continuation-manual-reentry` 并 disarm；Watchdog 自己的恢复 prompt 不被误判为人工接管。

新鲜验证：Watchdog 42/42 单元与隔离状态机测试 GREEN，Python compile 与 `git diff --check` GREEN；本机配置升级为 `workshop-watchdog-v2.5-20260815`，`continuation_watch.enabled=true/delay_seconds=300`。真实当前 thread no-op smoke 为 `tool-running / active_turn_detected=true`，`total_attempts` 前后均为 12；LaunchAgent 仍为 300 秒、last exit code 0。未故障注入当前任务，未来首个真实 continuation 仍须由当次新 episode、current Ack、新 final、提交/Receipt 共同证明，不能提前把测试承诺成现场成功。

实现后复审结论：`ACCEPTED_GREEN_WITH_FIRST_REAL_EPISODE_PENDING`。该结论只关闭“有效恢复一波后永久 idle”的机制缺口，不改变任何业务 Task 的依赖门或副作用权限。

## 17. V2.6 W2 数据依赖只读事实探针

### 17.1 缺口与边界

W1-10 已 GREEN 后，W2-00 的真实阻断转为 12 条 Pipeline 最新运行、注册、OT/query 数量与 P08/P10 合同门。V2.3 只监控 authority 和 Delivery Receipt；若 Cron 或 Data/Adapter 修复只改变 PostgreSQL durable fact、尚未形成 Receipt，Watchdog 不会感知，当前 thread 可能在数据门已经变化后仍长期静默。

本扩展只增加确定性只读 fingerprint 输入，不让 Watchdog 触发 Pipeline/Schedule、抢 Lease、修改数据库、读取业务属性正文或判断依赖 GREEN。探针只聚合：12 条 pipeline 是否注册、每条最新 durable run 的 status/errorCode/rowsWritten/startedAt、`ecom_object` 与 `obj_instance` 分 OT 数量及 canary 聚合；不输出 errorMessage、对象 properties、PII、Secret、DSN 或凭据。

### 17.2 设计裁决

1. `fact_watch.probes[]` 只接受结构化 `argv`，使用 `subprocess.run(..., shell=False)`；可执行文件与 cwd 必须为绝对路径，cwd 必须位于 `project_root` 内，禁止环境覆盖。
2. 子进程使用既有 sanitized environment，删除常见 API Key；超时与 stdout 上限均为小正整数。非零退出、超时、超限、非法 UTF-8 或空输出均失败关闭，不推进 baseline、不唤醒 Codex。
3. Watchdog 只把 `probe name + stdout SHA-256` 合入 fact fingerprint；不把 stdout 正文写入 state、日志、prompt 或 Ack。name 必须唯一，配置 revision 包含 probes。
4. W2 专用 probe 只加载 `psycopg`，不导入会初始化完整 FastAPI 应用的 `aos_api` 包；连接地址优先读取运行环境，缺省只解析仓内既有 `alembic.ini`，不在探针或 Watchdog 配置中复制 DSN。所有查询运行于 `REPEATABLE READ READ ONLY` 事务，并设置 5 秒连接、语句和锁等待上限；stdout 仅输出排序稳定、无敏感字段的 JSON。
5. 第一次探针结果只建立 baseline。后续 durable fact 变化仍沿用 V2.3：活跃 turn 只吸收新 baseline；idle 且无精确 Lease blocker时只唤醒一次 `dependency-fact-changed`，恢复 turn 必须重新核验完整依赖，不能把 fingerprint 变化解释为 GREEN。
6. 探针配置和代码不包含密码、Token、Cookie、API Key 或 DSN；数据库连接只复用本机既有安全配置。探针失败不影响原断流/Lease/Receipt 监控，但必须在 Watchdog stderr 留下错误类别并保持旧 baseline。

### 17.3 实现前复审与验收门

- R1：任意 shell 字符串或相对 executable/cwd 会扩大命令注入面。整改为 argv-only、shell=false、绝对路径与 project-root cwd containment；`CLOSED`。
- R2：把 probe stdout 写入 state 可能泄密。整改为只存最终 SHA-256，测试断言敏感测试字符串不进入 state；`CLOSED`。
- R3：时间戳或日志噪声会每 5 分钟伪造变化。整改为 probe 屏蔽框架输出并只生成 canonical sorted JSON，连续两次同库事实必须逐字节一致；`CLOSED`。
- R4：探针异常不应制造依赖变化 episode。整改为异常时本 tick fail-closed，runner=0，旧 fingerprint 不推进；`CLOSED`。

实现前结论：`APPROVED_FOR_RED_GREEN_IMPLEMENTATION`。必须完成 probe 单元/确定性测试、Watchdog 既有全回归、真实连续两次相同 fingerprint、本机 config mode-0600、LaunchAgent no-op 回读和业务数据库写入 0 后，才能启用。

### 17.4 实现后两轮复审

- R1：初版通过 `uv run` 导入 `aos_api.db`。前台虽然可在约 6 秒完成，但真实 LaunchAgent 连续两次达到 30 秒超时，不能算有效监控。根因是 Python 包入口会初始化完整 API 应用；整改为直接使用现有虚拟环境 Python、仅加载 `psycopg`、从环境或既有 `alembic.ini` 解析连接配置，并增加连接/语句/锁超时。相同现场探针耗时降至约 0.25 秒；`CLOSED`。
- R2：探针子进程若泄露 stdout、接受 shell 字符串或在仓外 cwd 执行，会扩大信息与执行边界。实现只接受绝对 executable、argv-only、project-root 内 cwd，state 仅保存 stdout SHA-256；非零、超时、空、超限和非 UTF-8 全部失败关闭；`CLOSED`。

新鲜验证：Watchdog 44/44 单元与隔离状态机测试 GREEN；同一数据库事实连续两次输出均为 2414 字节且 SHA-256 同为 `f7b0cc03040c4a23da5cfd16fff3dfbde333ec84b36c32d53ec2cdedcfb0f414`。本机配置升级为 `workshop-watchdog-v2.6-20260815` 且仍为 mode `0600`；真实 LaunchAgent 第 247 次运行 `last exit code=0`、`decision=live`，当前活跃任务下 `total_attempts` 保持 14，没有并发唤醒。`meta_schedule_run` 验收前后均为 92 条、最新时间均为 `2026-08-15T00:00:02.451829+00:00`，证明探针未触发 Schedule 或写业务数据；canary 聚合仍为 0/0。

实现后结论：`ACCEPTED_GREEN_WITH_FIRST_REAL_DATA_CHANGE_EPISODE_PENDING`。V2.6 已能每 5 分钟感知 W2 聚合数据事实变化，但 fingerprint 变化只触发重新核验，不代表 W2 Readiness 自动转绿；首个真实变化 episode 仍必须以当次重核、Ack、新 final、测试与 Delivery Receipt 证明有效续跑。

## 18. V2.7 目录级 Lease 与具体文件 Lease 的边界安全匹配

### 18.1 现场缺口

2026-08-15 `AOS-000045` 后，AIP P8-2 持有具体迁移文件 `services/aos-api/alembic/versions/aip8_001_analyst_query_authority.py` 的活动 Lease；Workshop Watchdog 配置监控的是目录 token `services/aos-api/alembic/versions`。V2.6 仍以集合完全相等判断 scope，因此未把该具体文件识别为目录内的迁移 Lease。当前 W2 虽然另受 `DEP-DATA_RED` 阻断，但若未来数据门先转绿，这个漏检会削弱“共享迁移资源占用时安全让路”的保证。

### 18.2 设计裁决

1. 保留 exact match；仅对含 `/` 的非根路径增加 segment-boundary descendant/ancestor overlap。`a/b` 可匹配 `a/b/c.py`，不得匹配 `a/b-old/c.py`。
2. 不做 filesystem resolve、glob、符号链接跟随或目录扫描；scope 仍只是声明式 token，匹配不得读取对方工作树。
3. 命中的状态继续只保存 configured scope token、task id、owner 与过期时间，不保存或读取对方文件内容。
4. 任一活动重叠 Lease 只会使 Watchdog arm/静默等待，不抢 Lease、不终止对方任务、不执行迁移；当前 turn/tool/task 活跃时仍为 no-op。
5. 非路径类别 token 继续 exact-only，避免 `db`、`database` 或任意业务标签因字符串前缀误命中。

### 18.3 红绿验收门

- 红测必须证明目录 token 对具体迁移文件旧实现漏检；实现后返回 `dependency-blocked`、runner=0，并记录 configured directory token。
- 相邻前缀 `services/aos-api/alembic/versions-old/x.py` 必须不匹配。
- 原 exact Lease、release one-shot、fact probe、continuation 和 Ack 全回归保持 GREEN。
- 真实 P8-2 migration Lease 在当前 active turn 下必须被识别，但不得新增恢复 attempt；数据库、Git HEAD 与对方 Lease 前后守恒。

实现前复审结论：`APPROVED_FOR_RED_GREEN_IMPLEMENTATION`。该修复只收紧共享资源冲突检测，不扩大执行、数据库、迁移、租户或发布权限。

### 18.4 实现后两轮复审

- R1：新增红测在旧实现上稳定得到 `idle`，证明目录 token 确实漏掉了具体迁移文件 Lease；最小实现保留 exact match，并只对双方均含 `/` 的 token 做去除尾斜杠后的路径段边界祖先/后代匹配。相邻目录 `versions-old` 的反例保持 `idle`，非路径类别仍为 exact-only；`CLOSED`。
- R2：组合回归确认命中结果仍只返回配置侧目录 token，不读取、解析或保存对方文件内容；活动 Lease 只 arm 并阻止 runner。原 exact match、release、continuation、fact probe 和 Recovery Ack 语义均未改变；`CLOSED`。

新鲜验证：新增 2 项边界测试后 Watchdog 46/46 全回归 GREEN，`git diff --check` GREEN。针对当前共享 Lease 的只读现场调用已识别 `aip-p8-2-query-authority-20260815`，命中的配置 token 为 `services/aos-api/alembic/versions`；调用前后 `total_attempts` 均为 18，未发起 runner、迁移或业务数据库操作。主 LaunchAgent 当时正等待本 recovery turn 完成，因此本波不并发改写其 state；当前 episode 收口后，下一 tick 才由同一单实例进程按新逻辑 arm。

实现后结论：`ACCEPTED_GREEN`。V2.7 关闭了目录级迁移互斥的漏检，但不改变 W2 的 `DEP-DATA_RED`，也不把 AIP P8-2 的开始或完成解释为 Workshop 依赖 GREEN。

## 19. V2.8 `safe-blocked` 定期依赖复核与解锁后连续波次

### 19.1 现场缺口

episode `dependency-fact-1787212406883` 以 `safe-blocked` 闭合后，现有状态机正确停止了当次 transport retry，但也同时永久 disarm continuation。后续只有 authority、Delivery Receipt 或 W2 数据探针 fingerprint 再次变化才可能唤醒。如果阻断依赖已在 AIP 持续开发，但变化未落入现有 fingerprint，Workshop 会长期保持静默，不符合“条件不具备时定期唤醒重核，具备后立即开工”的长任务目标。

### 19.2 设计裁决

1. 新增显式 `blocked_recheck_watch` 配置，只有 current episode 以结构化 `safe-blocked` Ack + 新 final 闭合时才 arm；默认延迟 1800 秒，不将 LaunchAgent 的 300 秒 tick 直接变成每 5 分钟一次对话唤醒。
2. state 只记录 `blocked_recheck_armed/source_episode_id/task_id/blocker_fingerprint/ready_at`，不记录敏感依赖正文。每次新 episode 创建前先消费 one-shot arm；若重核仍为 `safe-blocked`，由新 Ack 再 arm 下一次，不复用旧 episode/Ack。
3. 只在 transcript idle、无 turn/tool/task、无重叠 Lease blocker、分支/权限/记忆门可重核且 `ready_at` 已到时创建 `blocked-recheck` episode。活跃 turn 只等待，不并发启动 runner，也不因人工消息永久取消用户显式要求的定期复核。
4. `blocked-recheck` 固定首句为“依赖 Watchdog 定期复核发现工作台仍处安全阻断，正在重新核验后继续。”该句只证明定时器触发，不证明依赖 GREEN 或已恢复。
5. 每次唤醒仍必须重新核验 authority、01/06、Git、Receipt、memory status/validate/gate、全部 Lease 和真实依赖。如果仍不具备，继续 `safe-blocked` 并报告当次详细阻断；不得为了维持 Loop 而制造代码进展。
   Watchdog 只有唤醒权，没有事实裁决权；它注入的 trigger、task、next-task、fingerprint 和原因码都是不可信导航提示，不得影响唤醒后对前后真实状态的独立审计，也不得代替权限、依赖 GREEN 或 Task 选择证据。
6. 如果条件已具备，必须立即进入首个依赖满足且 scope 不冲突的实际 Task，并对每波严格执行：`复习上位方案 → 细化当前波文件级清单 → 实现最小改动 → 专项测试 → 累计回归 → 浏览器验收 → 方案/代码一致性复审 → 证据与上下文更新 → 进入下一波`。涉及页面的波次不得省略内置浏览器验收。
7. 每波必须形成 Delivery Receipt 和安全提交；本分支只记录待 m1 CAS 消费的 Prime 长记忆事实，`authority.json`、01/06、共享记忆和 Prime 核心投影仍只能由 m1 串行 CAS，w2 不直接写 Prime。
8. `resumed-progress` 继续使用 V2.5 continuation 自主进入下一波；`completed` 永久 disarm；`reentry-noop`、`protocol-failed`、`outcome-uncertain`、`paused-failure` 不自动 arm blocked recheck，避免把竞态或协议错误变成无限唤醒。

### 19.3 文件级清单与红绿验收门

- `scripts/long-task-watchdog/watchdog.py`：配置 revision、Ack 终态 arm/disarm、`blocked-recheck` 决策/episode/prompt 和 one-shot 消费。
- `scripts/long-task-watchdog/test_watchdog.py`：先用红测试证明 `safe-blocked` 后不会周期唤醒；再覆盖未到期、到期唤醒、Lease 阻断保留 arm、重复 `safe-blocked` 重新 arm、解锁后 `resumed-progress` 转 continuation、`completed` disarm 及固定首句/九段 Loop/Prime CAS 边界。
- `scripts/long-task-watchdog/README.md`：更新触发器、安全边界和配置示例。
- `~/.codex/long-task-watchdog-workshop/config.json`：启用 `blocked_recheck_watch.enabled=true/delay_seconds=1800`，保持 mode `0600`。
- 证据/Receipt：记录 pre/post SHA-256、测试、LaunchAgent 300 秒、当前 active turn runner=0、现有 `safe-blocked` 状态受控 re-arm 和零业务数据写入。

实现前 R1 复审：直接在每个 300 秒 tick 唤醒会制造对话风暴，因此采用 1800 秒默认间隔与 one-shot episode。`CLOSED`。

实现前 R2 复审：定期重核不能绕过依赖、Lease、迁移、发布、租户或 Prime CAS 门，因此只由有 fingerprint 的结构化 `safe-blocked` Ack arm，解锁后仍走原九段工程闭环和 V2.5 continuation。`CLOSED`。

实现前结论：`APPROVED_FOR_RED_GREEN_IMPLEMENTATION`。

### 19.4 实现后复审

- R1：红测试在旧实现上以 `KeyError: blocked_recheck_armed` 稳定失败；最小实现仅新增配置门、Ack 终态 arm/disarm、one-shot `blocked-recheck` episode/prompt 和旧 `safe-blocked` 本地状态 bootstrap。不改变 Lease、fact fingerprint、transport backoff、Ack 校验或 continuation 原语义；`CLOSED`。
- R2：组合测试确认 1800 秒前 runner=0，到期后只创建一次新 episode；重叠迁移 Lease 保留 arm 且 runner=0；新 `safe-blocked` 会重新 arm，解锁后 `resumed-progress` 会 disarm recheck 并 arm V2.5 continuation；无效 delay 失败关闭。prompt 已强制“Dog 只唤醒、事实独立核验、九段 Loop、Prime 只由 m1 CAS”；`CLOSED`。

新鲜验证：5/5 新增专项、Watchdog 53/53 累计回归、Python compile/compileall 和 `git diff --check` 全部 GREEN。本波无 UI 变更，浏览器验收为 `NOT_APPLICABLE`。本机配置为 `workshop-watchdog-v2.8-20260820`，mode `0600`，LaunchAgent 仍为 300 秒、last exit code 0。当前活跃 turn 真实 no-op 返回 `turn-running`，`total_attempts` 前后均为 183；旧 `safe-blocked` 已受控 bootstrap 为 `blocked_recheck_armed=true`，30 分钟后首次复核。

真实只读数据探针连续两次 SHA-256 同为 `568abf5e4d77304a883e7b18a4fe5f9ea5ecb6966a128fd564e6964d78c82f9d`；当前仍为 11/12 succeeded，P07 `PIPELINE_EXECUTOR_FAILED`，canary 0/0。因此 V2.8 机制本身 `ACCEPTED_GREEN`，但 W2 runtime 仍 `SAFE_BLOCKED`；首次真实定期 episode 必须以当次独立核验、current Ack 和新 final 证明结果，不预先声称依赖已恢复。

## 20. V2.9 唤醒结果可见状态契约

### 20.1 现场缺口

V2.8 上线后的真实记录证明 Dog 已在 2026-08-20 23:09 至 2026-08-21 04:03 间持续创建恢复 episode，并在每轮独立核验后形成 `safe-blocked` Ack 与 final；但普通任务视图没有固定展示累计唤醒序号、episode、触发原因、核验结果和下一次策略，用户因此合理地判断为“Dog 没有唤醒”。这是可观测性缺口，不是恢复调度缺口。

### 20.2 设计裁决

1. 新增显式 `visibility_watch.enabled`。启用时，Dog 在恢复 prompt 中注入非敏感元数据：本次累计唤醒序号、UTC 唤醒时间、episode、trigger、心跳周期与 blocked-recheck 周期。它们只证明调度发生，不代表依赖、权限或业务状态 GREEN。
2. 第一条用户可见消息仍必须以各 trigger 的固定句开头，随后紧接一行 `Dog 可见状态`，至少展示序号、时间、episode 和触发原因；不得因为增加展示而改变独立事实核验顺序。
3. 最终答复必须包含独立一行标记 `[DOG_VISIBLE_STATUS]`，并展示：本次核验 outcome、当前 Task/下一 Task、阻断摘要或完成证据、累计唤醒序号，以及下一次复核策略。`safe-blocked` 只能写“按配置周期重新 arm”，不能在状态机落盘前虚构精确 ready-at。
4. 状态机在 `visibility_watch.enabled=true` 时把“新 final 缺少 `[DOG_VISIBLE_STATUS]`”判为 `protocol-failed`，即使退出码为 0 且 Ack 有效也不接受为可见闭环；可见性检查只新增布尔检测，不额外把 final 正文复制到 state、日志或 Receipt。
5. `visibility_watch` 只增强同一 task/thread 的可见性，不发送外部消息、不创建第二个定时器、不触发 macOS 通知、不扩大 Git、网络、数据库、租户、迁移或发布权限。

### 20.3 文件级清单与验收门

- `scripts/long-task-watchdog/watchdog.py`：配置 revision、非敏感唤醒元数据、首条状态行、final marker 协议和布尔闭环校验。
- `scripts/long-task-watchdog/test_watchdog.py`：先用红测证明旧 prompt 缺少元数据且无 marker final 仍被错误接受；再覆盖完整状态卡 GREEN、缺 marker fail-closed 和禁用配置兼容。
- `scripts/long-task-watchdog/README.md`：记录固定状态卡、marker 和无外部通知边界。
- 本机配置：升级 revision，启用 `visibility_watch`，保持 `0600`、300 秒心跳和 1800 秒阻断复核。
- 证据/Receipt：记录 pre/post SHA-256、专项/累计回归、真实 active-turn no-op、LaunchAgent 与零业务数据副作用。

实现前 R1：直接由 LaunchAgent 另发桌面通知会引入新的外部副作用和双通道竞态，拒绝；状态必须留在同一 Codex task transcript。`CLOSED`。

实现前 R2：只在 prompt 里“建议展示”不能证明结果真的可见，必须以 transcript 中新 final 的固定 marker 失败关闭。`CLOSED`。

实现前结论：`APPROVED_FOR_RED_GREEN_IMPLEMENTATION`。

### 20.4 实现后复审

- R1：两项红测在旧实现上分别因 `wake_sequence` 缺失和无状态 marker 的 final 被错误接受而失败；实现只增加可选配置门、非敏感 prompt 元数据、最新 final marker 布尔检测及缺 marker 的 `protocol-failed` 分支，不改变 Ack、Lease、fact probe、backoff、blocked recheck 或 continuation 的事实语义。`CLOSED`。
- R2：`visibility_watch` 禁用时原 53 项行为保持兼容；启用时完整状态卡可闭环，缺 marker 失败关闭，非法 enabled 类型启动前拒绝。可见性检查没有新增 final 正文副本，也未增加外部通知、网络、数据库、迁移或租户副作用。`CLOSED`。

新鲜验证：V2.9 专项 3/3、Watchdog 累计 56/56、Python compile/compileall 与 `git diff --check` GREEN。本机配置 revision 为 `workshop-watchdog-v2.9-20260821`，mode `0600`；真实 active-turn no-op 返回 `turn-running`，`total_attempts` 前后均为 196。手工 no-op 首次与 LaunchAgent 单实例锁重叠并安全返回 `watchdog already running`，随后正常 no-op 通过；该锁竞争没有创建恢复副本。渲染的真实 prompt 已包含序号、UTC 时间、episode、trigger、300 秒心跳、1800 秒复核策略及 `[DOG_VISIBLE_STATUS]` 契约。

本波不涉及页面或视觉代码，浏览器验收为 `NOT_APPLICABLE`。V2.9 机制结论：`ACCEPTED_GREEN_WITH_FIRST_REAL_VISIBLE_EPISODE_PENDING`；只有下一次真实 episode 在 transcript 中出现带 marker 的状态卡并通过 Ack/final 校验，才能将现场可见性标记为已验证。

## 21. V3.0 陈旧 active turn 解锁与可见投递闭环

### 21.1 新鲜事故事实

V2.9 上线后，第 206～211 次真实唤醒均已在同一 rollout transcript 中形成带 `[DOG_VISIBLE_STATUS]` 的 `final_answer` 和配对 `task_complete`；这证明调度和 transcript 落盘成功，但 Codex Desktop 当前任务视图没有持续把后台新增 turn 推送到用户面前。V2.9 把“marker 已写 transcript”当成“用户已看到”，证据层级不足。

同时，`evaluate()` 在 `dependency_watch`、`fact_watch` 或 `blocked_recheck_watch` 任一启用时，对未闭合的 `task_started` 无条件返回 `turn-running`；这绕过了已有 `max_turn_silence_seconds` 超时语义。一旦 transcript 因客户端或传输故障缺少 `task_complete`，Dog 会将陈旧 turn 永久当成正在运行。

### 21.2 设计裁决

1. `task_started` 只在 transcript 最近活动小于 `max_turn_silence_seconds` 时具有强防重入权。超过该阈值后，不再因 watch 类型启用而永久拦截，而是继续经过待完成 tool、grace、backoff、Lease 和 episode 门。
2. 新增本地 mode-`0600` 持久状态卡，在唤醒开始和 episode 终态后原子写入。状态卡只包含 episode、trigger、wake sequence、stage、outcome、task/next task、reason code 和下次策略；不写入 transcript 正文、凭据、业务数据或阻断详情原文。
3. `visibility_watch.desktop_notification=true` 时，每次唤醒开始和终态通过固定 `/usr/bin/osascript` argv-only 路径投递本机 Notification Center。通知只展示序号、结果、Task 和通用复核策略，不展示 evidence、fingerprint、路径或秘密。
4. 本地通知是用户感知通道，transcript final + Ack 仍是恢复事实权威。通知投递失败必须在持久状态卡与 state 中记录 `delivery_error`，不得把已经完成的业务安全终态降格为 transport retry，以免重复副作用。
5. 不写 Codex SQLite，不伪造 Desktop 已读确认，不创建新 thread，不增加外部网络消息，不扩大 Git、数据库、租户、迁移或发布权限。

### 21.3 文件级清单与红绿门

- `scripts/long-task-watchdog/watchdog.py`：修复陈旧 turn 判定；增加持久状态卡、原子写/mode-`0600`、可选本机通知和投递结果记录。
- `scripts/long-task-watchdog/test_watchdog.py`：红测覆盖生产 watch 全开时陈旧 turn 必须进入 recover；持久状态卡、通知成功/失败、敏感内容不外溢和旧配置兼容。
- `scripts/long-task-watchdog/README.md`：明确 transcript 可见 marker、本地持久状态卡与 Notification Center 三层证据边界。
- `~/.codex/long-task-watchdog-workshop/config.json`：回归通过后升级 revision，显式启用本地可见投递，保持 mode-`0600`。
- `.evidence/workshop/2026-08-21-watchdog-visible-delivery-and-stale-turn-v30.json`：记录 pre/post SHA-256、红绿过程、累计回归、LaunchAgent 回读、真实 active-turn no-op 和零业务数据副作用。

必须先证明旧实现在 watch 全开时对陈旧 `task_started` 永久返回 `turn-running`，再做一行语义修复。真实当前 turn 只允许 no-op smoke，不人为中断、不启动并发恢复。

### 21.4 实现前复审

- R1：直接忽略未闭合 `task_started` 会在真实长工具执行时并发重入。整改为只在“最近 transcript 活动超过显式静默阈值”后解锁，且仍经过 tool/grace/backoff/Lease 门；`CLOSED`。
- R2：直接修改 Codex 本地 SQLite 或宣称能强制 Desktop 刷新会越权且伪造可见证据。整改为不触碰 App 内部库，用同 thread transcript + mode-`0600` 状态卡 + 本机 Notification Center 提供可审计的三层感知；`CLOSED`。
- R3：把通知失败当成恢复失败会重复已完成的提交或安全阻断。整改为投递失败独立记录，不改变 Ack/final 终态；`CLOSED`。

实现前结论：`APPROVED_FOR_RED_GREEN_IMPLEMENTATION`。

### 21.5 实现后复审

- R1：红测在 dependency/fact/blocked-recheck 生产 watch 语义下稳定复现陈旧 `task_started` 永久返回 `turn-running`。最小修复删除 watch 类型的无限特权，只保留 `now - last_activity_at < max_turn_silence_seconds` 的新鲜 turn 保护；真实当前 turn no-op 仍返回 `turn-running`，`total_attempts` 保持 `211 -> 211`；`CLOSED`。
- R2：新增的 `visible-status.json` 只由 state 路径派生，以临时文件 + `os.replace` 原子写入并强制 mode `0600`。内容只有 episode/trigger/sequence/stage/outcome/task/next/reason/strategy 与投递状态；测试确认 evidence 和 blocker fingerprint 不进入状态卡；`CLOSED`。
- R3：本机通知使用固定 `/usr/bin/osascript`、argv-only、去 API Key 环境和 5 秒超时。通知失败只记录类型/退出码，不保存 stderr；测试确认失败时 `resumed-progress` 终态仍保持，不触发重放；`CLOSED`。
- R4：不只有 Ack 终态才更新状态卡；纯 transport failure 也落盘 `retry-scheduled/transport-failed`，避免状态永久停在 `waking`；`CLOSED`。

新鲜验证：V3.0 专项红测先失败后转绿；Watchdog 累计 `60/60` GREEN；Python `py_compile/compileall`、`git diff --check` GREEN。本机配置已升级为 `workshop-watchdog-v3.0-20260821`，mode `0600`，`desktop_notification=true`；Notification Center 非敏感测试投递 `osascript exit 0`。LaunchAgent 仍为 300 秒周期、last exit code 0。

本波不涉及页面或视觉代码，浏览器验收为 `NOT_APPLICABLE`；未读写 w1-aip 工作树，未修改业务数据、迁移、authority、01/06 或 Prime 核心投影。证据见 `.evidence/workshop/2026-08-21-watchdog-visible-delivery-and-stale-turn-v30.json`。

实现后结论：`ACCEPTED_GREEN_WITH_NEXT_REAL_WAKE_DELIVERY_PENDING`。该结论证明本机通知可调用和状态卡可落盘，不声称 Codex Desktop 已读或已强制刷新；下一次真实唤醒仍须以当次 `visible-status.json`、Notification Center 投递状态、Ack 和 transcript final 四者对账。

## 22. V3.0 首个真实唤醒投递验收

### 22.1 当前波目标与边界

`dependency-fact-1787283725024` / wake sequence `212` 是 V3.0 上线后的首个真实恢复 episode。本波只验收 V3.0 可见投递链，并重新裁决 W2-00B 开工门；不修改 Watchdog 运行逻辑、业务页面、数据库、迁移、authority、01/06 或 Prime 核心投影，也不读取或写入 w1-aip 工作树。

### 22.2 文件级清单与完成门

1. 对账 mode-`0600` `visible-status.json`：episode、trigger、wake sequence 必须与本次恢复一致，stage 必须从 `waking/attempting` 在 Recovery Ack 后进入终态。
2. 对账本机可见投递：`notification_status=delivered` 只证明 Notification Center 调用成功；不得外推为 Codex Desktop 已读或已刷新。
3. 复跑 Watchdog `60/60` 累计回归、Python compile/compileall 与 `git diff --check`；不得为了验收修改业务运行逻辑。
4. 重新核验 authority、01/06、memory status/validate/gate、Git、全部 Lease、最新 Delivery Receipt、P01～P12 只读探针与 m1 exact owner/API。
5. 只有 canonical `SourceReadiness` owner/API、同 cutoff EvidencePack、B5 m1 CAS 与 operational handoff 同时 GREEN，才进入 W2-00B；否则形成当前 episode 的结构化 `safe-blocked`，并按 1800 秒周期重新 arm。
6. 新增本波 Evidence 与 Delivery Receipt，提交待 m1 串行 CAS 消费的 Prime Agent 独立长记忆事实；w2 不直接更新 authority、01/06 或 Prime。

### 22.3 实施前复审

- R1：当前 `visible-status.json` 的 `waking/attempting` 是 episode 进行中现场状态，不是失败，也不能提前作为终态验收。整改：先完成测试、Receipt、提交与 Recovery Ack，再回读终态；`CLOSED`。
- R2：P01～P12 已恢复且活动 Lease 已释放，但最新 operational-handoff Receipt 自身仍列出 SourceReadiness owner/API 与 B5 CAS 两个外部 owner blocker。整改：分别对 m1 code owner 与 authority 投影做 exact read-only 核验，不以数据/Lease 单点变化解锁；`CLOSED`。
- R3：真实唤醒验收若修改 Watchdog 逻辑，会把现场验收和新版本开发混成同一证据。整改：本波只新增方案、Evidence 与 Receipt，现有逻辑保持不变；`CLOSED`。

实施前结论：`APPROVED_FOR_EVIDENCE_ONLY_ACCEPTANCE_AND_GATE_RECONCILIATION`。

### 22.4 实施结果与一致性复审

- 当前真实 `visible-status.json` 为 mode `0600`，精确指向 episode `dependency-fact-1787283725024`、wake sequence `212`、trigger `dependency-fact-changed`；恢复进行中阶段为 `waking/attempting`，本机通知投递状态为 `delivered` 且无 delivery error。该结论只证明本地状态卡与通知调用链，不声明 Codex Desktop 已读。
- Watchdog 累计 `60/60`、Python compile/compileall 与 `git diff --check` GREEN；三个 V3.0 运行文件 SHA-256 与 `a13d406` 交付证据一致，本波未修改 Watchdog 逻辑。
- P01～P12 当前只读探针 `12/12 succeeded`、canary `0/0`，外部活动 Lease 为 0；但 `m1@5b71a32` exact grep 仍无 canonical `SourceReadiness` owner/API，authority 仍为 `AOS-000146 / W1_AIP_NEARFIELD_SEALED_AWAITING_W2_BROWSER`，未消费 B5。
- 最新 `AIP-WKS-DEP-ADP-OPERATIONAL-HANDOFF-REFRESH` Receipt 为 `GREEN_WITH_EXTERNAL_OWNERS`，明确保留 SourceReadiness canonical authority/同 cutoff EvidencePack 与 B5 m1 CAS 两个 blocker。因此 W2-00B 继续 `SAFE_BLOCKED`，不能用数据恢复或 Lease 释放绕门。
- 本波无页面/视觉改动，浏览器验收为 `NOT_APPLICABLE`；未写业务数据、未执行迁移、未读取或写入 w1-aip 工作树，未修改 authority、01/06 或 Prime 核心投影。

方案、现场事实与证据结论一致。当前 Recovery Ack 写入后必须立即只读回查状态卡终态；在此之前仅可声明“首个真实唤醒开始阶段可见投递 GREEN”，不得提前声明整个 episode 可见终态已闭合。

本波结论：`FIRST_REAL_WAKE_START_DELIVERY_GREEN / W2_00B_SAFE_BLOCKED / TERMINAL_ACK_READBACK_PENDING`。证据见 `.evidence/workshop/2026-08-21-watchdog-v30-first-real-wake-acceptance.json`。

## 23. V3.1 每次唤醒状态与逐项阻断任务契约

### 23.1 用户要求与现状缺口

用户要求每次 Dog 唤醒都必须先给出本次真实核验状态：条件具备时立即继续首个安全 Task；条件不具备时不能只输出一个笼统 reason code 或“仍受阻”，必须列出本次被阻断的具体任务及解除条件。

V3.0 已关闭“唤醒结果不持续可见”和“陈旧 turn 永久占用”两个机制缺口，但当前 final 可见性协议只要求 `[DOG_VISIBLE_STATUS]`、outcome、task/next、阻断摘要或完成证据。状态机只能证明有一张状态卡，不能失败关闭地证明 `safe-blocked` final 已包含可执行的逐项阻断清单。

### 23.2 设计裁决

1. 每次唤醒的首条可见消息继续只证明唤醒发生；独立核验完成前不得声明依赖 GREEN、恢复成功或 Task 已可执行。
2. 最终答复必须继续包含 `[DOG_VISIBLE_STATUS]` 和 `Dog 可见状态`，展示 outcome、task、next task、wake sequence 与下一次策略。
3. `safe-blocked` final 额外必须包含 `[DOG_BLOCKER_DETAILS]`，并至少有一个结构化阻断项。每个阻断项必须分别写明：`阻断任务`、`缺失条件`、`独立核验证据`、`责任边界`、`解除条件`、`下次复核策略`。
4. 有多个互不等价的 blocker 时必须逐项列出，不得把 SourceReadiness owner、同 cutoff EvidencePack、m1 CAS、Lease、评审或租户/安全门合并成一个不可执行的摘要。
5. 状态机只校验当前新 final 是否存在完整字段契约，不把阻断正文复制进 state、visible-status、通知、日志或 Receipt。阻断事实仍由当次 authority、01/06、Git/Receipt、memory gate、Lease、真实数据探针与代码状态核验产生。
6. 缺少 `[DOG_BLOCKER_DETAILS]` 或任一必填字段时，即使 Ack 有效、runner 退出码为 0，也按 `protocol-failed` 拒绝把本 episode 接受为可见闭环；不得据此重新执行业务副作用。
7. `resumed-progress` 与 `completed` 不要求 blocker 清单，但必须给出完成证据；`reentry-noop` 保持既有 fingerprint 与竞态说明，不伪装成依赖阻断。
8. 本增强不修改 Ack schema、blocked-recheck 调度、Lease、fact probe、业务 Task 选择、数据库、租户、迁移、发布或 Prime CAS 权限。

### 23.3 文件级清单与红绿验收门

- `scripts/long-task-watchdog/watchdog.py`：注入逐项阻断契约；在 transcript 解析阶段仅生成“字段契约完整”布尔值；`safe-blocked` 缺失时 fail-closed。
- `scripts/long-task-watchdog/test_watchdog.py`：先用红测证明只有 `[DOG_VISIBLE_STATUS]` 的 `safe-blocked` 会被旧实现错误接受；再覆盖完整阻断项 GREEN、缺 marker/缺字段 RED，以及 `resumed-progress` 兼容。
- `scripts/long-task-watchdog/README.md`：记录每次唤醒状态卡、逐项阻断格式与不持久化正文的边界。
- 本机 config：累计回归后只升级 revision 到 V3.1；保持 300 秒 heartbeat、1800 秒 blocked recheck、mode `0600` 与既有通知配置。
- Evidence/Receipt：记录 pre/post SHA-256、红绿测试、累计回归、LaunchAgent 回读、真实 active-turn no-op 与零业务数据副作用。

### 23.4 实现前复审

- R1：把 blocker 明细写入 `visible-status.json` 或通知会扩大本地敏感信息持久化面。整改：只在同一 task 的 final 中展示，状态机仅保留布尔校验结果；`CLOSED`。
- R2：仅在 prompt 中写“请详细说明”无法保证每次执行。整改：增加固定 marker 与六个字段的 fail-closed 校验；`CLOSED`。
- R3：状态机无法从 reason code 推导所有真实 blocker。整改：Dog 不推导、不补全，只要求恢复 turn 在完成独立核验后逐项列出；覆盖完整性仍由当次证据与方案复审负责；`CLOSED`。
- R4：详细阻断契约不得妨碍条件已具备时自动继续。整改：只对 Ack outcome=`safe-blocked` 生效；`resumed-progress/completed` 保持既有连续波次语义；`CLOSED`。

实现前结论：`APPROVED_FOR_RED_GREEN_IMPLEMENTATION`。

### 23.5 实现后复审

- R1：红测证明旧实现会把“只有 `[DOG_VISIBLE_STATUS]` 和笼统阻断摘要”的 `safe-blocked` 错误接受为终态。最小实现新增 `[DOG_BLOCKER_DETAILS]` 与六字段契约；缺 marker 或缺任一字段均返回 `protocol-failed`；`CLOSED`。
- R2：契约校验按每个 `阻断任务` 分块，保证每个列出的任务都分别包含缺失条件、独立核验证据、责任边界、解除条件和下一次复核策略，不能用跨任务拼接字段绕过；`CLOSED`。
- R3：transcript 解析只保存两个布尔值：可见状态 marker 是否存在、阻断字段契约是否完整。阻断正文没有进入 state、`visible-status.json`、通知、日志或 Receipt；`CLOSED`。
- R4：新门只在 `visibility_watch.enabled=true` 且 current Ack outcome=`safe-blocked` 时生效；`resumed-progress/completed`、旧禁用配置、Lease、fact probe、blocked recheck、continuation 和 Ack schema 保持兼容；`CLOSED`。

新鲜验证：新增专项 `3/3`、Watchdog 累计 `63/63`、Python `py_compile/compileall` 与 `git diff --check` 全部 GREEN。真实当前活跃 turn no-op 返回 `turn-running`，`total_attempts` 保持 `217 -> 217`，没有启动恢复 runner。本机配置 revision 为 `workshop-watchdog-v3.1-20260821`、mode `0600`；LaunchAgent 保持 300 秒周期、last exit code 0。

本波不涉及页面或视觉代码，浏览器验收为 `NOT_APPLICABLE`；未读取或写入 w1-aip 工作树，未修改业务数据、迁移、authority、01/06 或 Prime 核心投影。下一次真实 `safe-blocked` episode 必须同时出现 `[DOG_VISIBLE_STATUS]` 与逐项 `[DOG_BLOCKER_DETAILS]` 后，才能把 V3.1 现场行为标记为真实验收 GREEN。

实现后结论：`ACCEPTED_GREEN_WITH_NEXT_REAL_SAFE_BLOCKED_EPISODE_PENDING`。

## 24. V4.1 m1 单人主线恢复权限收敛

### 24.1 触发事实

Watchdog 已在 V4.0 切换为 `aos-platform/m1` 单人串行主线，并要求每个波次闭合 authority CAS、01/06、deterministic memory sync、Prime 回读和文档安全提交；但本机 `writable_roots` 仍沿用旧 w2 边界，只包含工作台技术方案目录与 `AOS项目开发上下文/memory` 子目录，缺少：

1. `/Users/ddt/work/projects/ai_agent/docs/palantier/AOS项目开发上下文`，导致同步 01/06 的原子临时文件创建被拒绝；
2. `/Users/ddt/work/projects/ai_agent/docs/.git`，导致已授权方案文档无法 staging/提交。

该漂移使 authority 已推进后强一致投影持续 `STALE`，并让 `memory-gate` 持续 RED。它是恢复执行环境缺口，不代表业务依赖、真实平台条款、Health、SourceReadiness、迁移或发布门已 GREEN。

### 24.2 最小权限裁决

- 保留 `sandbox_mode=workspace-write`、`expected_branch=m1`、network、Ack、1800 秒 blocked recheck 与全部业务硬门不变。
- 只追加上述两个精确 writable root；不授权 `/Users/ddt/work/projects/ai_agent/docs` 整体写范围，不授权或读取 `aos-platform-w1-aip` 未提交工作树。
- `AOS项目开发上下文` 权限只供 m1 按 authority 执行 deterministic sync；投影不能反写 authority，authority 仍必须 CAS。
- `docs/.git` 权限只供精确 staging/提交本波已复核的技术方案文件；禁止 reset/rebase/force push/clean 或纳入无关文件。
- 当前已运行 episode 的 sandbox 不会被配置热更新扩大；修复只对下一次 Watchdog 恢复 turn 生效。本 episode 仍须按实际 memory gate 形成 safe-blocked。

### 24.3 验收门

1. 配置 JSON 可解析，revision 升级为 `aos-sole-developer-watchdog-v4.1-20260827`，两个精确 root 各出现一次；
2. Watchdog 累计测试、Python compile 与 JSON 检查 GREEN；
3. 下一真实 episode 的 permission preflight 必须显示两个新增 root 为 writable；
4. 下一真实 episode 必须实际完成 `memory-sync --apply --prime`、status/validate/gate、Prime 精确回读和文档精确 staging；缺任一项仍不得称恢复；
5. 不修改业务数据、不执行 migration、不访问平台、不产生外部副作用、不发布。

实施前复审：`APPROVED_FOR_MINIMAL_LOCAL_CONFIG_REPAIR`。

### 24.4 实施结果与当前边界

- 本机配置 revision 已升级为 `aos-sole-developer-watchdog-v4.1-20260827`，两个新增 root 各出现一次，配置仍为 mode `0600`。
- JSON 解析、精确 root/revision 断言、Watchdog 累计 `63 tests + 10 subtests`、重定向 Python cache 后的 `py_compile` 与文档 `diff --check` GREEN。
- 默认 `py_compile` 首次因系统缓存目录不在当前 sandbox 写范围返回 `Operation not permitted`；改为受控 `/private/tmp` cache 后 GREEN，未修改源码或扩大生产权限。
- 当前 episode 的 sandbox 在启动时已经冻结，不能由配置热更新获得新增 root；因此本 episode 的 01/06 sync、Prime 回读和 docs staging 仍按实际结果 safe-blocked。V4.1 是否真正解除权限门，必须由下一真实 episode 的 permission preflight 和完整同步链确认。
- 本波没有读取 w1-aip 未提交工作区，没有修改业务数据、migration、平台配置、Secret、Session、schedule 或发布状态。

实施结论：`V4_1_LOCAL_CONFIG_GREEN / CURRENT_EPISODE_PERMISSION_STILL_BLOCKED / NEXT_REAL_EPISODE_ACCEPTANCE_REQUIRED`。

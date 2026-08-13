# AIP-6 智能体、Skill Registry 与 Handoff 实施清单

> 状态：`REVIEWED / APPROVED_FOR_IMPLEMENTATION`
> 唯一分支：`aos-platform/m1`
> 唯一真实范围：`org-org/dev-project`
> 负向隔离 canary：`dev-org/dev-project`

## 1. 实时差异结论

1. `aip_agents_engine.py`、`phase3_aip_agents.py` 与 `phase3_aip_capabilities.py` 仍是进程内过渡实现，不能作为 AIP-6 真源。
2. `wave_ext.py` 仍存在内存 capability 和 `mock://local` 自动补齐路径；AIP-6 禁止依赖或扩展该路径。
3. 当前 Alembic 单 head 为 `aip5_004`；AIP-6 只做 additive migration，不修改 AIP-1～AIP-5 权威表。
4. `AgentsPage`、`AgentRegistryPage`、`AgentImportPage` 已存在，必须最后切换唯一严格 SDK；API 空即真实空态，禁止静态 Agent fallback。
5. AIP-5 E7 的个人记忆和共享投影依赖本清单形成的 AgentInstance exact identity，因此执行顺序固定为 AIP-6 后回到 E7。

## 2. 权威边界

- 平台/包级：不可变 `AgentTemplateRevision`、`SkillTemplateRevision`、alias、来源、许可证、manifest/hash。
- 组织级：`AgentInstance`、`SkillBinding`、`CapabilityBinding`、Overlay、预算与治理策略。
- 工作区级：`AgentRun`、`HandoffEnvelope`、一次性消费事件与运行证据。
- 所有 mutable lifecycle 使用 expected revision CAS；不可变 revision/event/receipt 只追加。
- secret 只保存 `secretRef`；请求、响应、日志和 Receipt 禁止出现明文凭据。
- Handoff 只传 exact Object/Artifact/Evidence refs 与 schema allowlist 字段；接收方按当前权限重新解析。

## 3. 分波

### A6A：公共契约冻结（IMPLEMENTED_GREEN · `aos-platform/m1` 待提交）

文件：

- `services/aos-api/aos_api/aip_agent_registry_contracts.py`
- `services/aos-api/tests/aip/test_aip_agent_registry_contracts.py`

完成 DTO、状态机、exact ref、hash、overlay allowlist、Handoff 最小披露和错误语义。不得注册路由或写库。

实施结果：新增 `aip_agent_registry_contracts.py` 与 6 项专项测试；exact asset revision/hash、模板/实例/Run 状态、Overlay 白名单、secretRef-only、Handoff 最小披露和 AgentRun 五类 exact ref 全部失败关闭。compileall 与 diff check GREEN；未注册路由、未写数据库。

### A6B：PostgreSQL authority（IMPLEMENTED_GREEN · `aos-platform/m1` 待提交）

文件：

- `services/aos-api/alembic/versions/aip6_001_agent_skill_registry.py`
- `services/aos-api/tests/aip/test_aip6_001_migration.py`

新增模板 revision、实例、Skill revision/binding、Capability binding、AgentRun、Handoff/event 表；组织表与工作区表分别 RLS/FORCE RLS；模板 revision append-only；Handoff token 只存 hash。验证升级/降级、双租户、无 scope、跨租户 FK 和原表行数守恒。

实施结果：`aip6_001` 从唯一 head `aip5_004` 线性增加 8 张权威表。平台模板/Skill revision 与 Handoff event 追加不可变；6 张租户表 RLS/FORCE RLS；Handoff 只存 token hash，Capability 只存 secretRef。双租户、无 scope、约束/FK、降升级守恒 7 项，A6A/A6B/E6C 邻接累计 16 项、compileall、单 head/current、diff check GREEN。

### A6C：Store、CAS 与生命周期

文件：

- `services/aos-api/aos_api/aip_agent_registry_store.py`
- `services/aos-api/aos_api/aip_agent_instance_service.py`
- `services/aos-api/aos_api/aip_skill_registry.py`
- 对应 `tests/aip/test_aip_agent_*.py`

实现 publish 后不可变、实例 Overlay allowlist、binding exact revision、revoke/suspend/deprecate、历史回读和幂等 Receipt。

### A6D：Handoff、AgentRun 与 CapabilityBinding

文件：

- `services/aos-api/aos_api/aip_handoff_service.py`
- `services/aos-api/aos_api/aip_agent_run_service.py`
- `services/aos-api/aos_api/aip_capability_binding_service.py`
- 对应测试

实现 expiry、一次性消费、接收方重授权、撤权阻断新 Run、C0/C1/C2 exact adapter refs；不实现真实外部 provider。

### A6E：六同事与 37 Logic 唯一包

文件：

- `services/aos-api/aos_api/solution_packs/ecommerce_growth/*`
- manifest/schema/crosswalk/Eval/Memory/Handoff policy tests

只发布版本化模板资产和 blocked readiness；不写组织实例、不伪造工具/provider/Eval GREEN。旧 35 Skill 仅 alias 到 37 canonical Logic。

### A6F：Canonical API、唯一 SDK 与页面

文件：

- `services/aos-api/aos_api/routers/aip_agent_registry.py`
- `apps/web/src/api/aipAgents/*`
- `apps/web/src/pages/s2/AgentRegistryPage.tsx`
- `apps/web/src/pages/s2/AgentsPage.tsx`
- `apps/web/src/pages/s2/AgentImportPage.tsx`
- `apps/web/src/pages/StudioPage.tsx`
- 对应 API/页面测试

从认证 Principal 派生 scope；旧 singleton 路由迁移为兼容只读或明确 deprecated。页面覆盖 loading/empty/forbidden/stale/failed/unknown，所有写按钮有 Receipt 或禁用理由。

## 4. 退出门

- 两组织基于同一模板形成不同实例，修改/删除互不影响。
- template/skill revision 发布后不可改；revoke 阻止新 Run，历史 Run 可解析。
- Handoff 跨租户、过期、重复消费、超字段全部失败关闭。
- 37/37 Logic canonical ID 唯一，35 Skill alias 不重复注册。
- API/UI 无 singleton、Mock、localStorage 或静态 fallback 冒充真源。
- `org-org/dev-project` 浏览器显示真实实例/空态；`dev-org/dev-project` 不泄漏。
- 后端定向/累计、前端定向/累计、TypeScript、Vite、OpenAPI、迁移和 `git diff --check` 全部 GREEN。

## 5. 风险与回滚

- A6B 为 additive migration，可独立 downgrade；A6A DTO 无运行影响。
- A6F 前不替换旧路由，避免中途破坏现有页面；切换时保留明确 deprecated 兼容窗口，不保留双写。
- 外部 provider、Secret、真实 Skill 执行和组织实例安装均不在本清单自动发生。
- 任一 scope、hash、revision、license、Eval 或 Capability 不可证明时状态为 blocked，不回退到 singleton/mock。

## 6. 复审结论

方案与实时代码、最新工作台支撑审查、AIP-5 E7 依赖一致。A6A～A6F 可以按顺序实施；每波独立更新 `01/06`、测试、提交和共享记忆，不得跨波制造完成状态。

# AIP-6 A6E 电商领域 SolutionPack 实施清单与评审结论

> 状态：`APPROVED_FOR_IMPLEMENTATION`
> 日期：2026-08-13
> 唯一代码分支：`aos-platform/m1`
> 上位目录：`18-AIP-W0A十类共享专业Capability目录别名与六角色职责Crosswalk.md`
> 后续波次：A6F Canonical API / SDK / UI

## 1. 使用的 Rules

1. 先方案后编码；本清单通过复审后才执行 A6E。
2. L0 AIP 持有 Agent / Skill / Capability revision 与运行绑定真源；L1 SolutionPack 只贡献电商定义。
3. 只做 additive migration 和新增发布路径，不切换旧 singleton，不提前实现 W0B 八公共生产对象。
4. 目录可发布不等于运行可用。Provider、Route、Eval、License、数据或 W0B 依赖未知时必须失败关闭。
5. 六数字同事、37 Logic、十 Capability 使用 W0A 稳定 ID；中文只作显示名。
6. 只使用 `HandoffEnvelope`；`HandoffContext` 仅是历史文档别名。
7. A6E 不创建租户 AgentInstance、SkillBinding、CapabilityBinding；组织安装与页面交互归 A6F。
8. 测试不得写伪业务数据；数据库验证只发布全局不可变定义并读取 exact revision/hash。

## 2. 实时代码差异

| 项目 | 当前事实 | A6E 处理 |
|---|---|---|
| AgentTemplate revision | `aip_agent_template_revision` 已是全局不可变真源 | 发布六角色 revision 1 |
| SkillTemplate revision | `aip_skill_template_revision` 已是全局不可变真源 | 发布 37 条 Logic 对应 SkillTemplate revision 1 |
| CapabilityBinding | 已有租户级 binding、secretRef、health、quota/network policy | 本波不创建真实 binding |
| CapabilityRevision | **不存在**；binding 当前只能保存未经目录 FK 校验的 JSON ref | additive 新增全局 capability revision/alias authority |
| AgentInstance/Run/Handoff | A6C/A6D 已有；Run 进入 running 受 AIP-7 exact route authority 阻断 | 本波不绕过阻断 |
| 电商增长 SolutionPack | 仍是 1.1.0 三同事 placeholder 与 G2 BLOCKED | 升级为 1.2.0 六角色/37 Logic/十 Capability contribution |
| W0B 八公共对象 | 尚未创建 authority | readiness 明确 `blocked`，不以 Bundle JSON 冒充 |

## 3. Authority 与文件边界

### 3.1 L0 additive authority

新增线性迁移 `aip6_004`：

- `aip_capability_revision`
  - 主键：`capability_id + revision`；
  - 不可变：禁止 UPDATE / DELETE / TRUNCATE；
  - 保存 displayName、lifecycle、parent、Schema exact refs、risk、依赖 refs、Eval/Memory/Handoff/Effect/License/Readiness policy refs、source、content hash；
  - `content_hash` 为规范化 contribution 的 SHA-256，重复发布必须内容一致。
- `aip_capability_alias`
  - alias 全局唯一；
  - 指向 exact capability revision；
  - 未知、碰撞、漂移失败关闭。

全局模板表不加 tenant RLS；运行租户数据仍只进入既有 Instance/Binding 表。`aos_runtime` 仅获得 SELECT，发布使用迁移/发布者连接，不扩大运行写权限。

### 3.2 L1 SolutionPack contribution

`bundles/solutions/ecommerce-growth` 升级为 1.2.0，新增：

- 六角色 Agent manifest；
- 37 条 canonical Logic/Skill contribution；
- 十 Capability profile 与 aliases；
- exact Schema artifact；
- Memory/Handoff/Readiness/License/Responsibility policy artifact；
- contribution 自检与状态清单。

保留 D3 已交付的 W03/L05/Eval，不删除真实历史能力。仅删除已经被正式 contribution 替代的 placeholder。

### 3.3 发布器

新增通用 `AipSolutionPackPublisher`，职责仅为：

1. 严格读取指定 Bundle 的 contribution 文件；
2. 校验 6/37/10 数量、唯一 ID、alias、角色 crosswalk 和引用闭包；
3. 对每个 contribution 规范化计算 content hash；
4. 调用既有 Agent/Skill Store 与新增 Capability Store 发布不可变 revision；
5. exact readback 后生成发布结果；
6. 重复同内容幂等，任意同 revision 漂移、alias 碰撞或缺引用失败关闭。

发布器不安装 AgentInstance、不写 secret、不激活 binding、不启动 Run、不创建 W0B 对象。

## 4. 六角色与 37 Logic 冻结

| AgentTemplate ID | 显示名 | Logic | 数量 | 默认职责 |
|---|---|---|---:|---|
| `ecommerce.data_advisor` | 数据参谋 | D01-D06 | 6 | 经营增长协调 |
| `ecommerce.content_officer` | 内容官 | C01-C08 | 8 | `production.coordination` |
| `ecommerce.shopping_advisor` | 导购顾问 | G01-G06 | 6 | 商品与成交建议 |
| `ecommerce.customer_service` | 客服专员 | S01-S06 | 6 | 服务处置与人工升级 |
| `ecommerce.private_domain_manager` | 私域管家 | P01-P05 | 5 | consent/频控/关系维护 |
| `ecommerce.campaign_planner` | 活动策划师 | A01-A06 | 6 | 活动战役协调 |

计数必须为 6 / 37。`Coordinator` 只进入内容官 responsibility profile，不生成第七 Agent；`title.generate` 只作为 `copy.generate` alias/profile，不生成第十一 Capability。

37 条 Logic 本波发布为 `SkillTemplate lifecycle=evaluated`，因为实际 EvalPack、Provider、AIP-7 Route、部分 W0B 输入对象尚未齐备；它们可以 exact readback，但不可绑定为生产 active。后续独立 Eval/Logic 波次发布新 revision，不覆盖 revision 1。

## 5. 十 Capability 冻结

严格原样消费 W0A：

1. `material.collect`
2. `strategy.plan`
3. `copy.generate`
4. `script.compose`
5. `speech.synthesize`
6. `video.compose`
7. `content.review`
8. `live.orchestrate`
9. `platform.adapt`
10. `performance.review`

Capability 目录 revision 可发布为 `published`，但 contribution 内 readiness 初值统一为 `blocked`。目录状态描述“语义定义已发布”；readiness 描述“当前组织是否可运行”，两者不得混淆。

## 6. 任务清单

| ID | 任务 | 产物 | 验收 |
|---|---|---|---|
| A6E-01 | 冻结 capability revision/alias contract | DTO | 严格字段、SHA256、五态 readiness、alias 唯一 |
| A6E-02 | additive migration | `aip6_004` | 单 head、升级/降级、append-only、runtime 只读 |
| A6E-03 | Capability Store | publish/get/resolve alias | 同内容幂等；漂移/碰撞失败关闭 |
| A6E-04 | SolutionPack parser/validator | 通用发布器 | 6/37/10、引用闭包、Coordinator/alias 裁决 |
| A6E-05 | 六角色 contribution | agent manifest | 6/6 exact revision/hash |
| A6E-06 | 37 Logic contribution | logic manifest | 37/37 exact revision/hash；均非 production-active |
| A6E-07 | 十 capability contribution | capability manifest | 10/10 exact revision/hash；alias 唯一 |
| A6E-08 | Schema/Policy/Responsibility artifact | bundle files | exact artifact hash；W0B/provider unknown 明示 blocked |
| A6E-09 | Bundle 1.2.0 与旧 D3 共存 | bundle manifest/gate | W03/L05 不回退；placeholder 删除 |
| A6E-10 | CLI 与真实库发布验证 | publisher script | exact readback 6/37/10，重复发布幂等 |
| A6E-11 | 回归与证据 | tests/context | 定向+邻接+迁移+diff check GREEN |

## 7. 测试矩阵

### 7.1 纯契约与 Bundle

- 6 Agent IDs 唯一且角色数正确；
- D01-D06/C01-C08/G01-G06/S01-S06/P01-P05/A01-A06 完整无重复；
- 10 Capability IDs 与 W0A 完全相等；
- 所有 required capability 指向目录内稳定 ID；
- `title.generate` 解析到 `copy.generate`；未知 alias 失败；
- `production.coordination` 不是 Agent 或 Capability；
- 所有 Schema/Policy artifact ref 的 hash 与真实文件相等；
- readiness 非 `available`，不得误报生产可用。

### 7.2 数据库

- `aip6_004` 升级、降级、再升级；
- capability revision/alias append-only；
- runtime role 只读；
- 同 revision 同 hash 幂等；不同内容冲突；
- alias 碰撞冲突；exact get 与 alias resolve 正确；
- `CapabilityBinding` 引用不存在或 hash 不符的 capability revision 时失败关闭。

### 7.3 发布闭环

- 发布结果 6 Agent / 37 Skill / 10 Capability；
- exact readback 的 revision/hash 与 contribution 一致；
- 第二次运行 0 漂移；
- 不产生 AgentInstance、SkillBinding、CapabilityBinding 或 AgentRun；
- 不写 `org-org/dev-project` 业务数据；`dev-org/dev-project` 也不作为正向证据。

## 8. 风险与回滚

1. **旧 Bundle 测试固定 1.0.0 skeleton**：该测试是过期 M5 fixture 假设，必须改为验证真实内容和版本，不得为通过测试把 bundle 降回 placeholder。
2. **Skill exact Logic**：A6E 只发布 canonical Logic identity，不宣告执行实现；实际 LogicRevision/Eval 后续用新 revision 闭合。
3. **Capability 目录与 Binding 混淆**：目录 published 不等于 binding available；A6F 页面必须分别展示。
4. **历史 D3 回归**：保留 W03、L05、dry-run 与既有 gate；升级只替换 placeholder。
5. **迁移回滚**：降级只移除本波全局 capability 表；不触碰 A6A-A6D 租户数据。

## 9. 评审—整改—复审

### 9.1 第一轮评审发现

| ID | 发现 | 结论 |
|---|---|---|
| R1 | 只有 CapabilityBinding，没有 CapabilityRevision authority | BLOCKER |
| R2 | 直接用 Bundle JSON 会违反 W0A L0 authority 边界 | BLOCKER |
| R3 | 37 Logic 尚无真实 Eval/Route，不能伪装 published-active | BLOCKER |
| R4 | A6E 若创建组织实例会和 A6F 安装/API 职责重叠 | BLOCKER |
| R5 | 旧三同事 placeholder 与六角色目录冲突 | BLOCKER |
| R6 | Bundle 1.1.0 的 D3 真实交付不能被覆盖删除 | BLOCKER |

### 9.2 整改

- 增加 `aip6_004` capability revision/alias 全局真源；
- SolutionPack 作为发布输入，发布后 PostgreSQL exact revision 才是运行读取真源；
- 37 SkillTemplate 使用 `evaluated + blocked`，不伪称 production-active；
- A6E 只发布定义，A6F 才处理组织实例与 Canonical API/UI；
- 删除 placeholder，保留 D3 W03/L05/Eval；
- 增加真实库 exact readback、幂等、漂移与零租户副作用门。

### 9.3 第二轮复审

| 退出门 | 结果 |
|---|---|
| L0/L1/L3 authority 分层唯一 | PASS |
| 六角色/37 Logic/十 Capability 可逐项定位 | PASS |
| Coordinator、alias、职责不产生额外 identity | PASS |
| Provider/Route/Eval/W0B unknown 失败关闭 | PASS |
| 不提前创建组织实例或公共生产对象 | PASS |
| D3 历史交付保留且可回滚 | PASS |
| 迁移、测试、exact readback 和零业务数据副作用可执行 | PASS |

最终结论：`APPROVED_FOR_IMPLEMENTATION`。本清单授权 A6E，不授权 A6F 或 W0B/W2 越门编码。

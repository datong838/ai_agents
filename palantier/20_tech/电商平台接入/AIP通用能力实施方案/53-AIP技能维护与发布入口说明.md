# 53 · AIP 技能维护与发布入口说明（运维地图）

> 状态：`CURRENT` · 只改 `aos-platform-w1-aip` UI 指引；发布权威仍在 SkillRegistry  
> 触发：用户在智能体目录看到「仅已评测 · 未绑定」与「需先完成技能发布」提示，追问去哪维护/发布

## Design Read

运维要在中文目录页看懂：**哪些技能已可跑、剩余未发布是不是故障、去哪补齐**。

## 事实（org-org/dev-project · R2）

| 事实 | 说明 |
|---|---|
| 37 条技能定义 | SolutionPack / SkillTemplate，多数 lifecycle=`evaluated`（仅已评测） |
| 每同事 1 条 Pilot 已发布+绑定 | A02/C02/D03/G04/S04/P02（内容官另加 I01；V01 受视频 Health 影响） |
| 预检可运行条件 | **不要求** 6/6 全绑；要求已发布 Pilot 的 Binding 新鲜就绪快照（约 15 分钟） |
| 黄条「快照已过期」 | 不是缺发布；点目录「刷新」会 **POST refresh-readiness 软重评** 激活 Binding（见方案 55） |

## 运维入口地图

| 环节 | 去哪 | 做什么 |
|---|---|---|
| 看定义与绑定真相 | `/aip/agent-registry` 智能体目录 | 中文技能名、发布态、绑定态、可运行 |
| 看组织实例 | `/aip/agents` 智能体列表 | 实例是否已启用 |
| 评测门（发布前置） | `/aip/evals` Evals 门控 | 对 Logic Graph 跑套件；门控通过才允许 publish |
| 成熟度 | `/aip/maturity` 成熟度楼梯 | L2→L4 门槛说明；不替代 SkillRegistry 写入口 |
| 专业能力绑定 | `/aip/capabilities` 智能体插件 | 组织 Binding；未绑定走「去目录绑定」 |
| 能力导入 | `/aip/capability-import` | 新外部能力 Manifest |
| 模型/路由/健康 | `/aip/model-*` + 运行就绪 | 八维依赖中的 Route/Provider/Health |
| 逻辑编排 | `/aip/logic` 逻辑画布 | Logic 图版本；评测目标 |

## 当前缺口（诚实）

**前台尚无独立「技能发布台」页**：`evaluated → published` 与 SkillBinding 创建目前由受控脚本 / API（SkillRegistry `publish_evaluated`）完成。  
若要把「仅已评测」的其余 30+ 条全部发布并绑定，需另开交付波（Eval 绿 → publish → Binding → 八维就绪），不是点一下目录按钮即可。

R2 验收口径：六同事各自 **至少 1 条 Pilot 技能可运行** 即为 GREEN；全量 37 绑定是后续产品波次。

## UI 本波最小改动

- 目录页阻断态按钮 `title`：按真实 `blockers` 中文提示，不再笼统写「需先完成技能发布」
- 目录页增加一行入口提示：Evals / 插件 / 运行就绪

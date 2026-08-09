# AIP 现状代码、API、页面能力矩阵与缺口清单

> 状态：**2026-08-10 审计快照 · 待评审**
> 范围：`aos-platform/m1`、`org-org/dev-project`、AIP 菜单 19 个页面。
> 说明：本文件记录事实，不构成编码授权。

## 0. 使用的 Rules

- 真实 API 回读优先于 UI 文案；服务端空数据优先于静态 fallback。
- `source=sampled/demo/fallback` 不得标记为生产真实能力。
- 页面能打开、按钮能点、单测有 Mock 均不等于端到端完成。

## 1. 总体评级

| 域 | 评级 | 事实 |
|---|---|---|
| Logic Graph/DryRun/Publication | GREEN/YELLOW | canonical revision/hash、CAS、运行与发布证据已形成；旧 `aip_logic_engine` 默认仍走 Mock |
| Evals | YELLOW | API 与页面门控骨架真实；当前租户无 Eval Suite，尚无六同事 EvalPack |
| Draft | YELLOW | 页面为空态真实；旧引擎仍有进程内存储，需要确认 canonical store 与 Approval/Receipt 一致性 |
| Agent/Registry | RED | API 回读为空；目录/列表仍显示 11/5 个静态 Agent，形成“展示大于能力” |
| TAOR/Task | RED | Task/Plan/Checkpoint 是进程对象，缺 org/project、revision、幂等和持久化；旧执行默认 Mock；Observe 定义但主循环未调用 |
| Analyst | RED | 后端查询 `shops/inventory/sales` 内存样例；未知表返回 fallback；不能支撑栖月汇真实经营分析 |
| Assist/Studio | YELLOW | API/页面存在；Studio 在无 Agent 时无法配置，新建智能体仍禁用；与六同事任务链未贯通 |
| Wiki/Memory | RED/YELLOW | O1 Wiki 页面已封板，但 AIP long-memory 等仍是单例；三层运行记忆与治理晋升未接通 |
| Lineage | RED/YELLOW | 页面与接口存在；旧引擎可生成固定 6 段 trace，当前显示内容不能作为真实决策证据 |
| Observability | YELLOW | HTTP 进程采样真实；趋势为合成、Token 为估算、Dashboard 为 Mock；语义标识较诚实但能力不足 |
| Model/Route/Capacity | YELLOW/GREEN | 供应商、路由、容量页面和接口较完整；Model Catalog 在当前租户为空，需要注册闭环和成本真值 |
| Capability/Import | RED/YELLOW | Capability 页面可调用接口；导入向导大量预填扫描/测试/知识文档结果，尚未证明真实导入闭环 |

## 2. 页面交互矩阵

| 页面 | 当前表现 | 关键缺口 | 目标方案 |
|---|---|---|---|
| AIP 助手 | 会话壳、建议问题、SSE 文案 | 建议仍是平台样例；未绑定六同事/Task/Selection；权限证据不可见 | 07 |
| 对话机器人 Studio | Prompt/Tool 保存接口 | 当前无 Agent；“新建智能体”禁用；发布条件未形成统一证据视图 | 03/05/07 |
| AIP 分析师 | SQL/Chart/Map/Raw | 内存 Northampton 店铺样例；保存本机；非 Ontology 真查询 | 07 |
| AIP 逻辑画布 | canonical Graph、保存、DryRun | 首屏模板是本地未保存；旧执行器仍并存；Task/TAOR 未统一 | 02/05 |
| Agent 工具面板 | 工具配置与调用入口 | 质量分、测试数等存在静态展示；工具调用与 ActionType 策略未统一 | 03/04 |
| 成熟度楼梯 | L1-L4 导航与熔断演练 | 工作区/Agent 状态多为展示；申请、发布、降级证据未统一 | 05 |
| 智能体插件 | C0/C1/C2 分类 | 列表疑似默认数据；真实凭据、回执、租户实例与配额闭环不足 | 03/08 |
| 智能体目录 | 展示 11 Agent | API 实际为空，失败时回退 `MOCK_AGENTS`，状态严重失真 | 03 |
| 智能体列表 | 展示 5 Agent、向导 | 直接初始化 `MOCK_AGENTS/MOCK_MODELS`；发布/暂停等并非 canonical 回读 | 03 |
| 智能体导入 | 五步向导 | 扫描、映射、连通、安全结果是预定义数组；缺异步 Job/receipt | 03 |
| 能力导入 | 四步向导 | 预置 Wiki 文档/环境变量/测试项；未形成 Manifest revision + install receipt | 03/08 |
| Evals 门控 | 真实空态、可创建样例 | 缺六同事用例与业务数据集；需绑定精确 Logic revision/hash | 05/11 |
| Draft 审批台 | 真实空态 | 需与 ActionProposal/Approval/Receipt、职责分离和持久化对齐 | 04 |
| 决策谱系 | 6 段因果链展示 | 当前内容呈现为固定样例；缺真实 run/evidence/receipt 关联 | 05 |
| 可观测性 | HTTP sampled 指标 | Token 估算、趋势推演、Dashboard Mock；缺 Agent/Task/Logic 成本真值 | 05/09 |
| 模型目录 | 当前 0 模型 | 缺 provider->catalog->registered->route 的显式操作闭环 | 09 |
| 模型供应商 | 插件/凭据/默认网关 | 能力较完整；需统一 secretRef、健康、运行态和组织实例 | 09 |
| 模型路由 | 版本化规则和测试 | 当前规则需验证真实注册模型；图像模型不能成为文本 fallback | 09 |
| 容量管理 | 限额/用量 | 当前用量 0；需按 Agent/Task/租户预算与真实 token/cost 归因 | 09 |

## 3. 跨页面视觉与易用性问题

1. 1280px 视口下，双层左侧导航约占近半屏，AIP 主内容被裁切；分析师、Evals、可观测性尤为明显。
2. 页面把“产品导航树”和“任务工作区”同时永久展开，复杂编辑页缺少聚焦/全屏模式。
3. “真实 API”徽标与“采样推演/估算/静态数据”并列，用户容易把传输真实误解为业务真实。
4. 导入向导在未执行扫描前就展示“可达、许可证、测试通过”等结论，违反证据时序。
5. 同类动作命名不一致：新建智能体、导入 Agent、插件引入、能力导入、Capability Manifest 缺少统一对象关系。

## 4. 代码级关键缺口

| 编号 | 代码事实 | 风险 |
|---|---|---|
| C01 | `aip_logic_engine.execute_flow()` 默认 `_execute_mock`，仅环境变量切 Harness | 生产路径可能误入 Mock |
| C02 | `aip_task_model.Task` 无 org/project/revision/idempotency/evidence refs | 无租户与可重放保证 |
| C03 | `TAORLoopController._observe()` 未在成功循环中调用 | 上下文/产物观察链实际断开 |
| C04 | TAOR semantic/episodic memory 仍为空数组 | 行业 Wiki 没有被消费 |
| C05 | 多个 AIP engine 使用 Singleton dict | 重启丢失、跨租户混用风险 |
| C06 | Agent Registry API 为空但 UI fallback 为静态列表 | 状态失真，错误验收 |
| C07 | Analyst 是内存 SQL 和 fallback 数据 | 无法验证真实电商分析 |
| C08 | Observability Token/趋势为估算/合成 | 不能用于预算和 SLA |
| C09 | Lineage 可构造固定默认 trace | 不能证明真实调用链 |
| C10 | 新旧 `/v1/aip/*`、`/api/aip/*`、phase3 路由并存 | 契约漂移与双写风险 |

## 5. 已暂停的小项

O1 对象探索下拉、真实订单字段、商品筛选、图谱布局等 UX7 小项已记录并暂停。本轮仅在 AIP 方案中保留其上游依赖：AIP 分析师/Agent 必须消费 O1 canonical read model；不重新打开 O1 Waves 1～10。

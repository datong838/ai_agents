# 57 · AIP 逻辑画布蓝图差距清单 + 十类共享能力定义对账

> 状态：`CURRENT` · 只对账，本波不改码  
> 触发：用户对比 `http://127.0.0.1:5174/aip/logic` 与 `foundry/html/aip-logic.html`；并追问「10 个通用智能体」方案是否有定义  
> 租户：`org-org/dev-project` · 只改文档，不改 `w2`

## 1. 逻辑页：蓝图 vs 现网差距

| 维度 | 蓝图 `aip-logic.html` | 现网 `/aip/logic`（`LogicCanvasPage`） | 差距判定 |
|---|---|---|---|
| 信息架构 | Tab：**编辑 / 自动化 / 运行历史** | 单页堆叠：工具栏 + 画布 + 发布/试跑/历史面板 | **大**：缺独立 Tab 分区 |
| 顶栏动作 | 「取消」「保存到分支」 | 「保存」「刷新」「安全试跑」+ Draft/Evals 链 | **中**：无「分支」语义；多运维门禁按钮 |
| 左栏 | **Block 组件库**（10 种块，中英并列） | 调色板存在（同 10 种 kind），视觉为工程面板 | **中**：能力齐，观感未对齐蓝图 |
| 中栏 | 「编排 · 块链」纵向节点链 + 分支双栏 + 汇聚 | 自由坐标 Canvas（节点拖拽） | **大**：交互范式不同（链 vs 自由图） |
| 右栏 | 「配置 · 选中节点属性」（decision / artifacts / open_qs） | `LogicGraphInspector` + Publication/Run 面板 | **中**：有检查器，缺蓝图级 Handoff 配置密度 |
| 演示数据 | 风险分诊样例（订单 ORD、LLM 提示、分支） | 默认 WorkOrder 模板 4 节点 | **小**：样例故事不同，非功能缺口 |
| 自动化 Tab | Uses 列表 + 编辑弹窗（演示） | 无对等产品 Tab | **大**：产品未交付 |
| 运行历史 Tab | 独立表格式历史 | 同页内运行历史区（需先保存回读） | **中**：有权威读回，缺蓝图布局 |
| 文案军规 | 标题「风险分诊编排」等演示文案 | 「AIP Logic 无代码编辑器」+ 方案味 lede | **小**：可再产品化（见军规 52） |

### 结论（逻辑页）

1. **后端权威能力已有**：Graph 持久化、revision/hash 回读、Dry-Run、Publication、Run 历史。  
2. **与蓝图的主差距在壳层 IA/视觉**：三栏+Tab、块链叙事、自动化 Uses、分支保存话术。  
3. **不要把蓝图演示数据当真源**；现网诚实门禁（未保存不可试跑等）应保留。

### 建议收口波次（待拍板再编码）

| 波 | 内容 |
|---|---|
| L-UI-1 | Tab 壳：编辑 / 运行历史（自动化可先只读占位） |
| L-UI-2 | 左调色板视觉对齐蓝图；中栏可保留自由图但增加「块链预览」可选 |
| L-UI-3 | 选中 Handoff 节点时右栏对齐 decision/artifacts/open_qs 密度 |

---

## 2. 「10 个通用智能体」方案定义对账

截图底栏「共享技能 AGENT」（素材采集…数据复盘）**不是**逻辑画布蓝图本体，而是**工作台总控 / 多媒体流水线**产品叙事。

### 方案裁决（必须读）

权威冻结：

- `18-AIP-W0A十类共享专业Capability目录别名与六角色职责Crosswalk.md`（`APPROVED_FOR_A6E_INPUT`）
- `16` 审查报告 · `17` W0 增量方案 · `31` BIND-1

**正名**：这是 **十类共享专业 Capability（能力目录）**，**不是**必须常驻的 10 个运行 Agent。

| # | 稳定 ID | 中文名（与截图一致） |
|---:|---|---|
| 1 | `material.collect` | 素材采集 |
| 2 | `strategy.plan` | 策略规划 |
| 3 | `copy.generate` | 文案生成 |
| 4 | `script.compose` | 脚本撰写 |
| 5 | `speech.synthesize` | 语音合成 |
| 6 | `video.compose` | 视频合成 |
| 7 | `content.review` | 内容审核 |
| 8 | `live.orchestrate` | 直播编排 |
| 9 | `platform.adapt` | 平台适配 |
| 10 | `performance.review` | 数据复盘 |

### 与「六数字同事」关系

| 概念 | 是不是这十个 | 说明 |
|---|---|---|
| 六数字同事 | 否 | L1 AgentTemplate：内容官/数据参谋等业务责任主体 |
| 十类 Capability | 是 | 可发现专业能力；由 Binding 挂到技能/同事上执行 |
| Coordinator / 内容总监 | 否 | 内容官的统筹职责 profile，不占第十一能力 |

工作台文案可称「共享技能 Agent」，AIP 权威层必须以 **Capability ID + Binding** 计；禁止再复制 10 个常驻 AgentInstance。

### 现网落地状态（诚实）

| 层 | 状态 |
|---|---|
| SolutionPack / 目录定义 | **已有**：插件页「10 类专业能力」 |
| 组织 Binding | **部分**：当前租户约 3/10（如 `strategy.plan`、图像/视频生成链相关），其余诚实「未绑定」 |
| 前台入口 | `/aip/capabilities`（智能体插件），非逻辑画布底栏 |

补充：运行侧还出现过 `image.generate` / `video.generate` 等多媒体生成绑定，属 **扩展能力**，不改写 W0A 十类 canonical 名单。

---

## 3. 非目标

- 本清单不编码、不改 w2  
- 不把蓝图自动化演示接成真触发器而不走 Draft/Receipt  
- 不「生成十个 Agent」凑数  

## 4. 证据指针

- 蓝图：`docs/palantier/foundry/html/aip-logic.html`  
- 现网：`apps/web/src/pages/s2/LogicCanvasPage.tsx`  
- 十类冻结：`…/AIP通用能力实施方案/18-…Crosswalk.md` §4  
- 总控视觉叙事：`foundry/html/workshop-task-cockpit.html`（共享技能条）

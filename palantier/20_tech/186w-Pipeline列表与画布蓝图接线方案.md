# 186w · Pipeline 列表与画布蓝图接线方案

| 字段 | 内容 |
|------|------|
| 状态 | ✅ **v1.0** · 已编码 |
| 版本 | **v1.0** · 2026-07-20 |
| 分支 | **`w1`** |
| 触发 | 产品面 `/data/pipelines` 仅有简陋列表（图3），缺 PB-02 画布；与蓝图图1/图2 层次不符 |
| 对齐 | [05](../05-数据集成Connectors-Pipeline-Dataset产品方案.md) PB-01/02 · [80](80-蓝图按钮体系与复杂交互页层次规范.md) · HTML 真源 `pipeline-list.html` / `pipeline.html` · production-ui-no-temp |

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| **先看技术方案与蓝图，禁止自由发挥** | 布局/层次/控件以 HTML 真源为准，不另造卡片堆 |
| 上线态 | 列表/画布读真实 `/v1/pipelines`·`/v1/datasets`；无假保存 |
| 最小更改 | 重做列表结构 + 新增画布路由；不改 Data OS API |
| 80 按钮 | 顶栏 `btn` / `btn-nav` / `btn-primary`；禁止 muted 当导航 |

---

## 1. 问题对照

| | 蓝图（须对齐） | 现状（禁再犯） |
|--|----------------|----------------|
| **图2 · PB-01 列表** | `pipeline-list.html`：左项目树（管道/媒体集/数据集）+ 右「最近编辑」大卡 · 卡可点进画布 | `PipelinesPage`：粗糙 `BpSplit` + 裸 id 按钮 + 向量调试占主舞台 |
| **图1 · PB-02 画布** | `pipeline.html`：顶栏分支/保存/提议/计划/部署 · 中网格 DAG · 底预览 · 右输出属性 | **无路由**；提案页「打开管道画布」误链列表 |

侧栏「画布编辑」= 工作台 Module，**不是**管道画布。

---

## 2. 目标 / 非目标

### 2.1 目标

1. `/data/pipelines` **视觉与层次**对齐 `pipeline-list.html`（项目树 + 最近编辑卡）。  
2. `/data/pipelines/:pipelineId` 对齐 `pipeline.html`（DAG + 底预览 + 右属性）。  
3. 列表卡 / 树节点 → 画布；面包屑可回列表。  
4. 卡片展示中文可读名（栖月汇表映射），状态徽标对齐蓝图语义（已部署/草稿…）。  
5. 向量索引（104）**退出列表主舞台**，仅在画布「高级」折叠（不挡蓝图层次）。

### 2.2 非目标（本刀）

- 真 Filter/Join SQL 节点编辑器（G-PB-02 / 183w）  
- 分支 Git / 假「保存」写内存  
- Doc Intel 专页深接线（可链既有 `pipeline-doc-intel` 提案后置）

DAG 节点策略（诚实）：当前管道多为 Source→Dataset，画布渲染 **输入(Source) → 变换(Ingest) → 输出(Dataset)** 三节点；**不伪造**蓝图示意里的 Join，除非元数据有算子图。

---

## 3. 路由与入口

| 路由 | 蓝图 | 组件 |
|------|------|------|
| `/data/pipelines` | WF-PB-01 | `PipelinesPage` 重做 |
| `/data/pipelines/:pipelineId` | WF-PB-02 | 新建 `PipelineCanvasPage` |
| 提案「打开管道画布」 | — | 链到**当前选中/首条**画布或列表说明，禁止空喊「画布」却进列表 |

---

## 4. 工程落点

| 文件 | 变更 |
|------|------|
| `docs/.../186w-….md` | 本文 |
| `apps/web/src/pages/s2/data.tsx` | 列表按蓝图重排 |
| `apps/web/src/pages/s2/pipelineCanvas.tsx` | 画布页 |
| `apps/web/src/pages/s2/routes.tsx` · `nav.ts` | 注册路由 |
| `apps/web/src/styles.css` | `.bp-pipe-*` · `.grid-pattern` · `.pipeline-node` · `.flow-line`（自 demo.css） |
| `remainder.tsx` | 修正误链文案 |

---

## 5. 验收

- [x] 列表视觉接近图2：左树 + 右大卡，无开发腔向量主区  
- [x] 点卡进入画布 `/data/pipelines/:id`：顶栏 · 网格 DAG · 底表 · 右属性  
- [x] 栖月汇管道中文名可读；提案误链已修  
- [x] 部署/计划跳真实 builds · schedules  

---

## 6. 修订

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-07-20 | 初版：列表+画布按 HTML 真源接线 |

*v1.0 · w1 · 蓝图优先 · 禁止自由发挥*

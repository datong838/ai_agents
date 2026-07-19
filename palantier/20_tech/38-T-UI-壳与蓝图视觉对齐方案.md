# 38 · T-UI 壳与蓝图视觉对齐方案

> **版本**：v1.6 · 2026-07-18（§10 AIP 卡序：业务→决策→配置）  
> **任务**：端面 Web 与 [`foundry/html`](../foundry/html/) **v1.6.5** 差距过大 → 壳/导航/概览对齐（T-UI S1.5）  
> **对齐**：[T-UI](T-UI-前端工程与foundry-html落地规范.md) · [34](34-系统启动与蓝图符合性检查记录.md) · demo.js `DEMO_PAGES` / demo.css  
> **工程**：`aos-platform/apps/web`  
> **原则**：视觉真源=html；不另起皮肤；契约仍只打 aos-api；S2 全页迁入可后置但**侧栏不得缺项**

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| UI = foundry/html | Token / 壳 / 侧栏叙事与 Demo 同构 |
| 先方案后编码 | 本文通过后再改 AppShell |
| 最小更改 | 本刀聚焦**壳+概览+导航完整**；不重写全部业务页交互 |
| 诚实 | 未迁页用「蓝图占位」标 S2，禁止假装已实现 |

---

## 0. 概览分区序（v1.1 修订）

**问题**：`index.html` 曾把「Apollo 交付引擎」插在 AIP 与本体之间，打断业务主链路叙事。

**结论**：Apollo = 运维发布横切能力，**不得**插在业务链中间。

| 面 | 强制顺序 |
| --- | --- |
| 侧栏 `DEMO_PAGES` | 工作台 → AIP → 本体 → 数据 → Apollo |
| 概览分区卡片 | **同序**：工作台 → AIP → 本体 → 数据集成 → Apollo |

**落点**：仅调 `foundry/html/index.html` 区块顺序；侧栏 / 链接 / 页内容不变。

---

## 1. 差距诊断（现状）

| 维度 | html 蓝图 | apps/web 现状 | 本刀目标 |
| --- | --- | --- | --- |
| 品牌区 | 图标 +「AI操作系统」+ 副标 | 仅「AOS」大字 | ✅ 同构 |
| 侧栏 | 全量 `DEMO_PAGES` + SVG 图标 | 叙事子集、无图标 | ✅ 全量 + 图标 |
| 顶栏 | 面包屑 · 搜索 · 通知 · 外观菜单 | 「Wave-1」+ select | ✅ 面包屑 + 外观下拉 |
| 概览 | 分区入口卡片（工作台/AIP/本体/数据/Apollo） | 一行 health | ✅ 同构布局 |
| 外观默认 | dark | system | ✅ dark |
| 业务页细节 | 各 html 丰富 | 功能页偏「表单壳」 | ⚠ 本刀只加 PageChrome；深页迁入归 S2 |

---

## 2. 非目标

- 一次迁完全部 DEMO 业务页（S2）
- Playwright 视觉 CI（T-UI 已列，本刀不挡）
- 改 aos-api / 破坏既有护栏单测

---

## 3. 代码落点

| 路径 | 动作 |
| --- | --- |
| `src/nav.ts` | 对齐 `DEMO_PAGES` 全序；`live` / `s2` |
| `src/shell/icons.tsx` | 移植 demo.js ICONS |
| `src/shell/AppShell.tsx` | 品牌 · 图标导航 · 面包屑 · 外观菜单 · 版本脚 |
| `src/styles.css` | `.aos-nav-*` 密度与 html 一致；侧栏 14rem |
| `src/pages/OverviewPage.tsx` | 按 index.html 分区卡片重做 |
| `src/pages/BlueprintStubPage.tsx` | S2 占位（标明蓝图 id） |
| `src/components/PageChrome.tsx` | 页标题/副标统一 |
| `src/App.tsx` | 注册 S2 占位路由 |
| `src/lib/appearance.ts` | 默认 **dark** |
| 主路径页 | 套 PageChrome（最小 diff） |
| 34 / 31 / 00 | 回写 S1.5 |

---

## 4. 验收

| 项 | 通过 |
| --- | --- |
| 侧栏段序 | 工作台 → AIP → 本体 → 数据 → Apollo |
| 概览分区序 | 与侧栏同序（Apollo 在数据集成之后） |
| 侧栏项数 | 与 DEMO_PAGES 页条目一致（含 S2） |
| 概览 | 可见「AI操作系统」叙事与分区入口 |
| 外观 | 下拉三项；默认深色；刷新保持 |
| 回归 | vitest 绿；蓝图检查脚本 nav 段仍过 |

---

## 5. 完成判定

- [x] 方案入 00  
- [x] 壳/导航/概览落地  
- [x] 单测绿（14）  
- [x] 34 §3 更新 S1.5  

---

## 6. 补丁 · 工作台域 hint 与 Module 用语（v1.2）

**问题**：概览「工作台」域副文案字号偏大、层次弱于 [`index.html`](../foundry/html/index.html)（蓝图 `text-xs text-gray-500`）；界面仍混用英文 `Module`。

**结论（最小改）**：

| 项 | 定稿 |
| --- | --- |
| hint 样式 | `.bp-domain > p.hint` → **0.75rem**、次要灰、`line-height: 1.55`、下边距贴近标题（对齐蓝图 text-xs） |
| 用语 | 用户可见文案 **Module → 模块**（类型名 / API path 不改） |
| 文案对齐蓝图 | 补「，不是并列产品。」；示例条补「（勿与入口平级理解）」 |
| 蓝图同改 | `foundry/html/index.html` 工作台区块同步中文 |

**落点**：`OverviewDomainGrid.tsx` · `styles.css` · `index.html` · 概览控制面一处 `Module` 展示。

**非目标**：不动四域指标卡布局；不重做工作台深页。

---

## 7. 补丁 · 概览顶栏定位句 + 工作台可见中文（v1.3）

**问题**：
1. 概览右侧大标题「AI操作系统」与侧栏品牌重复；
2. 工作台面向业务人员，可见文案仍混英文（WorkOrder / Evals / Inbox / Buddy / Filter…）。

**定稿**：

| 项 | 值 |
| --- | --- |
| 概览 `h1` | `数据操作系统 · 本体数字孪生 · AIP 人工智能平台 · 工作台`（对齐 `index.html`） |
| 字号 | 与侧栏 `.brand-title` 同级：**0.875rem / font-weight 500**（不与品牌抢大标题） |
| 建设路径 lede | `连接器 → 管道 → 数据集 → OKF / 本体 → AIP → 工作台` |
| 中文例外 | **仅 Wiki 保留英文**；产品缩写 AIP / OKF 可保留 |
| 工作台域 | Buddy→智能助手 · WorkOrder→工单 · Evals→评测 · Inbox→收件箱 · Filter/Table/Object View/Action→筛选/表格/对象视图/动作 |

**落点**：`PageChrome`（可选 `titleTone=brand`）· `OverviewPage` · `OverviewDomainGrid` · `index.html` 工作台区块。

---

## 8. 补丁 · 概览顶栏面包屑与探活去重（v1.4）

**定稿**：

| 项 | 值 |
| --- | --- |
| 面包屑 | `工作区 > AOS 概览`（对齐 `index.html` initShell） |
| 顶栏 `ApiStatusBar` | **仅宕机时显示**；可达时不渲染（避免与页内状态条重复） |
| 页内状态条 | ~~绿点+模型~~ → **删除**（见 §9） |

---

## 9. 补丁 · 控制面并入工作台（v1.5）

**定稿**：删除独立「操作系统控制面」区块；独有指标并入「工作台」域，**保持工作台展示风格**（KPI 四格 + 唯一入口 Hero + 模块示例 + 底链）。

| 控制面原项 | 并入方式 |
| --- | --- |
| 接口健康 · 绿点 | 工作台标题旁绿点 + KPI「接口健康」 |
| 默认大模型 | KPI「默认大模型」 |
| 评测门控 | 与原「评测」合并为一格 |
| 工作台模块 / 打开应用列表 | 去掉重复 KPI；保留 Hero「应用列表」 |
| 模型路由 · 插件 · 人工审核 | 底链（不另起第二套瓦片墙） |
| 工单 | 保留 KPI |

---

## 10. 补丁 · AIP 概览卡序：业务 → 决策 → 配置（v1.6）

**问题**：AIP 区把「成熟度楼梯」放第一，演示从治理框架起讲，业务入口靠后。

| 段 | 卡片（左→右） |
| --- | --- |
| **业务** | 对话工作室 → 逻辑画布 → 工具面板 → 重能力接入 |
| **决策** | 提案审批台 → 评测门控 → 决策谱系 |
| **配置** | 模型供应商 → 模型路由 → **成熟度楼梯**（末位） |

**hint：** `业务工作室 → 逻辑/工具 → 提案决策 → 模型配置`  
**落点**：`OverviewDomainGrid.tsx` · `nav.ts` · `foundry/html/index.html` · `demo.js` 侧栏同序

---

*v1.6 · 2026-07-18 · AIP 卡序业务→决策→配置*  
*v1.5 · 2026-07-18 · 控制面并入工作台*  
*v1.4 · 2026-07-18 · 概览面包屑 / 探活去重*  
*v1.3 · 2026-07-18 · 概览定位句 + 工作台中文*  
*v1.2 · 2026-07-18 · 工作台 hint 字号 + Module→模块*  
*v1.1 · 2026-07-17 · 概览分区与侧栏同序（Apollo 在数据之后）*

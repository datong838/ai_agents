# 38 · T-UI 壳与蓝图视觉对齐方案

> **版本**：v1.1 · 2026-07-17  
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

*v1.1 · 2026-07-17 · 概览分区与侧栏同序（Apollo 在数据之后）*

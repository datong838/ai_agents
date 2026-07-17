# T-UI · 前端工程与 foundry/html 落地规范

> **版本**：v1.1 · 2026-07-17（**Appearance 浅/深/跟随系统**）  
> **状态**：✅ **方案完成**（可评审 / 可按 T-EVO 开工）  
> **对齐**：[20 §3·§5](20-AOS整体技术方案.md) · [html README](../foundry/html/README.md) · [25](25-LLM-Wiki启示与L2演进补丁.md) · [T-API](T-API-aos-api稳定契约.md) · [08a](../08a-Workshop产品设计线框图.md) · [10 §0.3](../10_v01/10-v0.1技术方案.md) · [26](26-AOS目标态开发计划.md)  
> **读者**：前端 · 全栈 · 架构

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| UI = foundry/html | 视觉 / IA / 主路径禁止另起皮肤 |
| 写到 UI 必引用蓝图 | 本篇定义如何引用与组件化 |
| 契约优先 | UI 只打 `aos-api`，禁直连上游 SDK（军规 [23](23-AOS开源引用与交付军规.md) R-ARCH-01） |
| 最小更改 | 从静态 Demo 渐进迁，不一次性重写 |

---

## 1. 目标与非目标

| 目标 | 非目标 |
| --- | --- |
| 把 `foundry/html` **v1.6.1** 变成可维护前端工程 | 用 ToolJet/Appsmith 发行壳冒充 AOS |
| Token / 壳 / 路由与 Demo 同构 | 第三套「管理后台」皮肤 |
| 桌面（Tauri）与 Web 共享 ui-kit | UI 直连 Dify / Airbyte / LiteLLM |

---

## 2. 真源与版本钉

| 钉 | 值 |
| --- | --- |
| Demo 真源 | [`docs/palantier/foundry/html/`](../foundry/html/) **v1.6.5** |
| Token 源 | `html/assets/demo.css`（含 **Appearance 语义色**）+ Tailwind 工具类约定 |
| 壳导航 | `html/assets/demo.js` · `DEMO_PAGES`（侧栏顺序不可擅自改叙事） |
| 外观 | `localStorage aos-appearance`：`light` \| `dark` \| `system`；解析后写 `html[data-aos-theme]` |
| 映射表 | [html README](../foundry/html/README.md) · [补页清单](../foundry/html/HTML补页改页任务清单.md) |

**侧栏 / 概览分区叙事（强制）：** 工作台 L3 → AIP → 本体 → 数据集成 → 交付 Apollo  
（Apollo 为运维发布，概览卡片不得插在业务链中间。） 

**命名陷阱：** `agents.html` = Chatbot Studio；边缘代理 = `data-connection-agents.html`。

---

## 3. 工程落点（自有仓）

```text
aos-platform/
├── apps/web/                 # Web SPA · **React 18 + TypeScript**（已决）
├── apps/desktop/             # 自 mybuddy-v01/desktop 演化：壳保留、内容区换路由
└── packages/
    ├── ui-kit/               # 颜色 / 间距 / 侧栏 / 顶栏 / Tab / Badge
    ├── page-shell/           # 等价 DemoUI.initShell
    └── contracts-client/     # 由 T-API OpenAPI 生成的 TS client
```

| 阶段 | 做法 | 退出标准 |
| --- | --- | --- |
| **S0** | 静态 html 继续售前 | 本地 `python -m http.server` 可演示 |
| **S1** | 抽 ui-kit Token；壳组件；运营台通 `/v1/object-sets/query`（Mock→真） | Inbox 可读 Object 列表 |
| **S2** | 按域迁页（工作台 → AIP → 本体 → 数据 → Apollo） | 侧栏全绿、无死链 |
| **S3** | 桌面 WebView 加载同构路由 | 与 v0.1 三栏助手可并存切换 |

### 已决技术选型

| 项 | 结论 | 理由 |
| --- | --- | --- |
| 框架 | **React 18 + TypeScript** | 与 Tauri 生态、ToolJet frontend 思路接近；团队可组件化 html |
| 路由 | React Router | 与侧栏 `DEMO_PAGES` 一一映射 |
| 样式 | Tailwind + ui-kit Token（自 demo.css） | 与 Demo 同构 |
| 数据 | TanStack Query + contracts-client | 只打 aos-api |
| 视觉回归 | **Playwright** 截图对比关键页（S2 起 CI） | 防 UI 分叉（20 R3） |
---

## 4. 组件化映射规则

### 4.1 页 → 路由（摘要）

| html | 建议路由 | 所属域服务 |
| --- | --- | --- |
| `workshop*.html` | `/workshop/*` | Module Runtime |
| `aip-*.html` · `agents.html` | `/aip/*` | AIP |
| `ontology*.html` · `funnel.html` · `ontology-graph-health.html` | `/ontology/*` | Ontology |
| `data-connection*.html` · `pipeline*` · `dataset` · `schedules` … | `/data/*` | L1 |
| `apollo-*.html` | `/apollo/*` | Apollo |

### 4.2 引用模板（详稿强制，本篇示范）

**UI 蓝图：** [`workshop-canvas.html`](../foundry/html/workshop-canvas.html)

- 分区：左 Layout 树 · 中 Canvas · 右属性 / Widget 选择  
- 控件：Header / Page·Inbox / Section / Overlay；变量 / Events  
- 态：构建态 vs 预览运行态；顶栏「发布」→ Apollo  
- 实现：`ModuleSchema` ↔ Layout；`WidgetRegistry` ↔「+ 添加 Widget」

完整域内引用见 T05～T09。

### 4.3 护栏类 UI（产品补强，前端必须实现）

| 护栏 | 蓝图页 | 前端行为 |
| --- | --- | --- |
| Selection≤10 维 | `workshop-module.html` | 维数计数；超限禁加筛选 |
| Table>1万行 | 同上 | 强制分页 / 虚拟滚动 |
| Widget Marking | 同上 | 无权限 Widget 不渲染 |
| 事件幂等 | module / object-view | 按钮防抖 + 带 `idempotencyKey` |
| L4 熔断徽标 | `aip-maturity.html` | 展示降级态 |
| 128KB 短路 | `sync-routing.html` | 路由选项 |
| DocIntel DLQ | `pipeline-doc-intel.html` | 死信列表 |
| Vault 引用非明文 | `apollo-config.html` | 密钥槽只显示 ref |

### 4.4 Appearance（浅色 / 深色 / 跟随系统）

> 对标常见产品「外观」菜单（如 Dify：浅色 · 深色 · 跟随系统）。**默认深色**（售前控制台气质）；浅色为可选项。

| 项 | 约定 |
| --- | --- |
| 选项 | `light` · `dark` · `system` |
| 持久化 | `localStorage` 键 `aos-appearance` |
| 解析 | `system` → `prefers-color-scheme`；结果写入 `html[data-aos-theme="light\|dark"]` |
| 默认 | 未设置时按 **dark**（与历史蓝图一致） |
| Wave-1 | React `ThemeProvider` 必须承接同一套 Token 名，禁止另起色板 |

| Token | 用途 |
| --- | --- |
| `--aos-bg` | 页面底 |
| `--aos-aside` · `--aos-header` | 壳 |
| `--aos-card` · `--aos-elevated` | 卡片 / 浮层 |
| `--aos-border` | 分割线 / 描边 |
| `--aos-text` · `--aos-muted` | 主/次文字 |
| `--aos-accent` | 强调（浅深共用色相） |

| 阶段 | 做法 |
| --- | --- |
| **现已做** | 全站 html 标 `aos-themeable`；顶栏「外观」浅色/深色/跟随系统；Token 见 `demo.css` |
| **后续** | 新页优先语义类（`.aos-bg` 等）；渐进去掉写死 `slate-*` |
| **禁止** | 另做第三套布局；Marketplace 式皮肤商店 |

**验收：** 顶栏可切换且刷新保持；`system` 跟随 OS；全站浅色可读；React 沿用同 Token 名。

---

## 5. 开源参考（已本地核对）

> **自有所需功能**见上文 §1～§4（html 真源 · React 工程 · 护栏 UI · 只打 aos-api）。全量选型总表见 [21](21-AOS开源选型与功能清单.md) §2.D。

| 参考仓（`mybuddy-v01`） | 抄什么 | 不抄什么 | 许可证注意 |
| --- | --- | --- | --- |
| `D1_WorkshopFactory/ToolJet` · `frontend/` `server/` | 低代码画布「左树-中画布-右属性」思路、组件注册模式 | 整站品牌壳、其数据模型、对外发行其 UI | 商用前看法务；**交付面禁止 ToolJet 品牌** |
| `D1_WorkshopFactory/appsmith` | Widget 配置 schema 思路 | 默认应用壳 | 同上 |
| `D3_HighPerfGrid/ag-grid` | 大表虚拟滚动 / 列模型 | 业务对象协议 | 社区版/企业版边界 |
| `B3_GraphViz/G6` · `cytoscape.js` | 知识图谱渲染 | Ontology 配置壳 | MIT 类为主 |
| `D4_Map/kepler.gl` | COP 地图层思路 | 独立产品壳 | — |

> **检查结论（2026-07-17）：** ToolJet / Appsmith / ag-grid / G6 等本地仓存在且可浏览。UI **视觉真源仍是 foundry/html**，开源只借「交互模式 / 性能组件」。

---

## 6. 与桌面 / v0.1 关系

| 项 | 策略 |
| --- | --- |
| Tauri 壳 | 保留；窗口 / 托盘 / 本地服务发现 |
| 内容区 | 逐步替换为与 `apps/web` 同构页面（或嵌入 Web） |
| `/v1/buddy/ask` | 经 `contracts-client` 调用；上游 Dify 可换（见 T-EVO） |
| 去品牌 | 延续 [10g](../10_v01/10g-交付面去Dify品牌说明.md) |

---

## 7. 质量门禁

| 门禁 | 标准 |
| --- | --- |
| Token 漂移 | ui-kit 与 `demo.css` 关键色板 diff CI |
| 死链 | 侧栏路由 ↔ html README 映射表一致 |
| 契约 | 禁止 `import` 上游 SDK；只允许 `aos-api` client |
| 可访问 | 主路径键盘可达；无 WF-* 编号露出 |

---

## 8. 已决结论（原缺口已关闭）

| ID | 结论 |
| --- | --- |
| TUI-G1 | **React 18 + TypeScript**（见 §3） |
| TUI-G2 | OpenAPI 真源见 **[T-API](T-API-aos-api稳定契约.md)**；S1 可用 Mock Server 对照契约 |
| TUI-G3 | Playwright 视觉回归列入 S2 CI 门禁 |
| TUI-G4 | Appearance：`light`/`dark`/`system` + Token（§4.4）；Demo **v1.6.5 全站** |

---

## 9. 关联

- 总纲：[20](20-AOS整体技术方案.md) · 索引：[00](00-技术方案索引.md)  
- 契约：[T-API](T-API-aos-api稳定契约.md) · 工作台：[T08](T08-Workshop工作台详细技术方案.md)  
- UI：[foundry/html](../foundry/html/README.md)

---

*T-UI v1.1 · docs/palantier/20_tech*

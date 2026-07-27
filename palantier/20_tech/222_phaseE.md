# Phase E 实施方案 · 端到端集成与回归

> **版本**：v1.0 · 2026-07-26
> **分支**：m1（MacBook 本机）
> **状态**：待确认
> **参考**：222plan-分阶段开发与里程碑计划.md · 222-产品补充说明.md

---

## 一、任务范围

### 1.1 菜单补齐与分组优化

| 页面 | HTML 蓝图 | 当前 nav.ts 状态 | 处理方式 |
|------|-----------|-----------------|---------|
| 智能体注册表 | agent-registry.html | 缺失 | 新增 |
| 智能体列表 | agents.html | 缺失 | 新增 |
| 智能体导入 | aip-agent-import.html | 缺失 | 新增 |
| 能力导入 | aip-capability-import.html | 缺失 | 新增 |
| 创建应用 | workshop-create.html | 缺失 | 新增 |
| 模块管理 | workshop-module.html | 缺失 | 新增 |

### 1.2 菜单分组结构（按视觉稿）

**AIP 决策引擎**：
- 应用层：AIP Assist、Chatbot Studio、AIP Analyst
- 逻辑编排层：AIP 逻辑画布、Agent 工具面板、成熟度楼梯
- 智能体：智能体插件、智能体注册表、智能体列表、智能体导入、能力导入
- 评测与治理：Evals 门控、Draft 审批台、决策谱系
- 决策谱系子项：可观测性（决策谱系选中时可见）

**工作台**：
- 应用列表、订单管理、风险告警管理、态势大屏、Buddy 智能助手、分析建模、创建应用、模块管理

### 1.3 Phase E 开发任务

| 批次 | 任务 | 说明 |
|------|------|------|
| E-1 | Pipeline Builder 深度对接 | E-01~E-06 |
| E-2 | Workshop Module 创建全流程 | E-07 |
| E-3 | Analytics 页面增强 | E-08 |
| E-4 | Agent 创建/导入/目录 | E-09~E-12 |
| E-5 | Wiki 索引/版本对比对接 | E-13~E-14 |
| E-6 | 全量回归测试 | E-15~E-17 |

---

## 二、技术方案

### 2.1 菜单分组实现

在 `nav.ts` 中新增 `NavSubgroup` 类型，用于渲染子分组标题：

```typescript
export type NavSubgroup = {
  subgroup: string;
};
export type NavItem = NavSection | NavSubgroup | NavPage;
```

### 2.2 菜单顺序调整

按视觉稿要求调整：
- 模型管理：模型目录 → 模型供应商 → 模型路由 → 容量管理
- AIP 决策引擎：应用层 → 逻辑编排层 → 智能体 → 评测与治理 → 决策谱系 + 可观测性

### 2.3 路由注册

新增路由到 `routes.tsx`：
- `/aip/agent-registry` → AgentRegistryPage
- `/aip/agents` → AgentsPage
- `/aip/agent-import` → AgentImportPage
- `/aip/capability-import` → CapabilityImportPage
- `/workshop/create` → WorkshopCreatePage
- `/workshop/module` → WorkshopModulePage

---

## 三、实施步骤

### 3.1 第一批：菜单补齐与分组（M-01~M-03）

1. 修改 `nav.ts`：新增 NavSubgroup 类型，添加子分组定义
2. 修改 `nav.ts`：重命名"重能力接入"为"智能体插件"，调整菜单顺序
3. 修改侧边栏组件：支持渲染 subgroup 标题

### 3.2 第二批：新增页面路由注册（R-01~R-06）

1. 检查并创建缺失的 React 页面组件
2. 在 `routes.tsx` 中注册新路由

### 3.3 第三批：Phase E 功能开发（E-01~E-14）

按计划开发 Pipeline、Workshop、Analytics、Agent、Wiki 功能

### 3.4 第四批：回归测试（E-15~E-17）

1. 前端构建验证
2. 后端 pytest 回归
3. 页面功能自测

---

## 四、验收标准

- [ ] 菜单分组正确显示（应用层、逻辑编排层、智能体、评测与治理）
- [ ] 缺失菜单全部补齐（6 个）
- [ ] 菜单顺序符合视觉稿要求
- [ ] 可观测性在决策谱系选中时可见
- [ ] Phase E 全部任务完成
- [ ] 前端构建无错误
- [ ] 后端测试 0 新增失败

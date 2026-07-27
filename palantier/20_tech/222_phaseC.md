# 222 Phase C 技术方案 · Workshop 画布深度对接

> **版本**：v1.0 · 2026-07-25
> **关联**：[222plan-分阶段开发与里程碑计划.md](222plan-分阶段开发与里程碑计划.md)
> **对应章节**：222 第 1-5 章 · 第 25-27 章
> **目标**：将 HTML Demo 中实现的画布交互（9 Tab / 三模式 / 事件向导 / 变量管理 / 组件注册）映射到 React 前端，并对接后端 API
> **状态**：✅ 已完成

---

## 一、核心洞察

后端 Workshop 引擎极其完整——变量引擎（register/evaluate/lineage/events）、事件引擎（vs_events）、Compute Job 轮询、Widget Plugin 全部已实现并注册到 main.py。Phase C 90% 的工作是**前端对接**。

## 二、现有后端 API（已实现，Phase C 直接对接）

| API 前缀 | 用途 | 关键端点 |
|----------|------|---------|
| `/workshop-compute-api/variables` | 变量引擎 | POST(register) / GET(list) / PUT(update) / DELETE / POST(evaluate) / GET(lineage) |
| `/workshop-compute-api/variables/{id}/events` | 变量事件 | POST(record) / GET(list) |
| `/workshop-compute-api/jobs` | Compute Job | POST(submit) / GET(list) / POST(poll) / GET(result) |
| `/workshop-compute-api/app-entries` | App Entry | POST(register) / GET(list) / POST(validate) |
| `/v1/modules` | Module CRUD | GET(list) / POST(create) / GET(detail) / PATCH / POST(publish) |
| `/v1/modules/{id}/runtime` | Module 运行态 | GET |
| `/api/module-interfaces` | Module 接口 | GET(list) / PUT(update) |
| `/v1/widget-plugins` | Widget 注册表 | GET(list) |
| `/v1/sql/preview` | SQL 预览 | POST |

## 三、现有前端 CanvasPage 结构（1089 行）

- 三栏布局：Layout 树 | Canvas 画布 | Props 配置面板
- 顶部工具栏有 9 个 Tab（dashboard/queries/functions/objects/events/data/dependencies/styles/variables）
- **问题**：Tab 按钮是纯装饰，没有 state 切换，没有内容面板
- Widget/Workflow 模式按钮也是纯装饰

## 四、Phase C 改造方案

### C-1 批：Tab 系统核心 + 后端补全（C-01~C-08 + C-11~C-15）

1. CanvasPage 增加 `activeTab` state，9 个 Tab 按钮接入点击切换
2. 为每个 Tab 实现内容面板组件（内联或独立函数组件）
3. 补充后端缺失的 Module 事件持久化（C-11~C-13）

### C-2 批：前端面板组件（C-02~C-07 + C-09~C-10 + C-14~C-17）

| Tab | 数据源 | 渲染内容 |
|-----|--------|---------|
| Dashboard | `/v1/modules/{id}/runtime` | 统计卡片 + Widget 绑定状态 |
| Queries | `/v1/sql/preview` | SQL 编辑器 + 查询列表 |
| Functions | `/workshop-compute-api/variables` (type=function) | 函数列表 + AIP Logic 导入 |
| Events | `/v1/modules/{id}/events` (新增) | 事件绑定列表 + 3 步向导 |
| Data | `/v1/sources` | 数据源列表 + 绑定编辑器 |
| Dependencies | `/workshop-compute-api/variables/{id}/lineage` | 依赖树 SVG |
| Styles | 前端 state（持久化到 Module.widgets.meta.styles） | 4 主题预设 + CSS 变量编辑 |
| Variables | `/workshop-compute-api/variables` | 变量表 + 7 类型 + 3 作用域 |
| Objects | 现有 CanvasPage 配置面板（保持不变） | 保持当前 |

### C-3 批：工作流模式 + 事件向导 + 组件注册表（C-08~C-10 + C-16）

- Workflow 模式：SVG 事件编排图（触发器→条件→动作）
- 事件 3 步向导：选择触发器 → 选择动作 → 变量幂等 + 预览链
- 组件注册表：对接 `/v1/widget-plugins`

## 五、后端需新增（最小量）

| 任务 | 说明 |
|------|------|
| Module 事件持久化 | `module_store.py` 增加 events 字段到 meta_module，暴露 `/v1/modules/{id}/events` GET/POST/DELETE |
| 变量↔Module 关联 | `WorkshopVariableEngine` 已有 module_id 字段，list 时按 module_id 过滤即可 |

## 六、工作流模式 SVG 事件编排图

```
┌─────────┐     ┌──────────┐     ┌─────────┐
│ 触发器   │────→│ 条件判断  │────→│ 动作     │
│ (蓝圆)   │     │ (橙菱形)  │     │ (绿矩)   │
└─────────┘     └──────────┘     └─────────┘
```

6 种触发器：on_value_change / on_click / on_timer / on_webhook / on_threshold / on_schedule
贝塞尔曲线连线，可拖拽节点位置

## 七、测试

- Module 事件 CRUD × 3
- 变量按 module_id 过滤 × 2
- 变量 evaluate × 2

## 八、验收标准

- [x] 9 个 Tab 全部有内容面板（非空壳）
- [x] 工作流模式可显示 SVG 事件编排图
- [x] 事件添加向导可完成 3 步并创建绑定
- [x] 变量管理器可 CRUD 变量
- [x] 组件注册表可展示 Widget 列表
- [x] 7 个单元测试全部 PASS

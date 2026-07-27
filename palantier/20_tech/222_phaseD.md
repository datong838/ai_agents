# 222 Phase D 技术方案 · AIP Logic 交互补强

> **版本**：v1.0 · 2026-07-25
> **关联**：[222plan-分阶段开发与里程碑计划.md](222plan-分阶段开发与里程碑计划.md)
> **对应章节**：222 第 20 章 · 第 21 章
> **目标**：将 AIP Logic 画布的 8 种 Block 交互绑定 + 配置区动态表单 + 调试器 + 自动化 Tab 全部对接后端 API
> **状态**：✅ 已完成（由 Tare 同学完成）

---

## 一、现状审计

### 代码审计发现

存在两个版本的 Logic 页面：

1. **旧版 `LogicPage`**（272 行，4 个 Block，简单执行）— 已废弃
2. **完整版 `LogicCanvasPage`**（686→828 行，8 个 Block + 动态表单 + 拖拽 + CoT 链）— 未注册路由

### LogicCanvasPage 现有能力

- 8 种 BlockKind：input / get_property / use_llm / apply_action / branch / merge / handoff / annotate
- 每个 Block 有配色：KIND_COLORS 映射
- 动态配置表单（ConfigForm）：根据 kind 渲染不同控件
- 执行引擎：`POST /v1/logic/run` → 展示输入/输出/Token/耗时
- CoT 链展开（results + cot 推理链）
- 选择/删除 Block

### 缺失功能

- ❌ Block 没有重排序功能
- ❌ 没有执行历史记录
- ❌ 没有自动化 Tab
- ❌ 没有可观测性页面
- ❌ 导入路径错误（`../api/client` → 应为 `../../api/client`）
- ❌ 未注册路由

## 二、增强方案

### D-1 Block 重排序

- 为每个 Block 增加 ▲▼ 按钮组件
- `moveBlock(id, dir)` 函数在 blocks 数组中交换位置
- SVG 连线自动跟随

### D-2 执行历史记录

- 新增 `runHistory: HistoryRecord[]` state，每次执行后追加记录
- 最多保留 20 条历史
- 历史记录显示：时间 / 输入 / 输出 / 状态 / 耗时

### D-3 3 Tab 右侧面板

将原来的单一配置面板升级为 3 Tab 切换：

| Tab | 内容 |
|-----|------|
| **属性** | 动态配置表单（原有 ConfigForm） |
| **历史** | 执行历史列表 + CoT 推理链 + 完整 JSON |
| **自动化** | 5 种触发器配置面板 |

### D-4 自动化 Tab（5 种触发器）

```
对象变更触发器  — 当 ObjectType.X 的属性变化时
定时触发器      — 每 N 分钟/小时/天
人工触发器      — 等待用户确认
Webhook 触发器  — 外部 HTTP 调用
阈值触发器      — 指标超过阈值时
```

每种触发器有配置表单（类型 + 参数 + 启用/禁用开关）

### D-5 AIP 可观测性页面

新建 `ObservabilityPage.tsx`，4 Tab：

| Tab | 数据源 | 内容 |
|-----|--------|------|
| **追踪** | `GET /tracing-perf-geo-map/tracing/traces` | Trace 列表 + Span 树 + 火焰图 |
| **函数** | `GET /v1/functions-runtime/functions` | 函数列表 + 代码面板 + 安全约束 |
| **测试** | `GET /v1/aip/evals` | Eval 门控结果 + 通过/失败统计 |
| **调试** | `POST /v1/logic/debug` | 逐步执行 + 工具调用链 + 变量快照 |

## 三、路由注册

```typescript
// routes.tsx
{ path: "aip/logic", Component: LogicCanvasPage },    // 替换旧 LogicPage
{ path: "aip/observability", Component: ObservabilityPage },

// App.tsx
import { LogicCanvasPage } from "./pages/s2/LogicCanvasPage";
import { ObservabilityPage } from "./pages/s2/ObservabilityPage";
```

## 四、验收标准

- [x] 8 种 Block 可拖拽排序
- [x] 执行后记录历史（最多 20 条）
- [x] 3 Tab 切换（属性/历史/自动化）
- [x] 5 种自动化触发器可配置
- [x] 可观测性页面 4 Tab 完整
- [x] 路由正确注册
- [x] TypeScript 编译 0 新增错误

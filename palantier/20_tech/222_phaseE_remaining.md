# Phase E 剩余任务实施方案（E-01~E-06, E-08, E-13~E-17）

> **版本**：v1.0 · 2026-07-26
> **状态**：编码前确认
> **关联**：[222plan v1.6](222plan-分阶段开发与里程碑计划.md)

---

## 一、现状审计结论

### E-01 Pipeline 列表页动态加载
- **现状**：`PipelinesPage`（data.tsx L139）已对接 `GET /v1/pipelines`，支持 sourceFilter 过滤
- **结论**：✅ 已完成，无需额外工作

### E-02~E-06 Pipeline DAG 画布增强
- **现状**：`pipelineCanvas.tsx`（294行）已有基础 3 节点画布（输入→变换→输出）+ 预览表
- **缺失**：
  - E-02：节点不可拖拽，位置硬编码
  - E-03：无算子工具栏（15 个变换算子）
  - E-04：预览表已有（对接 `/v1/analytics/datasets/preview`），需增强列类型显示
  - E-05：无管道类型选择器（batch/incremental/streaming）
  - E-06：输出配置只有 SNAPSHOT，缺 6 种 Write Mode

### E-08 Analytics 增强
- **现状**：`analytics.tsx`（911行）已极完整：读数/Draft/探索（contour/quiver/vertex）/SQL预览/导出/谱系
- **结论**：已深度对接，需补 3 个 Tab 切换器（读数/Draft/探索）将现有平铺内容收拢为 Tab

### E-13~E-14 Wiki 对接
- **现状**：`WikiPage`（ontology.tsx）已有知识卡片 + 4 Tab + `WikiVersionsPanel` 版本对比
- **缺失**：E-13 无 Wiki 索引页（分支树 + 页面卡片 + 搜索）
- **结论**：E-14 版本对比已基本完成（WikiVersionsPanel），E-13 需新建索引页

### E-15~E-17 回归测试
- 全量回归测试 + 前端构建验证 + 后端 pytest

---

## 二、技术方案

### 2.1 E-01~E-06：Pipeline DAG 增强

**修改文件**：`apps/web/src/pages/s2/pipelineCanvas.tsx`

**最小更改策略**：在现有 294 行基础上增量增强，不重构已有结构

#### E-02 节点拖拽
- 为 3 个节点增加 `draggable` + `onDragEnd` 事件
- 用 `useState` 记录节点位置 `nodePositions: { x, y }[]`
- SVG 路径根据节点位置动态计算

#### E-03 算子工具栏
- 在 DAG 画布上方增加算子工具栏（水平滚动条）
- 15 个算子分 3 组：输入(3) / 变换(8) / 输出(4)
- 算子按钮可拖拽到画布（drop 创建节点）

#### E-04 数据预览增强
- 预览表已有，增强列类型推断（string/number/date/bool）
- 在表头显示推断的类型徽章

#### E-05 管道类型选择器
- 在工具栏增加 3 选 1 单选按钮组：batch / incremental / streaming
- 选择后存储到 state，影响输出配置面板的可用选项

#### E-06 输出配置面板
- 将现有 `disabled` 的 SNAPSHOT 单选改为 6 种 Write Mode 可选：
  - SNAPSHOT / APPEND / MERGE / UPDATE / DELETE / UPSERT
- 根据 E-05 管道类型联动可选 Write Mode

### 2.2 E-08：Analytics Tab 收拢

**修改文件**：`apps/web/src/pages/s2/analytics.tsx`

**最小更改策略**：在现有 911 行基础上，将主内容区从平铺改为 3 Tab 切换

- Tab 1「读数」：读数结果 + 导出 + 谱系 + SQL 预览
- Tab 2「Draft 写回」：写回表单 + lastDraft 结果
- Tab 3「探索」：contour + quiver + vertex

### 2.3 E-13：Wiki 索引页

**新建文件**：`apps/web/src/pages/s2/WikiIndexPage.tsx`

**功能**：
- 左侧分支树（对接 `GET /v1/ontology/branches`）
- 右侧页面卡片网格（对接 `GET /v1/wiki?type={type}` 或列出所有 type 的 Wiki）
- 顶部搜索框（按 objectType / objectId 搜索）
- 点击卡片跳转到 `/ontology/wiki?type=X&id=Y`

**路由注册**：
- `nav.ts`：在「活知识 Wiki」下方新增「Wiki 索引」菜单
- `routes.tsx`：注册 `ontology/wiki-index`

### 2.4 E-14：版本对比视图

**修改文件**：`apps/web/src/pages/s2/ontology.tsx`（WikiVersionsPanel 增强）

**增强**：
- 版本列表增加「对比」按钮，选择两个版本做 diff
- diff 视图：左右两列 JSON 高亮差异字段

### 2.5 E-15~E-17：回归测试

- E-15：重启后端 → 验证全部页面路由 → 验证 API 对接
- E-16：`npm run build` 无错误
- E-17：后端全量 pytest

---

## 三、实施批次

| 批次 | 任务 | 文件 |
|------|------|------|
| **Batch 1** | E-02~E-06 | pipelineCanvas.tsx 增强 |
| **Batch 2** | E-08 | analytics.tsx Tab 收拢 |
| **Batch 3** | E-13~E-14 | WikiIndexPage.tsx 新建 + ontology.tsx 增强 + nav.ts + routes.tsx |
| **Batch 4** | E-15~E-17 | 回归测试 |

---

## 四、验收标准

- [ ] Pipeline DAG 节点可拖拽
- [ ] 算子工具栏 15 个算子可拖入画布
- [ ] 管道类型选择器 3 选 1
- [ ] 输出配置面板 6 种 Write Mode
- [ ] Analytics 页面 3 Tab 切换
- [ ] Wiki 索引页分支树 + 卡片 + 搜索
- [ ] Wiki 版本对比可 diff
- [ ] 前端构建无错误
- [ ] 后端全量 pytest 0 新增失败

# 228 · AIP Logic 端口拖线与方向箭头实施方案

> 版本：v1.1（2026-08-02，实施完成复核）
> 状态：**已完成；端口拖线、实时预览、方向箭头、画布松开兜底与原点击连接兼容均通过实机和回归门**
> 目标页面：`/aip/logic`、`/aip/logic/:flowId`
> 代码基线：m1 `1fb0fa2`
> 完成提交：m1 `186ddd9`

## 1. 使用 Rules

1. 先方案后编码；只扩展前端连线交互和视觉方向，不改变 canonical Graph/API/数据库契约。
2. 保留现有“点击源端口→点击目标端口”的键盘与无障碍路径；拖线是并存增强，不得替代或破坏旧路径。
3. 拖线只从输出端口开始，只能在输入端口结束；重复边、自环、环路和端口语义继续统一经过 `tryAddLogicEdge`，不得另造宽松校验。
4. 拖动过程中只展示临时预览线，不修改 graph、不标 dirty；仅成功落到合法目标端口后新增边并标记 `edge_add`。
5. 连接线必须展示从 source 指向 target 的箭头；删除按钮、Branch 多输出端口、缩放、节点拖动、运行态和保存语义保持不变。
6. 代码完成后执行专项交互测试、Logic 前端累计、Web 全量、TypeScript、production build 和 interaction-honesty。

## 2. 当前差距

1. 当前输出端口 `onClick` 只进入连接模式，目标端口 `onClick` 完成连接；用户不能按住源端口直接拖到目标端口。
2. 当前 SVG path 没有 marker，线条能表达连接关系但不能直接表达方向。
3. 当前没有拖线中的实时预览和无效落点取消反馈。

## 3. 冻结交互

1. Pointer 在输出端口按下时记录 source node、source port、branch path 与起点；移动超过 4px 后进入拖线态。
2. 拖线态实时将临时曲线更新到当前指针位置，并高亮可接收的输入端口。
3. 画布容器兜底接收移动、松开与取消事件，避免浏览器未维持端口指针捕获时预览线滞留。
4. Pointer 在输入端口上释放时，调用现有边校验与创建路径；成功后清理预览并标 dirty。
5. 在空白、输出端口或非法目标释放时不改变 graph，清理预览并显示“连接已取消/被拒绝”的真实反馈。
6. 未超过拖动阈值时保留原有 click 行为；拖动完成后的合成 click 必须被抑制，避免误进入第二次连接模式。
7. 正式边和预览边都使用 SVG `marker-end`；箭头尖端朝向 target，Branch 路径端口沿用各自端口起点。

## 4. 修改范围

- `apps/web/src/pages/s2/LogicGraphCanvas.tsx`：Pointer 拖线状态、坐标换算、目标端口识别、预览 path、SVG marker。
- `apps/web/src/pages/s2/LogicGraphCanvas.interaction.test.tsx`：拖线成功、取消、校验复用、click 兼容与箭头断言。
- `apps/web/src/styles/20-aip-ontology.css`：预览线、箭头和拖线态端口反馈。

不修改后端、Graph DTO、运行历史、dry-run executor、数据库迁移和其他页面。

## 5. 验收与风险

1. 输出端口拖到另一节点输入端口后只新增一条有向边；源/目标/端口/Branch path 正确。
2. 空白释放、自环、重复边、环路不修改边数组；错误或取消提示可见。
3. 所有正式连接具有 `marker-end`，预览线随 Pointer 更新并在结束/取消后消失。
4. 单击连线、键盘传感器、节点拖动、palette 拖入、删除边和缩放回归通过。
5. 风险：Pointer capture 下命中目标可能偏差；实现使用释放坐标的 `elementFromPoint(...).closest(input-port)`，并对找不到目标 fail-closed。
6. 回滚只需回退上述三个前端文件，不涉及服务端数据迁移。

## 6. 实施结果（2026-08-02）

1. 已支持从任一输出端口按住拖出预览曲线，在目标节点输入端口松开后新增 canonical 有向边；Branch 多输出继续保留 source port 与 branch path。
2. 正式边和预览边均使用独立 SVG marker，箭头朝向 target；空白释放取消，重复边、自环、环路继续复用既有 fail-closed 校验。
3. 浏览器实测：在未保存模板新增 Execute 与 Handoff，Execute 输出拖到 Handoff 输入后由“节点 6 · 连接 3”变为“节点 6 · 连接 4”，预览归零，4 条正式边均有 `marker-end`；刷新后临时图未写入服务端。
4. 测试证据：专项 `2 files / 16 passed`；Web 全量 `110 files / 1761 passed`；TypeScript、Vite production build、36 页 interaction-honesty、`git diff --check` 全部通过。
5. 一致性复核：实际改动仅限本文冻结的三个前端文件，无 API、DTO、数据库、dry-run、历史或生产写回变化；Stage C 仍保持禁用。

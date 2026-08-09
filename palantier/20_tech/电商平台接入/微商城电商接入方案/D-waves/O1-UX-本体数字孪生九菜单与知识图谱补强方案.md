# O1-UX：本体数字孪生九菜单与知识图谱补强方案

> **版本**：v1.4 · 2026-08-09
> **状态**：方案最终评审通过；O1-UX0 GREEN，下一波 O1-UX1
> **目标租户**：`org-org` · `dev-project`（默认工作区）
> **实施原则**：映射现有 O1/O1-R 架构与真实代码能力，不重建本体内核，不引入第二套数据真源
> **上位方案**：`O1-本体数字孪生层改造方案.md` v2.1、`O1-R-本体数字孪生复审整改与九页面闭环清单.md` v1.1、`228-微商城专项实施准备与FDE全链路规格.md`

## 0. 使用的 Rules

| Rule | 本方案约束 |
|---|---|
| 先方案后编码 | 本文件最终评审通过前，不修改 AOS 功能代码 |
| 真实数据与真实逻辑 | 浏览器、API、数据库验收只认 `org-org/dev-project`；不以 Mock、静态图或假成功补齐功能 |
| 权威真源不变 | PostgreSQL、本体合成读取、Installation/Overlay、Object/Link 权威链保持唯一；前端不得建立第二套图数据 |
| 租户双边界 | 所有探索、对象集、图布局、注释和分享资产必须同时按组织与工作区隔离；缺 scope、未知 scope、跨 scope 一律失败关闭 |
| 交互诚实 | 禁用、占位、浏览器 URL 提示不得被宣称为已保存、已共享或已闭环 |
| 最小演进 | 复用既有路由、Ontology Client、Draft、Wiki、Funnel、Overlay 与图查询能力；只补契约、持久化、交互和表现层 |
| 可逆可审计 | 保存、对象集、注释、布局和 Overlay 变更均有 Receipt/CAS 或 Draft/审批链；不得静默覆盖 |
| 浏览器验收 | 九菜单逐页验证可见、可操作、失败态、刷新恢复、窄屏/宽屏及跨页面联动 |

## 1. 背景与本次复审结论

O1-R4 的“GREEN”只证明九条路由存在、目标租户正确、页面无页面级异常，并证明部分权威读链已接通；它**不等于九页面产品功能、交互和视觉体验完成**。本方案新增 O1-UX 门，专门消除这一口径歧义。

2026-08-09 对当前真实页面、视觉稿和代码复核后，结论如下：

1. 对象探索采用通用 `BpSplit` 固定双栏；主结果区被限制为 220～280px，表格和图谱沦为次要面板。
2. 多标签、新建对象集、高级筛选、列配置、注释、展开和更多共 7 处控件明确禁用。
3. “共享”“保存”只显示地址栏提示，没有持久化探索、权限或分享资源，不得继续使用成功语义。
4. 图谱只取前 6 个邻居并使用固定 CSS 坐标，没有真实边、布局、缩放、平移、多跳、路径、筛选、图例或大图治理。
5. 图谱邻居映射丢失 `Neighbor.type`，点击跨类型邻居时仍按中心对象类型读取，存在错误对象/404 风险。
6. 后端已有高级搜索、保存探索、批量导出、多跳、最短路径和子图展开代码种子，但相关引擎是进程内单例，且路由未把 Principal scope 传入存储键，不能直接作为生产真源接入。
7. 图谱健康度已有权威指标和问题列表，但没有图形定位；当前真实读数存在大量属性冲突和孤立对象，健康页面不能只做 KPI 表格。
8. 其余七页虽有局部真实能力，但存在首屏断链、旧通用模型、只读状态页和缺少跨页面任务流等问题。

因此，O1-UX 当前状态为 **RED / 待实施**；O1-R4 保留“权威读链基础闭环”结论，但不得再被引用为“九页面功能完成”。

## 2. 不变架构与明确非目标

### 2.1 不变架构

```text
栖月汇只读 Source / Pipeline
  → ecom_object / ecom_link（权威对象与关系）
  → Outbox / Projector
  → obj_instance / graph_edge（兼容投影视图）
  → Installation 感知的 Ontology Compose
  → Object Explorer / Wiki / Funnel / Graph Health / Workshop
```

以下边界不得因 UI 补强而改变：

- Object/Link 身份、关系方向和租户归属由服务端权威层决定。
- 平台模板、Installation、组织 Ontology Overlay、Module Instance Overlay 保持分离。
- 对象或本体写入必须走 Action/Draft/审批或 Overlay CAS，不允许页面直接写兼容表。
- 图谱健康、对象探索和 Workshop 必须消费同一个合成 schema 与同一对象/Link 视图。
- PII 按服务端 masking contract 脱敏；客户端不得自行获取完整值后再遮挡。

### 2.2 非目标

- 不新建另一套“图数据库真源”替代 PostgreSQL 权威链。
- 不复制 Foundry 产品或照搬视觉稿数据、品牌和信息架构。
- 不在本波实现本体推理、机器学习图嵌入或通用 BI 系统。
- 不用 Canvas 静态图、SVG 手绘关系或本地 JSON 冒充真实知识图谱。
- 不把 `dev-org` 测试数据写入或展示在栖月汇工作区。

## 3. 九菜单产品定位与完成定义

| 菜单 | 核心任务 | 现状 | O1-UX 完成定义 |
|---|---|---|---|
| 本体管理 | 发现、理解和治理 Object/Link/Action 类型 | 真实列表与入口已接，信息密度过高 | 类型/关系总览、搜索收藏、详情下钻、组织定制入口职责清晰 |
| 对象探索 | 查找对象、分析属性与关系、保存探索 | 真实对象/邻居已接，主画布被压缩 | 全宽表格/图谱、可折叠详情、筛选/列/对象集/保存/共享真实可用 |
| Funnel 管道 | 查看 Object 水合四阶段及失败原因 | 有状态框架，选择与重跑体验不完整 | 显式类型、阶段状态、失败证据、受控重跑和结果刷新闭环 |
| OKF funnel | 映射外部字段到行业本体 | 映射/Lint/保存已接，内容偏通用 | 默认进入栖月汇电商映射，缺失字段、影响范围、Lint 与保存结果可解释 |
| OKF 概览 | 查看各行业映射完整度 | 只有简单卡片 | 电商优先、映射覆盖率、阻断字段、最近修订与下钻一致 |
| 图谱健康度 | 发现冲突、孤立、悬空与治理影响 | 权威指标/列表已接，无图 | List/Graph 双视图、问题着色定位、过滤、对象下钻、修复入口 |
| 活知识 Wiki | 为真实对象沉淀知识并走 Draft | 对象绑定与 Draft 已接，直达为空 | 可从对象选择器或探索进入；编辑、版本、Draft 状态和返回上下文完整 |
| Wiki 索引 | 找到各类型知识资产和覆盖缺口 | 类型选择后可查 | 全局搜索、类型/分支过滤、覆盖率、缺失 Wiki 清单和对象下钻 |
| 分支与 Overlay | 查看组织定制、版本和当前生效状态 | Installation 历史只读 | 差异预览、目标过滤、当前/历史比较、进入受控定制和 reset-to-inherit 流程 |

九页完成不是“9/9 可打开”，而必须同时满足：

- 数据来源明确且为目标租户真实数据；
- 页面主任务可从入口走到明确结果；
- 所有可见主按钮有真实结果或被移除；
- 错误、空态、权限不足和服务不可用可区分；
- 页面间 type/id/branch/installation/revision 上下文不丢失；
- 自动化测试和浏览器证据同时存在。

## 4. 对象探索信息架构冻结

### 4.1 页面布局

默认桌面布局冻结为：

```text
探索标签 / 新建探索 / 已保存探索
搜索与过滤 / 类型 / 列配置 / 分享 / 保存
表格 | 图谱 | 注释    结果数    展开 | 更多
┌──────────────────────────────────────────────┐
│               全宽主结果画布                 │
│     Table / Graph / Annotation workspace     │
└──────────────────────────────────────────────┘
                                      ┌────────┐
选择对象后按需打开 →                  │详情抽屉│
                                      └────────┘
```

- 主画布默认占全部可用宽度，不再使用通用 `BpSplit`。
- 详情抽屉默认宽 400px，允许 320～640px 调整；关闭后主画布恢复全宽。
- “展开”切换主画布专注模式，收起应用侧栏和详情抽屉；再次点击可恢复。
- 表格允许横向滚动；页面内容超过一屏时使用纵向滚动，不把全部内容压进固定高度。
- 小于 900px 时详情改为底部 Sheet，不产生两个不足 300px 的并排区域。

### 4.2 表格模式

- 列来自 composed Object Type schema，不再仅取第一条对象的前 5 个字段。
- 默认列、顺序、宽度、固定列和可见性保存到探索视图，不修改本体 schema。
- 服务端分页/游标、排序和过滤为权威；客户端只做当前页即时检索提示。
- 行选择与“当前详情对象”分离：多选用于对象集/导出，单击用于详情。
- 所有 PII 列保持服务端脱敏；导出复用同一列和 masking contract。

### 4.3 详情抽屉

- 分为概览、属性、关系、Wiki、Action、时间线六个页签。
- 关系列表中的每一项必须保留 `type + id + rel + direction`。
- 跨类型邻居点击使用邻居自己的 type/id，更新 URL 并保留返回路径。
- Action 只进入 Draft/审批链；不可因抽屉交互直接写生产对象。

## 5. 控件真实语义与持久化契约

### 5.1 探索资产

新增/补强 `ontology_exploration` 权威表，而不是继续使用进程内 `ExplorationEngine`：

| 字段 | 约束 |
|---|---|
| `org_id, workspace_id` | 复合租户键、FK、RLS + FORCE RLS |
| `exploration_id` | 服务端生成，不由名称充当身份 |
| `name` | 当前租户工作区内非空；是否唯一由产品确认，v1 建议允许同名但列表展示拥有者/时间 |
| `object_type` | 必须来自当前 composed schema |
| `view_mode` | `table|graph|annotation` |
| `query_json` | 规范化筛选 AST，不保存任意可执行表达式 |
| `column_json` | 列顺序、宽度、可见性 |
| `graph_json` | 布局偏好、过滤器、种子；不复制对象或 Link 业务数据 |
| `visibility` | `private|workspace`；v1 不支持匿名公开链接 |
| `revision` | 单调递增，强 ETag/CAS |
| `archived_at` | 归档时间；v1 不提供生产物理删除 |
| `created_by/updated_by` | 从 Principal 推导 |
| `created_at/updated_at` | 服务端时间 |

保存接口必须使用 `Idempotency-Key + If-Match`；同 key 同请求原样重放，同 key 异 payload 冲突，旧 ETag 返回 412。读取、列表、更新、归档和恢复均由 Principal scope 限制。v1 不提供生产物理删除；“删除探索”在产品语义上执行可恢复归档并生成 Receipt。

分享权限冻结如下：

- `private` 只允许创建者与拥有工作区治理权限的管理员读取；
- `workspace` 只允许当前组织、当前工作区的有效成员读取；
- 分享不会生成越过 AOS 身份认证的匿名 URL；
- visibility 变更必须 CAS 更新并记录 actor、旧值、新值和 Receipt；
- 撤销分享即把 visibility 改回 `private`，旧站内链接再次访问返回 403/404，不泄露资源是否存在；
- 创建者离开工作区时按组织治理策略移交或归档，不产生无主公开资源。

授权不硬编码前端角色名，统一检查服务端 capability：

- `ontology.exploration.read`
- `ontology.exploration.write`
- `ontology.exploration.share`
- `ontology.object-set.write`
- `ontology.graph.read`

工作区管理员的治理能力也必须来自 Principal capability，不因 UI 显示“管理员”就放行。

### 5.1.1 Exploration 状态机

```text
不存在 --POST--> active@revision=1
active@n --PUT If-Match:n--> active@n+1
active@n --archive If-Match:n--> archived@n+1
archived@n --restore If-Match:n--> active@n+1
```

- archived 资产默认不出现在普通列表，但可由创建者/治理者查询和恢复。
- archived 资产不可执行、分享或更新布局，必须先 restore。
- 每次状态变化都写 Receipt，revision 不复用、不回退。
- 浏览器 dirty/clean 只是客户端编辑状态，不进入服务端生命周期；服务端保存失败时保持 dirty。

### 5.1.2 ObjectSet 边界

- `ontology_object_set` 与 `ontology_object_set_item` 均含 `org_id/workspace_id` 并启用 RLS/FORCE RLS。
- item 冻结 `object_type + canonical_object_id`；不复制 properties、PII 或当前标题。
- v1 一个对象集只允许一个 Object Type；跨类型选择必须拆分或明确拒绝。
- 创建时批量验证对象属于当前 composed schema 且在当前租户可见；失效对象保留引用并标记 unavailable，不静默换绑。
- 对象集的创建、改名、增删成员、归档同样使用 revision/CAS/Receipt。

### 5.2 各按钮语义

| 控件 | 真实行为 | 失败行为 |
|---|---|---|
| 新建对象集 | 从当前多选对象创建静态对象集，保存 type/id 引用和创建证据 | 无选择、跨类型不支持或权限不足时说明原因，不显示成功 |
| 保存 | 新建或更新探索资产；成功后服务端回读 revision/ETag | 服务端失败保持 dirty 状态，不能只显示 toast |
| 共享 | 设置 `private/workspace` 并生成站内链接；展示权限范围 | 不复制公开 URL，不绕过工作区权限 |
| 高级筛选 | 构建规范化 AST，服务端验证字段、类型、操作符和复杂度 | 非法表达式 422；超限 413/422；不得回退全量前端过滤 |
| 列设置 | 修改探索视图的列偏好 | 不修改 Object Type，不依赖 Overlay 完成 |
| 注释 | 对当前对象/选择集创建 Wiki/Draft 注释 | 未选择对象时禁用并显示可见原因 |
| 展开 | 切换专注模式 | 纯客户端布局状态，可恢复，不声称保存 |
| 更多 | 导出、复制查询、查看修订、归档探索等真实操作 | 高风险操作二次确认并有回读/Receipt |

## 6. 权威知识图谱工作台

### 6.1 图谱数据契约

图谱视图不从前端 `neighbors.slice(0, 6)` 拼装。统一返回：

```json
{
  "scope": {"orgId":"org-org","workspaceId":"dev-project"},
  "schemaEtag": "composed-schema-v1:sha256:...",
  "snapshot": {"asOf":"...","watermark":"..."},
  "nodes": [{"key":"Order:1","type":"Order","id":"1","label":"...","depth":0,"masked":true}],
  "edges": [{"key":"...","type":"Order.hasPayment","source":"Order:1","target":"Payment:12","direction":"out"}],
  "page": {"truncated":false,"nextCursor":null},
  "limits": {"maxNodes":500,"maxHops":5}
}
```

硬约束：

- 节点 key 至少包含 type/id，不能只用外部 id。
- 边包含稳定身份、关系类型、方向和两端完整身份。
- schema ETag、数据 watermark、截断状态和 cursor 必须可见。
- 查询服务从 Principal 取得租户，不接受客户端覆盖 scope。
- 图读取统一经过 `OntologyGraphReadService`：电商 owned OT/Link 从 `ecom_object/ecom_link` 权威层读取；非 owned 通用类型从受 OwnershipGuard 约束的 `obj_instance/graph_edge` 读取；前端只看统一 DTO，但响应必须带 `sourceAuthority=ecom_authoritative|compat_projection`。禁止对同一 owned 类型同时拼接两个来源。
- 进程内 `GraphQueryEngine` 只能保留为单元测试辅助；生产查询必须读取上述租户隔离的权威路由。
- 查询默认 1-hop、100 节点；用户显式展开才增加 hops，最大 5-hop/500 节点，超限返回截断信息而不是浏览器卡死。

### 6.2 图谱交互

- 鼠标与触控板：缩放、平移、框选、拖动节点、适配画布。
- 键盘：Tab 聚焦、Enter 打开、方向键在相邻节点移动、Esc 关闭菜单/详情。
- 单击节点：打开详情抽屉；双击或“展开邻居”拉取下一跳。
- 单击边：显示关系类型、方向、来源、更新时间和健康状态。
- 工具栏：自动布局、撤销本地布局、适配、图例、类型过滤、关系过滤、方向过滤、深度和时间点。
- 分析：最短路径、多种子子图、仅显示选择、隐藏节点、聚合重复边。
- 视觉：对象类型颜色稳定；同一关系颜色/线型稳定；节点/边选中、高亮、告警、弱化状态可区分。
- 大图：渐进加载、视口裁剪或同等性能机制；不得一次性渲染全租户全部节点。

### 6.2.1 视觉与可读性门

- 画布最小可用高度为视口内容区的 70%，专注模式至少为 85%。
- 节点标签默认单行省略，悬停/聚焦显示完整值；不得像参考关系图那样让大量标签互相覆盖。
- 自动布局完成后，100 节点基准图中节点包围盒重叠率必须小于 2%，关键 seed 与一跳邻居不得重叠。
- 边在普通、选中、路径、告警四种状态下有清晰层级；方向不只靠颜色表达。
- 图例固定显示当前可见类型/关系及数量，可折叠但不能遮挡核心 seed。
- 当前节点、键盘焦点、选中集合和健康告警使用不同视觉状态，焦点环满足主题对比要求。
- 390px 视口不强行缩小完整图谱：默认进入可访问的邻居列表，用户可切到全屏图；两种视图共享同一 selection 和 GraphSnapshot。

### 6.3 图谱布局与保存

- 自动布局算法由渲染适配层负责，不写回对象/Link 真源。
- 用户拖动坐标只在保存探索时进入 `graph_json`。
- 未保存布局只存在当前页面会话，刷新恢复服务端最近保存版本。
- 不允许把整个对象 properties 或 PII 复制进布局 JSON。

### 6.4 图谱健康联动

对象探索和图谱健康度复用同一个 `OntologyGraphCanvas`：

- 对象探索以对象与关系分析为中心。
- 图谱健康度以 GH-01～GH-04 问题覆盖层为中心。
- 点击健康问题定位相关节点/边；从图中可回到问题列表。
- “处理”只进入修复 Draft、Link Type 编辑器或数据健康任务，不直接篡改对象/Link。

## 7. 其余八页补强要求

### 7.1 本体管理

- 首屏分成“发现”“类型与关系”“治理”三块，创建 Object Type 移入独立受控流程。
- 增加 Object Type 与 Link Type 的关系总图入口；实例级图仍进入对象探索。
- 收藏、最近、重要使用同一服务端偏好来源；不得仅依赖 localStorage。

### 7.2 Funnel 管道

- 必须显式选择当前 composed schema 中的 Object Type。
- 读取四阶段状态、worker 水位、最后成功/失败时间与错误证据。
- 重跑前展示影响范围；调用真实执行入口；回包后轮询并回读最终状态。
- 无 Pipeline、无权限、执行器不可用、运行中必须分别显示。

### 7.3 OKF funnel 与概览

- 当前租户默认行业为 `ecom`，对象类型来自栖月汇已安装电商包。
- `WorkOrder` 不得作为电商默认对象；历史通用映射需明确标注或迁移。
- 展示字段覆盖率、缺失必填、类型不匹配、下游 Object/Logic/Workshop 影响。
- 保存后服务端回读映射 revision，概览与编辑页使用同一真源。

### 7.4 活知识 Wiki 与 Wiki 索引

- Wiki 页面无 type/id 时提供真实对象选择器和“返回最近对象”，不是空白编辑器。
- 保存继续走 UpdateWikiCard Draft；展示 Draft id、审批状态和生效版本。
- Wiki 索引支持全局关键词、Object Type、分支、是否缺失 Wiki、更新时间过滤。
- 索引结果和摘要继续执行 PII 脱敏；搜索失败不得显示模拟结果。

### 7.5 分支与 Overlay

- 以 Installation 为上文，显示当前 composed schema ETag、安装修订、Ontology Overlay 集合 hash。
- 支持当前与历史修订的字段级差异预览。
- “管理组织定制”进入现有 Overlay CAS 流；reset-to-inherit 追加新修订，不删除历史。
- 没有 Overlay 时明确显示“继承安装模板”，不把 0 修订表示为异常。

## 8. API 与持久化改造边界

### 8.1 复用

- `GET /v1/ontology/object-types`
- 对象列表、对象详情、neighbors 和 Wiki API
- Overlay compose/history/CAS
- Draft、Wiki versions、Funnel status、OKF mappings、Graph Health
- 现有 shortest path / expand 的输入上限和算法可作为新服务的行为参考

### 8.2 必须补强

| 能力 | 当前问题 | 目标 |
|---|---|---|
| Exploration | 进程内单例，Principal 未进入键 | PostgreSQL + 双租户键 + RLS/FORCE RLS + CAS/Receipt |
| 高级搜索 | 需先内存 index，scope 未隔离 | 对权威对象查询或受控索引查询，字段/schema/复杂度校验 |
| Graph query | 进程内边集合，dev 写边接口 | 读取权威 `ecom_link/graph_edge` 租户视图；移除生产可达 dev 写接口 |
| 图谱快照 | 无 schema/watermark/truncated 元数据 | 冻结统一 GraphSnapshot DTO |
| 对象集 | 无权威持久化 | PostgreSQL 静态引用集，租户隔离、对象存在性校验 |
| 分享 | 只有 URL toast | Exploration visibility + 权限校验 + 站内链接 |

### 8.2.1 冻结 API 形态

| 方法与路径 | 用途 | 并发/幂等要求 |
|---|---|---|
| `GET /v1/ontology/explorations` | 当前 scope 列表 | 支持 status/type/owner/cursor；不返回跨租户数量 |
| `POST /v1/ontology/explorations` | 新建探索 | `Idempotency-Key` 必填，成功返回 ETag |
| `GET /v1/ontology/explorations/{id}` | 读取探索 | 返回 revision/ETag/visibility/capabilities |
| `PUT /v1/ontology/explorations/{id}` | 保存/分享/恢复 | `Idempotency-Key + If-Match` 必填，成功后客户端回读 |
| `POST /v1/ontology/explorations/{id}/archive` | 可逆归档 | `Idempotency-Key + If-Match` 必填，无 DELETE |
| `POST /v1/ontology/object-sets` | 创建对象集 | 幂等、对象存在性与同类型校验 |
| `PUT /v1/ontology/object-sets/{id}` | 改名/成员变更/归档 | CAS + Receipt |
| `POST /v1/ontology/graph/query` | seed、多跳、方向、类型/关系过滤 | schema 校验、复杂度预算、cursor、水位 |
| `POST /v1/ontology/graph/path` | 最短路径 | 两端对象可见性校验、超限失败关闭 |

现有 `DELETE /v1/ontology/explorations/{id}` 在新 PostgreSQL Store 切换前保持旧实现隔离且不向目标租户 UI 暴露；切换时先从 OpenAPI/客户端移除调用，再在生产路由返回 405 与 `EXPLORATION_ARCHIVE_REQUIRED`，引导使用 archive。不得把旧 DELETE 映射成无 Receipt 的物理删除。

### 8.2.2 错误码冻结

| HTTP | code | 场景 |
|---:|---|---|
| 401 | `TENANT_SCOPE_REQUIRED` | Principal 缺少组织或工作区 |
| 403 | `TENANT_SCOPE_FORBIDDEN` | scope 冲突、未知或跨租户访问 |
| 403 | `EXPLORATION_SHARE_FORBIDDEN` | 无分享 capability |
| 404 | `EXPLORATION_NOT_FOUND` | 当前 scope 不可见；不泄露跨租户存在性 |
| 409 | `IDEMPOTENCY_CONFLICT` | 同 key 不同规范化请求 |
| 409 | `OBJECT_REFERENCE_UNSTABLE` | O1-D 门未通过却尝试保存不稳定引用 |
| 412 | `REVISION_CONFLICT` | If-Match 与当前 revision/ETag 不一致 |
| 413 | `GRAPH_QUERY_TOO_LARGE` | 请求或响应预算超限 |
| 422 | `GRAPH_QUERY_INVALID` | seed、hops、关系或过滤表达式不合法 |
| 422 | `OBJECT_SET_TYPE_MISMATCH` | v1 对象集包含多个类型 |
| 429 | `GRAPH_QUERY_RATE_LIMITED` | 当前用户/scope 查询预算耗尽 |
| 503 | `GRAPH_AUTHORITY_UNAVAILABLE` | 权威图读取不可用；禁止静态图回退 |

### 8.3 数据库迁移原则

- expand-only 新增表/索引/RLS/Receipt；不删除旧接口或旧数据。
- 先双读核对，再切换前端；旧进程内引擎退出生产路径后再单独清理。
- migration 提供 downgrade；任何真实写验证先在可回滚事务或临时测试租户执行。
- 目标租户只写真实用户触发的探索资产；自动化回归不得污染 `org-org/dev-project`。

### 8.4 可观测性与安全预算

- 日志记录 request id、scope hash、query kind、hops、node/edge count、truncated、latency、authority 和错误码；不记录对象 properties、PII、完整筛选值或分享链接。
- 指标至少包含查询 P50/P95、429/413/503、截断率、布局耗时、保存冲突率和跨租户拒绝次数。
- 服务端对 `hops × seeds × maxNodes` 计算复杂度预算；不能仅相信前端最大值。
- 路径查询先校验两端对象在同一 scope 可见，再执行图遍历。
- 图查询超时立即取消数据库工作并返回受控错误，不继续后台消耗连接。

## 9. 前端组件边界

建议新增或拆分，不在单个 `workshop.tsx` 继续堆积：

```text
apps/web/src/pages/s2/objectExplorer/
  ObjectExplorerPage.tsx
  ExplorerToolbar.tsx
  ExplorerTable.tsx
  ExplorerDetailDrawer.tsx
  ExplorerAnnotations.tsx
  SavedExplorations.tsx
  graph/
    OntologyGraphCanvas.tsx
    GraphToolbar.tsx
    GraphLegend.tsx
    GraphDetails.tsx
    graphAdapter.ts
```

- 图渲染库必须经过 bundle 体积、可访问性、500 节点性能、许可证和主题适配评审后选择；方案不预先锁死具体库。
- `OntologyGraphCanvas` 同时供对象探索与图谱健康度使用，禁止复制两套图实现。
- API DTO 和查询状态放在 `apps/web/src/api/`，不在组件内复制租户、ETag、Receipt 判断。
- 沿用现有主题 token 与图标库；不手绘 SVG 资产冒充组件体系。

## 10. 波次拆分与开发顺序

### O1-UX0：契约和诚实性门

- 冻结 GraphSnapshot、Exploration、ObjectSet、Share DTO 与错误码。
- 为九路由补 `interactionHonestyManifest` 条目和最小交互测试。
- 修复跨类型邻居 type 丢失问题。
- 将“共享/保存”假成功改为明确不可用，直到后端真契约接通。
- 未实现控件默认不显示；若为路线预告必须使用明确“即将开放”标签和可访问说明，不能放在主任务工具栏伪装可用。

**退出条件**：无假成功；DTO/错误码/租户矩阵评审通过；现有功能不回归。

### O1-UX1：对象探索布局与表格

- 主画布全宽、详情抽屉、专注模式、响应式布局。
- schema 驱动列、服务端分页/排序/筛选、选择状态分离。
- 完成表格、详情、关系跳转的浏览器闭环。

**退出条件**：1280/1440/1920 宽屏及 768/390 窄屏无挤压；跨类型邻居正确下钻。

### O1-UX2：探索资产、对象集、分享和注释

- PostgreSQL migration、Store/Service/Router、RLS、CAS、Receipt。
- 保存探索、列配置、对象集、private/workspace 分享和 Wiki/Draft 注释。
- 替换进程内 Exploration 生产路径。

**退出条件**：保存后回读一致；同 key 重放、异 payload 冲突、旧 ETag 412；跨租户零可见。

**前置门**：O1-D Canonical ID/别名迁移已完成 copy/hash 对账与冲突隔离。未通过前，UX2 只允许完成数据库/DTO/测试，不得在真实租户保存包含不稳定对象引用的对象集或探索资产。

### O1-UX3：权威图谱查询

- 图谱读取适配到权威 Object/Link 视图。
- GraphSnapshot、1～5 跳、最短路径、多种子、过滤、cursor、watermark。
- 关闭生产可达的进程内/dev 写边入口。

**退出条件**：同一对象的详情邻居与图谱边一致；断边/孤立统计与 Graph Health 可对账。

**前置门**：O1-D 稳定身份门通过；owned/non-owned source authority 路由测试通过。

### O1-UX4：统一知识图谱画布

- 图渲染适配层、自动布局、缩放/平移、选择/展开、图例与过滤。
- 详情抽屉联动、布局保存、性能与可访问性。
- 对象探索与图谱健康度复用同一组件。

**退出条件**：100/300/500 节点性能门通过；无标签大面积重叠；键盘可完成核心浏览。

### O1-UX5：其余八页任务流补强

- 本体管理职责拆分、Funnel 受控重跑、OKF 电商默认和影响分析。
- Wiki 选择/版本/Draft、Wiki 索引覆盖、Overlay diff/reset 入口。

**退出条件**：九页主任务逐页闭环，所有主按钮有真实结果或明确不可用原因。

### O1-UX6：证据封板

- 浏览器九页全量回归、API/DB/RLS/跨租户 canary、性能与可访问性验证。
- 同步 O1-R、O1 主方案进度、D-waves、AOS 项目开发上下文和证据索引。
- 不改变既定证据后续；整体顺序冻结为：

```text
O1-UX0 诚实性/契约门
  → O1-UX1 布局与只读探索
  → O1-D alias migration（稳定对象身份门）
  → O1-UX2/UX3/UX4/UX5/UX6
  → D4 规格同步
  → D5-E1 DLQ harness
  → D5-E1 跨租户 23 资源 canary
  → D5-E2 最终封板
```

O1-UX 不得吞并或跳过 O1-D/D4/D5；O1-D 也不得以阻塞全部只读布局工作为由延迟 UX0/UX1。

### 10.1 分波 feature flag 与兼容策略

- flag 按组织/工作区和能力启用，不使用全局 localStorage 开关决定服务端能力。
- `UX1` 新布局可在读链不变的情况下回退旧表格，但旧假成功按钮不得恢复。
- `UX2` 后端先上线并影子读取；新表/Receipt/RLS 验证通过后才向目标 scope 开放保存。
- `UX3` 对同一 seed 并行比较旧 neighbors 与新 GraphSnapshot，仅保存脱敏计数/hash 对账；一致后切读。
- `UX4` 仅替换渲染层；查询 DTO 与 authority 不随渲染库切换。
- flag 状态必须在证据中记录，最终封板时目标 scope 不允许依赖实验 flag 才可用。

## 11. 具体代码与文档文件范围

### 11.1 前端

- 修改 `apps/web/src/pages/s2/workshop.tsx`，最终迁移为 objectExplorer 目录入口。
- 修改 `apps/web/src/pages/s2/ontology.tsx`、`remainder.tsx`、`WikiIndexPage.tsx`。
- 修改 `apps/web/src/styles/10-data-workshop.css`、`20-aip-ontology.css`。
- 修改 `apps/web/src/api/ontologyClient.ts` 及新增探索/图谱 API client。
- 修改 `apps/web/src/interactionHonestyManifest.ts`。
- 新增对象探索、图谱画布和九页交互测试。

### 11.2 后端

- 维护 `services/aos-api/aos_api/routers/oe_enhancements.py`，移除无 scope 的生产行为。
- 维护 `services/aos-api/aos_api/routers/ontology_governance.py` 与图谱读取服务。
- 新增 Exploration/ObjectSet PostgreSQL Store、Service、DTO、Router 和 migration。
- 复用 Ontology compose、TenantScope、Receipt/CAS、Graph Health 与对象/Link 查询。
- 新增 RLS、跨租户、幂等、分页、路径、展开和限流测试。

### 11.3 文档与证据

- 本文件作为 O1-UX 总方案和波次入口。
- 每波新增 `O1-UX<n>-改动清单.md`，登记文件、测试、浏览器证据、风险和下一波。
- 波次完成更新 `AOS项目开发上下文`、O1-R 状态和证据索引。
- O1-UX0 同步修订 O1-R4 文案为“九页面权威读链基础闭环”，避免继续把 9/9 可打开解释为产品功能 GREEN。

## 12. 测试与验收矩阵

| 类别 | 必测场景 | 通过条件 |
|---|---|---|
| 租户 | 缺 scope、未知 scope、claim/header 冲突、org-org/dev-project 与测试组织互访 | 401/403/零可见；真实租户数据不污染 |
| 探索保存 | 新建、更新、重放、同 key 异请求、旧 ETag、归档/恢复 | 回读一致；冲突 fail-closed；审计字段完整；无生产物理删除 |
| 对象集 | 空选择、同类型多选、跨类型、对象失效、批量导出 | 合法引用稳定；非法组合明确拒绝 |
| 表格 | schema 列、分页、排序、过滤、PII、宽表、空态 | 服务端结果权威；无明文 PII；无假结果 |
| 图谱身份 | 同 id 异 type、跨类型邻居、双向关系、重复边 | 节点/边身份不碰撞，点击进入正确对象 |
| 图谱查询 | 1～5 跳、路径不存在、过滤、截断、cursor、并发刷新 | 结果稳定、上限生效、watermark 可解释 |
| 图谱表现 | 100/300/500 节点、缩放、平移、布局、图例、选择 | 100 节点首个稳定布局 ≤1.5s、300 节点 ≤3s、500 节点 ≤5s；拖动/平移交互目标 ≥30fps；无不可读大面积重叠 |
| 健康联动 | GH-01～04 列表到图、图到对象、修复入口 | 指标/节点/边数量可对账，写操作走治理链 |
| 九页流 | 每页首屏、主按钮、失败、空态、刷新、返回上下文 | 9/9 主任务闭环；0 假成功；0 页面异常 |
| 可访问性 | 键盘、焦点、对比度、缩放 200%、屏幕阅读器名称 | 核心任务无需鼠标可完成；焦点顺序稳定；状态不只靠颜色；200% 缩放无核心控件丢失 |

浏览器证据必须至少覆盖 1280×720、1440×900、1920×1080、768px 和 390px；截图之外还要保存操作步骤、请求/响应摘要、scope、revision/ETag 和最终回读。

证据目录冻结为：

```text
docs/palantier/20_tech/evidence/o1-ux/<wave>/<timestamp>/
  manifest.json
  browser-steps.json
  api-contract.json
  db-assertions.json
  tenant-canary.json
  screenshots/
  test-summary.txt
```

`manifest.json` 记录 git commit、前后端版本、数据库 migration head、目标 scope、feature flags、schema ETag、数据 watermark、证据文件 sha256 和总体结论。截图不得包含未脱敏 PII。

## 13. 风险与缓解

| 风险 | 严重度 | 缓解 |
|---|---|---|
| 把前端升级演变为第二套本体架构 | 高 | 所有对象/Link/schema 从既有合成与权威读层获取 |
| 进程内探索/图引擎跨租户串数据 | 高 | 生产路径切 PostgreSQL + 双租户键 + RLS/FORCE RLS 后再开放 UI |
| 图谱一次加载过大导致浏览器卡死 | 高 | 默认 1-hop/100；cursor/截断；500 节点硬上限；性能门 |
| 保存/共享继续假成功 | 高 | O1-UX0 先移除成功语义；后端回读前不宣告成功 |
| PII 进入图节点标签或保存布局 | 高 | 服务端 masking；GraphSnapshot 和 graph_json 禁止完整 properties |
| 图健康指标与画布数据不一致 | 高 | 同一 snapshot/watermark 对账；不允许两个独立图数据源 |
| 通用 BpSplit 改动影响其他页面 | 中 | 对象探索新增专用布局，不全局修改 BpSplit |
| 图渲染库体积/许可证/主题不适配 | 中 | O1-UX4 前完成候选评审与基准，不在方案阶段锁死 |
| 九页范围过大造成长期不闭环 | 中 | UX0～UX6 串行门禁；每波可独立验证和回滚 |
| O1-D 前保存旧别名引用导致探索失效 | 高 | UX2/UX3 以前置门依赖 O1-D；迁移前只做契约和只读布局 |

## 14. 回滚策略

- 前端按 feature flag 分波启用；失败时退回上一已验证视图，但不得恢复假成功文案。
- Exploration/ObjectSet 表 expand-only；关闭入口不删除用户资产。
- 图查询新适配器失败时回到只读对象表/邻居列表并明确显示图谱不可用，不回退静态假图。
- 图布局属于探索视图，不影响 Object/Link 权威数据，可独立禁用。
- 数据库 migration downgrade 只删除确认无生产资产的新表；已有用户资产时走审计归档，不直接 drop。

## 15. 方案评审门

方案只有同时满足以下条件才能标记“评审通过”：

- [x] 不重建本体真源，不绕开 O1/O1-R 权威链。
- [x] 九页面每页有明确任务、现状、完成定义和退出证据。
- [x] 对象探索布局、详情抽屉、表格、保存、共享、对象集和注释语义冻结。
- [x] 图谱身份、快照、租户、分页/上限、交互、健康联动和保存边界冻结。
- [x] 进程内 Exploration/Graph 生产风险有迁移和关闭方案。
- [x] PostgreSQL/RLS/CAS/Receipt 与跨租户负向测试完整。
- [x] 文件范围、波次顺序、测试、证据、风险和回滚可执行。
- [x] 与 O1-D、D4、D5-E1/E2 后续顺序无冲突。

## 16. 评审记录

| 轮次 | 结论 | 阻断项 | 处理状态 |
|---|---|---|---|
| v1.0 初稿 | 不通过 | O1-D 依赖顺序、图真源路由、可审计归档、分享权限、性能/可访问性门不完整 | v1.1 已整改 |
| v1.1 复审 | 不通过 | 接口错误码、状态迁移、对象集边界、浏览器证据口径、观测和兼容开关不完整 | v1.2 已整改 |
| v1.2 复审 | 通过但需收口 | 旧 DELETE 退场路径与 O1-R4 口径同步需补入 | v1.3 已整改 |
| v1.3 最终复审 | **全面通过** | 无架构、租户、产品、交互、测试、证据或回滚阻断项 | 结束方案评审 Loop，等待进入 O1-UX0 实施 |

## 17. 实施进度记录

| 波次 | 状态 | 代码 | 结论 |
|---|---|---|---|
| O1-UX0 | **GREEN** | `aos-platform@m1@71f97ea` | Exploration/ObjectSet/GraphSnapshot DTO 与错误码已冻结；九页面纳入 43 页面交互诚实性门；跨类型图节点身份和稳定引用解析已修复；未实现/假成功主控件已隐藏 |
| O1-UX1 | 待实施 | — | 建设对象探索专用全宽只读布局、可折叠详情抽屉和宽表滚动，不改变读链与权威数据架构 |

O1-UX0 浏览器证据只证明现有真实读链上的交互诚实性与跨类型上下文一致，不代表 O1-UX1 布局、O1-UX2 持久化或 O1-UX4 知识图谱画布已经完成。

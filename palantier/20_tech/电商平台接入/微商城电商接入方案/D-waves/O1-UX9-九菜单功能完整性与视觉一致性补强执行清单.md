# O1-UX9：九菜单功能完整性与视觉一致性补强执行清单

> **版本**：v1.1 · 2026-08-10  
> **状态**：`IMPLEMENTED_GREEN` · 用户已授权编码 · 九菜单代码、浏览器、租户 canary 与证据封板通过  
> **真实正向范围**：`org-org` · `dev-project`（栖月汇商贸有限公司 · 默认工作区）  
> **负向隔离范围**：`dev-org` · `dev-project`（只做零污染 canary，不作为完成证据）  
> **上位方案**：`O1-UX-本体数字孪生九菜单与知识图谱补强方案.md`、`O1-PLAN-本体数字孪生层全量编码任务与实施顺序.md`  
> **既有封板**：O1 Waves 1—10、D4/D5、O1-UX1～UX8 保持封板；本清单只补产品完整性、真实状态语义和视觉体验

## 实施封板摘要（2026-08-10）

- UX9-0/1：对象查询增加安全排序合同；Order 默认 `createdAt DESC + objectId DESC + NULLS LAST`，订单主列显示真实订单号，默认列不再重复展示 `orderNo`，历史保存探索显式列继续兼容；Funnel 具备真实 Object Type 选择和 idle/loading/empty/error 分态。
- UX9-2：OKF 延续 `meta_aip_kv + revision/CAS` 真源，增加电商 Object Type 明细合同；旧 `okf_mapping:ecom` 只读兼容 Order。真实电商整体必填覆盖为 `6/59=10%`，12 个有源类型逐项展示，11 个未配置，不再用 Order 100% 冒充行业 100%。
- UX9-3：Graph Health 使用 `GH-SCORE-v2` 可复算 breakdown；系统字段、兼容别名与真实冲突分开，允许孤立对象不直接扣分。当前真实读数为 617 实例、592 边、0 悬空、0 真实属性冲突、176 个必需关系缺失、score 75；问题可定位到权威 GraphSnapshot。
- UX9-4：活知识 Wiki 直接入口可选择 composed schema 类型和真实业务对象；不存在 Wiki 进入 knowledge-gap 空态，不再报错或默认 WorkOrder。Product Wiki 与索引只统计 39 个实际上架商品，卡片使用业务展示名与源记录标签。
- UX9-5：页面明确为 Installation 绑定的组织定制 Overlay，而非 Git/旧本体分支；显示 composed schema ETag、Overlay 集合 hash、当前/历史修订和字段级差异；无定制是“继承安装模板”正常态。
- UX9-6/7：内置浏览器 9/9 路由无阻断页面错误；保存 1280×720 九菜单与关键交互截图，并复用 O1-UX6 窄屏证据。`org-org/dev-project` 正向数据与 `dev-org/dev-project` 负向 canary 为 0 泄漏、0 写入。

验证结果：后端 O1 回归 `67 passed`；前端定向 `8 files / 36 tests passed`；TypeScript、production build 均通过。代码已提交并推送 `m1@68abae6`。机器证据：`services/aos-api/tests/d5e/evidence/O1-UX9_20260810T093850Z.json`。

## 0. 使用的 Rules

1. **先方案后编码**：本清单完成循环评审前不修改 `aos-platform`；本文件评审通过也只代表方案可执行，不代表授权编码。
2. **真实数据、真实逻辑**：正向验收只认 `org-org/dev-project` 的真实微商城对象、关系、Funnel、OKF、Wiki 与 Overlay；禁止 Mock、静态 JSON 或假成功。
3. **不重建架构**：继续复用 PostgreSQL 权威对象/关系、Installation-aware compose、Ontology Client、GraphSnapshot、Draft、Wiki、Funnel、OKF 和 Overlay；不建立第二套本体、图谱或知识真源。
4. **最小兼容演进**：接口只做可回滚、向后兼容扩展；稳定 `objectId`、GraphSnapshot key、Link 端点、历史探索和已封板证据不变。
5. **交互诚实**：加载、空数据、未选择、无权限、服务失败、执行中与完成必须是不同状态；不可用按钮应隐藏或解释，不能点击后无结果。
6. **读写边界**：只读查询可直接回读；保存、重跑、Draft、Overlay 和分支合并必须具备权限、幂等、CAS/Receipt 与回读验证。
7. **服务端权威排序和过滤**：涉及全量结果、分页、游标、排序与 active 状态的语义由服务端冻结；前端不得用当前页排序冒充全局排序。
8. **浏览器门禁**：涉及页面的每个子波必须用内置浏览器实际点击，覆盖主路径、空态、失败态、刷新恢复、宽屏和窄屏；控制台与网络请求同时检查。
9. **证据不覆盖历史**：O1-UX5 的 GREEN 继续表示当时合同与主任务门通过；本波新发现的产品完整性问题以 O1-UX9 新证据闭合，不修改旧证据口径。

## 1. 本次真实页面复审结论

### 1.1 总结

九个菜单目前已经具备稳定路由和一批真实读写合同，但“能打开”与“产品完成”仍有差距。当前缺口主要集中在五类：

- 页面没有选择上下文时把空态误画成永久加载；
- 电商行业模板仍以单一 `Order` 映射代表整个电商领域；
- 图谱健康指标、问题清单和图形定位之间没有形成可解释闭环；
- Wiki 编辑页与索引页没有形成面向业务对象的知识工作流；
- 分支与 Overlay 页面只呈现 Installation Overlay 历史，菜单名称和用户预期不完全一致。

### 1.2 页面事实与整改口径

| 页面 | 当前事实 | 严重度 | O1-UX9 完成口径 |
|---|---|---:|---|
| 本体管理 | 现有类型、关系与组织定制读链可用 | P2 | 做跨页入口和视觉回归，不重做内核 |
| 对象探索 | 真实 Order/Product 已接；订单首列已显示真实订单号，但又保留独立“订单号”列；服务端按 canonical ID 排序 | P0 | 默认去重列；Order 按真实下单时间倒序、稳定排序；保存探索兼容 |
| Funnel 管道 | 直接进入且未带 `type` 时不发请求，`stages.length===0` 被渲染为“加载流水线…” | P0 | 显式对象类型选择器；未选择、加载、空、失败、运行中分态 |
| OKF funnel | 当前 `okf_mapping:{industry}` 一行业只保存一个 Object Type；电商直接打开 `Order` | P1 | 电商包内按 Object Type 查看和维护映射，保留 Order 兼容入口 |
| OKF 概览 | 三张行业卡片把 Order 100% 映射近似成电商整体 100% | P0 | 展示行业整体与各 Object Type 覆盖、阻断、修订、水位；禁止误导性 100% |
| 图谱健康度 | 当前真实读数约为对象 617、属性冲突 617、孤立 237、规则 1、score 75；问题与图形定位弱 | P0 | 先解释指标和计分，再提供 List/Graph 问题覆盖层和治理入口 |
| 活知识 Wiki | 无 type/id 时为空态；有真实对象但无 Wiki 时可能显示“not found”；表单仍有 WorkOrder 文案残留 | P0 | 菜单入口可选对象；知识缺口不是错误；字段和模板由 Object Type 驱动 |
| Wiki 索引 | 结构基本可用，但卡片显示 raw ID；Product 取历史对象而非实际上架口径 | P1 | 统一业务展示名、真实覆盖、active 口径、分支和更新时间筛选 |
| 分支与 Overlay | 页面消费 Installation 绑定的组织 Overlay；菜单中的“分支”容易让用户误以为是模板源码分支 | P1 | 明确页面只管理 Installation/Overlay 的当前态、历史、diff 与恢复继承；不重开旧分支模型 |

## 2. 冻结架构和共享语义

### 2.1 继续沿用的权威链

```text
微商城真实源数据
  → ecom_object / ecom_link（领域权威对象与关系）
  → obj_instance / graph_edge（兼容投影）
  → Installation-aware Ontology Compose
  → 对象查询 / Funnel / OKF / Graph Health / Wiki / Branch & Overlay
  → 九菜单页面和上层 AIP、六数字同事、工作台
```

本清单不允许：

- 用前端静态数组补出 Product、Payment 等 OKF 完成度；
- 用局部对象列表替代服务端全局排序、active 过滤或 Wiki 覆盖；
- 为图谱健康创建第二套节点、边或问题真源；
- 把不存在的 Wiki、Overlay、分支或 Receipt 画成已存在；
- 修改 canonical identity 解决显示问题。

### 2.2 共享 Object Type 范围

微商城电商主链至少包含：

`Shop`、`Weapp`、`Category`、`Product`、`ProductSku`、`ProductReview`、`CustomerLite`、`Order`、`OrderLine`、`Payment`、`Shipment`、`SystemConfig`。

页面不得各自维护互相漂移的类型清单。类型中文名、业务展示名、active 过滤、默认列、默认排序、Wiki 模板和图谱颜色应从同一注册表或服务端 composed schema 派生；前端只保留无业务含义的表现层 fallback。

### 2.3 状态机统一

所有页面的数据区至少区分：

`idle/unselected` → `loading` → `success-with-data` / `success-empty` / `error`。

执行类操作另加：`submitting` → `accepted` → `reconciling` → `succeeded` / `failed` / `unknown`。外部效果超时必须进入 `unknown/reconcile`，不得直接显示成功或失败。

## 3. UX9-0：真值、合同和失败测试冻结（串行前置）

### 3.1 对象查询排序合同

在现有 `ObjectQuery { branch?: string }` 上做向后兼容扩展：

```ts
type ObjectQuery = {
  branch?: string;
  sortBy?: string;
  sortDirection?: "asc" | "desc";
};
```

服务端只接受当前 Object Type 的安全 allow-list 字段，禁止把任意客户端字符串拼入 SQL。V1 至少冻结：

| Object Type | 默认排序 | 稳定次序 | 空值 |
|---|---|---|---|
| `Order` | `createdAt DESC` | `objectId DESC` | `NULLS LAST` |
| 其他类型 | 保持现有 canonical 顺序 | `objectId ASC` | 不适用 |

细则：

- `createdAt` 必须是 Order composed schema 中映射自真实下单时间的字段，不得使用同步时间、更新时间或当前时间兜底。
- 时间无法解析时记录数据质量问题并排在末尾；不得让整页 500，也不得伪造时间。
- 排序必须发生在分页/游标截断之前；前端只以同规则做防御性稳定排序，不能作为权威实现。
- branch effective view 与 production view 使用相同排序语义。
- 响应应返回实际生效的 `sort` 元数据，便于页面和证据回读。

### 3.2 默认列与保存探索兼容

- Order 第一列继续叫“订单”，主标题为 `订单 · <真实订单号>`，次标题为 `源记录 #<source_pk>`。
- 默认列中隐藏独立 `orderNo/订单号`，避免同一订单号重复展示。
- `orderNo` 不从 schema、API 或对象数据中删除；继续用于搜索、详情、导出、图谱/Wiki 标题和上层 Action 输入。
- 新探索默认隐藏 `orderNo`；已有保存探索如果明确保存了 `orderNo`，回放时继续显示，不做静默迁移。
- 列配置中允许用户重新启用“订单号”；保存后按探索资产 revision/ETag 回读。
- Product、Payment 等类型不得套用 Order 的隐藏规则。

### 3.3 active、覆盖和健康语义

- Order active：沿用 `status=active AND isDelete=0`。
- Product 实际上架：沿用 `status=active AND isDelete=0 AND state=1`；历史下架对象保留审计但不计入“实际上架商品”默认覆盖分母。
- Wiki 覆盖、对象探索默认视图和 OKF 影响分析复用同一服务端对象可见性/运营过滤器。
- 图谱健康必须区分 schema 冲突、兼容别名、系统字段、关系必需但缺失、允许孤立五类语义；不能先把 617 条全部算坏再用封顶扣分掩盖。

### 3.4 UX9-0 失败测试清单

- [ ] Order API 未按 `createdAt DESC, objectId DESC` 返回时测试失败。
- [ ] 非 allow-list `sortBy` 返回 `422 OBJECT_SORT_INVALID`，不执行动态 SQL。
- [ ] 不可解析下单时间排末尾并产生可观测计数。
- [ ] 新 Order 探索默认列包含 `orderNo` 时测试失败。
- [ ] 旧探索显式保存 `orderNo` 却被隐藏时测试失败。
- [ ] Funnel 无 type 显示 loading 时测试失败。
- [ ] OKF 概览把 Order 100% 直接显示为电商整体 100% 时测试失败。
- [ ] Wiki knowledge gap 被当成请求错误时测试失败。
- [ ] Product Wiki 覆盖分母包含已下架商品时测试失败。
- [ ] Graph Health 总分无法从问题分类与计分规则复算时测试失败。
- [ ] Overlay 页面把“无定制”显示成异常时测试失败。

### 3.5 预计文件

**SDK / 前端合同**

- `packages/ontology-sdk/src/client.ts`
- `packages/ontology-sdk/src/client.test.ts`
- `apps/web/src/components/ontology/ObjectExplorerWorkspace.tsx`
- `apps/web/src/pages/s2/workshop.tsx`
- 对应 `*.test.ts(x)`

**后端合同**

- `services/aos-api/aos_api/routers/ontology.py`
- `services/aos-api/aos_api/branch_store.py`
- 共享运营对象过滤/排序服务（优先扩展现有模块，不新建第二套查询引擎）
- `services/aos-api/tests/` 下 ontology 定向测试

## 4. UX9-1：对象探索与 Funnel P0 闭合

### 4.1 Order 表格

- [ ] 默认首屏最新订单在最上方。
- [ ] “订单”主列已经展示订单号时，不再默认展示独立“订单号”列。
- [ ] 表头或列配置明确当前排序“下单时间 ↓”；用户切换排序后保存进探索资产。
- [ ] 同一分钟或同一秒订单按 `objectId DESC` 保持刷新稳定，不随机跳行。
- [ ] 搜索订单号仍可命中；点击、勾选、对象集、图谱、Wiki 继续使用 canonical ID。
- [ ] 横向滚动、全屏画布和详情抽屉不因少一列破坏布局。

### 4.2 Funnel 页面状态和选择

- [ ] 直接访问 `/ontology/funnel` 显示 Object Type 下拉与解释，不显示“加载流水线…”。
- [ ] 下拉只列当前 composed schema 可见类型，默认建议最近使用类型，不硬绑测试对象。
- [ ] 带 `?type=Order` 深链时直接读取真实四阶段状态。
- [ ] `loading` 只在请求进行时显示；无 pipeline、无状态、失败证据为空分别呈现。
- [ ] 重跑前展示类型、影响对象数、当前水位和幂等边界；回包后以 Receipt + GET 回读判定结果。
- [ ] 从对象探索、Object Type 详情、OKF 进入 Funnel 时保留 type/branch 上下文。

### 4.3 预计文件

- `apps/web/src/pages/s2/workshop.tsx`
- `apps/web/src/components/ontology/ObjectExplorerWorkspace.tsx`
- `apps/web/src/pages/s2/ontology.tsx`
- `apps/web/src/pages/s2/ObjectTypeDetailPage.tsx`
- `apps/web/src/pages/s2/objectTypeDetail.tsx`
- `packages/ontology-sdk/src/client.ts`
- `services/aos-api/aos_api/routers/ontology.py`
- `services/aos-api/aos_api/branch_store.py`
- 对应前后端定向测试

## 5. UX9-2：OKF 电商领域多 Object Type 闭合

### 5.1 合同演进

不新建 OKF 真源，继续使用当前租户内 `meta_aip_kv` 与 revision/CAS。采用兼容扩展：

- 保留 `GET/PUT /v1/ontology/okf-mappings/{industry}` 作为行业摘要和旧 Order 兼容入口。
- 新增按 Object Type 的集合/明细读取与保存能力；存储键扩展为 `okf_mapping:{industry}:{objectType}`。
- 旧 `okf_mapping:ecom` 只读迁移/兼容为 `ecom:Order`；不得静默覆盖现有组织映射。
- 行业概览聚合各 Object Type 的 revision、coverage、blockedFields、watermark 与 impact。

覆盖率公式冻结为：

- 单类型必填覆盖率 = `已合法映射的 required properties / 当前 composed schema required properties`；
- 单类型可选覆盖率单独展示，不混入必填完成门；
- 电商整体必填覆盖率 = `所有具备真实 source dataset 的类型之已合法映射 required properties 总和 / 同范围 required properties 总和`；
- 无 source dataset、schema 不可读或水位未知的类型不进入百分比分母，必须以“不可判定”单列并阻止行业整体宣告完整；
- 所有分子、分母、排除项、revision 与 watermark 由服务端返回，前端只格式化。

### 5.2 电商产品要求

- [ ] 电商行业左侧展示微商城已安装的真实 Object Type，而非环境/生物演示对象占据主视图。
- [ ] Order、OrderLine、Payment、Shipment、Product、ProductSku、CustomerLite、Shop、Weapp 等均可查看映射状态。
- [ ] 没有源数据或尚未配置映射的类型显示“未配置/无源数据/不可判定”，不能显示假 0% 或假 100%。
- [ ] 每个映射展示源字段、目标 Property、类型转换、必填、状态、修订和影响范围。
- [ ] 保存继续使用 expectedRevision/CAS；成功后回读同一 Object Type，同步刷新概览。
- [ ] OKF 概览先显示“电商整体”，再显示各 Object Type；整体覆盖率采用加权分母并展示算法说明。
- [ ] `Modules=0` 等指标若不是完成门，不得与“100% 完成”并列误导；命名改为真实业务含义。

### 5.3 预计文件

- `apps/web/src/pages/s2/remainder.tsx`
- `services/aos-api/aos_api/routers/ontology.py`
- 现有 OKF DTO/测试文件
- `apps/web/src/styles/20-aip-ontology.css`

## 6. UX9-3：图谱健康度真值、解释与图形治理闭合

### 6.1 先校准指标，不先美化

对当前 617/617/237/1 的读数执行样本核验：

- `GH-01 悬空`：边端点不可见或不存在；属于强错误。
- `GH-02 属性冲突`：拆分为未声明字段、兼容别名、系统字段、类型不符；只有真实冲突进入扣分。
- `GH-03 孤立`：只对声明“必须有关联”的 Object Type/Link 约束计错；允许独立存在的配置或类目不直接算坏。
- `GH-04 规则`：展示命中的具体治理规则、对象范围与影响。
- `P2 归档候选`：保持独立治理建议，不混入图结构错误。

健康分必须由服务端返回可复算 breakdown：分项原始数、有效分母、扣分、阈值和总分。前端不自行发明分数。默认计分冻结为：

```text
score = 100
  - 40 × min(1, dangling_endpoint_rate / 0.01)
  - 25 × min(1, actual_property_conflict_object_rate / 0.10)
  - 25 × min(1, required_link_orphan_rate / 0.10)
  - 10 × min(1, governed_rule_violation_object_rate / 0.05)
```

- 所有 rate 的分母必须随 breakdown 返回；同一对象命中同类问题多次只计一次受影响对象。
- 当分类注册表、分母或权威图水位不可用时，`scoreStatus=unknown`，不得沿用旧 75 分。
- 阈值后续只能通过带版本的治理配置和 ADR 修改；页面显示公式版本，历史证据继续保留原公式。

### 6.2 List / Graph 双视图

- [ ] List 按问题类型、Object Type、严重度、是否可处理筛选。
- [ ] Graph 复用 `OntologyGraphCanvas` 与同一 GraphSnapshot，不复制节点边。
- [ ] 选择问题后只加载相关问题子图，节点/边按问题类型着色；默认不把 617 个问题全塞进一个画布。
- [ ] 图例展示 Object Type、问题类型、数量；方向和严重度不只靠颜色表达。
- [ ] 点击问题节点打开真实对象详情；点击“处理”进入 schema/Link/Draft/数据健康任务，不直接改对象。
- [ ] 空态、扫描失败、图 authority 不可用均失败关闭；旧快照须标明 watermark 和扫描时间。

### 6.3 预计文件

- `apps/web/src/pages/s2/ontology.tsx`
- `apps/web/src/components/ontology/OntologyGraphCanvas.tsx`
- `services/aos-api/aos_api/routers/ontology.py`
- 图谱健康扫描/分类的现有服务模块
- `apps/web/src/pages/s2/W3CGraphHealthInteractions.test.tsx`
- 后端图谱健康定向测试

## 7. UX9-4：活知识 Wiki 与 Wiki 索引业务闭合

### 7.1 活知识 Wiki

- [ ] 菜单直接进入时展示 Object Type 与真实对象选择器、最近对象和 Wiki 缺口，不是空白编辑器。
- [ ] 从对象探索进入时保留 type/id/branch/returnTo，返回后仍定位原对象。
- [ ] Wiki 不存在返回 `knowledge_gap` 业务空态，不显示请求错误；可创建 Draft，但不得直接写生效 Wiki。
- [ ] 标题、结构化字段和 Agent 可读字段由 Object Type/schema/模板驱动，删除“工单备注标题”等 WorkOrder 遗留。
- [ ] 页面展示主体业务名、系统身份、分支、当前版本、Draft 状态、审批状态和生效版本。
- [ ] PII 始终由服务端脱敏；摘要、索引和 Agent 字段不扩大暴露。

### 7.2 Wiki 索引

- [ ] 卡片主标题使用 UX8 业务展示名，不显示 `niushop:1:*` raw ID。
- [ ] Product 默认分母为实际上架 39 条口径；历史下架对象通过显式筛选查看。
- [ ] Order 默认按下单时间倒序；Wiki 更新时间排序与对象时间排序明确区分。
- [ ] 卡片风格吸收视觉稿层级：类型/覆盖状态、业务标题、摘要、更新时间、作者/版本/分支；缺值不伪造。
- [ ] 支持关键词、Object Type、覆盖/缺口、分支、更新时间和运营状态筛选。
- [ ] “为该主体补充知识”进入同一主体 Wiki Draft；刷新后覆盖数从服务端重算。

### 7.3 预计文件

- `apps/web/src/pages/s2/ontology.tsx`
- `apps/web/src/pages/s2/WikiIndexPage.tsx`
- `apps/web/src/pages/s2/WikiDetailPage.tsx`
- `services/aos-api/aos_api/routers/ontology.py`
- 现有 Wiki/coverage-index 服务与测试
- `apps/web/src/styles/20-aip-ontology.css`

## 8. UX9-5：组织定制与 Overlay 信息架构闭合

### 8.1 页面作用冻结

该页不是 Git 或模板源码分支页面。它负责解释当前组织实例如何在平台模板与 Installation 之上形成“千人千面”的可审计本体视图。

现有 `/v1/ontology/branches`、`meta_branch` 和 `obj_branch_overlay` 只保留兼容/开发用途，不作为组织定制真源，也不在目标租户主页面重新暴露 create/checkout/merge。组织定制唯一真链继续是：

`平台模板 → Installation → 不可变组织 Ontology Overlay revision → compose → 当前生效视图`。

### 8.2 功能清单

- [ ] 页面标题或帮助说明解释“分支”是组织定制修订历史，不是模板源码 Git 分支；后续可将菜单改名为“组织定制与 Overlay”。
- [ ] Overlay 显示当前 Installation、composed schema ETag、active revision、历史和相邻 diff。
- [ ] 当前无 Overlay 时显示“继承平台安装模板”，这是正常状态，不是空白或异常。
- [ ] reset-to-inherit 追加新 revision，不物理删除历史；强 ETag + Idempotency-Key + 回读缺一不可。
- [ ] 从本页进入“管理组织定制”时继续使用现有 Overlay CAS 流；不得写 `obj_branch_overlay` 或平台模板。
- [ ] `org-org/dev-project` 的组织定制只作用于当前 scope；`dev-org` 不可见数量、名称和 revision。

### 8.3 预计文件

- `apps/web/src/pages/s2/ontology.tsx`
- Installation/Overlay 现有前端 client、DTO 和交互测试
- `services/aos-api/aos_api/routers/ontology_overlay.py`
- `services/aos-api/aos_api/ontology_overlay.py`
- `services/aos-api/aos_api/ontology_compose.py`
- 对应 Overlay/Installation 定向测试

## 9. UX9-6：跨页视觉、易用性和无效控件清零

- [ ] 页面主标题、面包屑、帮助说明和返回路径采用统一层级。
- [ ] 真实选择器使用下拉/搜索组合，不要求用户手输 Object Type 或 canonical ID。
- [ ] 宽屏充分使用横向空间；表格、图谱和卡片不被固定窄栏压缩。
- [ ] 390/768/1280/1440/1920 视口分别验收；小屏图谱提供邻居列表或全屏入口。
- [ ] 按钮必须满足：真实可用、带原因禁用、或移除；全项目扫描这九页无无效按钮。
- [ ] 焦点顺序、键盘选择、对比度、ARIA、错误提示和 loading announcement 可访问。
- [ ] 视觉稿只用作信息层级与交互参考，不复制其假数据、英文行业或静态画布。

## 10. 实施顺序与并行边界

```text
UX9-0 合同/失败测试
  → UX9-1 对象探索与 Funnel P0
  → UX9-2 OKF 多类型
  → UX9-3 图谱健康
  → UX9-4 Wiki 与索引
  → UX9-5 分支与 Overlay
  → UX9-6 跨页视觉与无效控件清零
  → UX9-7 浏览器、租户 canary、证据封板
```

原因：`apps/web/src/pages/s2/ontology.tsx` 和 `services/aos-api/aos_api/routers/ontology.py` 是 Funnel、Graph Health、Wiki、Branch 共用热点文件。在页面拆分完成前不建议四 worker 同时修改；可并行的仅限：

- 独立测试与证据脚本；
- `remainder.tsx` 的 OKF 与 `WikiIndexPage.tsx` 的索引；
- 浏览器验收矩阵和文档对账。

若后续决定并行，必须从干净 `m1` 建立真实 worktree，先冻结 DTO 和文件所有权，合并后让所有 worker 再 merge 最新 `m1`；不得只创建分支引用冒充 worker 已就绪。

## 11. UX9-7 验证与证据封板

### 11.1 自动化门

- 前端相关 Vitest、TypeScript、production build。
- 后端对象排序、Funnel、OKF、Graph Health、Wiki coverage、Branch/Overlay 定向测试。
- OpenAPI 与 TypeScript DTO fixture 对账。
- 保存探索旧 fixture 回放，证明 `orderNo` 列兼容。
- 跨租户 canary 证明 `dev-org/dev-project` 对正向数据、mapping、Wiki、分支、Overlay 均为 0 泄漏。

### 11.2 浏览器门

| 页面 | 必点路径 | 关键证据 |
|---|---|---|
| 对象探索 | Order 表格 → 排序 → 搜索 → 详情 → 图谱 → Wiki | 最新订单首行、无重复订单号列、canonical ID 不变 |
| Funnel | 无 type → 选择 Order → 四阶段 → 重跑/失败态 | 无永久 loading；Receipt/回读一致 |
| OKF funnel | ecom → 切换 Order/Product/Payment → Lint/保存 | 多类型真映射、revision 与影响 |
| OKF 概览 | 电商整体 → 类型下钻 | 总体口径可解释、不假 100% |
| 图谱健康 | List 筛选 → Graph 定位 → 对象/治理入口 | 问题、扣分、节点/边一致 |
| 活知识 Wiki | 菜单直选对象 → 知识缺口 → Draft | 无 WorkOrder 残留、不直写 PUT |
| Wiki 索引 | Product active → 业务卡片 → 补知识 | 39 条实际上架口径、无 raw ID 主标题 |
| 分支与 Overlay | Installation → Overlay current/history/diff → 管理定制/恢复继承 | 无 Overlay 正常继承；不出现旧 branch 写入口；跨租户不可见 |
| 本体管理 | Object Type → 上述各深链 | type/branch/returnTo 不丢失 |

### 11.3 证据要求

- 每个证据包含时间、commit、scope、authority、请求/响应摘要、页面截图、console/network 结论和测试命令结果。
- 真实正向写验证仅使用用户实际触发的探索/Draft/Overlay；自动化写测试使用 run-unique 可清理范围。
- 机器证据清楚标记 `GREEN/RED/UNKNOWN`，不得因部分页面通过把整波标为 GREEN。
- 封板后更新 `AOS项目开发上下文`、D-waves 状态、提交与远端分支状态，并检查 Prime Agent 是否需要长期任务支持。

## 12. 完成定义与回滚

### 12.1 完成定义

- [ ] Order 默认表格不重复展示订单号，且全量按真实下单时间倒序稳定展示。
- [ ] Funnel 不再永久加载；所有状态可区分。
- [ ] OKF 电商完成度覆盖真实多 Object Type，不用 Order 代表整个行业。
- [ ] Graph Health 指标、计分、列表和图形可以互相解释并回到治理动作。
- [ ] Wiki 菜单可发现对象、识别知识缺口、创建 Draft；索引使用真实业务卡片和 active 口径。
- [ ] 分支与 Overlay 明确为 Installation 绑定的组织定制修订历史，不重开旧分支模型；读写边界和继承语义明确。
- [ ] 九页无无效主按钮，真实租户浏览器、定向测试和跨租户 canary 全绿。
- [ ] 方案、代码、OpenAPI、证据、上下文和 commit 口径一致。

### 12.2 回滚

- Object 排序扩展为兼容参数；回滚参数消费即可恢复旧顺序，不修改对象数据。
- 默认隐藏 `orderNo` 仅是新探索表现配置；回滚不影响 schema、历史探索或订单搜索。
- OKF 多类型使用新 key；旧 `okf_mapping:ecom` 保持可读，回滚不得删除新旧 revision。
- Wiki、Graph Health、Branch/Overlay 均以读链或追加 revision 演进；不得用物理删除回滚。
- 任一权威服务不可用时页面失败关闭，不回退为 Mock 或旧静态数据。

## 13. 循环评审记录

### 第一轮：产品完整性与真值评审

**发现**：

1. 订单“首列业务名 + 独立订单号列”重复，且当前 canonical ID 顺序不符合经营查看习惯。
2. 初稿若只在前端排序，会在未来分页后产生跨页乱序。
3. OKF、Wiki 覆盖和 Product 实际上架口径可能各自维护，造成分母漂移。

**已整改进方案**：

- 冻结默认隐藏 `orderNo`、旧探索兼容、列配置可恢复；
- 冻结服务端 `createdAt DESC, objectId DESC, NULLS LAST` 和 allow-list；
- 将 active/实际上架过滤提升为共享服务端语义。

**结论**：第一轮整改后通过。

### 第二轮：架构、安全与可逆性评审

**发现**：

1. OKF 多类型若替换旧 industry key 会破坏现有 Order 映射。
2. 初稿将旧 `/v1/ontology/branches` 误当成目标组织定制主产品能力，违反 Installation/Overlay 真源冻结。
3. 图谱健康若只调权重，无法解释 617 属性冲突和 237 孤立是否真实问题。

**已整改进方案**：

- OKF 使用新 Object Type key，旧 key 只读兼容，不静默覆盖；
- 移除重开旧分支模型的设计，页面只强化 Installation/Overlay current/history/diff/reset-to-inherit；
- Graph Health 先分类校准、再按版本化公式计分和可视化，返回可复算 breakdown；
- OKF 补齐必填/可选与“不可判定”聚合公式，避免前端自算。

**结论**：第二轮整改后通过。

### 第三轮：可实施性、验收与回滚评审

**检查结果**：

- 任务具备串行依赖、文件落点、测试门、浏览器门、租户 canary、证据格式和回滚边界；
- O1 Waves 1—10、D4/D5、O1-UX1～UX8 的权威合同未被重开；
- “订单号默认隐藏、下单时间倒序”已覆盖 API、SDK、保存探索、前端、测试与浏览器证据；
- 九菜单全局补强与局部 P0 问题位于同一计划，不再分散成口径冲突的小清单；
- 未将方案通过误写为代码 GREEN。

**最终结论**：本清单达到可直接执行标准，状态为 **`PLAN_APPROVED`**；等待用户明确授权编码后，从 **UX9-0** 开始。

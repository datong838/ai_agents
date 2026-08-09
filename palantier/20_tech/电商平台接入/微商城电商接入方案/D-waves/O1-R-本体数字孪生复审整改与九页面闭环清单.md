# O1-R：本体数字孪生复审整改与九页面闭环清单

> **版本**：v1.1 · 2026-08-09
> **状态**：O1-R0～R4 复审通过；D5 最终门仍阻断
> **目标租户**：`org-org` · `dev-project`（默认工作区）
> **上位方案**：`O1-本体数字孪生层改造方案.md` v2.1、`D5-E-G17G18G19证据闭合方案.md` v2.9

## 1. 复审结论

2026-08-09 对当前 `m1@46c210e` 的代码、自动化测试和本体数字孪生九页面进行复审，结论为**代码验收不通过**。方案本身维持评审通过，但实现状态必须回退为：

- D5-E：已有基础实现和局部证据，未达到 G17/G18/G19 总体 GREEN；
- O1：A 阶段部分实现，权威 Outbox、单一 Projector、投影所有权、Overlay/Installation 合成和 Receipt/CAS 未闭合；
- 九页面：路由 9/9 存在，只有对象读取/探索和图谱健康度具备部分真实能力，其余存在静态数据、无效按钮、接口契约错误或旧分支模型。

## 2. 执行波次

### R0：内置浏览器本地访问桥接

- [x] 浏览器只访问 `http://localhost:5173`，不直接访问被拦截的 8000 端口；
- [x] 开发环境 API Base 使用同源 `/api`；
- [x] Vite 在宿主机代理 `/api/*` 到 `http://127.0.0.1:8000/*`；
- [x] 保留 `VITE_AOS_API_BASE` 显式覆盖能力；
- [x] 自动化测试覆盖相对 API Base（3/3 通过）；
- [x] 内置浏览器确认页面不再显示 `aos-api 不可达`，并显示 `org-org · dev-project`。

**R0 结论（2026-08-09）**：GREEN。宿主机 `frontend`、`/api/openapi.json`、`/api/v1/health` 均返回 200；内置浏览器已成功接管 `/ontology`，租户显示正确且 API 可达。

### R1：权威写入与失败关闭

- [x] 缺失组织/工作区、未知 scope 和 claim/header 冲突统一 fail-closed；
- [x] Live Source 缺少 `source_id` 时禁止 sample input 回退；
- [x] DLQ 使用 PostgreSQL 权威表、冻结错误码、去 PII、幂等重试 Receipt；
- [x] `apply_batch` 同事务生成权威 Outbox，ignored/replayed 不产生新事件。

**R1 结论（2026-08-09）**：GREEN。新增 `o1r1_001`、`o1r1_002` 两个可逆迁移；真实库已到 `o1r1_002 (head)`。历史 3002 条事后 Outbox 标记为 `legacy_post_projection`，不冒充权威事件；新 DLQ/Receipt/Event 均以 0 行干净起步并启用 RLS。Pipeline Engine 为每次执行生成 `run_id`，失败写 PostgreSQL 且不替换原异常；`GET/POST /v1/dlq` 和 retry 已脱离进程内字典。累计针对性验证 63/63 通过；真实页面显示 `栖月汇商贸有限公司 · 默认工作区`。

### R2：单一 Projector 与投影所有权

- [x] Projector 消费 Outbox 后写兼容 `obj_instance/graph_edge`；
- [x] 移除 `ec_live_executor` 的直接 OT 写入和事后伪 Outbox；
- [x] 电商 owned OT/Link 只允许 Projector actor 落库；
- [x] executor 未登记 SQL 写点由测试阻断，数据库 trigger 阻断其他入口绕过；
- [x] 事务回滚、重放、并发 `FOR UPDATE SKIP LOCKED` lease、Canonical 店铺身份均有实现与负向证据。

**R2 结论（2026-08-09）**：GREEN。真实库已到 `o1r2_001 (head)`；`ecom-projector-v1` 是电商 owned OT/Link 写 `obj_instance/graph_edge` 的唯一数据库 actor。Projector 校验 payload hash/schema，在同一事务完成兼容投影与 Outbox 水位确认；并发双 worker 只投影一次，重放为 0，墓碑同步删除兼容对象及关联边。累计 R1+R2 核心验证 64/64 通过，Projector 专项 5/5 通过。

### R3：Installation、组织 Overlay 与分支合成

- [x] 平台模板、安装实例和组织定制 Overlay 分层；
- [x] Overlay 采用不可变版本、强 ETag/CAS、Receipt 与 reset-to-inherit；
- [x] ObjectType/LinkType 列表与单体读取统一按安装状态和 `org-org/dev-project` 合成；
- [x] 组织定制写入独立 Overlay 真源，不直接改平台模板或兼容对象表。

**R3 结论（2026-08-09）**：GREEN。新增 `o1r3_001` 可逆迁移、Installation 绑定 Overlay Store/Router/Composer；每次变更生成不可变修订和 Receipt，以强 ETag/If-Match 防止并发覆盖，支持 reset-to-inherit。页面仅展示和编辑当前 Installation 的组织定制，不再把旧 `obj_branch_overlay` 当作组织定制真源。

### R4：九页面真实交互闭环

- [x] 本体管理：真实分支、健康指标和 Installation 绑定 Overlay 入口；
- [x] 对象探索：真实 type/id；未闭环动作明确禁用，不保留无效按钮；
- [x] Funnel 管道：必须显式选择 Object Type，不再伪装成“提案审批”或回落 WorkOrder；
- [x] OKF funnel/概览：行业参数使用 `ecom|env|bio`，读取服务端映射并允许概览下钻；
- [x] 图谱健康度：读取权威 `ecom_object/ecom_link`，显示冲突、孤立对象和缺边诊断；
- [x] 活知识 Wiki：必须从选中对象传递 type/id，不硬编码不存在对象；
- [x] Wiki 索引：统一 POST 分析契约、分支感知并对结果做 PII 脱敏；
- [x] 分支与 Overlay：展示 Installation 绑定的不可变修订历史，不再以旧分支表直接改 OT。

**R4 结论（2026-08-09）**：GREEN。内置浏览器在 `org-org/dev-project` 对九个菜单逐页验收，9/9 非空白、9/9 租户正确、0 个页面级异常。真实图谱读数为 `511` 个对象、`590` 条边、`133` 个孤立对象、`0` 条 dangling edge，健康分 `75`，引擎标识 `ecom_authoritative`。本结论只代表**九页面权威读链基础闭环**，不代表九页面产品功能、交互或视觉完成；后续产品化缺口统一由 O1-UX0～UX6 收口，也不把健康分 75 或 D5 指标缺口包装成业务 GREEN。

### R5：D5-E 与最终验收

- [x] 修复 TypeScript 错误和现有前端失败测试；
- [x] 九页面逐页浏览器交互验证；
- [x] G17、G18、G19 已按 v2.9 生成 D5-E0 只读持久化 JSON；
- [ ] 图谱健康门、投影所有权门、D4-SPEC-SYNC 和 G17-SPEC 全部通过；
- [x] 更新 AOS 项目开发上下文、ADR/代码地图、Prime Agent 运行状态和下一波入口。

**R5 当前结论（2026-08-09）**：BLOCKED，不得宣告 D5 总体 GREEN。前端 `151 files / 2007 tests` 全部通过，TypeScript `--noEmit` 通过；后端 O1/D5-E0 针对性回归 `126 passed`。最新只读证据中 G18 regex 检查为 PASS、G19 记录当前真实规模和租户边界，但 G17 明确为 `RED/BLOCKED`：Payment 共 100 条，`pay_duration_min` 非空 47 条，且 `_order_create_time` 未形成权威写入链。必须在后续 O1-A/P12 波次修复并执行 D5-E1/E2，当前不能用只读脚本退出码替代门禁结论。

## 3. 执行纪律

1. 严格按 R0 → R1 → R2 → R3 → R4 → R5 串行推进；后波不得掩盖前波架构缺口。
2. 每波先补失败测试，再做最小实现，再跑针对性与累计验证。
3. 不使用 Mock、不写入 `dev-org`，不以路由存在、按钮可见或测试脚本退出码代替功能验收。
4. 涉及真实数据库写入、失败注入、跨租户 canary 和清理动作时，按上位方案门禁执行并保存可逆证据。

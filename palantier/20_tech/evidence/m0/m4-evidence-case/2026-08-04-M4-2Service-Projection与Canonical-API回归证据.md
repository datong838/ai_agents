# M4-2 Service、Projection 与 Canonical API 回归证据

> 日期：2026-08-04
> 结论：GREEN
> 代码基线：`aos-platform m1@483dd0f`
> tree：`b07a4755cff1a11e309675c180c5244b8d8ff531`

## 1. 本波范围

本波只在 M4-1 冻结的 PostgreSQL Store、strict DTO 和 Stage Policy 上增加应用层：expiry projector、五用例 Service、内部 `EvidenceWriter`、PostgreSQL Reader、Marking Resolver 与五个 Canonical HTTP 端点。未修改页面，未新增具体电商平台模型或 API，未开放公共 Evidence 写入/撤销通道。

## 2. Worker 与总控交付

| 路线 | 提交 | 交付 |
|---|---|---|
| W1 | `1d17466` | `integration_projection.py`；统一数据库 cutoff、`SKIP LOCKED` 批处理、单 Case 独立事务、失败审计与健康 Case 继续、重复投影幂等 |
| W2 | `c52a5e5` | `integration_service.py`；五用例、receipt-first 回放、Snapshot CAS、内部 `EvidenceWriter`、读取前过期投影 |
| W3 | `0418e5e` | `routers/integration_cases.py`；五个稳定 operationId、严格 body/query/header、角色与 marking、统一错误投影 |
| 总控 | `483dd0f` | PostgreSQL Reader、Marking Resolver、生产 wiring、真实 JWT + PostgreSQL HTTP E2E、manifest/aggregate 确定性收口 |

## 3. 关键契约验证

- create 与 snapshot 成功均返回 `201 Created`；幂等回放保持原 status、body 与 ETag。
- Snapshot body 严格为 `{}`；客户端不能提交 stage、cutoff、metrics、Evidence refs 或 effective status。
- current list 只处理当前 org/project 的到期投影；任何重投影失败均失败关闭，不返回旧的高阶段。
- total、分页和统计在 org/project/scope/marking 授权过滤之后计算；`admin` 不绕过 marking。
- M2 Installation 尚无独立 marking 字段时，创建 Case 只固化已验证 Principal 的 marking，不接受 body 自报或降级。
- reference 不计入 current 统计；无有效测量为 `null`，明确测得零才为 `0`。

## 4. 自动化验证结果

| 验证面 | 结果 |
|---|---|
| Projector 专项 | 9 passed |
| Service 专项 | 4 passed；相关组合 55 passed |
| Router 专项 | 61 passed |
| PostgreSQL Reader | 3 passed |
| 真实 JWT + 隔离 PostgreSQL HTTP | 1 passed；创建、回放、列表统计、详情、Snapshot CAS、旧 ETag 409、timeline、marking 隐藏、跨租户 404 均通过 |
| M4-0～M4-2 后端累计 | 115 passed，7 个既有 warning，2 subtests |
| Router 生成物 | 512 manifest entries；生成检查 GREEN；OpenAPI paths 2281 |
| Web 全量 | 143 files / 1982 passed |
| TypeScript | GREEN |
| Web production build | GREEN |

## 5. 分支一致性

`m1` 与四个 `feature/228-m3-*` Worker 分支的本地及远端均指向 `483dd0f`，tree 均为 `b07a4755...`，ahead/behind 为 `0/0`，五个工作树 clean。历史分支名继续保留，不重写历史。

## 6. 风险与下一门

- 当前后端能力已经可供真实页面读取，但 `/apollo/cases` 仍有静态伪事实；M4-3 必须通过现有 SDK 接入五端点并删除这些常量。
- M4-3 不得在前端复刻 Stage Policy、hash、权限或过期判断，也不得修改后端架构。
- M4 尚未最终 GREEN；M5 和任何具体电商平台接入仍受门禁约束。

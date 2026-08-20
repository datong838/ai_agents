# 109 · W-J3 Evals↔Draft↔Lineage 真实样例链

> 状态：`GREEN` · 2026-08-20  
> 证据：`.evidence/aip/2026-08-20-w-j3-sample-chain/` · Proposal `proposal-1d4d878cd36e45cfb8ee`  
> 清单：`59` §7.10 **W-J3** · 验收：一条真实样例链可在三页间互跳且 ID 同源

## 1. 目标

在正向租户 `org-org/dev-project` 落一条**权威**样例链，并把三页用查询参数串起来：

| 环 | 权威对象 | 页面 | 深链参数 |
|---|---|---|---|
| Eval 证据 | `EvalSuite`（挂在 Proposal.evidenceRefs） | `/aip/evals` | `?suite=<suiteId>` |
| Draft / Action | `aip_action_proposal` + Draft | `/aip/drafts` | `?proposal=<proposalId>` |
| Lineage | root=`action` / rootId=proposalId | `/aip/lineage` | `?rootType=action&rootId=<proposalId>` |

禁止：用 `draft_dataset` 冒充 Canonical Draft；无 ID 时伪造 Trace；跨租户硬编码。

## 2. 不做

- 不全量 Eval 矩阵（属 **W-K05**）
- 不跑完整 Approve→Lease→Execute（属 **W-K04**；本波只到 drafted + lineage reconcile）
- 不改 `aos-platform-w2-workshop`

## 3. 实现要点（最小）

1. **权威样例**：`POST /v1/aip/action-proposals`（CloseWorkOrder + evidenceRefs→EvalSuite）→ `POST .../lineage-authority/roots/action/{id}/reconcile`
2. **Drafts**：读取 `proposal`，选中并对账；详情区链到 Evals（suite）与 Lineage（action root）
3. **Lineage**：读取 `rootType`/`rootId`，有值则自动查询；链回 Drafts / Evals
4. **Evals**：读取 `suite` 预选套件；链到 Drafts（可带 proposal）与 Lineage

## 4. 验收

- API：proposal 可读、lineage 事件 ≥1、evidenceRefs 含 EvalSuite
- UI：三页互跳 URL 参数生效；浏览器截图 + JSON 证据入 `.evidence/aip/2026-08-20-w-j3-sample-chain/`
- `59`：W-J3 / B2 / §2.4 相关行标 `已完成`

## 5. 风险

- 本地 API 重启后内存/库若清空，需重新 bootstrap 样例（证据脚本可幂等 Idempotency-Key）
- Draft 空态仍合法；本波用真实 proposal 填满待批 Tab，不注入 Mock

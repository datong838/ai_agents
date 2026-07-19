# 111 · TA.2 Facade 会话票据方案

| 字段 | 内容 |
|------|------|
| 状态 | **已落地（Dev shaped）** |
| 关联 | [73](./73-产品1.3分析建模下一阶段方案.md) **TA.2** · [110](./110-TA1-analytics-runtime边车方案.md) · [109](./109-TA0分析建模契约骨架方案.md) · OpenAPI `NotebookSession` |
| 索引口径 | **v1.0.80** |

## 1. 目标 / 非目标

**目标（DoD）**

- `POST /v1/notebooks/sessions`：边车绿时 **200**，返回 `id` · `status=idle` · **受控 `uiUrl`** · `ticketExpiresAt`。
- Web **不**持有边车 admin / 内部密钥；仅持短期 `ticket`（嵌在 `uiUrl` query）。
- `DELETE /v1/notebooks/sessions/{id}`：Facade 调边车吊销 + 本地元数据 `stopped`。
- 内核态诚实：`status=idle`（shaped；非真 Jupyter kernel busy）。

**非目标（→ TA.3+）**

- 真 Notebook 7 / Jupyter Server 嵌入与内核生命周期。
- Ontology 左栏插片段、SQL 真预览、Draft 写回演示。
- 把分析内核嵌进 `aos-api`（禁止）。

## 2. 架构

```
浏览器 ──Bearer──► aos-api Facade
                      │ POST/DELETE /v1/sessions  (内部)
                      ▼
               analytics-runtime (:8084)
                      │ 签发 ticket · 内存会话
                      ▼
浏览器 ──ticket──► GET /ui/{id}?ticket=…  （受控 UI，非 admin）
```

| 角色 | 持有 | 禁止 |
|------|------|------|
| Web | Facade Bearer + 短期 ticket（uiUrl） | 边车 admin、`AOS_ANALYTICS_*` 密钥 |
| aos-api | `AOS_ANALYTICS_URL`（服务端） | 把 admin 回传 UI |
| 边车 | 会话表 + ticket 明文（内存） | 信任无 ticket 的 /ui |

## 3. 边车契约（相对 TA.1 增量）

| 方法 | 路径 | 行为 |
|------|------|------|
| `POST` | `/v1/sessions` | 创建 · `status=idle` · 签发 ticket · TTL 默认 900s |
| `GET` | `/v1/sessions/{id}` | 元数据（含 ticket 是否仍有效） |
| `DELETE` | `/v1/sessions/{id}` | 吊销 ticket · `status=stopped` |
| `GET` | `/ui/{id}?ticket=` | HTML shaped 页；ticket 无效 → 403 |

请求体（Facade→边车）：`objectType` · `datasetRid` · `purpose` · `principal`（subject）。

响应：`id` · `status` · `uiUrl` · `ticket` · `ticketExpiresAt`（ISO8601 Z）· `notebookUi` · `engine`。

## 4. Facade 行为

| 条件 | `POST /v1/notebooks/sessions` |
|------|-------------------------------|
| URL unset / 探活失败 | 503 `ANALYTICS_SIDECAR_UNAVAILABLE` |
| 边车创建失败 | 503 `ANALYTICS_SESSION_TICKET_UNAVAILABLE` |
| 成功 | **200** `NotebookSession`（持久化元数据；**不**单独回传 admin） |

`uiUrl` 优先用边车返回；若设 `AOS_ANALYTICS_PUBLIC_URL`，Facade 可改写 host（Dev 默认同 `AOS_ANALYTICS_URL`）。

`DELETE`：尽力调边车 DELETE；本地必标 `stopped`（边车已停仍可收口）。

## 5. 环境变量

| 变量 | 说明 |
|------|------|
| `AOS_ANALYTICS_URL` | 边车基址（服务端） |
| `AOS_ANALYTICS_PUBLIC_URL` | 可选；写进 `uiUrl` 的对外基址 |
| `AOS_ANALYTICS_TIMEOUT_SEC` | 探测/代理超时 |
| `AOS_ANALYTICS_TICKET_TTL_SEC` | 边车侧 TTL（边车读；默认 900） |

## 6. 工程落点

| 路径 | 说明 |
|------|------|
| `deploy/dev/analytics-runtime/app.py` | sessions + /ui |
| `aos_api/routers/analytics.py` | 创建/销毁代理 |
| `apps/web/.../analytics.tsx` | 展示 uiUrl |
| `tests/test_analytics_ta2_111.py` | 单测 |
| OpenAPI 描述 | stub → TA.2 已实现（schema 不变） |

## 7. 验收

```text
# 边车已起
curl -X POST http://127.0.0.1:8080/v1/notebooks/sessions \
  -H "Authorization: Bearer dev" -H "Content-Type: application/json" \
  -d '{"objectType":"WorkOrder","purpose":"explore"}'
# → 200 · uiUrl · status=idle

pytest tests/test_analytics_ta2_111.py tests/test_analytics_ta1_110.py -q
```

## 8. 风险

| 风险 | 缓解 |
|------|------|
| shaped UI ≠ 真 NB7 | `engine=shaped-dev` 诚实标注 |
| ticket 在 query 泄露 | TTL 短 · DELETE 吊销 · 后续可改 HttpOnly cookie |
| 浏览器直连 8084 | Dev 可接受；生产可 Facade 反代（后置） |

## 9. 下一刀

~~**TA.3**~~ → ✅ [112](112-TA3-Ontology左栏插片段方案.md)。下一刀 **TA.4** 读数。

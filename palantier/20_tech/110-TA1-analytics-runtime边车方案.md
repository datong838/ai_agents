# 110 · TA.1 analytics-runtime 边车方案

| 字段 | 内容 |
|------|------|
| 状态 | **已落地（Dev shaped）** |
| 关联 | [73](./73-产品1.3分析建模下一阶段方案.md) **TA.1** · [109](./109-TA0-分析建模契约落地方案.md) · [72](./72-系统启停与健康检查手册.md) · [20 §6.5](./20-AOS整体技术方案.md) |
| 索引口径 | **v1.0.79** |

## 1. 目标 / 非目标

**目标（DoD）**

- Dev 可起 **独立进程/容器** `analytics-runtime`（不嵌进 `aos-api`）。
- 容器/本机进程 **`/health` 绿**。
- Facade `GET /v1/analytics/health` 在 `AOS_ANALYTICS_URL` 可达时返回 **`status=ok` · `sidecar=ok`**。
- [72] 增启停与探活说明；`health-check` 对 8083 可选 WARN。

**非目标（→ TA.2+）**

- Jupyter / Notebook 7 真会话票据与 iframe 代理。
- SQL 真预览、分析→Draft 演示故事。
- 将分析内核并入 Host 进程（禁止）。

## 2. 架构

```
浏览器 → aos-api Facade (/v1/analytics/*, /v1/notebooks/*)
              │  AOS_ANALYTICS_URL（Dev 推荐 http://127.0.0.1:8084）
              ▼
         analytics-runtime（进程隔离 · shaped Dev）
              GET /health → 200 { status, notebookUi, engine }
```

与 OCR（8082）/ LiteLLM 同形：**compose 服务 + 可选本机 uvicorn 脚本**。

## 3. 边车契约（Dev shaped）

| 路径 | 行为 |
|------|------|
| `GET /health` | `200` · `status=ok` · `notebookUi=notebook7` · `engine=shaped-dev` · `service=analytics-runtime` |
| `GET /` | 简要说明页 JSON（供探活备用） |
| `GET /api/status` | 与 health 同形扩展字段 |

真 Jupyter Lab / Notebook 7 镜像可在后续以 **compose profile `jupyter`** 替换；本刀不强制拉重镜像。

## 4. 工程落点

| 路径 | 说明 |
|------|------|
| `deploy/dev/analytics-runtime/app.py` | FastAPI shaped |
| `deploy/dev/analytics-runtime/Dockerfile` | python:3.11-slim · 8083 |
| `deploy/dev/docker-compose.yml` | 服务 `aos-dev-analytics` · **8084:8084** |
| `scripts/demo/start-analytics-sidecar-host.ps1` | 本机 uvicorn（无 Docker 时） |
| `aos_api/routers/analytics.py` | 探测优先 `/health`；健康绿后 session 仍 **503 ticket**（TA.2） |
| `tests/test_analytics_ta1_110.py` | 单测 |

## 5. 环境变量

| 变量 | 说明 |
|------|------|
| `AOS_ANALYTICS_URL` | 默认空=unset；Dev 推荐 `http://127.0.0.1:8084`（**勿用 8083**，与 Keycloak oidc profile 冲突） |
| `AOS_ANALYTICS_TIMEOUT_SEC` | 探测超时，默认 2 |

`ensure-api` / 本机启动可不强制注入；演示「分析建模」前手动 export 或写 `.env`。

## 6. Facade 行为（相对 TA.0）

| 条件 | `GET /v1/analytics/health` | `POST /v1/notebooks/sessions` |
|------|---------------------------|-------------------------------|
| URL 未设 | `degraded` · `sidecar=unset` | 503 `ANALYTICS_SIDECAR_UNAVAILABLE` |
| URL 设但探活失败 | `degraded` · `sidecar=unreachable` | 503 |
| URL 设且 `/health` 200 | **`ok` · `sidecar=ok`** | ~~503 ticket~~ → **TA.2 已落地** [111](111-TA2-Facade会话票据方案.md)（200 + uiUrl） |

## 7. 验收

```text
docker compose -f deploy/dev/docker-compose.yml up -d aos-dev-analytics
curl http://127.0.0.1:8084/health
# → status=ok

$env:AOS_ANALYTICS_URL="http://127.0.0.1:8084"
# 重启 aos-api 后
curl http://127.0.0.1:8080/v1/analytics/health
# → status=ok, sidecar=ok

pytest tests/test_analytics_ta1_110.py -q
```

## 8. 风险

| 风险 | 缓解 |
|------|------|
| shaped ≠ 真 Notebook | UI/契约标明 `engine=shaped-dev`；TA.2 换真票据 |
| compose 默认拉起增加资源 | 镜像极轻（仅 fastapi）；可后续改 profile |
| 与 Keycloak / OCR 端口冲突 | 固定 **8084**（8083=oidc · 8082=OCR）；72 表注明 |

## 9. 下一刀

~~**TA.2**~~ → ✅ [111](111-TA2-Facade会话票据方案.md)。下一刀 **TA.3** Ontology 左栏。

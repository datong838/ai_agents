# 157 · 真 Jupyter（Notebook 7）边车 MVP

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 方案定稿 · 已编码 · 已自测  
> **对齐**：[73](73-产品1.3分析建模下一阶段方案.md) · [118](118-产品1.3分析建模阶段退出收口.md) · [110](110-TA1-analytics-runtime边车方案.md) · [111](111-TA2-Facade会话票据方案.md) · [72](72-系统启停与健康检查手册.md)  
> **点名**：用户明确「开真 Jupyter」· 停车场出库本项

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| 最小更改 | Facade `/v1/notebooks/*` 契约不变；Host 读数/Draft/TA.8 **不动** |
| 不破 MVP | `AOS_ANALYTICS_ENGINE=shaped` 仍可用；默认演示不强制 Jupyter 镜像 |
| 军规 | UI 不经 Facade 拿 Jupyter admin；会话仅 ticketed `uiUrl`；写回仍 Draft |
| 诚实 | 本刀 = Notebook 7 + ipykernel + ticket 门闸；**≠** Hub / Lab / BI 全集 / R |
| 分轨 | 新增 `.sh` 宿主机启停；不改 Windows `*.ps1` 行为（可并列提示） |

## 1. 目标 / 非目标

| DoD | 非目标 |
| --- | --- |
| 边车可 `engine=jupyter-server`（真 Jupyter Server + Notebook 7 + ipykernel） | JupyterHub / K8s Spawner |
| `POST /v1/notebooks/sessions` 仍返回短期 **ticketed `uiUrl`**（响应体不落 Jupyter token） | JupyterLab 替换 NB7 |
| ticket 校验后跳转真 Notebook；内核可执行样例 `1+1` | R 内核 · papermill 产线 |
| `nbclient` 无头 smoke（可选脚本） | Contour/Quiver/Vertex 全集 · BI 服务端进包 |
| shaped 模式保留作回退 | 改写 TA.3～8 Host Facade |

## 2. 架构

```
Web /analytics → aos-api Facade (/v1/notebooks/sessions)
                      │
                      ▼
              analytics-runtime :8084
                ├── FastAPI：/health · /v1/sessions · /ui?ticket=（门闸）
                └── Jupyter Server :8888（Notebook 7 UI + ipykernel）
                      AOS_ANALYTICS_ENGINE=jupyter|shaped
```

- **ticket 门闸**：`GET /ui/{id}?ticket=` 校验通过后 **302** 到 Notebook URL（token 仅出现在跳转，不进 Facade JSON）。  
- **浏览器**需可达 `:8888`（compose 映射）；日常探活仍以 `:8084/health` 为准。  
- **完整 WS 反向代理进 Facade** 后置（本刀诚实：跳转直达 Jupyter UI；门闸仍防无票直入会话元数据）。

## 3. 配置

| 变量 | 含义 |
| --- | --- |
| `AOS_ANALYTICS_ENGINE` | `jupyter`（真）· `shaped`（假页回退） |
| `AOS_JUPYTER_PORT` | 默认 `8888` |
| `AOS_JUPYTER_TOKEN` | 可选；空则进程启动时生成 |
| `AOS_JUPYTER_ROOT` | notebook 工作目录（默认 `/notebooks` 或 `deploy/dev/analytics-runtime/notebooks`） |
| `AOS_ANALYTICS_PUBLIC_URL` | ticket `uiUrl` 对外基址（仍指向 :8084） |
| `AOS_JUPYTER_PUBLIC_URL` | 跳转基址（默认 `http://127.0.0.1:8888`） |

## 4. 落点

| 路径 | 变更 |
| --- | --- |
| `157-…` | 本文 |
| `deploy/dev/analytics-runtime/app.py` | 双模 + Jupyter 子进程 + ticket→302 |
| `deploy/dev/analytics-runtime/Dockerfile` | 装 notebook / jupyter_server / ipykernel / nbclient / pandas |
| `deploy/dev/analytics-runtime/notebooks/aos_smoke.ipynb` | 样例 |
| `deploy/dev/analytics-runtime/requirements-jupyter.txt` | 依赖钉扎 |
| `deploy/dev/docker-compose.yml` | env + `8888:8888` + volume |
| `scripts/demo/start-analytics-sidecar-host.sh` | 宿主机双模（并列 ps1） |
| `scripts/ci/smoke-jupyter-sidecar.sh` | health + nbclient smoke / SKIP |
| `tests`（边车轻测或 aos-api 透传 engine） | 有则补 |
| `demo_story.py` · `118` · `72` · `26` · `00` | 回写诚实口径 |

## 5. 风险

| 风险 | 缓解 |
| --- | --- |
| 镜像变大 | 仅 Dev compose；不进客户包 |
| token 出现在浏览器地址栏 | 行业常态；Facade JSON 不返回 token |
| 无 Docker / 未装包 | `shaped` 回退；smoke SKIP |
| 话术 | health.`engine` 区分 `jupyter-server` vs `shaped-dev` |

## 6. 自测

1. shaped：`AOS_ANALYTICS_ENGINE=shaped` · `/health` → `shaped-dev`  
2. jupyter：起边车 · `/health` → `jupyter-server` · 开会话 · ticket 门闸 · 打开 NB  
3. `bash scripts/ci/smoke-jupyter-sidecar.sh`（无 Jupyter → SKIP）  
4. aos-api 既有 TA.1/TA.2 mock 单测仍绿  

### 6.1 自测结果（2026-07-19）

| 项 | 结果 |
| --- | --- |
| `test_analytics_runtime_157.py` | ✅ 3 passed（shaped） |
| 宿主机 jupyter 模式 `/health` | ✅ `engine=jupyter-server` |
| `smoke-jupyter-sidecar.sh` | ✅ health + nbclient |
| ticket `/ui` → 302 Notebook | ✅（本机验证） |
| Docker compose 重建 | 本机 Docker 未起 · 清单已写；有 Docker 时 `up -d --build aos-dev-analytics` |

## 7. 台账

- [26](26-AOS目标态开发计划.md) → v1.88  
- [00](00-技术方案索引.md) → v1.0.126 · 挂 157  

## 8. 下一停车场建议

**Full Spoke**（Helm/运行时运维面；本机需集群或明确 mock 边界）。其后 BI 子集加深 → Apollo Full。  

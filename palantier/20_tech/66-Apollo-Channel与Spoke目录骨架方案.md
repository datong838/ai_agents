# 66 · Apollo Channel / Spoke 目录骨架（Full 元数据 · 非 K8s）

> **版本**：v1.0 · 2026-07-17  
> **任务**：台账下一刀 #2 — Full Spoke / Channel 产品（本刀 = **Channel+Spoke 目录骨架**）  
> **对齐**：[T09](T09-Apollo交付引擎详细技术方案.md) OPS-004/010 · Wave-5 Lite stub · [64](64-Ferry真cosign密钥链方案.md)  
> **工程**：PG 表 · `/v1/apollo/channels*` · spokes 落库 · fleet 读真源 · 单测  
> **硬规则**：不装 Helm/K8s；`kind=full` 仅元数据；运行时仍 `fullSpokeRuntimeDeferred=true`

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文后改 |
| 最小更改 | 扩 Apollo API + PG；UI 仅消费既有 fleet 字段即可 |
| 不影响主路径 | 旧 stub 路径兼容（spokes/local 仍 200） |
| 诚实 | Full Spoke **产品壳/目录** ≠ Full 运行时 |

---

## 1. 目标 / 非目标

| 目标（DoD） | 非目标 |
| --- | --- |
| Channel：`dev`/`staging`/`stable` 种子；list/get | Argo/Helm 真部署 |
| `POST .../promote` · `.../recall`（状态机） | Change Management 全流程 UI |
| Spoke：PG 目录；`kind=lite\|full`；fleet 读库 | Full 节点真实心跳集群 |
| ferry/status：`channelCatalogReady`；`fullSpokeRuntimeDeferred=true` | 宣称 Full Channel 运行时 ✅ |
| 单测绿 | 改客户安装包 |

---

## 2. 状态机（Channel）

```
dev ──promote──► staging ──promote──► stable
  ▲                 │                   │
  └──── recall ←────┴──── recall ←──────┘
```

| 操作 | 规则 |
| --- | --- |
| promote | 仅当 `status=open` 且存在下一档；写 `promotedAt` · 审计日志字段 |
| recall | stable→staging 或 staging→dev；`status` 保持 open；记 `recalledAt` |

Spoke：`channelId` 绑定；`kind=full` 时 `runtime="deferred"`。

---

## 3. API

| Method | Path | 说明 |
| --- | --- | --- |
| GET | `/v1/apollo/channels` | 列表 |
| GET | `/v1/apollo/channels/{id}` | 详情 |
| POST | `/v1/apollo/channels/{id}/promote` | 晋升 |
| POST | `/v1/apollo/channels/{id}/recall` | 召回 |
| GET | `/v1/apollo/spokes` | 列表 |
| GET | `/v1/apollo/spokes/{id}` | 详情（兼容 local/dev/lite 别名） |
| GET | `/v1/apollo/fleet` | hub + spokes + channels（读 PG） |

---

## 4. 落点

| 路径 | 变更 |
| --- | --- |
| `docs/.../66-*.md` | 本文 |
| `aos_api/apollo_catalog.py` | 表/CRUD/状态机 |
| `routers/wave_ext.py` | 挂路由 |
| `ferry.py` status | 目录就绪标志 |
| `openapi/v1.yaml` | paths |
| `tests/test_apollo_channels.py` | 单测 |
| 26/31/00/27 | 回写 |

---

## 5. 自测

- [x] channels 三档种子  
- [x] promote/recall 路径绿；非法晋升 400  
- [x] fleet 含 PG spokes/channels  
- [x] spokes/local 兼容  
- [x] status.`fullSpokeRuntimeDeferred`=true  
- [x] ferry cosign 回归（12 绿含本刀）  

---

*v1.0*

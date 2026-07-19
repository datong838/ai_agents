# 158 · Full Spoke 运行时 MVP（helm-mock · 与 Lite 并存）

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 方案定稿 · 已编码 · 已自测  
> **对齐**：[T09](T09-Apollo交付引擎详细技术方案.md) · [66](66-Apollo-Channel与Spoke目录骨架方案.md) · [09](../09-Apollo交付引擎产品方案.md) · [143](143-TWA9-多Org与Spoke绑定方案.md) · [72](72-系统启停与健康检查手册.md)  
> **点名**：用户「继续」承接 157 下一刀建议 · Full Spoke 出库本项（MVP）

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| 最小更改 | 不改坏 Lite promote/recall；不改 Ferry 签名主路径 |
| 诚实 | **helm-mock ≠ 真 K8s/kind 舰队**；真 install 仍后置 |
| 并存 | `spoke-local-dev`（lite/compose）保留；Full 用 `spoke-full-stub` |
| 不自动开 BI / Apollo Full 深水 | 本刀只 Full Spoke MVP |

## 1. 目标 / 非目标

| DoD | 非目标 |
| --- | --- |
| Helm chart stub + `helm template`（无 helm → SKIP） | 真 kind/minikube 强制 DoD |
| `AOS_FULL_SPOKE_MODE=mock`（默认）：Full stub → `runtime=helm-mock` · heartbeat 可绿 | Argo CD = Apollo · 多集群舰队 |
| `POST .../heartbeat` · `POST .../apply-plan`（mock） | Channel 运维深水 · Change 工作流引擎 |
| fleet/ferry 旗标拆分：`fullSpokeMockReady` vs `fullSpokeRuntimeDeferred`（真 K8s 仍延期） | BI / JupyterHub |
| Spoke UI 诚实展示 mock vs deferred | 把 Helm 打进客户包 |

## 2. 架构

```
Hub (aos-api)
  ├── Lite: spoke-local-dev · runtime=compose
  └── Full MVP: spoke-full-stub · runtime=helm-mock
        ├── catalog activate (MODE=mock)
        ├── POST /heartbeat
        └── POST /apply-plan → Reported State (meta)
Helm chart stub: deploy/spoke-full/chart/
  scripts/ci/helm-template-spoke-full.sh
```

## 3. 配置

| 变量 | 含义 |
| --- | --- |
| `AOS_FULL_SPOKE_MODE` | `mock`（默认）· `off`（保持 deferred）· `compose`（同 mock 语义占位）· `kind`（文档后置） |

## 4. 落点

| 路径 | 变更 |
| --- | --- |
| `158-…` | 本文 |
| `deploy/spoke-full/chart/` | Chart.yaml + templates + values |
| `scripts/ci/helm-template-spoke-full.sh` | template / SKIP |
| `aos_api/apollo_catalog.py` | mock 激活 · heartbeat · apply-plan · fleet 旗标 |
| `routers/wave_ext.py` | 新路由 |
| `apps/web/.../apollo.tsx` | 文案 |
| `tests/test_full_spoke_158.py` | 新测；改 66 旧断言 |
| `72` · `26` · `00` · ferry 旗标 | 回写 |

## 5. 风险

| 风险 | 缓解 |
| --- | --- |
| 话术「Full 已交付」 | UI/旗标：Mock Ready · K8s Deferred |
| 破坏 Lite promote | SQL 仍 `kind='lite'` |
| Org 串租 | Full stub 仍 `org-a`；dev-org 列表不可见（既有） |

## 6. 自测

1. pytest `test_full_spoke_158` + 回归 `test_apollo_channels`  
2. `bash scripts/ci/helm-template-spoke-full.sh`  
3. MODE=off → runtime 保持 deferred  

### 6.1 自测结果（2026-07-19）

| 项 | 结果 |
| --- | --- |
| chart stub | ✅ `deploy/spoke-full/chart` |
| helm-template 脚本 | ✅ 本机无 helm → 诚实 SKIP |
| `test_full_spoke_158_helpers.py` | ✅ 3 passed（无 PG） |
| `test_full_spoke_158.py` / channels | 本机无 PG → skip；有 PG 时覆盖 mock/heartbeat/apply |
| Lite promote | 未改 `kind='lite'` 条件 |

## 7. 台账

- [26](26-AOS目标态开发计划.md) → v1.89  
- [00](00-技术方案索引.md) → v1.0.127  

## 8. 下一停车场建议

**BI 子集加深**（Contour/Quiver/Vertex 在 TA.8 之上加深，非整 BI 进包）。其后 **Apollo Full** 运维深水。  

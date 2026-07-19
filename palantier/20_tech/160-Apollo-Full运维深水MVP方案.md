# 160 · Apollo Full 运维深水 MVP（Change · 健康晋升 · hotfix）

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 方案定稿 · 已编码 · 已自测  
> **对齐**：[T09](T09-Apollo交付引擎详细技术方案.md) · [67](67-Apollo-Change与Release通道UI方案.md) · [66](66-Apollo-Channel与Spoke目录骨架方案.md) · [158](158-Full-Spoke运行时MVP方案.md) · [118](118-产品1.3分析建模阶段退出收口.md)  
> **点名**：用户「继续」承接 159 · **≠** Full Spoke helm-mock

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| 最小更改 | 复用 Channel 梯子；不改坏 Lite promote 主路径（健康绿时行为不变） |
| 诚实 | 运维深水 MVP · catalog+门控；**≠** 真多集群 / Argo=Apollo |
| 切割 | 158 = Spoke 运行时 mock；本刀 = Change/晋升/hotfix |

## 1. DoD

| 项 | 验收 |
| --- | --- |
| Change | `GET/POST /v1/apollo/changes` · approve/reject · 审计字段 |
| 健康晋升 | promote 时源 Channel 上 lite Spoke `heartbeatOk=false` → `CHANNEL_PROMOTE_UNHEALTHY` |
| hotfix | 种子 Channel `hotfix`；Change `kind=hotfix`；可选 merge-stable stub |
| Asset 同绑 | assets 持久化 `compatibleChannels`；promote 目标不在列表 → `CHANNEL_PROMOTE_ASSET` |
| UI | `/apollo/change` 绑 Change API（Draft 区保留为 Ontology 旁路链接） |
| 话术 | Release/Change lede：运维深水 MVP · 真舰队延期 |

## 2. 非目标

- 真多集群 / kind 强制 · Argo CD = Apollo  
- 完整 Required Approvers RBAC  
- Ferry 现场加严 · 生产 IdP  
- 重做 158 helm-mock  

## 3. 落点

| 路径 | 变更 |
| --- | --- |
| `160-…` | 本文 |
| `aos_api/apollo_ops.py` | Change + Asset 登记（KV） |
| `apollo_catalog.py` | hotfix 种子 · promote 门控 |
| `wave_ext.py` | changes / assets 深化路由 |
| `remainder.tsx` | Change/Release 文案与操作 |
| `tests/test_apollo_ops_160*.py` | 单测 |
| `26` · `00` · `118` | 回写 |

## 4. 台账

- [26](26-AOS目标态开发计划.md) → v1.91  
- [00](00-技术方案索引.md) → v1.0.129  

## 5. 自测结果（2026-07-19）

| 项 | 结果 |
| --- | --- |
| `test_apollo_ops_160_helpers.py` | ✅ 3 passed（内存 KV） |
| `test_apollo_ops_160.py` | 本机无 PG → 未跑；有库时覆盖健康/Asset 拒升 |
| `apps/web` tsc | ✅ |
| Lite 健康绿时 promote | 行为保持（门控仅拦 unhealthy） |

## 6. 收口建议

本地停车场主链（真 Jupyter · Full Spoke mock · BI 子集 · Apollo 运维深水）**已出库**。  
更远项仍须点名：真多集群舰队 · JupyterHub · R 内核 · BI 全集进包 · 客户生产 IdP（微商城）· Ferry 现场加严。  

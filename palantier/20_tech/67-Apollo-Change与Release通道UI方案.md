# 67 · Apollo Change / Release 通道 UI（对接 Channel 目录）

> **版本**：v1.0 · 2026-07-17  
> **任务**：台账下一刀 #3 — Change Management 深页（本刀 = **Release/Change UI 对接 promote/recall**）  
> **对齐**：[66](66-Apollo-Channel与Spoke目录骨架方案.md) Channel API · [49](49-T-UI-S2余量第三刀与Ferry叙事方案.md) S2 壳 · T09 OPS-004  
> **工程**：仅前端 S2 页接线；不改后端契约  
> **硬规则**：不宣称 Full Spoke 运行时；不引入审批工作流引擎

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文后改 |
| 最小更改 | 只动 `remainder.tsx` / `apollo.tsx` 文案与按钮；复用 `useJsonGet`/`apiPost` |
| 不影响主路径 | Draft 列表、Lite Upgrade、旧 fleet JSON 仍可用 |
| 诚实 | Channel 梯子 = 目录状态机演示；≠ Helm 发布 |

---

## 1. 目标 / 非目标

| 目标（DoD） | 非目标 |
| --- | --- |
| Release 页：列出 `/v1/apollo/channels`；对可晋升档点 Promote；对可召回档点 Recall | 多级审批 / RBAC 审批人矩阵 |
| Change 页：保留 Draft 列表 + 嵌入 Channel 梯子摘要与跳转 | 新建独立「变更单」表 |
| Spoke 页：列出 `/v1/apollo/spokes`（含 full stub） | Full 节点真实部署 UI |
| lede 诚实：目录 ✅ · 运行时仍延期 | 宣称 Full Channel 产品完成 |

---

## 2. UX 约定

```
Release 通道
  [Lite Upgrade] [刷新]
  Channels（card-list）
    · dev     [Promote → staging]
    · staging [Promote → stable] [Recall → dev]
    · stable  [Recall → staging]
  Fleet JSON（既有）

Change 审批
  Draft 列表（既有）
  Channel 梯子摘要 + Link → /apollo/release

Spoke 详情
  spokes 列表 + local / lite 兼容块
```

Promote/Recall 成功后刷新 channels + fleet；失败展示 `status · code · message`（与 Ferry 页一致）。

---

## 3. 落点

| 路径 | 变更 |
| --- | --- |
| `docs/.../67-*.md` | 本文 |
| `apps/web/src/pages/s2/remainder.tsx` | Release + Change |
| `apps/web/src/pages/s2/apollo.tsx` | Spoke 列表 |
| 26/31/00/27 | 回写 |

---

## 4. 自测

- [ ] 前端 `npm test`（nav）绿  
- [ ] 手工/逻辑：Promote 按钮对 `stable` 隐藏；Recall 对 `dev` 隐藏  
- [ ] 后端契约不变：`pytest tests/test_apollo_channels.py` 仍绿  
- [ ] 文案含 `fullSpokeRuntimeDeferred` / 运行时延期诚实句  

---

*v1.0*

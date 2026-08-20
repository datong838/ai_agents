# 116 · W-L18 ImpactPreview actionBindingHash

> 状态：`GREEN` · 2026-08-20  
> 清单：`59` §8.5 **W-L18** · 验收：外部 Action 与 Preview 联合哈希一致；缺/漂移 fail-closed  
> 证据：`aos-platform-w1-aip/.evidence/aip/2026-08-20-w-l18-action-binding-hash/`  
> 代码：`aos-platform-w1-aip` · 分支 `w1-aip`（合入 `m1`）

## 1. 目标（已兑现）

1. Preview revision **服务端**计算并返回 `actionBindingHash`（64-hex，不落库独立列，派生自冻结材料）
2. ActionProposal 绑 Preview 时，将同值写入 draft `snapshot.actionBindingHash` 并进入 `proposalHash`
3. ProductionStart：绑 Preview 的 Proposal 缺 hash → `ACTION_BINDING_HASH_REQUIRED`；漂移 → `ACTION_BINDING_HASH_MISMATCH`；不创建 TaskRun
4. UI 只读展示；客户端不得自填冒充
5. 无 Preview 的 legacy proposal 仍兼容

## 2. 不做

- 不改 w2；不做完整 W5 ExternalActionProfile / 账号 authority 全开
- 不破坏「无 Preview 的 legacy proposal」内部路径

## 3. 哈希材料（ADR 42 §4 确定性子集）

```text
sha256(canonical_json({
  tenant:{orgId,projectId}, previewId, revision, contentHash,
  dependencySnapshotHash, bindingRefs, capabilityRef, accountRef, expiresAt
}))
```

## 4. 改动面

| 路径 | 说明 |
|---|---|
| `aip_production_contracts.py` | `ImpactPreviewRevision.action_binding_hash` 必填 |
| `aip_production_contract_store.py` | `compute_action_binding_hash`；`_impact_preview` 派生 |
| `aip_action_store.py` | `create_proposal` 固化 binding hash |
| `aip_production_start_service.py` | Start 复验 fail-closed |
| `apps/web/.../contracts.ts` + `parser.ts` | 必填 `actionBindingHash` |
| `ProductionContractsPage.tsx` | 只读展示 |

## 5. 验收

- `pytest`：`test_w2d_contracts` / `test_w2d_action_binding` / `test_w2d_start_gate`（含 mismatch 门）
- `vitest`：parser + ProductionContractsPage

## 6. 风险

- 旧 draft 绑 Preview 但无 `actionBindingHash`：Start fail-closed（符合）
- 篡改 draft snapshot 中的 hash：Start `ACTION_BINDING_HASH_MISMATCH`

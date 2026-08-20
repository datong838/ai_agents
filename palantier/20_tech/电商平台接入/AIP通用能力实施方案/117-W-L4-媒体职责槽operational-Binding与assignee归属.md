# 117 · W-L4 媒体职责槽 operational Binding + assignee 归属

> 状态：`GREEN` · 2026-08-20  
> 清单：`59` §8.5 **W-L4** · 上游 `59-W7-01` / Binding operational（BIND-1）  
> 证据：`aos-platform-w1-aip/.evidence/aip/2026-08-20-w-l4-responsibility-operational-assignee/`  
> 代码：`aos-platform-w1-aip` · 分支 `w1-aip`（合入 `m1`）  
> 边界：仅 `aos-platform-w1-aip`；不做 W-L20 四 kind；不改 w2

## 1. 目标（已兑现）

1. ResponsibilityPlan coverage 按 **assignee 归属** 解析 CapabilityBinding（SkillBinding.`capability_refs` = binding_id 列表）
2. 要求 Binding `active` + `healthy` + **operational usable** + readiness 未过期
3. **禁止**租户全局任意 Binding 点亮槽位
4. 媒体八职责槽 → 十 Capability 映射表可解析；缺 Binding / 非 operational → `coverage=blocked` + 明确 blocker

## 2. 不做

- `AssigneeResolutionReceipt` 全量、四 kind resolver（W-L20）
- 签名 LITE/STANDARD/FULL Bundle 全集发布
- 改 `ecommerce-standard` 已发布 contentHash

## 3. 哈希/解析链

```text
Slot.requiredCapabilityIds
  → assignee AgentInstance
  → active SkillBinding.capability_refs (binding_ids)
  → CapabilityBinding(status/health/operational/fresh)
  → capability assetId 集合 ⊇ required
  → covered | blocked(reasonCode)
```

Blocker codes：`SKILL_BINDING_NOT_ACTIVE` · `CAPABILITY_BINDING_MISSING` · `CAPABILITY_BINDING_NOT_ACTIVE` · `CAPABILITY_BINDING_NOT_OPERATIONAL` · `CAPABILITY_BINDING_STALE`

## 4. 改动面

| 文件 | 说明 |
|---|---|
| `aip_media_responsibility_capability_map.py` | 八槽映射权威 |
| `aip_production_contract_store.py` | 收紧 `_responsibility_blockers` |
| `tests/test_w2b_production_contract_store.py` | 假绿 / operational 负向 |
| `tests/aip/test_aip_media_responsibility_capability_map.py` | 映射齐全 |

## 5. 验收

- pytest：map + responsibility store（含全局 Binding 不点亮、operational blocked）
- 与方案自洽：不再用租户全局 active∩healthy 假绿

## 6. 风险

现网依赖「全局 Binding 假 ready」的 Plan 会变 blocked——符合 W-L4 验收。

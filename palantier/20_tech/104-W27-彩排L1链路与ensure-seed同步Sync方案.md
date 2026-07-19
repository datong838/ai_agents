# 104 · W27 彩排 L1 链路与 ensure-seed 同步 Sync

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[103](103-W26-DataPage-Sync-Pipeline跳转链方案.md) · [CUSTOMER-DEMO.md](../../aos-platform/scripts/demo/CUSTOMER-DEMO.md)  
> **约束**：最小后端补种 · 不改 BFF 契约形态

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 CUSTOMER-DEMO |
| 先方案后编码 | 本文 → seed + smoke + 话术 |
| 最小更改 | 仅 `sync-demo-wo` 幂等补种 |
| 自测 | pytest demo + run-demo-smoke |

---

## 1. 问题

W26 UI 链路 `Sync.sourceId → Pipeline.sourceId`，但 **ensure-seed 只种 Source/Pipeline，无 Sync** → Hub Sync 表空、彩排断链。

---

## 2. 方案

| 层 | 变更 |
| --- | --- |
| `wave_ext.ensure_demo_data_seed` | 幂等创建 `sync-demo-wo` ← `demo-file-wo` |
| `run-demo-smoke.sh` | 新增 `l1-chain`：sources + syncs + pipelines 同 sourceId |
| `CUSTOMER-DEMO.md` | §1 `/data` 分钟段加入 L1 指屏步骤 |
| `test_demo_story.py` | ensure-seed 后断言 sync ≥1 |

---

## 3. 涉及文件

```
services/aos-api/aos_api/routers/wave_ext.py
services/aos-api/tests/test_demo_story.py
scripts/demo/run-demo-smoke.sh
scripts/demo/CUSTOMER-DEMO.md
```

---

## 4. 验收

1. ensure-seed 后 `/v1/syncs` ≥1 且 sourceId=`demo-file-wo` ✅  
2. `run-demo-smoke.sh` 含 `l1-chain` OK ✅  
3. CUSTOMER-DEMO `/data` 段可照读 ✅  
4. pytest demo 用例绿 ✅  

---

*v1.0*

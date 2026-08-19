# 66 · W-E2 StageTemplate 写入波（文件级）

> 状态：`APPROVED_FOR_IMPL` · 2026-08-20  
> 上位：59 D6/W-E2、65 W-E1  
> 目标：`org-org/dev-project` StageTemplate 表非空，「尚无 StageTemplate」消失；sourceBundleRef 走 Bundle allowlist（与 E1 同模式）

## 1. 复习结论

Create 不强制 resolver；`_stage_template` 无 resolver 则 readiness=blocked。本波挂载 SolutionPack exact allowlist，使至少 1 条 draft 可见；freeze 仅在 READY 时做（诚实阻断可接受）。

## 2. 文件级清单

| 路径 | 动作 |
|---|---|
| `aip_stage_template_authority.py`（新建） | SolutionPack allowlist |
| `routers/aip_production_contracts.py` | 注入 `stage_template_source_resolver` |
| `scripts/aip/bootstrap_w_e2_stage_template.py` | 写入 ≥1 条，slot 对齐 E1 `content.review` |
| `.evidence/aip/2026-08-20-w-e2-stage-template/` | API + 无头 Chrome |

## 3. 非目标

不改 w2；不伪造 freeze READY。

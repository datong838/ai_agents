# 67 · W-E3 ImpactPreview 写入波（文件级）

> 状态：`APPROVED_FOR_IMPL` · 2026-08-20  
> 上位：59 D6/W-E3、E1/E2 已 GREEN  
> 目标：`org-org` ImpactPreview 表非空；「尚无 ImpactPreview」消失；启动门仍 fail-closed（无伪造 started）

## 1. 复习

CreateImpactPreview 需真实 Task + Plan exact + frozen Brief/Evidence/Eval + ResponsibilityPlan + StageTemplate。ResponsibilityPlan 仍 draft/blocked → Preview 可创建但 readiness=blocked，**不**强行 freeze。

## 2. 文件

| 路径 | 动作 |
|---|---|
| `scripts/aip/bootstrap_w_e3_impact_preview.py` | 组装现网 exact refs 写入 ≥1 Preview |
| `.evidence/aip/2026-08-20-w-e3-impact-preview/` | API + 无头 Chrome |

## 3. 非目标

不伪造 Start Decision started；不改 w2。

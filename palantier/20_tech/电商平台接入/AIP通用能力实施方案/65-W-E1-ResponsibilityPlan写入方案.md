# 65 · W-E1 Responsibility Plan 写入波（文件级）

> 状态：`APPROVED_FOR_IMPL` · 2026-08-19  
> 上位：59 D6/W-E1～E4、现页 `/aip/production-contracts`  
> 目标：组织内 ResponsibilityPlan 表非空，「尚无」消失；与 StageTemplate（E2）同 profile 可配对

## 1. 复习结论

UI 已能 list/freeze；缺口是 **权威资产写入**（不能前端伪造）。须从已验证 Bundle exact ref 导入或受控 bootstrap，租户仅 `org-org/dev-project`。

## 2. 文件级清单（开工时核对）

| 路径 | 动作 |
|---|---|
| `services/aos-api` ProductionContract store / publish API | 查找已有 create/import；补最小写入 |
| `scripts/aip/bootstrap_*responsibility*` 或新建 | 写入至少 1 条电商 profile Plan |
| `apps/web/.../ProductionContractsPage.tsx` | 仅验收文案；无假数据 |
| `.evidence/aip/2026-08-19-w-e1-responsibility-plan/` | API list count≥1 + 无头浏览器 |

## 3. 非目标

不在本波完成 E3 start 全链；不改 w2。

## 4. 九步

按 59 §7.15；浏览器用无头 Chrome。

## 5. 实现结论（2026-08-20）

- **路径**：Bundle allowlist `ResponsibilityTemplateRevision`（`ecommerce-standard@1`）+ live `agent_instance` exact version；**不**新建模板表。
- **接线**：`aip_responsibility_template_authority.py` → `AipProductionContractStore(responsibility_template_resolver=…)`。
- **修复**：`_responsibility_blockers` 兼容 capability ref 为 **字符串或对象**（原 `.get` 对 str 500）。
- **写入**：`scripts/aip/bootstrap_w_e1_responsibility_plan.py` → `org-org/dev-project` listCount≥1；draft + readiness=blocked（Skill/Capability 覆盖诚实阻断，可接受）。
- **Canary**：`dev-org` count=0。
- **验收**：API bootstrap + 无头 Chrome `/aip/production-contracts` 「尚无 Responsibility Plan」消失。

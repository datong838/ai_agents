# 52 · AIP 前台中文展示军规（目录/技能/阻断码）

> 状态：`IN_PROGRESS` · 只改 `aos-platform-w1-aip`  
> 触发：用户指出智能体目录把 `Skill`、`ecommerce.logic.*`、英文阻断码当主文案不可接受  
> 叠技能：`taste-skill`（可读性/反 slop）+ AOS Palantir 数据密集风格（非 landing 默认审美）

## Design Read

AIP 运维目录页，给中文运营/交付看；**中文名是主文案，方案代号最多作次级/调试**。

## 规则

1. UI 主文案禁止裸露 `Skill` / `Capability` / `ecommerce.logic.A01` / `*_stale` 英文码。
2. 技能名取自 `ecommerce-37-logic-catalog.json` 的 `name`。
3. 专业能力名取自 W0A Crosswalk 中文显示名。
4. 阻断码经 `aipChineseLabels.blockerDisplayName` 翻译后再展示。
5. 模板 ID（`ecommerce.customer_service@1`）不放在卡片标题旁作主视觉。
6. **禁止把方案正文贴上产品页**：`R2 口径`、`Pilot`、`evaluated→published`、`API/脚本`、验收口径说明等只留在 `docs/`；页上最多放简短操作提示与相关入口链接。

## 本波范围（22 页全菜单）

- 决策引擎 16 页 + 模型管理 6 页（见方案 51 §5）
- 中文军规：`aipChineseLabels` + 各页 PageChrome/卡片主文案
- 滚检脚本：`audit_aip_menu_content_scroll_cdp.mjs`（含 `english_primary_copy`）

## 插件页诚实展示

R2 正向组织当前仅有 3 条 Capability Binding（`strategy.plan` / `image.generate` / `video.generate`）。其余定义卡显示「未绑定」是真相，不是白屏；文案须写清「未建组织绑定，请经目录绑定」，禁止把定义层 `blocked` 渲染成运维事故红字。

后续波次：模型页同类英文码一并收口。

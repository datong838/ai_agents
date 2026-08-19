# 56 · AIP 技能发布台（evaluated → published）产品方案

> 状态：`DRAFT` · 本波只出方案，不编码  
> 租户：`org-org/dev-project`  
> 关联：`53-AIP技能维护与发布入口说明.md` · 权威 SkillRegistry

## 问题

智能体目录诚实显示「仅已评测 · 未绑定」。运维没有前台「发布」按钮；`evaluated → published` 只能走受控脚本 / SkillRegistry API。R2 每同事 1 条 Pilot 已够 GREEN，但全量 37 条无法在 UI 闭环。

## Design Read

运维要在一张中文工作台完成：**选技能 → 看 Eval 门 → 确认发布 →（可选）创建 SkillBinding**，全程 Receipt / 幂等 / 租户隔离，不造假成功。

## 范围

### In

| 能力 | 说明 |
|---|---|
| 列表 | 当前租户可见 SkillTemplate 最新修订；中文名 + lifecycle |
| 门控只读 | 引用 Evals / 成熟度状态；未过门禁用发布 |
| 发布动作 | 调现有 `publish_evaluated`（或等价 API）；`Idempotency-Key` |
| 绑定入口 | 发布成功后 CTA 跳转目录/插件；本波可不内嵌完整 Binding 向导 |
| 审计 | 展示最近 RegistryReceipt（无 Secret/正文） |

### Out

- 批量一键发布全部 37 条（需另开波 + 逐条 Eval）  
- 改 w2 Logic Graph  
- 重放密封 Pilot  
- 在浏览器维护第二套 lifecycle  

## 页面与路由

建议：`/aip/skill-publish`（侧栏「技能发布」），入口链自目录黄条与 `53` 地图。

## 军规

- 中文主文案；方案 ID / assetId 只进次级  
- 失败关闭：Eval 未绿、修订漂移、跨租户一律拒  
- 正向租户仅 `org-org/dev-project`  

## 验收

1. evaluated 技能在门绿时可发布，刷新后 lifecycle=`published`  
2. 门红时按钮禁用且中文原因可读  
3. 幂等重放不双写  
4. canary `dev-org` 不可见 org-org 技能写路径  

## 实现波次建议

| 波 | 内容 |
|---|---|
| W-A | 只读列表 + 门控投影 + 文档导航（无写） |
| W-B | 单条 publish API 挂 UI |
| W-C | 发布后创建 SkillBinding 向导（可选） |

## 依赖确认

编码前需产品确认：本台归属 AIP 侧栏还是挂在 Evals 子页；是否允许非 owner 角色发布。

# 54 · AIP 功能性缺口全景（2026-08-19 复检）

> 状态：`CURRENT` · 证据：UI 无头滚检 + DB/权威回读  
> UI：`.evidence/aip/2026-08-19-aip-menu-functional-audit/` → **21 product_ok · 1 warn · 0 crash**  
> 租户：`org-org/dev-project`

## 结论分层

| 层 | 含义 |
|---|---|
| **A · 真坏（产品该可用却不可用）** | 用户点了期望能用，被环境/依赖挡住 |
| **B · 诚实未齐（设计如此）** | 空态/未绑定/需上游上下文；页面诚实，不是白屏 |
| **C · 产品债（缺入口）** | 功能在后端/脚本有，前台没有完整运维台 |

---

## A · 真坏 / 当前不可用

| ID | 页面 | 现象 | 根因 | 建议 |
|---|---|---|---|---|
| A1 | `/aip/model-runtime` | 控制面「部分就绪」路由 **1/3** | 图像/视频 Provider Health 过期或 `provider_http_error` | 图像外呼恢复后再三探；视频不连打 |
| A2 | `/aip/capabilities` | `image.generate` / `video.generate` 绑定 blocked | `PROVIDER_HEALTH_UNAVAILABLE` + `MODEL_ROUTE_BLOCKED` | 同 A1；文本 `strategy.plan` 可用 |
| A3 | 内容官 I01/V01 技能绑定 | SkillBinding blocked | `CAPABILITY_BINDING_NOT_ACTIVE`（依赖 A2） | 多媒体能力恢复后重评 |
| A4 | 智能体目录（间歇） | 黄条「就绪快照已过期」、预检灰 | Binding readiness **15 分钟 TTL**；点刷新不够，需服务侧重评 | 目录页「刷新」应触发 re-evaluate，或 Loop 自动续期（本会话已在脚本侧续） |

> 文本六同事 Pilot（A02/C02/D03/G04/S04/P02）在快照新鲜时 **可运行 6/6**。  
> 历史 D03.r2 blocked、D03.r3 过期快照属旧修订，**不挡** 当前 r4 Pilot。

---

## B · 诚实未齐（不是 crash，但「用不了完整业务」）

| ID | 页面 | 现象 | 说明 |
|---|---|---|---|
| B1 | `/aip/assist` | 「尚无可执行上下文」 | 需 URL exact Task/TaskRun/AgentRun；不造假 Agent |
| B2 | `/aip/drafts` | 待审批 0 | 无真实 Action Proposal 时诚实空 |
| B3 | `/aip/production-contracts` | 职责计划/阶段/预览/启动 = 0；创建按钮禁用 | **根因已查**：DB `aip_responsibility_plan_*` / `aip_stage_template_*` / `aip_impact_preview_*` / `aip_production_start_decision` 在 `org-org/dev-project` **行数均为 0**；Brief/Eval 各 8 条。不是 UI 白屏，是 R2 尚未写入职责计划与阶段模板权威，组合门诚实关闭。补齐需走生产契约创建 API/Workshop 编排，非本页刷新可解 |
| B4 | `/aip/capabilities` | 7/10「未绑定」 | R2 仅建了 3 条组织 Binding；有 CTA「去目录绑定」 |
| B5 | `/aip/agent-registry` | 多数技能「仅已评测 · 未绑定」 | R2 每同事 1 条 Pilot；全量 37 非本波门禁 |
| B6 | `/aip/agents` | 「本页不直接外呼」 | 列表只展示；试运行走目录/Pilot 权威 |

---

## C · 产品债（缺前台工作台）

| ID | 缺口 | 影响 |
|---|---|---|
| C1 | **无「技能发布台」**（evaluated→published） | 只能脚本/API；运维在目录看不到发布按钮 |
| C2 | 目录「刷新」只重读、**不自动 re-evaluate** Binding | 易反复出现 A4 黄条 |
| C3 | 图像 Health 外呼不稳 | A1/A2 长期 P1 |

---

## UI 滚检（壳层）

22/22 无白屏、无 product_gap。唯一 warn：`capability_partial_bound`（=B4）。

## 本会话已做

- 文本 Health 续期 GREEN  
- Binding 软刷新 → catalog **runnable 6/6**（文本 Pilot）  
- 目录页入口说明 + 过期快照 tooltip 纠偏（`524d86e`）  
- **A4**：`POST /agent-registry/refresh-readiness` + 目录「刷新」改重评（方案 55）  
- **A1**：图像 Health 再探 → 仍 `provider_http_error`（2/3 calls），**不连打**  
- **C1**：技能发布台方案 `56-…DRAFT`（未编码）  
- **B3**：职责/阶段表行数 0 根因已写入本清单  

## 建议下一刀（需你拍板）

1. ~~P0 UX：目录「刷新」连带 re-evaluate（消 A4）~~ **已落地，待合 m1**  
2. **P1**：图像外呼恢复后窗口再探（消 A1/A2/A3 图像链）  
3. **P2 产品**：技能发布台按方案 56 开波（消 C1 + B5 全量）  
4. **P2**：若业务要组合门打开，需另开「职责计划+阶段模板」写入波（B3）  

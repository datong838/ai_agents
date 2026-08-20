# 119 · W-L10 Evidence 不可变/revoke + Disclosure/Marking

> 状态：`DRAFT` · 2026-08-20  
> 清单：`59` §8.5 **W-L10** · 上游 W-L9  
> 证据：待封板  
> 边界：仅 `aos-platform-w1-aip`；不改 w2

## 1. 目标

1. Evidence / EvidenceBundle **不可变**；revoke 走 append-only 事件，不改历史行
2. 三层 Disclosure / Marking **执行 API**（Drawer 可消费真实披露决策）
3. revoke 后引用该 Bundle 的 Start/门必须 fail-closed

## 2. 不做

- 完整 Marking 策略编辑器 UI 大改
- 跨租户披露联邦

## 3. 现状（待实现时核对）

- Bundle revision 已 frozen append-only（W-L9）
- 缺：revoke 事件表 / disclosure decision API / marking 执行面

## 4. 最小改动（拟定）

| 面 | 说明 |
|---|---|
| store + alembic | `aip_evidence_revoke_event` / disclosure decision |
| API | revoke + get disclosure |
| Start/门 | 已 revoke Bundle → blocker |

## 5. 验收

- revoke 后 GET 仍可读历史；新引用 blocked
- disclosure 决策可审计、无客户端自填冒充

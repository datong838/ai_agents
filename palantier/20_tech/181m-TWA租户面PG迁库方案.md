# 181m · TWA 租户面 PG 迁库（组织/工作区/邀请/成员/人档）

> **版本**：v1.1 · 2026-07-19  
> **状态**：✅ 方案定稿 · **已编码**（M1-W1a）  
> **分支**：`m1` · 计划真源 [180m](180m-M1后置闭环开发计划.md)  
> **对齐**：[164](164-TWA10-组织工作区创建与邀请审批方案.md) · [166](166-TWA11-组织工作区删除与清数据方案.md) · [168](168-成员自然人识别-邮箱手机号方案.md) · [127](127-TWA7-工作区成员与审计方案.md) · [20a](20a-多用户与工作区整站隔离方案.md)  
> **消化**：179 ③ **164 PG 迁库**；支撑标准企业「重启不丢租户」  
> **实现**：`aos_api/twa_pg.py` 写穿 · `AOS_TWA_STORE=memory|pg|auto` · 单测 `tests/test_twa_pg_181m.py`

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文后改 `aos-api` |
| 最小 | 复用现有 API 契约；换存储，不换 URL |
| 不破坏 | 内存行为 Dev 可双写/迁移开关；种子 org 仍可 bootstrap |
| 诚实 | 不含 OTP（→182m）；不含 MinIO 物理删（→183m） |

## 1. 现状与缺口

| 层 | 现状 |
| --- | --- |
| API | `/v1/orgs` · `/v1/workspaces` · invites · members · `/v1/me/profile` 已有 |
| 存储 | **进程内 dict**（重启丢） |
| 目标 | 落 **既有 Dev PG**（`AOS_DATABASE_URL` · 元库 `aos_meta`） |

## 2. 已决模型（表）

建议 schema（可微调命名，迁移脚本一版）：

| 表 | 要点 |
| --- | --- |
| `twa_org` | id, name, join_policy, created_at, … |
| `twa_workspace` | id, org_id, name, … |
| `twa_org_member` / `twa_ws_member` | (org/ws, subject, role) |
| `twa_invite` | token, org_id, role, max_uses, expires_at, … |
| `twa_join_request` | id, org_id, subject, message, status, … |
| `twa_person_profile` | subject PK, display_name, email, phone, title, … |
| `twa_audit`（可选） | 复用或附录审计 |

**键不变**：Membership 仍以 **subject** 为键；email/phone 为人档字段（与 168 一致）。

## 3. 行为

| 项 | 已决 |
| --- | --- |
| 启动 | `init_schema` 建表；可选 seed 与现有 `dev-org` / 种子人档对齐 |
| 读写 | orgs/workspaces/invites/members/person 仓储改 PG |
| 开关 | `AOS_TWA_STORE=pg\|memory`（默认 **pg** 当 DATABASE_URL 可达，否则 memory+日志警告） |
| 迁移 | 无旧 PG 数据则空库+seed；不做复杂在线迁移 |

## 4. 非目标

- OTP / 发信 / 二维码  
- OpenFGA 组同步加深  
- 跨 Org 搬迁  
- Win 专用脚本  

## 5. 落点

| 路径 | 变更 |
| --- | --- |
| `aos_api/` 新 `twa_store.py` 或拆分 | PG 仓储 |
| `orgs.py` / `org_invites.py` / `membership.py` / `person_identity.py` | 调仓储 |
| `db.py` / migrations | DDL |
| `tests/test_twa*_pg.py` | 重启语义或事务回滚测 |
| 164 / 179 / 26 | 回写 |

## 6. 自检

- [ ] API 进程重启后人档/成员/组织仍在  
- [ ] 既有 TWA.10/11/12 单测适配或加 PG 测  
- [ ] memory 回退仍可用于无 PG 环境  

---

*v1.0 · 181m · M1-W1a*

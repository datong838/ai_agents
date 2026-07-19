# 194m · 工作区通讯录 CSV 导入

> **版本**：v1.1 · 2026-07-20  
> **状态**：✅ **已编码**（M1-W5b）· 自测通过  
> **计划**：[180m](180m-M1后置闭环开发计划.md)  
> **对齐**：[168](168-成员自然人识别-邮箱手机号方案.md) · [182m](182m-成员邮箱手机OTP方案.md)  
> **点名**：用户「继续」→ W5 B  
> **边界**：管理员批量加人；≠ IdP 组同步 · ≠ 通讯录 OAuth  
> **落点**：`aos_api/members_import.py` · `POST …/members/import` · `WorkspaceMembersPage` · `tests/test_w5_193_194m.py`

## 已决

| 项 | 行为 |
| --- | --- |
| API | `POST /v1/workspaces/{id}/members/import` |
| Body | `{ csv: string, defaultRole?: viewer\|… }` |
| CSV 列 | `email,phone,displayName,role`（首行表头可识别则跳过；email/phone 至少一） |
| 上限 | 默认 **200** 行（`AOS_MEMBERS_IMPORT_MAX`） |
| OTP | **按行跳过**（管理员批量信任）；审计写 `members.import` |
| 权限 | `can_manage_members` |
| 结果 | `{ ok, imported, skipped, errors:[{line,message}] }` |
| UI | `WorkspaceMembersPage`：粘贴 CSV → 导入 |

## 非目标

- 通讯录 OAuth / LDAP 同步  
- 逐行 OTP（不现实）  
- 跨 Org 搬迁  

## 自检

- [x] 合法 CSV → imported≥1  
- [x] 坏行进 errors，不拖垮整批  
- [x] 超上限 → 400  
- [x] 非管理员 → 403（沿用成员管理门禁）  

---

*v1.1 · 194m · 已编码*

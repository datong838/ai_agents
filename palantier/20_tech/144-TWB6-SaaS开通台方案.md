# 144 · TWB.6 SaaS 开通台（多 Org · 配额）

> **版本**：v1.0.1 · 2026-07-19  
> **状态**：✅ 方案定稿 · ✅ 已编码 · ✅ 已自测  
> **对齐**：[20b](20b-AOS端云分离与交付形态方案.md) E4 / §5.7 · [26 §14 TWB.6](26-AOS目标态开发计划.md) · 依赖 TWA.9 [143](143-TWA9-多Org与Spoke绑定方案.md)

## 1. 目标（DoD）

| 项 | 验收 |
| --- | --- |
| 开通 | 运维可 `POST` 创建 Org + 默认工作区 + owner 成员 |
| 配额 | `maxWorkspaces` / `maxMembers` / `maxStorageGb`；可 PATCH |
| 列表 | `GET /v1/ops/tenants` 仅 **platform_admin / admin / developer** |
| UI | 运维交付侧栏「SaaS 开通」· 非业务一级推销 |
| 计费 | **外置**（本刀只记 `plan` 文案字段，不接支付） |

## 2. 非目标

- 真计费/发票（外置）  
- Ferry 气隙矩阵（→ **TWB.7**）  
- 租户业务员可见开通台  

## 3. 落点

| 路径 | 改动 |
| --- | --- |
| `aos_api/provisioning.py` | 租户开通记录 + 配额 |
| `aos_api/routers/ops_tenants.py` | `/v1/ops/tenants*` |
| `apps/web/.../SaasProvisioningPage.tsx` | UI |
| `nav.ts` · `App.tsx` | `/apollo/provisioning` |
| `tests/test_twb6_saas_provisioning.py` | 无 PG |

## 4. 配额强制（最小）

开通时写入配额；`assert_quota` 钩子：创建工作区前检查 `maxWorkspaces`（本刀在 ops API 自检；业务 create workspace 全量挂钩可后置）。

## 5. 自测

```bash
pytest tests/test_twb6_saas_provisioning.py -q
```

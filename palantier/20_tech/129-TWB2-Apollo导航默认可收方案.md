# 129 · TWB.2 端导航 Apollo 默认可收

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 已编码 · 已自测  
> **对齐**：[20b](20b-AOS端云分离与交付形态方案.md) C8/C9 · [26 §14 TWB.2](26-AOS目标态开发计划.md)

## 落点

- `nav.ts`：`collapseDefault` · section「运维交付」  
- `AppShell`：折叠 / `/apollo*` 自动展开  
- `EnvReadonlyBadge` · AIP `MODEL_CONFIG_NO_VAULT`  
- 测试：`productCopy.test.ts` · `nav.test.ts`

## 自测

- vitest nav + productCopy · Apollo ≥7 路由保留


## 目标

| DoD | 做法 |
| --- | --- |
| ①② 业务在壳主路径 | 默认登录仍进概览/工作台 |
| Apollo **默认可收** | 侧栏「运维交付」折叠；进 `/apollo*` 自动展开 |
| **路由不少** | 不删任何 `/apollo/*` 路由与 nav 页 |
| 环境只读 | 顶栏徽章，无 Promote |
| 配模型不碰 Vault | AIP 配置仅 `secretRef`；文案禁止「打开 Vault」 |

## 落点

- `nav.ts`：`NavSection.collapseDefault` · section「运维交付」  
- `AppShell`：折叠逻辑  
- `EnvReadonlyBadge`  
- `productCopy.ts` + vitest

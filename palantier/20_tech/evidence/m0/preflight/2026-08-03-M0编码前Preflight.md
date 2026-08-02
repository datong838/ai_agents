# M0 编码前 Preflight 证据

> 时间：2026-08-03（Asia/Shanghai）
> 代码基线：`aos-platform m1@bc9711a`
> 结论：**允许进入 M1；存在 1 个方案内待补依赖和 1 个不阻断的 pnpm 非交互包装问题。**

## 1. 工作树与分支

| 工作树 | 分支 | HEAD | 状态 |
|---|---|---|---|
| `aos-platform` | `m1` | `bc9711a` | 仅保留用户原有 `apps/web/src/shell/AppShell.tsx` 修改 |
| `aos-platform-w1` | `feature/228-ec-w1-contracts` | `bc9711a` | 干净 |
| `aos-platform-w2` | `feature/228-ec-w2-rest-oauth` | `bc9711a` | 干净 |
| `aos-platform-w3` | `feature/228-ec-w3-consistency` | `bc9711a` | 干净 |
| `aos-platform-w4` | `feature/228-ec-w4-pipeline` | `bc9711a` | 干净 |

五个工作树处于同一起跑线，不需要同步提交；M0 不修改或覆盖 `AppShell.tsx`。

## 2. 环境与真源

| 检查 | 结果 |
|---|---|
| Node.js | `v24.14.0`（Codex workspace runtime） |
| pnpm | `11.9.0` |
| Python | API venv `3.11.15` |
| PostgreSQL | 本地开发库 `SELECT 1` 回读成功；未记录连接串 |
| Alembic heads/current | 单 head 且 current 均为 `228logicpublish` |
| 路由聚合 | `generate_domain_aggregates.py --check` 通过，508 个 manifest entries |
| M1 SemVer 依赖 | `semantic_version` 尚未安装；按冻结方案在 M1 增加 `semantic-version>=2.10,<3.0` |

## 3. 基线测试

| 门 | 结果 |
|---|---|
| AssetBundles / IntegrationCases 页面测试 | 3 files、32 tests 通过 |
| Web TypeScript | `tsc --noEmit` 通过 |
| Apollo Asset / Plugin 兼容测试 | 13 tests 通过 |
| OpenAPI 确定性与契约测试 | export/check 通过；10 tests 通过 |

现有 Pydantic `schema` 字段、Starlette/httpx 和 React `act` 警告均为基线警告，本波不顺手扩大修复。

## 4. 已知不阻断问题

直接通过全局 pnpm 包装器运行过滤测试时，包装器试图在无 TTY 环境重建 `node_modules`，触发 `ERR_PNPM_ABORTED_REMOVE_MODULES_DIR_NO_TTY`。现有 workspace 依赖完整，改用已安装的本地 Vitest/TypeScript 可稳定完成基线测试。后续累计回归使用已锁定 workspace runtime；如确需重装，显式使用 CI 非交互安装并检查 lockfile 不漂移。

## 5. 开发门

- M1 只实现 Registry 真源、Manifest 安全、状态/不可变保护和独立 API。
- 不双写旧 Apollo Asset，不提前实现 Resolver/Installation/UI/Evidence/电商业务。
- M1 专项、迁移、OpenAPI 和累计回归未全部通过前，不进入 M2。

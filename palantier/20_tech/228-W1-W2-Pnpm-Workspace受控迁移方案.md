# 228-W1-W2 pnpm Workspace 受控迁移方案

> 日期：2026-07-31
> Worker：W2 / `aos-platform-w2` / `feature/223-worker-2`
> 基线：`7f6434a`
> 状态：✅ 已完成并合入 `m1`

## 1. 目标

把 Web、Desktop、Ontology SDK、UI Kit 四个前端包收敛为单一 pnpm workspace、单一根 lock 和固定 Node/pnpm 入口；不借机升级 Vite/Vitest/TypeScript 大版本，不让 CI 或 Demo 隐式安装依赖。

## 2. 现状证据

- 根目录没有 `package.json`、workspace 定义或 lock。
- 三个嵌套 `package-lock.json` 共约 7,573 行，Desktop 同时含 npmmirror 与 npmjs 来源。
- 四个 manifest 的工具链版本不同，必须原样保持。
- Web/Desktop 以 `file:../../packages/ontology-sdk` 连接本地 SDK。
- 根 `node_modules` 仅有 Vite 缓存，却会使当前 CI 把依赖误判为完整。
- 当前 runner 会按宿主环境自动选择 npm/pnpm，不具备可复现性。
- Desktop Vite resolver 依赖包级 `node_modules/react`，必须在全新 pnpm 安装中验证。

## 3. 设计与文件所有权

W2 可修改：

- 新增根 `package.json`、`pnpm-workspace.yaml`、`pnpm-lock.yaml`、Node 版本约束文件
- `apps/web/package.json`
- `apps/desktop/package.json`
- `packages/ontology-sdk/package.json`
- `packages/ui-kit/package.json`
- 验证通过后删除三个嵌套 `package-lock.json`

W2 禁止修改：

- 业务源码、Vite 配置、CI/Demo/pack 脚本、README
- OpenAPI、CSS/nav、Helm、后端

总控合并阶段负责：

- CI 强制使用项目固定 pnpm，删除宿主机 auto 选择。
- 依赖完整性检查不得被空的根 `node_modules/.vite` 欺骗。
- 清理通用脚本中的 npm/隐式 install；具体电商脚本不在本波。

## 4. 迁移步骤

1. 固定当前已验证的 Node 20.20.2 兼容范围与 pnpm 11.9.0。
2. 建立四包 workspace，保持全部外部依赖版本不变。
3. 本地 SDK 引用改为 `workspace:*`。
4. 在隔离临时目录生成根 lock，先保留旧锁作对照。
5. 全新安装执行 `pnpm install --frozen-lockfile`，再执行离线 frozen install，lock 不得漂移。
6. 全部测试/构建通过后，在同一原子提交删除三个旧 lock。

## 5. 验收

- [x] 全仓只保留一个根 `pnpm-lock.yaml`，无 `package-lock.json`、无 `file:` workspace 依赖。
- [x] lock 包含四个 importer，不含 npmmirror 来源。
- [x] `pnpm list -r --depth -1` 可识别四包。
- [x] Web/Desktop 可解析 SDK、React 与本地 bin。
- [x] Web 1555（最终 1557）、Desktop 40、SDK 6、两端 typecheck/build 全绿。
- [x] 缺 pnpm、缺实际包依赖、旧 lock 残留、lock 漂移均 fail-closed。
- [x] CI runner 不联网安装依赖。

## 6. 完成证据

- Worker `f480ab3`，合并 `771c8e3`；总控 pnpm-only 接线 `e34c66e`。
- pnpm 11.9.0；5 个 importer（根 + 四包）；lock SHA-256 `e204487f6be9cf8ffb3aea99059393ed4ca5847bf19e1ed6ccb25730b6713ec0`。
- 在线 frozen 与全新目录离线 frozen 均通过，离线安装 `downloaded 0`，lock 零漂移。
- CI 自测 14 项覆盖非 pnpm、缺真实本地 bin 与失败传播；最终 `full` 12/12。

## 7. 回滚

迁移保持单一原子 commit。任何 clean install、离线 install、测试或 build 失败，都不删除旧锁、不提交迁移；已提交后可 revert 恢复三个 npm lock 与 `file:` 引用。所有清理仅在临时隔离目录执行，不改用户现有 `node_modules`。

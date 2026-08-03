# M4-1 PostgreSQL 真源与 SDK 回归证据

> 日期：2026-08-04  
> 代码基线：`aos-platform m1@14311e2`  
> tree：`6f89a37e5817d896f9bf21cc2d2a241a901fb318`  
> 结论：**M4-1 GREEN，允许进入 M4-2 Service、Projection 与 API**

## 1. 本波范围

M4-1 只建立 Integration Case 的 PostgreSQL 唯一真源、Store 持久化原语和 Web SDK adapter。本波未新增 Router/Service 公开路由，未修改 `/apollo/cases` 页面，未接入任何具体电商平台。

## 2. 四路交付

| 路线 | 关键提交 | 主要交付 |
|---|---|---|
| W1 | `7e6a367` | 唯一 `228assetintegration` 迁移、8 张表、复合租户 FK、canonical/hash/stage 函数、不可变与尾指针 trigger、受控 downgrade |
| W2 | `da93ab5`、`f409cb3` | PostgreSQL Store，Case/Evidence revision/Snapshot/Event/Projection/Receipt 原子事务，并发 CAS、重启回读、reference 隔离 |
| W3 | `6eef14b` | 五端点 Web SDK，tenant/auth/header、幂等键、强 ETag、离线禁写、未知结果与结构化错误 |
| W4/总控 | `38b105b`、`14311e2` | 重启镜像完整性补强、高权限绕 trigger 对抗、handler/receipt 全回滚、总控集成 |

用户同期的两份数字同事掘金文档以独立提交 `f2d561f` 保存和推送，没有混入 M4 功能提交。

## 3. 固化事实

- Alembic 唯一 head 为 `228assetintegration`，`down_revision=228assetinstall`。
- Case、Instance revision、Evidence revision、Snapshot、Stage Event 和 Command Receipt 使用 PostgreSQL 作为唯一真源。
- Evidence 按 `(producer, seriesKey)` 追加修订；Snapshot 保存 cutoff 时的完整 canonical envelope 和最新 series head。
- Snapshot 同事务推进 instance revision/ETag、Stage Event、Projection 和 Receipt；阶段未变时不伪造 Event。
- 同 ETag 并发只有一方成功；同幂等键同 envelope 回放回执，不同 envelope 稳定冲突。
- current/reference 保持物理与统计隔离；reference 不保留 owner/安装绑定，指标为 `null`。
- 重启回读同时复验 current instance、latest snapshot、projection 的 revision/ETag/stage/policy/cutoff/gates 镜像和 marking 绑定。
- Web SDK 只映射冻结五端点，不引入页面事实或前端阶段算法。

## 4. 验证结果

| 验证面 | 结果 |
|---|---|
| W1 真实 PostgreSQL 迁移专项 | 6 passed |
| W1 迁移链累计 | 71 passed |
| W2 真实 PostgreSQL Store 专项 | 6 passed |
| W2 migration/contract/policy/store 累计 | 52 passed |
| W4 补强后真实 PostgreSQL Store 专项 | 11 passed |
| 后端 M4-0/M4-1 及迁移链累计 | 107 passed，7 个既有 warning |
| Ruff / Python compile / diff check | GREEN |
| Web Integration Case 专项 | 5 files / 58 passed |
| Web 全量 | 143 files / 1982 passed |
| Web TypeScript | GREEN |
| Web production build | GREEN，233 modules |
| 五代码分支/五远端 | 同 HEAD `14311e2`，tree `6f89a37e...`，ahead/behind `0/0`，工作树 clean |

全量 Web 首次调用未加载 `apps/web/vite.config.ts`，导致需要 DOM 的既有测试统一报 `document is not defined`；按 Web 工作目录加载 `jsdom` 配置后重跑 1982/1982 GREEN，确认为调用参数问题而非代码回归。

## 5. 未完成边界与下一波

M4-1 只提供持久化与 SDK 原语，还没有公开 HTTP 能力。M4-2 应严格实施：

- expiry projector 与 Python/PG 阶段交叉验证；
- `integration_service.py` 与仅内部可用的 `EvidenceWriter`；
- 五个 Canonical Router 及统一错误、权限、marking、OpenAPI/header 契约；
- 仍不修改真实 Case 页面，不接入具体电商平台。

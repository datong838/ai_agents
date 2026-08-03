# M5-2 Composition 与 Installation 闭环回归证据

> 日期：2026-08-04
> 结果：GREEN
> 代码基线：`aos-platform m1@2d16a64af13e`
> tree：`7eb9e58cb850c5622880e4bef9ff3292448ac368`

## 1. 本波范围

M5-2 只在测试层复用现有 Resolver、Composition、Installation、Evidence 和 PostgreSQL Store，证明四个 M5 无业务 Bundle 可以组成 immutable lock 并走完安装/回滚。没有修改生产代码、迁移、Router、OpenAPI、Web 或 Bundle source。

## 2. 完成事实

- 三叶请求由生产 Resolver 自动补入唯一 core，形成四包、三条 required edge。
- 候选和请求乱序、重复解析保持相同 snapshot/lock payload/hash、选择原因、边和三类 diff。
- 真实 PG resolve 同 key 回放不新增记录、同 key 异 envelope 冲突零写；GET lock 与 receipt 对拍。
- Installation 走完 `draft→submitted→approved→applied→active→rolled_back`，revision/ETag 为 1～6。
- stale ETag 与 maker 自批失败关闭且零写；checker 批准绑定 exact lock/diff hashes。
- dry_apply、verification、rollback 三类服务端 Evidence 内外 hash 可复算。
- 首装 active 时 `activeRevision=5`；rollback 后 active/previous 均为 null。
- active 后撤销已选 Niushop test release，真实 revalidation stale，但 rollback 仍可安全退出。
- 无关 draft installation 的 revision、ETag、pointer 和 event 不变；空 contribution diff/hash 全程不漂移。

## 3. 验证

| 验证 | 结果 |
|---|---|
| M5 专项 | 100 passed，7 个既有 warning |
| W2 Composition/Installation 相关累计 | 131 passed |
| W3 rollback/安装链相关累计 | 119 passed |
| Ruff check / format-check | GREEN / GREEN（2 helper + 10 个 M5 测试文件） |
| M5 scoped scanner | 41 files，critical=0、warning=0 |
| 五分支本地/远端 | 同 `2d16a64`，ahead/behind `0/0`，clean |

两次资产域全量复跑均受宿主机外部高负载（load average 超过 230）影响而在 FastAPI 初始路由装配阶段长时间等待后人工中断；没有出现测试断言失败，不计入 GREEN。M5-2 的 GREEN 由本波 100 项专项、W2/W3 相关累计以及上一波 `774 passed` 的完整资产域基线组成；M5-3 必须在宿主负载恢复后重新完成最终资产域及平台全量门。

## 4. 下一门

M5-3 只做最终累计回归、Alembic/OpenAPI/security/静态边界和五分支证据收口。M5 最终 GREEN 后必须停在具体平台接入门前向用户汇报，不得自动开始 Niushop/微商城、微信小店、抖音或快手实现。

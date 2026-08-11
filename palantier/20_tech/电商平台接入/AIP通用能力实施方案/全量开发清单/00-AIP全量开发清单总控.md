# AIP 全量开发清单总控

> 状态：**v1.3 · 已获用户全量编码授权 · AIP-0～AIP-3 IMPLEMENTED_GREEN · AIP-4 E0A～E1C IMPLEMENTED_GREEN，下一门 E2**
> 上位总控：`../00-228-AIP通用能力与六数字同事统一实施总方案.md`
> 范围：把上位 `01～15` 和 38 份电商 AIP/FDE/Wiki/内容官/增长参谋长方案转换为可执行、可验收、可回滚的明细清单；完整覆盖由 `17` 矩阵证明。

## 1. 统一 Rules

1. `00` 是架构与阶段总控；本目录只拆任务，不重新设计 Task、Action、Agent、Memory、O1 或安装主链。
2. 方案通过、清单通过、授权编码、代码 GREEN 是四个不同状态；本清单包只推进到“清单统一评审”。
3. PostgreSQL/不可变 Receipt/Lineage 是真源；客户端状态、单例、Mock、静态数组、localStorage 不能成为完成证据。
4. 真实正向范围固定 `org-org/dev-project`；`dev-org` 仅负向 canary；scope 只取认证上下文。
5. O1 Waves 1～10、D4/D5、UX9 保持封板；AIP 只消费公共 Object/Link/Action/OKF/Wiki，不复制。
6. 外部副作用全部经过 Proposal/Draft/Approval/Lease/Receipt；超时进入 unknown/reconcile。
7. 每个清单进入编码前必须重新核对 HEAD、dirty、OpenAPI、迁移 head、服务版本、真实页面和数据水位。
8. 后续只在 `m1` 单分支、由一个执行者串行开发；不创建 w1～w4、worker branch 或 worker worktree。
9. AIP 通用底座、电商 `solution.ecommerce.growth`、PlatformAdapterPack、InstanceOverlay 分层；不得把领域或平台专项写入通用内核。
10. `REQUIRED/DEFERRED/BLOCKED` 都必须登记；延期不等于遗漏，未核验的平台能力不得声称已支持。

说明：02 中的 `runtime worker lease` 是系统运行时并发安全机制，不是 Git worker 分支；本轮禁止的是代码分支/worktree 并行。

## 2. 01～15 映射与规模

| 清单 | 对应上位文件 | 开发主题 | 前置 | 单分支执行边界 |
|---|---|---|---|---|
| 01 | `../01-*` | 现状真值、路由/API/页面基线 | 无 | 串行采集与裁决 |
| 02 | `../02-*` | Task/Plan/Run、TAOR、Checkpoint | 01、14/15 的 AIP-0 | 强串行主链 |
| 03 | `../03-*` | Agent/Skill/Capability/Handoff、37 Logic 目录 | 02、04、05 公共契约 | 按 Registry→Catalog→UI 串行 |
| 04 | `../04-*` | Action/Draft/Approval/Receipt | 02 | 强串行安全链 |
| 05 | `../05-*` | Evals、发布门、Lineage、Observability | 02、04 | 按契约→Runner→Telemetry→UI 串行 |
| 06 | `../06-*` | 三层运行记忆、七知识管道、美妆冷启动、治理晋升 | 02、04、05 | 按存储→治理→检索→管道→知识包串行 |
| 07 | `../07-*` | 助手、分析师、通用工作台 | 03、05、06、09 | API 后再逐页串行 |
| 08 | `../08-*` | 内容官 Agent 团队、短视频、直播 L0～L5、14 Harness | 03～07、09 | Content→Video→Harness→Live 串行分波 |
| 09 | `../09-*` | 模型供应、路由、容量、真实成本 | 01、02、05 | Provider→Route→Usage→UI 串行 |
| 10 | `../10-*` | FDE 六 Skill、26 Reflection、Checkpoint、平台适配抽象 | 02～07、09 | S1～S6 后进入 Reflection/Adapter |
| 11 | `../11-*` + 增长 G0～G6 | 37 Logic、G0～G6、九大真实场景 | 02～10 | G0→G6 严格分波；场景随依赖解锁 |
| 12 | `../12-*` | 来源、许可证、ADR、冲突裁决 | 全程 | 治理清单，持续执行 |
| 13 | `../13-*` | 方案包一致性与变更门 | 01～12 | 统一评审，不并行裁决 |
| 14 | `../14-*` | AIP-0 真值与公共契约实际执行 | 01、13 | 已有详细清单，本文件做执行索引 |
| 15 | `../15-*` | AIP-0 证据、复审和封板 | 14 | 封板串行 |
| 17 | 38 份上位方案 | 全量目标覆盖、延期和冲突矩阵 | 00～16 | 持续对账；每波更新 |

DeerFlow 最小适配不是新的平行真值层，而是贯穿 02/03/05/06/07/09/10/11/12/13 的受控输入；它只能提交 ResearchJob、Artifact、Draft、Candidate 和 Delivery Receipt。

## 3. 关键路径

```text
01 现状真值
 -> 12/13 来源与方案门
 -> 14 AIP-0 执行 -> 15 AIP-0 封板
 -> 02 Task/TAOR
 -> 04 Action 安全链
 -> 05 Eval/Lineage
 -> [03 Agent/Skill | 06 Memory/Wiki | 09 Model/Cost]
 -> 07 Assistant/Analyst/Workbench
 -> [08 Content | 10 FDE]
 -> 11-G0 → G1 → G2 → G3 → G4 → G5 → G6
 -> 11 的 SC01～SC09 随依赖逐项封板
 -> 17 全量覆盖复核
```

## 4. 统一工作包结构

每个明细清单必须具备：目标/非目标、上位来源、前置输入、文件边界、后端/前端/数据任务、API/OpenAPI、租户/RLS、并发/幂等、错误/回滚、测试矩阵、浏览器步骤、EvidencePack、DoD、停止条件、延期项和下一清单。任何一项缺失不得开工。

## 5. 统一证据目录

```text
docs/palantier/20_tech/evidence/aip/<checklist-id>/<run_id>/
  00-baseline.json
  01-contract-and-openapi/
  02-migration-and-data/
  03-backend-tests/
  04-frontend-tests/
  05-browser/
  06-tenant-canary/
  07-failure-and-rollback/
  08-risk-and-deferred.md
  09-final-manifest.json
```

`09-final-manifest.json` 必须记录 commit、scope、contract hash、migration head、测试命令/退出码、浏览器视口、真实数据截止时间、失败证据、回滚结果和文件 hash。

## 6. 统一编码门

- 用户已明确授权清单内全部编码并要求串行 Loop；历史“不授权编码”门已失效。
- 编码时仍一次只实施一个明确子波；全量授权不取消方案复核、证据、租户、安全和逐波 GREEN 门。
- 每波 GREEN 后重新对账剩余清单；上游 contract 变化必须触发所有下游清单 compatibility review。
- 本清单包的统一评审结论见 `16-AIP全量开发清单统一评审与封板结论.md`。
- `16` 的 v1.0 GREEN 已因扩大到 38 份上位方案而撤回；当前以补强后的 v1.1 复审结论为准。

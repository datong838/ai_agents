# 共享记忆 Phase 1～5 实施清单

> 状态：`IMPLEMENTED_GREEN / SEALED`
> 实施提交：`aos-platform/m1@3196251`、`docs/m1@17e9233`
> 上位方案：`/Users/ddt/work/projects/ai_agent/docs/多对话共享记忆机制.md` v1.2
> 边界：不进入 AIP-5 E5，不读写真实业务数据，不保存凭据。

## 1. 文件范围

### 文档权威层

- `memory/authority.json`
- `memory/projection-manifest.json`
- `memory/schemas/*.schema.json`
- `memory/templates/*-receipt-template.json`
- `memory/events/*.jsonl`
- `01-当前项目状态.md`、`06-当前执行检查点.md` frontmatter

### CLI

- `aos-platform/scripts/memory/memoryctl.py`
- `aos-platform/scripts/memory/memory-status`
- `aos-platform/scripts/memory/memory-sync`
- `aos-platform/scripts/memory/memory-receipt`
- `aos-platform/scripts/memory/memory-gate`
- `aos-platform/scripts/memory/memory-validate`
- `aos-platform/scripts/memory/memory-watch`
- `aos-platform/scripts/memory/tests/test_memoryctl.py`
- `prime-agent/prime-agent-runtime/src/rlm/harness.py`
- `prime-agent/prime-agent-runtime/test/test_harness.py`

## 2. 阶段与退出门

| 阶段 | 实施 | 验收 |
|---|---|---|
| Phase 1 | authority、revision、manifest、schema、Receipt 模板 | ✅ Schema GREEN；01/06 revision/hash 一致 |
| Phase 2 | 只读 `memory-status` | ✅ 七状态故障分类单测 GREEN |
| Phase 3 | `memory-sync` dry-run/apply、原子写、写后回读 | ✅ 同输入同 hash；重复运行 0 change；Prime 实际回读 CURRENT |
| Phase 4 | `gate` 双状态退出门 | ✅ delivery 与 memory 分开；真实投影篡改 RED/exit 2，恢复后开门 |
| Phase 5 | Task/Delivery Receipt、lease、event log、expected revision | ✅ 冲突 lease/旧 revision/路径穿越拒绝；跨 revision 完成并释放 |

## 3. 强弱一致性

强一致投影：

- `01-当前项目状态.md` authority frontmatter
- `06-当前执行检查点.md` authority frontmatter
- 项目共享 projection
- WorkBuddy projection
- Prime Agent 三个项目 memory 条目

最终一致投影：

- Codex ad-hoc ingestion note；写入候选后为 `PENDING_ASYNC`，不能伪报 CURRENT。

Phase 4 只以强一致投影作为状态变更门；最终一致延迟必须显示警告。

## 4. 安全与失败关闭

- 所有输出经过秘密模式扫描；命中 Key、Token、Cookie、Password、私钥时拒绝写入。
- 权威更新必须提供 `expected_revision`；不匹配拒绝。
- 文件在同目录临时文件写入、`fsync` 后 `os.replace`；事件日志 append-only。
- Prime 投影不再委托模型根据 prompt 创建/更新条目；`memory-sync` 确定性读写 global Harness JSON，避免 session scope 漂移和模型自由裁决。
- Prime 三条投影除 revision/hash marker 外，还由 `prime-version-state.json` 维护最后成功版本与内容哈希；版本低于最后成功值时必须报 `DRIFTED`。
- Prime 写入前在本机建立 `0600` 备份，采用独占 `flock` + mtime 并发检测 + 原子替换；Prime 原生 Harness 写入使用同一把锁并在陈旧快照保存时失败关闭；任一写后回读失败时恢复备份并保留 RED。
- 仅替换每个 Prime 条目中受管投影段，保留旧有历史叙述、其他 Harness 条目和 refinements。
- Prime 不可用时报告 `UNAVAILABLE/STALE/DRIFTED`；禁止从旧 Prime 投影反向覆盖 authority。
- 不自动修改 Codex 主记忆索引；仅生成用户已授权的 ad-hoc ingestion note。
- `flock` 保护同机临界区，语义 Lease 保护跨对话 scope；守护只读且健康快照权限 `0600`。
- Prime 子进程使用最小环境白名单，不继承 `AGNES_API_KEY` 或无关 shell 环境。

### 4.1 Prime 版本恢复门

2026-08-12 真实故障中，模型驱动的脱离 session 未读到 global 条目，将三条已有历史的投影重建为 `v1`。因此增加强制恢复门：

1. 最后已验证版本基线为 `aos-milestones=v21`、`aos-current-delivery=v23`、`aos-aip-full-checklists=v17`；
2. 恢复 `AOS-000006` 时必须从该基线单调提升到 `v22/v24/v18`，不得接受当前错误 `v1`；
3. 同一 authority revision 重复同步必须幂等，不得继续增加版本；
4. 回读版本、revision、content hash 和投影内容哈希全部一致后，才能重新开门。

## 5. 最终封板

- 所有单元测试、故障注入和真实 Prime 回读 GREEN（当前 13 tests）。
- `memory-status --json` 的 blocking projections 全 CURRENT。
- `gate` 返回 delivery GREEN、memory GREEN 或 GREEN_WITH_WARNINGS。
- 01/06、Git、Prime、WorkBuddy、Codex 候选投影对账。
- 每项提交只包含本实施文件，现有 browser/Kitewright 改动不纳入。

## 6. 运行入口

```bash
cd /Users/ddt/work/projects/ai_agent/aos-platform
scripts/memory/memory-validate --json
scripts/memory/memory-status --json
scripts/memory/memory-gate --json
scripts/memory/memory-sync --json              # dry-run
scripts/memory/memory-sync --json --apply --prime
```

用户级 `launchd` 服务 `com.aos.memory-health` 每 900 秒执行一次 `memory-watch --quiet`，只更新 `/Users/ddt/.prime/agent/memory-health.json`。发现强一致漂移时快照为 RED 且进程退出码为 2，但不会自动修复或改写 authority。

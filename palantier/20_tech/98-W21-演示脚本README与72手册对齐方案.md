# 98 · W21 演示脚本 README 与 72 手册对齐 · Agnes 冒烟稳态

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[72](72-系统启停与健康检查手册.md) · [94](94-W17-Agnes默认接入与LLM回归方案.md) · [95](95-W18-Buddy运行态API数据与彩排脚本方案.md)  
> **约束**：不改 Win `*.ps1` 真源 · Apollo 不深化

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 README/72 |
| 先方案后代码 | 本文 → scripts/demo · 72 |
| 最小更改 | 文档 + agnes 脚本稳态（wait/retry） |
| 双平台 | Win ps1 不动 · mac/Linux bash 补齐 |

---

## 1. 范围

| 项 | 落点 | 动作 |
| --- | --- | --- |
| 10 分钟路径 | `scripts/demo/README.md` | 增 rehearsal/agnes/pytest · `.env` · `--restart` |
| 运行手册 | `72-系统启停与健康检查手册.md` | v1.3 · §5 回归矩阵 · §6 稳态排障 |
| Agnes  flaky | `run-agnes-smoke.sh` | 重启后 wait health · chat 重试 1 次 |

---

## 2. 回归命令矩阵（macOS/Linux）

| 用途 | 命令 |
| --- | --- |
| 健康 | `bash scripts/demo/health-check.sh` |
| 业务冒烟 | `bash scripts/demo/run-demo-smoke.sh` |
| Agnes LLM | `bash scripts/demo/run-agnes-smoke.sh` |
| TB.8 彩排 | `bash scripts/demo/run-rehearsal-smoke.sh` |
| API pytest | `bash scripts/ci/run-pytest.sh` |
| Web 单测 | `cd apps/web && npm test` |

---

## 3. 验收

1. README 与 72 命令一致 ✅  
2. Agnes smoke 重启后 wait + chat 重试 ✅  
3. `run-rehearsal-smoke.sh` 绿 ✅  

---

*v1.0*

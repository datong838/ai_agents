# 113 · W36 Windows 冻结快检与 demo-smoke l1-chain 对齐

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[110](110-W33-可演示冻结维护Runbook方案.md) · [104](104-W27-彩排L1链路与ensure-seed同步Sync方案.md)  
> **约束**：脚本 parity · 不改 API

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文 |
| 先方案后编码 | 本文 → ps1 |
| 最小更改 | l1-chain + freeze-check.ps1 |
| Win 分轨 | 与 README/CUSTOMER-DEMO 一致 |

---

## 1. 问题

`run-demo-smoke.ps1` **缺 l1-chain**（bash 已有 W27）；Windows 无 `run-freeze-check.ps1`。

---

## 2. 方案

| 文件 | 变更 |
| --- | --- |
| `run-demo-smoke.ps1` | 增 `l1-chain` Ok 块 |
| `run-freeze-check.ps1` | demo smoke + `npm test` |
| `README.md` / `CUSTOMER-DEMO.md` | Windows 快检说明 |

`--full` 在 Windows 提示用 Git Bash 跑 `.sh` 全量。

---

## 3. 验收

1. ps1 l1-chain 逻辑与 bash 同构 ✅  
2. `npm test` 路径正确 ✅  
3. macOS `run-freeze-check.sh` 仍绿 ✅  

---

*v1.0*

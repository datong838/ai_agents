# 110 · W33 可演示冻结维护 Runbook

> **版本**：v1.1 · 2026-07-18（Win parity · 挂 [113](113-W36-Windows冻结快检与demo-smoke-l1-chain对齐方案.md)）  
> **状态**：✅ 本波落地  
> **前置**：[102](102-W25-蓝图审计P1收口与可演示冻结方案.md) · [109](109-W32-门禁台账W29-W31证据回写与cosmetic收口方案.md) · [72](72-系统启停与健康检查手册.md)  
> **约束**：仅维护脚本 · 不开新功能编码

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 README |
| 先方案后编码 | 本文 → `run-freeze-check.sh` |
| 最小更改 | 一条聚合命令 · 文档对齐 |

---

## 1. 背景

W32 后 **cosmetic 清零 · UI 编码默认冻结**。日常只需证明 TB.8 彩排面仍绿，不必重复跑全量 pytest（CI/发版前再跑）。

---

## 2. 维护分层

| 层级 | macOS / Linux | Windows | 何时 |
| --- | --- | --- | --- |
| **快检** | `bash scripts/demo/run-freeze-check.sh` | `powershell -File scripts\demo\run-freeze-check.ps1` | 改 Web/CSS · 日常 |
| **彩排** | `bash scripts/demo/run-rehearsal-smoke.sh` | Git Bash 同左 · 或 `run-demo-smoke.ps1` | 客户彩排前 |
| **全量** | `bash scripts/demo/run-freeze-check.sh --full` | **Git Bash** 同左 | 发版/大改 API 前 |

Win `run-demo-smoke.ps1` 已含 **l1-chain**（W36 · 与 bash 同构）。

---

## 3. 涉及文件

```
scripts/demo/run-freeze-check.sh   # macOS / Linux
scripts/demo/run-freeze-check.ps1  # Windows（W36）
scripts/demo/run-demo-smoke.ps1    # + l1-chain（W36）
scripts/demo/README.md
docs/palantier/20_tech/72-…md
```

---

## 4. 验收

1. `run-freeze-check.sh` / `.ps1` → `FREEZE CHECK OK` ✅  
2. README/72/CUSTOMER-DEMO 挂接 ✅  
3. ps1 **l1-chain** 与 bash 同构 ✅  

---

| 版本 | 说明 |
| --- | --- |
| v1.1 | W36 · Win parity · 113 |
| v1.0 | W33 · run-freeze-check.sh |

---

*v1.1*

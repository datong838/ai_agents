# 45 · T-UI S2 余量第二刀（成熟度·态势·模块接口）方案

> **版本**：v1.0 · 2026-07-17  
> **任务**：关闭部分 S2 Stub：`/aip/maturity` · `/workshop/cop` · `/workshop/module-interface`  
> **对齐**：[43](43-T-UI-S2业务深页按域方案.md) 余量 · foundry/html 叙事  
> **工程**：`aos-platform/apps/web`  
> **硬规则**：非 html 像素 1:1；只调 aos-api；Ferry 等仍延期

---

## 范围

| path | 行为 |
| --- | --- |
| `/aip/maturity` | 静态楼梯 L0～L4 叙事 + 链到 Evals/Logic/Draft |
| `/workshop/cop` | 态势面板：graph-health + metrics totals + evals |
| `/workshop/module-interface` | `GET /v1/modules` 列表 |

仍 Stub：OKF · pipeline-proposals · code-repos · data/lineage · apollo release/ferry/change

---

## 自测

- [x] vitest：三 path `status===live`（S2_LIVE=24）
- [x] 既有 nav 段序不变

---

*v1.0*

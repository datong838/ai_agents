# 155 · Web `tsc` 门禁清零与 pack 完整 `npm run build` 恢复

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 方案定稿 · 已编码 · 已自测  
> **对齐**：[151](151-macOS打包清单与pack脚本方案.md) · [152](152-Linux打包清单与pack脚本方案.md) · [26](26-AOS目标态开发计划.md) · pack-desktop-{mac,linux}.sh

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 中文 · 先方案后编码 | 本文先于改码 |
| 最小更改 | 只消 `tsc --noEmit` 现有报错；不顺手重构页 |
| 不破既有功能 | UI 行为不变；仅类型与无用 import |
| 不自动开停车场 | ≠ 真 Jupyter / Full Spoke / BI / 客户现场 IdP |
| 诚实 | 恢复门禁后 pack `--check` 须跑通完整 `apps/web` `npm run build` |

## 1. 背景

[151]/[152] 打包脚本为避开无关 TS 债，对 `apps/web` 仅跑 `npx vite build`（跳过 `tsc`）。本地 `tsc -p tsconfig.json --noEmit` 仍有 **9** 处错误，使「完整构建」与 pack 门禁不一致。

本刀目标：清零该债 → pack 改回 `npm run build` → 三端打包与日常 CI 口径一致。

## 2. DoD

| 项 | 验收 |
| --- | --- |
| `npx tsc -p tsconfig.json --noEmit`（`apps/web`） | exit 0 · 零报错 |
| `npm run build`（`apps/web`） | exit 0 |
| `pack-desktop-mac.sh` / `pack-desktop-linux.sh` | web 步骤改为 `npm test && npm run build` |
| `scripts/pack/{macos,linux}-desktop.md` | 覆盖说明与脚本一致 |
| 功能 | Data / Schedules / OT 深页 / remainder 交互与文案不变 |

## 3. 根因与改法（最小）

| 文件 | 现象 | 改法 |
| --- | --- | --- |
| `blueprintUi.tsx` `BpPropGrid` | `value: string`，调用方传 JSX | `value: ReactNode` |
| `DataPage.tsx` | 未用 `BuildRow`；PropGrid 传 Element | 删未用 type；依赖 PropGrid 放宽 |
| `s2/data.tsx` | 未用 `BpLinkRow`；`detail?.name` 为 `unknown`→`{}` 不入 ReactNode | 删 import；标题 `String(...)` |
| `s2/dataSchedules.tsx` | 未用 `Link` | 删 import |
| `s2/objectTypeDetail.tsx` | `funnelTone === "bad"` 与字面量无交集 | 改为 `ok ? "ok" : "warn"` |
| `s2/remainder.tsx` | 未用 `BpKvList` | 删 import |

## 4. 非目标

- 大规模 React Compiler / 死代码清扫  
- 改 Windows `*.ps1`  
- 客户生产 IdP / 停车场项  

## 5. 风险

| 风险 | 缓解 |
| --- | --- |
| PropGrid 放宽后误塞复杂节点 | 既有调用已如此；仅对齐类型与运行时 |
| pack 变慢 | `tsc` 增量通常秒级；可接受 |

## 6. 自测清单

1. `apps/web`: `npx tsc -p tsconfig.json --noEmit`  
2. `apps/web`: `npm run build`  
3. （可选）`bash scripts/ci/pack-desktop-mac.sh --check`  

## 7. 台账回写

- [26](26-AOS目标态开发计划.md) → v1.86  
- [00-技术方案索引](00-技术方案索引.md) → v1.0.124 · 挂 155  

## 8. 自测结果（2026-07-19）

| 项 | 结果 |
| --- | --- |
| `npx tsc -p tsconfig.json --noEmit` | ✅ exit 0 |
| `npm run build`（apps/web） | ✅ tsc + vite |
| pack 脚本 | ✅ mac/linux 已改 `npm test && npm run build` |

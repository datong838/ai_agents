# 71 · W-H1 Logic 编辑壳 Tab（编辑/历史/自动化占位）

> 状态：`APPROVED_FOR_IMPL` · 2026-08-20  
> 上位：57、59 D8/W-H1  
> 目标：`/aip/logic` 增加 Tab：**编辑**（保留自由画布）/ **运行历史** / **自动化（占位）**；不改 Graph 权威语义

## 文件

| 路径 | 动作 |
|---|---|
| `apps/web/src/pages/s2/LogicCanvasPage.tsx` | shellTab 状态 + Tab 栏；编辑区保持现状；历史移入 Tab；自动化诚实占位 |
| `.evidence/aip/2026-08-20-w-h1-logic-tabs/` | 无头 Chrome |

## 非目标

不改 w2；不把蓝图演示数据当真源；自动化不写假 Uses。

# 96 · W19 Studio/Logic AIP 薄页加深与 CUSTOMER-DEMO 对齐

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[94](94-W17-Agnes默认接入与LLM回归方案.md) · [95](95-W18-Buddy运行态API数据与彩排脚本方案.md) · [92](92-W15-概览控制面bp-ui与死代码清理方案.md)  
> **约束**：Apollo 不深化 · JSON 仅折叠调试 · WorkOrder id 统一 `wo-*`

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文与 UI |
| 先方案后代码 | 本文 → Studio/Logic/CUSTOMER-DEMO |
| 最小更改 | 3 文件 + 彩排话术 |
| Agnes | 试聊走 `/v1/aip/chat` 网关（.env 已配则真模型） |

---

## 1. 范围

| 项 | 文件 | 动作 |
| --- | --- | --- |
| Studio 试对话 | `StudioPage.tsx` | `wo-1001` 示例 · 注入 systemPrompt · 展示 defaultModel/route |
| Studio 预览链 | 同上 | 链 `/workshop/buddy?order=wo-1001` |
| Logic Use LLM | `LogicPage.tsx` | 默认图增 LLM 节点 · 选中时 `/v1/aip/chat` 试聊 |
| 彩排脚本 | `CUSTOMER-DEMO.md` | 去 StoryChain · 四域概览 · bash 命令 · rehearsal-smoke |

---

## 2. 验收

1. `/aip/studio` 试对话含 systemPrompt · provider 非 mock（有 Agnes 时） ✅  
2. `/aip/logic` LLM 节点可试聊 ✅  
3. `CUSTOMER-DEMO.md` 与 92/95 故事链一致 ✅  
4. `npm test` + `run-rehearsal-smoke.sh` 绿 ✅  

---

*v1.0*

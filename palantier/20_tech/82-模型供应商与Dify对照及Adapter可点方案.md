# 82 · 模型供应商页：与 Dify 对照、Adapter 可点、目录可折叠

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 方案定稿 · 可编码（本刀仅 UX 澄清 + Adapter 接线 + 折叠）  
> **对齐**：[78](78-模型供应商页蓝图分层方案.md) · foundry `aip-model-providers.html` · 产品 [07a](../07a-AIP引擎产品设计线框图.md)  
> **Rules**：`production-ui-no-temp`（禁止 disabled 假按钮）· 最小更改 · 先方案后编码

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 先答清产品口径，再改 `ProvidersPage` |
| 禁止临时代码 | 「Adapter 管理」不得再 `disabled`；点开须进真实配置视图 |
| 不搬 Marketplace | 学 Dify 交互层次；**不做** Dify 商店刷量；供应商走 Facade + LiteLLM/Agnes |

---

## 1. 用户三问 · 产品口径

### Q1：已接入是按「具体模型」做插件吗？字段为何不同？

| 层 | Dify | AOS 目标态 | 本页现状 |
| --- | --- | --- | --- |
| 安装单元 | **供应商插件**（DeepSeek / OpenAI-compatible…） | **供应商类型**（OpenAI 兼容 / Azure / Anthropic / vLLM / 自定义 Adapter） | 「可接入类型」= 类型卡（对） |
| 配置差异 | **按插件 schema**：字段、按钮组合不同（DeepSeek 常「配置」一体；OpenAI-compatible 常「管理凭据」+「添加模型」） | **按类型**出不同表单（78 / 蓝图已实现） | 配置页已按 type 分表单（对） |
| 模型 | 装在某个 Provider 下，可开关多模型 | 类型配置里勾选/填写模型 id；路由页再选任务首选 | 「已接入」当前把 Agnes **text / image 端点**拆成两张卡（像模型卡），易误解成「一模型一插件」 |

**结论（给产品/用户）：**

- **不是**「每个模型 id 一个插件」。正确粒度是 **供应商类型（Provider）→ 凭据 → 其下若干模型**。
- 接入字段不同，是因为 **类型不同**（Azure 要部署名/API 版本；vLLM 要本机地址/GPU；Adapter 要 artifacts），不是因为「每个模型换一套插件」。
- Dify 截图里 DeepSeek vs OpenAI-compatible 管理按钮不同，正是 **插件元数据驱动 UI**；我们用 **类型化表单** 达到同效果，不引入 Marketplace 插件运行时。

### Q2：Adapter 管理点了没响应

- 原因：实现写成 `disabled title="后置"`，违反上线态规则。
- 蓝图：`btn-adapter` → `openCfg('adapter')`。
- **本刀**：顶栏「Adapter 管理」=`openConfigure({ type: "adapter" })`，与点「自定义 Adapter 包」一致。

### Q3：全集可折叠；能否把 Dify 那么多插件接过来；「自动更新(最新)」是什么？

| 项 | 说明 |
| --- | --- |
| 折叠 | Dify：「已安装」与「安装模型供应商」可折叠。本刀：「可接入类型」默认展开，可折叠；标题旁显示数量 |
| 接 Dify 全家桶？ | 本地有 `mybuddy-v01/dify` 克隆；**模型供应商已外置 Marketplace**，并非仓库内固定插件树。AOS **不搬** Dify Marketplace；按需用 **LiteLLM 已支持的供应商** + 自定义 Adapter 扩。插件「在手上」≠ 可直接当 AOS 正式供应商运行时 |
| 自动更新(最新) | Dify：**已安装的 Marketplace 插件** 定时对比远端 `latest_version`，策略 `latest` = 有新版就升（模型类常默认 latest；其它类常 fix_only）。**不是**更新 AOS 平台本身。我们本阶段 **不做** 该按钮（无 Marketplace）；若以后做 LiteLLM/Adapter 包版本同步，另开方案 |

---

## 2. 本刀改动清单

| 文件 | 变更 |
| --- | --- |
| `docs/…/82-….md` | 本文 |
| `pages/s2/aip.tsx` `ProvidersPage` | Adapter 可点；可接入类型折叠 |
| `styles.css` | 折叠头样式（若缺） |
| foundry `aip-model-providers.html` | 可选：补折叠示意（真源对齐后置亦可） |

**明确不做：** sessionStorage 草稿债清理、真 PUT providers、自动更新按钮、导入 800+ Dify 插件。

---

## 3. 自测

1. 「Adapter 管理」→ 进入自定义 Adapter 配置视图，可返回列表  
2. 「可接入类型」折叠/展开正常  
3. 已接入 Agnes 卡与路由页不受影响  

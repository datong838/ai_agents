# 25 · LLM-Wiki 启示与 L2 / AIP 演进补丁

> **版本**：v1.0 · 2026-07-17  
> **状态**：✅ 方案补丁（产品 + 技术 + html 蓝图指针）  
> **性质**：需求验证吸收，**非**竞品对标  
> **对齐**：[20](20-AOS整体技术方案.md) · [T06](T06-Ontology与Action-Function详细技术方案.md) · [T07](T07-AIP人工智能平台详细技术方案.md) · [06](../06-语义本体Ontology-Mapping产品方案.md) · [07](../07-AIP引擎k-LLM与AgentStudio产品方案.md) · html **v1.6.1**

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 中文 | 全文中文 |
| 先方案后代码 | 本补丁先于实现；实现按 T-EVO 排期 |
| 最小更改 | 不推翻 HR-01/02/05、AGE 主存、解法 A、Draft 隔离 |
| 与产品自洽 | 回写 06/07/06a/07a；html 最小补页/改页 |

---

## 1. 结论（一句话）

LLM-Wiki 用 MD+Git+AI 演示了「编译式知识沉淀」；AOS 已用 Funnel/Iceberg/Action 解决企业级规模与行动力。本补丁吸收四点：**Insight 回填 · 图谱健康 · 生命周期遗忘 · 可执行 Constitution**，使 L2/AIP 从「可用」补齐「知识复利与治理」。

**架构哲学不变：** 语义建模在 **L2**；L1 不做复杂业务逻辑；写回只经 **Action / Draft**（HR-01）。

---

## 2. 范围 / 非目标

| 做 | 不做 |
| --- | --- |
| 定义 Insight ObjectType 与 Backfill 管线 | 用个人 Wiki 最终一致替代 Iceberg ACID |
| L2 图谱健康度指标与仪表盘 | 把 `health.html`（L1）冒充图谱健康 |
| Object/Property TTL 与归档策略（可审计） | 静默物理删除核心业务 Object |
| OKF 升级为可执行、版本化「AOS Constitution」 | 第二套游离 Markdown 宪法绕过 Bundle/Lint |
| html 最小蓝图对齐（见 §7） | 本期实现代码 / 改 AGE 选型 |

---

## 3. 同构与差异（钉死口径）

| LLM-Wiki | AOS | 口径 |
| --- | --- | --- |
| `wiki/` MD | Object Type + Property | 一致 |
| 双向链接 | Link Type | 一致 |
| Compilation | Funnel 水合 | 一致（数据层） |
| `claude.md` | OKF → **Constitution** | 升级为可执行契约 |
| Backfill Q&A | **Insight Backfill**（≠ Funnel） | **缺口补齐** |
| Health Check | **图谱健康度**（≠ L1 数据健康） | **缺口补齐** |
| 遗忘 | Object/Property **TTL/归档** | **缺口补齐（P2 落地）** |

企业差异（规模 / ACID / RBAC / Action / 流批 / Apollo）见产品叙事：Wiki=知识花园，AOS=生产线。

---

## 4. 四条演进（优先级）

### 4.1 P0 · Insight Backfill Pipeline（知识复利）

**问题：** Funnel = L1→Object 数据水合；Decision Lineage = 决策审计。缺「高价值结论沉淀为可复用 Ontology 知识」。

**产品规则：**

1. Logic / Agent 产生高置信结论 → 默认进 **Draft**（类型：`InsightBackfill`）。  
2. HITL 批准后：  
   - 可选更新相关 Object 属性（仍走 Action / Edits）；  
   - **必须**可生成 `Insight` Object（或行业等价类型），并 **Link** 到相关 Object；  
   - Lineage 记录：Trace → Draft → Insight/Action。  
3. **禁止** LLM 直写 Insight（HR-01）。

**技术落点：** T07（管线触发/门控）· T06（Insight Meta + Link）· UI：`aip-draft-inbox` · `aip-decision-lineage`。

**验收：** 一次批准可复盘「结论 → Insight → 被引用 Object」；驳回不污染生产。

---

### 4.2 P1 · 图谱健康度（L2 运维）

**问题：** L1 `health.html` 管连通/新鲜度/Schema；不覆盖图结构与语义冲突。

**扫描项（最低集）：**

| ID | 问题 | 说明 |
| --- | --- | --- |
| GH-01 | 悬空链接 | Link 指向不存在 Object |
| GH-02 | 属性冲突 | 多源同 Object 属性不一致（Merge 策略未收敛） |
| GH-03 | 孤立对象 | 长期无 Query/Action/Logic 访问（知识僵尸） |
| GH-04 | 规则冲突 | Function 结果与 Action Criteria/预期不符 |

**落点：** Ontology Manager · UI 新页 `ontology-graph-health.html` · 链自 Discover；与 L1 health **互链、分责**。

**验收：** 四类问题可列表/计数；悬空 Link 可一键进入修复或开 Draft。

---

### 4.3 P2 · 生命周期 / 遗忘（防膨胀）

**问题：** Iceberg 时间旅行 ≠ 无限保留所有热路径明细。

**策略（默认建议，可配置）：**

| 对象 | 策略 |
| --- | --- |
| 临时 `Insight` | 90 天无引用 → **归档**（可回放，非静默物理删） |
| 高频时序 Property（如 `real_time_status`） | 明细保留近 N 天；更早聚合进 `historical_stats` |
| 核心业务 Object | 禁止自动物理删；仅软删/归档策略 |

冷热识别可借 Right Engine（PPR/ANN）作**辅助信号**；淘汰决策须可审计、可审批。落地排期：规模痛点出现后，不阻塞 M1–M3。

**UI：** 图谱健康页「归档候选」区 + Object Overview 生命周期徽标（可后置）。

---

### 4.4 P0 · AOS Constitution（可执行 OKF）

**问题：** OKF 易被理解为静态列映射；企业需要版本化、可 Lint、随 Apollo 发布的「宪法」。

**三类条款（写入 Bundle，Lint 强制）：**

| 类 | 示例 | 失败行为 |
| --- | --- | --- |
| **语义契约** | `Order.total_amount == sum(Item.price * Item.quantity)` | Lint 红 / 不可 Publish |
| **推理边界** | `RiskScore` 仅允许 Function-X，输入须来自 Dataset-Y | 运行时拒绝越界调用 |
| **伦理护栏** | 无 `Human-Approval` Action 不得改 `FinancialRecord` | Action Runtime 硬拦 |

**格式演进（兼容现 Bundle）：**

```text
okf-bundle-{name}-{semver}.tar.gz
├── manifest.json
├── ontology/
├── mappings/
├── constitution/          # 新增：语义 · 推理 · 伦理条款 JSON
│   ├── semantic.json
│   ├── reasoning.json
│   └── ethics.json
├── wiki-templates/
└── README.md
```

Git 管理 · Apollo Asset 同绑 Channel · Lint 失败不可 Publish（与现军规一致）。

**UI：** `funnel.html` / OKF 增加 Constitution 面板与 Lint 徽章。

---

## 5. 文档回写清单

| 文档 | 动作 |
| --- | --- |
| 本篇 25 | 真源 |
| T06 | § 图谱健康 · TTL · Constitution · Insight Meta |
| T07 | § Insight Backfill Pipeline |
| 20 | §5.3 页映射 · 演进指针 |
| 00 索引 | 挂 25 · html v1.6.1 |
| 一致性自检 | 增补本轮吸收项 |
| 06 / 06a | 产品能力 + WF-OM-09 |
| 07 / 07a | Backfill 闭环 + Draft/Lineage 线框注记 |
| foundry/html | 见 §7 |

---

## 6. 与 T-EVO 排期建议

| 里程碑 | 吸收项 |
| --- | --- |
| 方案即刻 | 25 + 产品/技术/html 蓝图 |
| M2（Ontology） | Constitution Lint 子集 · 图谱健康只读扫描 |
| M3（AIP） | Insight Backfill + Draft 类型 |
| 后置 / 规模痛点 | TTL 归档作业 · 冷热淘汰 |

---

## 7. html 蓝图结论：**要动（最小）**

| 动作 | 文件 | 说明 |
| --- | --- | --- |
| ➕ 补页 | `ontology-graph-health.html` | 图谱健康度仪表盘（GH-01～04） |
| 🔧 改页 | `aip-draft-inbox.html` | 增加 Insight Backfill 待审样例 |
| 🔧 改页 | `aip-decision-lineage.html` | 链末增加「回填 → Insight」节点 |
| 🔧 改页 | `funnel.html` | Constitution 三类条款 + Lint |
| 🔧 改页 | `health.html` | 标明 L1 职责 · 链到图谱健康 |
| 📄 | `demo.js` / `index.html` / README / 任务清单 | 导航 · 版本 **v1.6.1** |

**不新开：** 独立「遗忘引擎」页（合入图谱健康「归档候选」即可）。

---

## 8. 验收（方案层）

| # | 标准 |
| --- | --- |
| S1 | 产品/技术文明确区分 Funnel 水合 vs Insight Backfill |
| S2 | L1 数据健康 vs L2 图谱健康分责清晰 |
| S3 | Constitution 进入 OKF Bundle 路径，非游离 MD |
| S4 | html v1.6.1 可演示四条启示的最小路径 |
| S5 | HR-01/Draft/Apollo 同绑未被削弱 |

---

## 9. 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-07-17 | 首版：四条演进 · 文档/html 回写清单 |

---

*25 v1.0 · docs/palantier/20_tech*

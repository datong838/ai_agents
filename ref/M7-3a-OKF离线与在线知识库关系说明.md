# M7-3a · OKF 离线与在线知识库关系说明

> **版本**：v1.1 · 2026-07-11  
> **状态**：现状说明 · **Compile 未接入** · 已补充 Karpathy 四操作与 LLM 自维护 OKF 沟通定稿  
> **v1.1 变更**：新增 §7「LLM 自维护 OKF · 四操作」、链接抓取 Ingest、金句与双模 Query 对照  
> **关联**：[M7-3 WorkBuddy 方案](M7-3-跨境电商AI-WorkBuddy-知识网与Claude范式方案.md) · [knowledge/schema/OKF_ECOM.md](../../knowledge/schema/OKF_ECOM.md) · [Karpathy LLM Wiki](https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw/) · [knowledge/README.md](../../knowledge/README.md)

---

## 1. 文档目的

回答工程与产品问题（2026-07-11 讨论定稿）：

1. 仓库新增的 `knowledge/`、`third_party/okf/` 与 `ditingclient`、`salesagent` 是什么关系？  
2. OKF 从功能上是否可用？磁盘文档与现有在线知识库是否已建立 **离线 + 在线** 互动？  
3. **如何让 LLM 按 OKF 自学习**——从本地文档、从链接抓取，执行 Ingest / Query / Lint / 输出反写四操作？与 RAG、与 Layer 3 PPR 如何分工？

---

## 2. 新增目录与 client / salesagent 的关系

### 2.1 仓库布局（平级）

```text
wchat/
├── ditingclient/      # 客户端（Electron · IPC 调 API）
├── salesagent/        # 服务端（API · 知识网 · PPR · Skills）
├── shared/            # 双端共享配置
├── docs/              # 方案文档
├── knowledge/         # ★ 新增 · Layer 1+2 知识资产（git 管理）
└── third_party/okf/   # ★ 新增 · OKF v0.1 规范本地快照
```

### 2.2 结论表

| 维度 | 现状 |
|------|------|
| **是否独立进程** | 是——`knowledge/` 没有自己的服务；client / salesagent **当前不读取**该目录 |
| **是否独立 git 模块** | 否——与代码同仓，随 wchat 一起版本管理 |
| **运行时数据位置** | 仍在仓库外 `SALESAGENT_DATA_ROOT`（如 `C:/work/salesagent/data`） |
| **代码引用** | 截至 v1.0：**salesagent / ditingclient 零引用** `knowledge/bundles`、`OKF_ECOM` |

### 2.3 产品定位（设计意图 vs 当前实现）

| | 说明 |
|--|------|
| **设计意图** | `knowledge/` 是 salesagent 知识网的 **Layer 1+2 源码仓**（OKF Bundle）；Compile 后写入 Layer 3；client 仍只调 API |
| **当前实现** | **仅规范 + 样例 Bundle**；与在线知识库 **未打通** |
| **一句话** | 目录平级 ≠ 功能已集成；是「离线知识源码层」的占位，不是第三个应用 |

---

## 3. OKF 功能可用性

### 3.1 现在能用什么

| 能力 | 状态 |
|------|------|
| 按 OKF 格式手写 / Agent 维护 Markdown Concept | ✅ 可用（`knowledge/bundles/beauty/`） |
| 本地规范：[OKF_ECOM.md](../../knowledge/schema/OKF_ECOM.md) + [third_party/okf/SPEC.md](../../third_party/okf/SPEC.md) | ✅ 可用 |
| git diff / PR 审阅知识变更 | ✅ 可用 |
| 在线图谱 / 客服 / 写作 **自动读 Bundle** | ❌ 未接 |
| **Compile**：Bundle → `knowledge_nodes` / `knowledge_edges` | ❌ 未建（无 `okf_compile.py`） |
| 在线检索 **一跳到** 离线 Concept 文件 | ❌ 未建 |
| 离线 Ingest / 改文档 **自动反馈** 在线 | ❌ 未建 |

**结论**：OKF 作为 **Layer 2 磁盘文档标准** 已可用；作为 **与在线知识库联动的系统**，尚未建立。

---

## 4. 离线 + 在线：设计 vs 现状

### 4.1 三层与数据位置

```text
                    ┌─────────────────────────────────────┐
  离线（仓库内）      │  knowledge/raw/          Layer 1     │
                    │  knowledge/bundles/      Layer 2 OKF │
                    └──────────────┬──────────────────────┘
                                   │
                          Compile ↑ ↓ 回写（★ 未实现）
                          diting.graph_node_id / compile_status
                                   │
                    ┌──────────────┴──────────────────────┐
  在线（data_root）  │  Chroma · SQLite knowledge_*         │
                    │  PPR 检索 · 图谱 Tab · Skills          │  Layer 3
                    └─────────────────────────────────────┘
```

| 层 | 路径 | Query 模式 |
|----|------|------------|
| L1 | `knowledge/raw/{category}/` | 不直接 Query；Ingest 输入 |
| L2 | `knowledge/bundles/{category}/` | 审计 / 开发：**读 Markdown**（index → Concept） |
| L3 | `{SALESAGENT_DATA_ROOT}/{category}/` | 生产：**PPR 子图**（WorkBuddy Skills） |

### 4.2 目标双向关系（规范已写，工程未接）

| 方向 | 目标行为 | 依赖（未做） |
|------|----------|--------------|
| **在线 → 离线** | PPR 命中节点 → 展示「源码 Concept」路径 / 可打开 Markdown | Compile 回填 `diting.graph_node_id`；API/UI 返回 `okf_concept_path` |
| **离线 → 在线** | Ingest / 改 Bundle → Compile → 更新 nodes/edges/Chroma | `okf_compile.py`；`compile_status: pending → compiled` |
| **Query 回写** | 高价值回答 → Layer 2 `Synthesis` Concept → 再 Compile | Query Agent + Compile 触发 |

### 4.3 当前状态一句话

**离线草案 + 在线照旧跑**；中间缺 **Compile 管道** 与 **双向索引字段**（`graph_node_id`、`resource`、`compile_status` 已在 [OKF_ECOM.md](../../knowledge/schema/OKF_ECOM.md) 定义，代码未接）。

---

## 5. 与现有在线能力的对照（部分同构，未统一）

在线侧已有「磁盘 Markdown ↔ 图」片段，**不是 OKF Bundle**：

| 现有能力 | 路径 / 模块 | 与 OKF 关系 |
|----------|-------------|-------------|
| 文库文章 | `data_root/articles/{category}/` | 类似 Layer 2，无 OKF frontmatter / `index.md` |
| 素材包 | M6-3 `material_bundle` | 子图 → 文章；未 Compile 到 OKF |
| 图谱 / PPR | `knowledge_search.py` 等 | 纯 Layer 3；不指回 `knowledge/bundles/` |
| 技能策略 | `salesagent/config/agent_skills` | 类似 Playbook；未纳入 Bundle 树 |

**含义**：M6-3 文库、图谱 Tab 已是「在线知识」；OKF 是更规范的 **离线源码层**——二者尚未通过 Compile + 互链接统一。

---

## 6. 护城河在离在线分工中的位置

（对齐 M7-3 §6.0）

| 机制 | 主要所在层 |
|------|------------|
| 超越 RAG、Wiki 复利 | L2 Ingest / Query 回写 / Lint |
| OKF 标准、git 审计 | L2 |
| 生产 Query、可解释传导 | L3 PPR + meta-path |
| 边权进化（突触可塑性） | L3 `knowledge_edges.props_json` |
| Skill 契约 | L3 → `agent_skills` / Playbook |
| MCP 行动 | L3 输出 → 平台 API |

**Markdown = 源码与审计；PPR 子图 = 生产默认。** 两层互补，非二选一。

---

## 7. LLM 自维护 OKF：四操作（Karpathy × 谛听）

> 思想来源：[Karpathy · LLM Wiki](https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw/) · 格式约束：[OKF v0.1](../../third_party/okf/SPEC.md) · 电商扩展：[OKF_ECOM.md](../../knowledge/schema/OKF_ECOM.md)  
> 链接 enrich 可参考 [Google OKF reference agent Web pass](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf)（种子 URL + 域白名单 + 页数上限）

### 7.1 核心思想：Wiki 是代码库，LLM 是程序员

| Karpathy 原话 | 中文含义 | 谛听落地 |
|---------------|----------|----------|
| *"The LLM writes and maintains all of it."* | 人不写 Wiki 正文，LLM 维护交叉引用与多页更新 | Ingest / Lint Agent + `schema/OKF_ECOM.md` 纪律 |
| *"Obsidian is the IDE; the LLM is the programmer; the wiki is the codebase."* | 人用 Obsidian/图谱 **读**；LLM **写** Bundle | 图谱 Tab / git diff = IDE；`knowledge/bundles/` = 代码库 |
| *"RAG rediscovers knowledge from scratch on every question."* | RAG 每次从 chunk **重新发现**，无复利 | L2 Wiki **编译一次**；L3 PPR **传导**；Query **反写** 滚雪球 |

**PPT 可引金句（中英）：**

> **"RAG 的问题是 AI 每次都在从零开始重新发现知识。"**  
> *"The problem with RAG is that the AI rediscovers knowledge from scratch on every question."*

> **"Obsidian 是 IDE，LLM 是程序员，Wiki 是代码库。"**  
> *"Obsidian is the IDE, the LLM is the programmer, the wiki is the codebase."*

### 7.2 两个「Compile」不要混

| 名称 | 层 | 做什么 | Karpathy / 我们 |
|------|-----|--------|-----------------|
| **Wiki Compile（汇入编译）** | L2 | 一条 raw/URL → LLM 更新 **10–15 个** OKF Concept 页 | Karpathy **Ingest**；「**编译，不是索引**」|
| **Graph Compile（图编译）** | L2→L3 | OKF Bundle → `knowledge_nodes/edges` + Chroma | 谛听 `okf_compile.py`（未建） |

```text
raw / URL ──Ingest(Wiki Compile)──► OKF Bundle（10+ 页.touch）
                                        │
                                        └──Graph Compile──► 知识网 + PPR
```

**索引**只存片段等检索；**编译**把理解写进持久结构（Concept 页 + 链接 + 摘要）。这是我们超越普通 RAG 的第一步。

### 7.3 操作一 · Ingest（汇入）

**输入源（三类）**：

| 源 | 路径 / 方式 | 说明 |
|----|-------------|------|
| **本地文档** | `knowledge/raw/{category}/` | HTML/PDF/Word/邮件/平台导出；**只读不改** |
| **链接抓取** | Ingest Agent `fetch_url` | 种子 URL 列表（平台政策、品牌官网、竞品页）；**域白名单 + `--max-pages` 上限** |
| **在线回灌** | 成交/客服日志（远期） | 结构化事件触发再 Ingest，写 `Synthesis` / 更新 Concept |

**标准流程**（单条来源）：

```text
1. 新资料进入 raw/ 或 fetch 完成 → 快照进 raw/（可选）
2. LLM 读：新源 + 现有 index.md + 相关 Concept 页
3. 蒸馏：去噪 · 实体抽取 · 小语种对齐 · 标注与旧页矛盾
4. 写/更新：
   · 1 篇摘要/商品/Reference 母页
   · 触达 10–15 个 concepts/products/sections（bookkeeping）
   · 更新各级 index.md
5. 追加 log.md（ISO 日期 + Ingest 条目）
6. frontmatter：diting.compile_status = pending
7. （可选）触发 Graph Compile → Layer 3
```

**链接抓取纪律**（对齐 OKF Web pass）：

- 种子文件：`knowledge/raw/{category}/seeds.txt` 或 Ingest 参数  
- 同域/白名单：`shopee.com`、`seller.*.com` 等可配置  
- 产出：`references/{slug}.md`（`type: Reference`）或 enrich 已有 Concept  
- 禁止：无上限爬站；raw 不可被 LLM 改写  

**自学习含义（L2）**：不是微调模型权重，而是 **LLM 每次 Ingest 把理解写进可 diff 的 Wiki**，交叉引用与矛盾标记累积下来，后续 Query 不再从零拼凑。

### 7.4 操作二 · Query（查询）

**Karpathy 路线（Layer 2 · 审计 / Agent 起草）**：

```text
1. 读 bundles/{category}/index.md（渐进披露，不必加载全库）
2. 按链接 + 反向引用（Lint 可预计算 cited-by）打开相关 Concept
3. LLM 综合 Markdown 作答，附 Citations
4. 规模参考：Karpathy 亲测 ~100 篇 / ~40 万字，index 导航够用，无需 embedding 基础设施
```

**谛听增强（Layer 3 · 生产 / WorkBuddy）**：

| 场景 | 用什么 | 不用什么 |
|------|--------|----------|
| 运营审阅、Agent 维护 Bundle | index + Markdown | 非必须 PPR |
| 导购/文案/选品 **在线** | **PPR 子图** + Skill | 非裸 RAG chunk；非每次全库 Markdown |

**双模 Query 一句话**：  
**L2 = Karpathy 式导航读 Wiki；L3 = 谛听式 PPR 传导。** 二者通过 `okf_concept_path` ↔ `graph_node_id` 互指（Graph Compile 后）。

### 7.5 操作三 · Lint（体检）

定期（建议 **周批** + 大批量 Ingest 后）由 LLM **扫全库**：

| 检查项 | 动作 |
|--------|------|
| **矛盾** | 页 A 与页 B 声明冲突 → 标注；以新源 / 成交数据为准 |
| **孤立页** | 无入链 orphan → 补交叉引用或合并 |
| **缺失交叉引用** | 正文多次提及的概念无独立 Concept 页 → 补建 |
| **断链** | 报告待补；OKF 允许 broken link |
| **stale** | 下架 SKU、过期政策 → `compile_status: stale` |
| **数据缺口** | 建议新 seeds / 新 raw 来源 |

产出：Lint 报告（可写 `log.md` 或 `lint/{date}.md`）；严重项触发人工 PR 或自动 Ingest 修复任务。

### 7.6 操作四 · 输出反写（Query → Wiki 滚雪球）

**原则**：高价值问答 **不应只留在 chat history**。

| 反写类型 | OKF 落地 | 后续 |
|----------|----------|------|
| 对比表、选品结论 | 新建 `type: Synthesis` Concept | Graph Compile |
| Listing A/B 变体 | 更新 `products/{sku}.md` 或 variants 节 | 文案 Skill 可读 |
| 导购话术采纳版 | 更新 Playbook 或 product 页「话术要点」 | cs_dialogue |
| 失败案例 | 标注概念页「慎用」+ 边权弱化（L3） | 突触可塑性 |

```text
用户/Agent Query → 答案（L2 和/或 L3）
       ↓
值得保留？ ──是──► 写入 Bundle 新页/更新页 → log.md → pending → Graph Compile
       ↓
      否 → 仅会话，不进 Wiki
```

这是 Karpathy **「explorations compound」**：探索结果与 Ingest 源一样，成为持久资产。

### 7.7 四操作与离在线闭环

```text
        ┌──────── Ingest ────────┐
        │  raw + URL → Bundle    │
        └───────────┬────────────┘
                    ▼
              OKF Bundle (L2)
                    │
     ┌──────────────┼──────────────┐
     ▼              ▼              ▼
  Query(L2)      Lint          输出反写
  index导航      全库体检       → 新/改 Concept
     │              │              │
     └──────────────┴──────────────┘
                    │
                    ▼ Graph Compile（未建）
              知识网 + PPR (L3)
                    │
                    ▼
            WorkBuddy · Skill · MCP
                    │
                    └──反馈──► 边权进化 + 可选再 Ingest
```

| 操作 | 当前状态 |
|------|----------|
| Ingest（含链接抓取） | 📋 规范在 OKF_ECOM；🔜 Agent/脚本未建 |
| Query L2（index 导航） | ✅ 可人工/Agent 读 Bundle 试跑 |
| Query L3（PPR） | ✅ 现有 salesagent 已运行 |
| Lint | 📋 规范已写；🔜 未自动化 |
| 输出反写 | 📋 与 M6-3 文库逻辑同构；🔜 未统一到 OKF |
| Graph Compile | ❌ 未建 |

### 7.8 Agent 纪律摘要（写入 `AGENTS.md` / Ingest Prompt）

```text
你是 OKF_ECOM Bundle 维护者（LLM = 程序员，Wiki = 代码库）。

· Ingest：raw/URL 只读；单源必须 touch 10–15 页；更新 index + log；compile_status=pending。
· Query(L2)：先 index.md，再 Concept；不编造无 source 的 resource。
· Query 生产：交给 PPR 子图，你负责 Layer 2 草稿与反写。
· Lint：报矛盾、孤儿、缺链、缺 Concept 页。
· 输出反写：对比表/选品/Listing 变体 → Synthesis 或更新 Concept。
· 链接抓取：遵守 seeds + 域白名单 + 页数上限；外链进 references/。
```

---

## 8. 建立「离线↔在线」最小闭环（建议 · 未排期）

**原则**：可先只动 **salesagent**，**不必改 ditingclient**（API 扩展即可）。

| 步骤 | 内容 | 产出 |
|------|------|------|
| **① Compile** | `scripts/okf_compile.py`（或 `salesagent/scripts/`） | 读 `bundles/beauty/*.md` → 写 nodes/edges + Chroma |
| **② 回填** | 更新 Concept frontmatter | `diting.graph_node_id`、`compile_status: compiled` |
| **③ 检索扩展** | `knowledge_search` / 子图 API | 节点附 `okf_concept_path`（如 `bundles/beauty/products/BEAUTY-SUN-001.md`） |
| **④ 触发** | Bundle 变更 | `compile_status: pending` → 手动或定时 Compile |

闭环验收：

- 在线：问功效 → PPR 子图 → 能打开对应 OKF Concept  
- 离线：Ingest 新 SKU → Compile → 图谱 Tab / 客服可检索  

后续可再写专篇 **M7-3b-OKF-Compile接入方案.md**（对接 `document_link_ingest`、现有入库 API）。

---

## 9. FAQ

**Q：`knowledge/` 要不要挪进 `salesagent/`？**  
A：不必。放仓库根与 `docs/` 并列，表示 **资产与代码分离**；Compile 脚本读相对路径即可。运行时数据仍在 `data_root`。

**Q：会不会影响现有功能？**  
A：在 Compile 接入前 **零影响**；仅新增目录与文档。见 M7-3 §6.8。

**Q：和 Google OKF 仓库要 clone 吗？**  
A：不必整库 clone。已 vendor `third_party/okf/SPEC.md`；Ingest 自研，可借鉴 Web pass **思想**（种子 URL、域限制），不对接 `--source bq`。

**Q：Query 不用 RAG，生产够用吗？**  
A：**Layer 2** 在 ~100 篇规模可 index 导航（Karpathy 验证）。**Layer 3 生产**仍用 PPR 子图 + Skill，不靠 chunk RAG——二者分工见 §7.4。

**Q：「自学习」是微调模型吗？**  
A：**不是。** L2 = LLM 维护 Wiki 结构与内容复利；L3 = 边权突触可塑性 + Query 反写。模型权重可不变。

---

## 10. 相关路径索引

| 路径 | 说明 |
|------|------|
| [knowledge/README.md](../../knowledge/README.md) | 知识资产总览 |
| [knowledge/schema/OKF_ECOM.md](../../knowledge/schema/OKF_ECOM.md) | 电商 OKF 契约 |
| [knowledge/bundles/beauty/](../../knowledge/bundles/beauty/) | 试点 Bundle |
| [third_party/okf/SPEC.md](../../third_party/okf/SPEC.md) | OKF v0.1 上游规范 |
| [Karpathy LLM Wiki](https://gist.githubusercontent.com/karpathy/442a6bf555914893e9891c11519de94f/raw/) | §7 四操作 · 金句 |
| [Google OKF Web pass](https://github.com/GoogleCloudPlatform/knowledge-catalog/tree/main/okf) | §7.3 链接抓取参考 |
| [M7-3 方案](M7-3-跨境电商AI-WorkBuddy-知识网与Claude范式方案.md) | WorkBuddy 总方案 §6 |

---

*v1.1 · 2026-07-11 · OKF 离线与在线知识库关系说明*

# T06 · Ontology / Action·Function 详细技术方案

> **版本**：v1.0.2 · 2026-07-17  
> **状态**：✅ **方案完成**（含 [25](25-LLM-Wiki启示与L2演进补丁.md) L2 演进补丁）  
> **对齐产品**：[06](../06-语义本体Ontology-Mapping产品方案.md) · [06a](../06a-语义本体Ontology-Mapping产品设计线框图.md) · [06b](../06b-Action与Function产品设计.md) · [03 §3.2 Wiki](../03-对标Palantir-AOS-PRD框架.md) · [20 §6.6](20-AOS整体技术方案.md) · [25](25-LLM-Wiki启示与L2演进补丁.md) · [T-API](T-API-aos-api稳定契约.md) · [T-CROSS](T-CROSS-横切能力详细技术方案.md) · [21](21-AOS开源选型与功能清单.md) · [23 军规](23-AOS开源引用与交付军规.md)（Outline/Wiki.js 只参考）

---

## 使用的 Rules

产品对齐 · UI 引用 ontology* · HR-01/02 · ACT/FUNC 护栏必写 · 插件化（Action 模板 / 解析可扩展）

---

## 1. 范围

| 做 | 不做 |
| --- | --- |
| Object/Link/Property Meta · Funnel · Branch | 把图库 UI 当 OMA |
| Action 壳 + Criteria + Side Effects · Function 核 | LLM 直写 Ontology |
| Wiki 双向绑定（方向 A/B） | 静态 Document 挂载冒充 Wiki |
| 解法 A 为主；B/C 红线 | 解法 C 作高频筛选项 |

---

## 2. 架构

```text
ontology-service
├── Meta Store          # ObjectType / LinkType / Property / ActionType / FunctionType
├── Funnel Worker       # Changelog → Merge → Index → Hydration
├── Graph / Object Store# 实例读写（实现可换）
├── Wiki Service        # 结构化字段 + 版本
├── Action Runtime      # Criteria · 幂等 · Draft · Webhook
└── Function Runtime    # 沙箱 · 超时/内存
```

工程落点：`services/ontology/` · `services/action-runtime/`（可同仓多模块）。

---

## 3. Meta 与 Funnel

### 3.1 ObjectType 发布门禁（HR-02）

- 每个 ObjectType **唯一** Backing Dataset（或官方等价）  
- 发布前校验；失败不可上线  

### 3.2 Funnel 四阶段

对齐产品 06 §5 · UI [`ontology-funnel.html`](../foundry/html/ontology-funnel.html)

| 阶段 | 技术要点 |
| --- | --- |
| Changelog | L1 Write-back / Edits 入队 |
| Merge | 主键合并 · 冲突策略 |
| Index | 检索/图索引 |
| Hydration | 供 Workshop / AIP 读取 |

编排参考：`B5_Workflow/temporal`（长事务/重试）或轻量队列；**不**把 Temporal UI 当产品。

> **口径钉死（25）：** Funnel = **数据水合**（L1→Object）。AIP 高价值结论沉淀为 `Insight` Object 属 **Insight Backfill**（T07），**不是** Funnel 的同义词。

### 3.3 多源解法红线（产品 06 §6）

| 解法 | 规则 | 工程 |
| --- | --- | --- |
| A | Join 预计算进 Curated | Pipeline（T05）产出 |
| B | Link 跨域 | **Link 边 >100 万** 须 MDO/预聚合，否则禁发生产 · UI [`ontology-link.html`](../foundry/html/ontology-link.html) |
| C | 派生属性 | **禁止**作高频筛选/排序主字段 · 同页禁用态 |

---

## 4. Action Runtime（06b）

### 4.0 自有所需功能（先于开源）

| 功能项 | 我们要什么 | 验收 |
| --- | --- | --- |
| Action 壳 | Criteria · Side Effects · 幂等 · 软删除 · Draft 隔离 | ACT-01～10 |
| 写回路径 | 只经 Edits / Action；禁 LLM/Wiki 直写 | HR-01 |
| Webhook | 声明式副作用 · ×3 重试 · DLQ | ACT-10 |
| HITL / Draft | 提案进审批台，不污染生产 Dataset | Draft UI |
| 编排能力 | 长事务重试/超时（实现可借工作流引擎） | 产品壳自有 |

### 4.1 条款落地

| ID | 规则 | 实现要点 |
| --- | --- | --- |
| ACT-01 | 单一职责 | ActionType 审计 |
| ACT-02 | Submission Criteria | 服务端强制；UI 仅提示 |
| ACT-03 | 写回 L1/Edits | 禁直写湖仓文件 |
| ACT-04 | Side Effects 声明 | Webhook/通知面板 |
| ACT-05 | 乐观 UI | Workshop 先反馈 |
| ACT-06 | 可调 Function | 壳核分离 |
| ACT-07 | **幂等** | `idempotencyKey` 去重表 |
| ACT-08 | **软删除** | `is_deleted` / tombstone |
| ACT-09 | **Draft Dataset 隔离** | 提案不进生产主 Dataset |
| ACT-10 | Webhook 重试 | ×3 间隔 1s → **DLQ** |

**UI 蓝图：** [`ontology-action.html`](../foundry/html/ontology-action.html) · 审批台见 T07 `aip-draft-inbox.html`

### 4.2 开源参考

| 仓 | 抄 | 不抄 | 选型 |
| --- | --- | --- | --- |
| Temporal `B5_Workflow/temporal` | 工作流重试 / 超时模式 | 工作流产品壳 | **建议**：Action 异步副作用 / Funnel |
| Conductor `B5_Workflow/conductor` | 任务编排 DSL 思路 | Netflix 运维语义 | 备选 |

---

## 5. Function Runtime（06b）

### 5.0 自有所需功能（先于开源）

| 功能项 | 我们要什么 | 验收 |
| --- | --- | --- |
| Function 核 | 类型绑定 Ontology；默认只读 | FUNC-01/02 |
| 资源上限 | ≤60s · ≤2GB 强杀 | FUNC-03 |
| 隔离 | Worker 级故障隔离；禁裸 HTTP 外写 | FUNC-06 · 外写走 Action |
| 组合 | 注册表复用 | FUNC-05 |

| ID | 规则 | 实现 |
| --- | --- | --- |
| FUNC-01 | 类型绑定 Ontology | 编译期/发布校验 |
| FUNC-02 | 默认只读 Ontology | 写必须经 Action/Edits |
| FUNC-03 | **≤60s · ≤2GB** | Runtime 强杀 · 指标告警 |
| FUNC-04 | 无 Submission UI | 仅被 Action/Logic/Workshop 调 |
| FUNC-05 | 可组合 | 注册表复用 |
| FUNC-06 | 资源隔离 | Worker 级故障隔离 |

**UI 蓝图：** [`ontology-function.html`](../foundry/html/ontology-function.html)

TS Function **禁止裸 HTTP 写外部**；外部写走 Action Webhook（官方边界对齐 06b）。

---

## 6. Wiki 双向（03 WIKI-001～004）

### 6.0 自有所需功能（先于开源）

| 功能项 | 我们要什么 | 验收 |
| --- | --- | --- |
| 方向 A | Object→Wiki 块刷新 + 版本 | 变更可追溯 |
| 方向 B | Wiki→**Action 提议**写回；禁引擎直写 | HR-01 |
| 冲突 | LWW + 审计；关键字段可仲裁 | 版本号 |
| Agent | Wiki 字段 **只读** Tool | 无写 API |
| 数据模型 | 字段映射与 Object **同源**（自研） | 非静态挂载文档 |

| 方向 | 行为 | 工程 |
| --- | --- | --- |
| **A 系统→人** | Object 变更 → 映射表刷新 Wiki 块 → 版本 | 订阅 Changelog / Object events |
| **B 人→系统** | Wiki 编辑 → **Action 提议/受控写回** → Object | **禁止** Wiki 引擎直写存储（HR-01） |
| 冲突 | Last-Write-Wins + 审计；关键字段可升仲裁 | 版本号比较 |
| Agent | **只读**结构化字段 | AIP Tool 不提供 Wiki 写 |

**UI 蓝图：** [`ontology-wiki.html`](../foundry/html/ontology-wiki.html)

### 6.1 开源参考（已核对）

| 仓 | 抄 | 不抄 | 选型 |
| --- | --- | --- | --- |
| Outline `B7_Wiki/outline` | 协作编辑 / 权限 / 版本思路 | 直接当 Object Wiki 数据模型 | **建议**借 UX |
| Wiki.js `B7_Wiki/wiki` | 文档树与权限 | 同上 | 备选（更偏站点 Wiki） |

Wiki **字段映射与 Object 同源** 必须自研；上游只借编辑体验。

---

## 7. Meta / 图存储

### 7.0 自有所需功能（先于开源）

| 功能项 | 我们要什么 | 验收 |
| --- | --- | --- |
| Meta Store | ObjectType/LinkType/Property/Action/Function 元数据 | 发布门禁 HR-02 |
| Funnel | Changelog→Merge→Index→Hydration | 四阶段可观测 |
| Graph 实例 | Object/Link 读写；API 不绑具体图库方言 | Adapter 可换引擎 |
| OKF Bundle | tar.gz + manifest；与 Apollo 资产同族 | Lint 失败不可 Publish |
| 检索附属（可选） | 全文/过滤加速 | 不替代 Graph 主存 |

### 7.0.1 开源参考

| 仓 | 路径 | 用途 | 选型 |
| --- | --- | --- | --- |
| LinkML | `B4_Metadata/linkml` | Schema DSL · 校验 · 代码生成思路 | Meta DSL 参考 |
| **Apache AGE** | `B1_GraphStore/age` | PG 扩展属性图 | **v1 默认** |
| Nebula | `B1_GraphStore/nebula` | 分布式图 | 规模备选 |
| Memgraph | `B1_GraphStore/memgraph` | 内存图 / 低延迟 | 备选评测 |

### 7.1 图引擎已决

| 项 | 结论 |
| --- | --- |
| v1 默认 | **PostgreSQL + Apache AGE** |
| 切换条件 | 边规模/查询延迟超阈值 → 评估 Nebula；经 Adapter，禁止业务代码直绑 AGE Cypher |
| Meta 存储 | PostgreSQL（与 AGE 同实例或同集群） |
| 对象文档/检索附属 | 可按需加 OpenSearch 等，不替代 Graph 主存 |

**不抄：** 各图库自带 Console 当 OMA。

### 7.2 OKF Bundle 格式（已决 · Constitution 升级）

```text
okf-bundle-{name}-{semver}.tar.gz
├── manifest.json      # id, semver, aosChannelRange, checksums
├── ontology/          # ObjectType/LinkType/Action 片段 JSON（含可选 Insight）
├── mappings/          # 列→Property 映射 + Lint 规则
├── constitution/      # AOS Constitution（25）：可执行契约
│   ├── semantic.json    # 语义不变量
│   ├── reasoning.json   # 推理边界（允许的 Function/Dataset）
│   └── ethics.json      # 伦理护栏（须 Human-Approval 的类型）
├── wiki-templates/    # 可选
└── README.md
```

- 与 Apollo **Asset Bundle** 同族：可被 `apollo-assets` 收录并 Channel 同绑（T09）  
- Lint 失败不可 Publish（产品 OKF）；**Constitution 条款纳入 Lint**  
- 仓储：Git 管理；**manifest 为真源**；随 Channel 发布保证全环境一致  
- **禁止**另起游离 Markdown「宪法」绕过 Bundle

**UI：** Discover [`ontology.html`](../foundry/html/ontology.html) · Object [`ontology-object.html`](../foundry/html/ontology-object.html) · Property/Link 对应页 · Branch [`ontology-branches.html`](../foundry/html/ontology-branches.html) · OKF/Constitution [`funnel.html`](../foundry/html/funnel.html) · 图谱健康 [`ontology-graph-health.html`](../foundry/html/ontology-graph-health.html)

### 7.3 Insight ObjectType（与 T07 Backfill 对齐）

| 项 | 规则 |
| --- | --- |
| 定位 | 高价值推理结论的可复用沉淀；**非** L1 行镜像 |
| 写入 | 仅经 Draft `InsightBackfill` → Action；禁 LLM 直写（HR-01） |
| Link | 须链接相关业务 Object，便于举一反三 |
| 生命周期 | 默认可归档（见 §7.5）；核心业务 Object 不适用自动物理删 |

### 7.4 图谱健康度（L2 运维 · P1）

与 L1 [`health.html`](../foundry/html/health.html)（连通/新鲜度/Schema）**分责**。扫描最低集：

| ID | 问题 |
| --- | --- |
| GH-01 | 悬空 Link |
| GH-02 | 多源属性冲突未收敛 |
| GH-03 | 长期无访问的孤立 Object（知识僵尸） |
| GH-04 | Function 结果与 Action 预期/Criteria 冲突 |

**UI：** [`ontology-graph-health.html`](../foundry/html/ontology-graph-health.html)

### 7.5 生命周期 / TTL（P2 · 防膨胀）

| 策略 | 说明 |
| --- | --- |
| Insight | 建议 90 天无引用 → **归档**（可回放，非静默物理删） |
| 高频时序 Property | 明细保留近 N 天；更早聚合进历史统计 Property |
| 核心业务 Object | 禁止自动物理删；软删 / 审批归档 |
| 冷热信号 | Right Engine 可辅助，淘汰须可审计 |

Iceberg 时间旅行保留合规回放能力；TTL 管的是**热路径噪音与成本**，不是取消谱系。

---

## 8. 授权

见 **[T-CROSS](T-CROSS-横切能力详细技术方案.md)**：OpenFGA + Markings；本层强制 Object/Action 检查点。

---

## 9. API 摘要

完整路径见 [T-API §2.2](T-API-aos-api稳定契约.md)。

---

## 10. 验收

| # | 标准 |
| --- | --- |
| A1 | ObjectType 无唯一 Backing 无法发布 |
| A2 | 双击 Action 只产生一单 |
| A3 | Draft 失败不污染生产 |
| A4 | Wiki 方向 B 必经 Action；Agent 只读 |
| A5 | Link>100万 配置触发阻断；解法 C 字段不可作主筛选 |
| A6 | 默认部署使用 AGE；业务测试不依赖 Nebula |
| A7 | Constitution Lint 失败不可 Publish；Insight 仅经 Draft 写入 |
| A8 | 图谱健康四类问题可扫描（GH-01～04） |

---

## 11. 已决结论（原缺口已关闭）

| ID | 结论 |
| --- | --- |
| T06-G1 | **PG + AGE** 为 v1 默认；Nebula 为规模备选（§7.1） |
| T06-G2 | OKF Bundle = **tar.gz + manifest.json**（§7.2），与 Asset Bundle 同族 |
| T06-G3 | OKF 含 **constitution/**（语义·推理·伦理）；Insight Meta + 图谱健康 + TTL 见 §7.3～7.5 / [25](25-LLM-Wiki启示与L2演进补丁.md) |

---

*T06 v1.0.2 · docs/palantier/20_tech*

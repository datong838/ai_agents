# M3-S2 — 知识库「大类知识图谱」Tab 方案

> **阶段**：MVP M3–M5（知识库 Level 2 可视化）  
> **状态**：**P0 开发中**（forest/subtree API + 客户端 Tab 已落地）  
> **关联 PRD**：§5.7.7 知识库管理 · §5.5.5 知识库地图  
> **前置依赖**：M1.6 知识网（`knowledge_edges` / `knowledge_media_nodes`）、M3-S1（挂接边 `related_product` / `mentions`，可选增强）  
> **复用组件**：`KnowledgeGraphViz.vue`（技能集 · 知识关系图检索）、`GET /api/knowledge/graph/neighbors`

---

## 〇、产品决策（2026-06-28 定稿）

| 议题 | 决策 |
|------|------|
| **Tab 名称** | **「知识图谱」**（原「已入库向量条目」）；切片列表降为折叠区「切片明细」 |
| **未归类节点** | 无 `sub_category` 的 document **先归入「未归类」**；上线后由产品检查再调归类规则 |
| **P0 范围** | **仅展示 beauty**（当前唯一有图数据的大类）；**API/组件按大类通用设计**，其他大类 `edge_count=0` 时 **不展示图谱**（空态提示「该类目暂无知识网数据」） |

---

## 一、背景与问题

### 1.1 现状

知识库页 **「知识图谱」Tab**（原「已入库向量条目」）当前实现为：

- 标题：`419 条 · 类目 beauty`（Chroma 切片计数）
- 正文：按时间排列的 **切片文本列表**（`niushop_product` / `niushop_evaluate` …）

这对运营/业务同学 **过于技术化**：

| 用户关心 | 当前界面给的是 |
|---------|---------------|
| 这个大类里有哪些 **商品/资料树**？ | 散落的 chunk 行 |
| 资料和产品 **怎么关联**？ | 看不出边 |
| 图片/段落 **挂在哪**？ | 需懂 `chunk_id` / `source` |
| 子类（防晒/护肤…）结构 | 只在地图 Tab 有计数，与条目 Tab 脱节 |

### 1.2 已有能力（可复用）

| 能力 | 位置 | 说明 |
|------|------|------|
| **关系图检索** | 技能集 `/skills/knowledge-graph` | 输入问题 → ANN 种子 → **子图** 可视化（12 节点 · 16 边） |
| **图存储** | SQLite `knowledge_edges` | beauty 现约 **973 条边**、**303 媒体节点** |
| **邻域 API** | `GET /api/knowledge/graph/neighbors` | 1-hop 展开（`depth=1`） |
| **地图统计** | `GET /api/knowledge/map-overview` | 大类/子类条数与来源 |

关系图检索是 **「问句驱动的小子图」**；本方案要做的是 **「大类全景 · 可收缩的知识森林」**，二者互补、组件可复用。

---

## 二、目标

### 2.1 产品目标

将 **「已入库向量条目」Tab** 升级为 **「知识图谱」Tab**（切片明细折叠入口见 §5.3）：

1. **按当前地图选中大类**（如 beauty）展示该类目下 **真实知识网**（点 + 边），非单纯向量条数。
2. 默认以 **思维导图式树** 呈现：**子类 → 文档根 → 段落/媒体**，大图 **默认收缩**，点击展开。
3. 跨文档关系（`related_product`、`mentions`，M3-S1 后）以 **虚线/异色边** 展示，可开关。
4. 与 **知识库地图**（§5.5.5）联动：地图选 beauty → 图谱 Tab 即 beauty 森林。

### 2.3 P0 展示范围（定稿）

- **仅 beauty** 在 P0 启用图谱 Tab 内容（现网约 973 边 / 303 媒体节点）。
- 客户端逻辑 **按 `selectedCategory` 通用**；切换至 `ai_agent` / 无图数据大类时：
  - Tab 仍可见，主区展示 **空态**（「该类目暂无知识网，请先同步或上传」）；
  - **不**伪造节点或边。
- 待其他大类入库后 **无需改 Tab 框架**，仅数据到位即自动可展示。

---

### 2.2 非目标（本迭代不做）

- 不做全库力导向大图（数百节点一次性铺开）。
- 不替代 **关系图检索** 的「问句召回 + 种子高亮」场景。
- 不在客户端本地拼假图；**必须读服务端 `knowledge_edges` + Chroma 索引**。
- 不实现图编辑（增删边）；只读浏览。

---

## 三、数据模型与「实际出图」规则

### 3.1 节点类型（与 M1.6 一致）

| `node_type` | 含义 | 典型 `node_id` | 标签来源 |
|-------------|------|----------------|----------|
| `document` | 商品/文章/上传资料根 | `goods_{id}` / `article_{id}` / `upload_{hash}` | 商品名 / 文章标题 |
| `section` | 段落切片 | `niushop_product_{id}_s0` … | 段落摘要前 40 字 |
| `media` | 全局媒体 | `media_{url_hash}` | 图片/视频 + 缩略类型 |
| `evaluate` | 用户评价（可选层） | `niushop_evaluate_*` | 评价摘要 |
| `concept` | 概念节点（M3-S1 后） | `concept_{slug}` | 概念名 |

### 3.2 边类型（按数据实际写入）

| `rel_type` | 方向 | 含义 | beauty 现网量级（约） |
|------------|------|------|----------------------|
| `contains` | document → section/media | 文档包含段落或媒体 | 444 |
| `appears_in` | media → document | 媒体出现于哪些文档 | 342 |
| `references` | section → media | 段落引用媒体 | 187 |
| `related_product` | upload_doc → goods_* | 资料挂接商品（M3-S1） | 0（待 M3-S1） |
| `mentions` | section → concept | 段落提及概念（M3-S1） | 0（待 M3-S1） |

**出图原则**：只画 **库里存在的边**；无 `related_product` 时不画挂接边，避免「空关系误导」。

### 3.3 森林结构（默认收缩层级）

```
beauty（大类根 · 虚拟节点）
├── [子类] 防晒 (43)
│   ├── 📦 goods_25  断黑王钻石光感4件套 …     [▶ 收缩]
│   └── 📦 goods_31  …
├── [子类] 护肤 (116)
│   ├── 📦 goods_12  …
│   │   ├── 📄 段落 s0 …
│   │   ├── 📄 段落 s1 …
│   │   └── 🖼 media_abc…（3）
│   └── 📄 article_7  …
└── [未归类]              ← 定稿：无 sub_category 的 document 先归此类；上线后产品再检归类规则
```

- **L0**：大类（Tab 上下文，不单独画根，用标题区展示）。
- **L1**：**子类**（来自 `map-overview.sub_categories` 或 Chroma `sub_category`；与 §5.5.5 地图一致）。
- **L2**：**document 根**（每个 `goods_*` / `article_*` / `upload_*` 一棵树）。
- **L3+**：**section / media / evaluate**（**默认折叠**在 document 下，点击 ▶ 展开；展开时调 `neighbors` 或一次性拉子树）。

**评价节点**：可作为 document 同级叶子，或挂在对应 `goods_*` 下（通过 `goods_id` 关联，V1 可仅列表不入树）。

---

## 四、交互与视觉（线框意图）

### 4.1 Tab 布局

```
┌─ Tab：知识图谱（原「已入库向量条目」）────────────────────────────────────┐
│  beauty · 四季护肤/美妆    973 边 · 303 媒体 · 71 商品树 · 43 文章树          │
│  [🔍 在图谱内搜索节点…]  来源：[全部|商城|资料|挂接]  [展开全部 L2] [全部收缩] │
├──────────────────────────────────────────────────────────────────────────┤
│  ┌─ 思维导图 / 可收缩树（主区域 70%）──────────┐ ┌─ 节点详情（30%）──────┐ │
│  │ ▼ 防晒 (12 文档)                              │ │ 选中：goods_25      │ │
│  │   ▶ 断黑王钻石光感4件套                       │ │ 来源：商城商品       │ │
│  │   ▶ 蜜丝婷防晒喷雾…                           │ │ 段落 3 · 图片 5      │ │
│  │ ▼ 护肤 (28 文档)                              │ │ [在关系图检索中打开] │ │
│  │   ▼ 栖月汇面膜…                               │ └─────────────────────┘ │
│  │       📄 段落：成分表…                        │                           │
│  │       🖼 图片 ×2                              │                           │
│  └──────────────────────────────────────────────┘                           │
│  图例：━━ contains  ┄┄ appears_in  ┄┄ references  ┄┄ related_product      │
└──────────────────────────────────────────────────────────────────────────┘
```

### 4.2 收缩 / 展开规则

| 层级 | 默认状态 | 展开行为 |
|------|----------|----------|
| 子类 L1 | **展开**（仅显示 document 列表，不含 section） | 点击 ▼ 收起该子类下所有 document |
| document L2 | **收缩**（只显示标题 + 计数 badge） | 点击 ▶：请求该 document 子树（sections + media） |
| section / media L3 | 随 document 展开 | 叶子节点；点击右侧详情面板 |
| 跨文档边 | 默认 **隐藏** | 工具栏「显示挂接关系」开启（有数据时） |

**大图保护**：

- 单 document 下 section > 20：分页或「加载更多」。
- 子类下 document > 50：虚拟滚动 + 按名称搜索。
- 首次进入 Tab：**不**一次拉全库 973 边；只拉 **L1 索引 + L2 列表**。

### 4.3 与「关系图检索」差异

| 维度 | 关系图检索（技能集） | 大类知识图谱（本 Tab） |
|------|---------------------|------------------------|
| 入口 | 输入问句 | 地图选中大类 |
| 范围 | 问句相关 **子图** | 大类 **森林索引** |
| 布局 | 列式 SVG（现有） | **树/思维导图**（可展开） |
| 种子 | ANN 命中高亮 | 无种子；可选「搜索定位」高亮节点 |
| 跳转 | — | 详情面板 →「用此节点发起关系图检索」 |

---

## 五、API 设计（建议）

### 5.1 新增：大类图谱索引

```
GET /api/knowledge/graph/forest?category=beauty
```

**响应（示例）**：

```json
{
  "category": "beauty",
  "stats": {
    "edge_count": 973,
    "media_node_count": 303,
    "document_count": 82,
    "section_count": 312
  },
  "sub_categories": [
    {
      "code": "防晒",
      "label": "防晒",
      "document_count": 12,
      "documents": [
        {
          "node_type": "document",
          "node_id": "goods_25",
          "label": "断黑王钻石光感4件套",
          "doc_type": "niushop_product",
          "source": "niushop",
          "section_count": 3,
          "media_count": 5,
          "has_cross_links": false
        }
      ]
    },
    {
      "code": "_uncategorized",
      "label": "未归类",
      "document_count": 8,
      "documents": []
    }
  ]
}
```

**数据来源**：

- document 列表：`knowledge_edges` 中 `src_type=document` 且 `rel_type=contains` 的去重 `src_id`。
- 标签：`knowledge_chunks.preview` / Chroma `goods_name` / snapshot JSON。
- 子类归属：Chroma metadata `sub_category`（已入库补全）→ 无则归 `未归类`。
- 计数：按边聚合，**不**用向量条数冒充树节点数。

### 5.2 新增：单文档子树

```
GET /api/knowledge/graph/subtree?category=beauty&node_type=document&node_id=goods_25
```

返回该 document 下 **contains / references** 的 section、media 节点及边（复用 `_edges_in_subgraph` 逻辑）。

### 5.3 复用：邻域扩展

已有 `GET /api/knowledge/graph/neighbors` — 用于 **按需增量展开**（与 subtree 二选一实现即可）。

### 5.4 保留：向量明细（降级）

- Tab 内 **「切片明细」** 折叠区或二级入口，保留现有列表 + 来源筛选（给开发/运营 debug）。
- PRD §5.7.7 表格中「已入库向量条目」行改为 **「知识图谱（含切片明细）」**。

---

## 六、客户端改造要点

| 模块 | 改动 |
|------|------|
| `KnowledgePage.vue` | Tab 改名；主区挂载 `KnowledgeForestPanel` |
| 新建 `KnowledgeForestPanel.vue` | 子类树 + 收缩状态（Pinia 或 localStorage 记忆） |
| 扩展 `KnowledgeGraphViz.vue` | 抽出 **边/节点样式**；新增 **树形布局** 模式（或新组件 `KnowledgeTreeViz.vue`） |
| `knowledge_service.ts` | `fetchGraphForest` / `fetchGraphSubtree` IPC |
| 地图联动 | `selectedCategory` 变化 → 重载 forest |

---

## 七、分期建议

### P0 — 可演示（1–1.5 周）· **仅 beauty**

- [ ] `GET /api/knowledge/graph/forest`（**category 参数通用**，P0 验收 beauty）
- [ ] Tab 标签 **「知识图谱」**；主视图：子类 → document 列表，document 点击展开 subtree
- [ ] **「未归类」** 分组展示无 sub_category 的 document
- [ ] 非 beauty / 无图数据大类：**空态**，不展示假图
- [ ] 节点详情侧栏（标题、来源、段落/媒体计数）
- [ ] 「切片明细」折叠区保留原 vector 列表

**验收**：beauty 下能看到 ≥70 商品树；展开任一商品可见真实 section/media 边；**不展示**不存在的 `related_product`；drink 等无数据大类为空态。

### P1 — 体验增强

- [ ] 图谱内搜索（按商品名/标题过滤 L2）
- [ ] 来源筛选（商城 / 资料 / 挂接）
- [ ] 「在关系图检索中打开」跳转并预填节点上下文
- [ ] `ai_agent` 大类（技术文档树，子类为 video/image/llm…）

### P2 — M3-S1 后

- [ ] 展示 `related_product` / `mentions` 跨树虚线
- [ ] `concept` 节点层
- [ ] 与 M2-3 存量补边后的全库概念网

---

## 八、PRD §5.7.7 修订（已合入）

1. Tab 名称：**「知识图谱」**（副标题：Level 2 知识网预览；**切片明细**折叠）。
2. 主指标：**「N 文档树 · M 边 · K 媒体」**，弱化「419 条向量」。
3. 与 §5.5.5 地图：地图看 **统计**，图谱 Tab 看 **结构**。
4. P0 仅 **beauty** 有内容；其他大类空态。
5. **未归类** 分组定稿；归类规则后续迭代。
6. 技能集「知识关系图检索」保留为 **问答式子图**。

---

## 九、风险与约束

| 风险 | 缓解 |
|------|------|
| 231 条无 `sub_category` 落入「未归类」 | 已做入库补全 + backfill；后续 ingest 持续写入 |
| 973 边一次渲染卡顿 | 默认只加载 L2 索引；子树按需 |
| M3-S1 未上线时无挂接边 | UI 不展示空关系；文案说明「资料挂接后此处出现虚线」 |
| 评价 chunk 未入 `knowledge_edges` | P0 可不进树，仅切片明细可见；P1 评估是否补 `evaluate` 边 |

---

## 十、验收标准（P0）

1. 知识库页选中 **beauty**，图谱 Tab 展示 **≥5 个子类分组**（含「未归类」）。
2. 每组下列出 **真实 document 节点**，标签与商城商品名一致。
3. 展开任一 document，展示 **contains** 段落与 **references** 媒体，边数与 SQLite 一致。
4. 默认仅 **子类 + document 标题** 展开；section 层默认收缩。
5. 切片明细折叠区仍可查看原 vector 列表（回归 ingest 预览能力）。

---

## 十一、文档索引

| 文档 | 关系 |
|------|------|
| [产品设计文档-谛听.md §5.7.7](产品设计文档-谛听.md) | Tab 定义（待修订） |
| [M3-1-元宝文档挂接知识网技能方案.md](M3-1-元宝文档挂接知识网技能方案.md) | `related_product` / `mentions` 边来源 |
| [知识库-结构化入库方案.md](知识库-结构化入库方案.md) | M1.6 边表模型 |
| [开发计划-总览.md §14.4](开发计划-总览.md) | 排期挂载位（建议 **M3-S2**，在 M3-S1-5 之后） |

---

| 版本 | 日期 | 说明 |
|------|------|------|
| v0.2 | 2026-06-28 | 定稿：Tab 名「知识图谱」；未归类分组；P0 仅 beauty、无数据大类空态 |
| v0.1 | 2026-06-28 | 需求讨论稿：向量 Tab → 大类知识图谱（可收缩树） |

# 187w · 数据连接列表列跳转与 Source 详情蓝图接线方案

| 字段 | 内容 |
|------|------|
| 状态 | ✅ **v1.0** · 已编码 |
| 版本 | **v1.0** · 2026-07-20 |
| 对齐 | [05](../05-数据集成Connectors-Pipeline-Dataset产品方案.md) DC-03 · [80](80-蓝图按钮体系与复杂交互页层次规范.md) · `data-connection.html` / `source-detail.html` |

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 蓝图优先 | 列表列徽标可点；详情页统一壳，插件差异只在内容区 |
| 上线态 | 链到真实 Source/Dataset API，无假页 |
| 最小更改 | 抽 `dataConnectionUi` · 新路由 `/data/sources/:id` · 列表改 Link |

---

## 1. 交互定稿（用户确认）

| 列 | 点击目标 | 路由 |
|----|----------|------|
| **连接器**（MySQL JDBC / PostgreSQL / …） | Source 详情（连接器页） | `/data/sources/:sourceId` |
| **存储类型**（数据集 / 媒体集） | 数据集或媒体集页 | `/data/datasets?rid=` · `/data/media-sets` |
| **名称** | 同 Source 详情 | `/data/sources/:sourceId` |

各连接器插件文案/色调可不同，**页面壳一致**（Tab · 探索三栏 · 右侧面板），对齐 `source-detail.html`。

---

## 2. 工程落点

| 文件 | 变更 |
|------|------|
| `pages/s2/dataConnectionUi.tsx` | 可点 ConnectorTag / StoragePill · 共享 label/tone |
| `pages/s2/sourceDetailPage.tsx` | DC-03 详情页 |
| `pages/DataPage.tsx` | 列表列改 Link；去掉同页内嵌 detail |
| `pages/s2/data.tsx` | Datasets 支持 `?rid=` |
| `pages/s2/routes.tsx` | 注册 `data/sources/:sourceId` |
| `styles.css` | `.data-tag-link` / `.data-storage-link` hover |

---

## 3. 验收

- [x] 连接器徽标可点 → Source 详情
- [x] 数据集徽标可点 → 数据集预览（带 rid）
- [x] 详情页层次：Tab + 探索 + 右栏信息（统一壳）
- [x] 插件不同仅改 label/tone，不改布局

*v1.0 · w1*

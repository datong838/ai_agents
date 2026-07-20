# 183w · Pipeline 多表 Join 平台能力方案

| 字段 | 内容 |
|------|------|
| 状态 | 📝 **方案定稿 · 暂不编码**（通过后改 aos-platform；自测后关 G-PB-01） |
| 版本 | **v1.1** · 2026-07-20 |
| 分支 | **`w1`** |
| 父案 | [180w](180w-w1台账债与平台能力验证总案.md) |
| 触发 | 产品目标含 Join；现状 PB Join **非 live**；外部多子表孪生（[182w](182w-外部数据源数字孪生与全栈能力验证方案.md)）需要 |
| 对齐 | [05](../05-数据集成Connectors-Pipeline-Dataset产品方案.md) · [T05](T05-L1数据集成详细技术方案.md) · [36](36-T4.6-MySQL去stub方案.md) · [97](97-Connector插件化整改方案.md) · [100](100-Connector运行时插件分发方案.md) |
| 核查夹具 | 可选：案例目录 `01-Pipeline多表JOIN…`（能力缺口记录；非平台定制依据） |

---

## 使用的 Rules

| Rule | 应用 |
|------|------|
| 中文 | 全文 |
| 先方案后编码 | 本文通过前不改 Pipeline/JDBC 实现 |
| **红线 · 通用平台** | **禁止** 行业/品牌 Join 专用包；能力对所有 JDBC Source 可用；正文 **无品牌名** |
| 最小 MVP | 先等值 Join / 或 Sync 自定义 SQL |

---

## 1. 现状（已核实）

| 层 | 现状 |
|----|------|
| 产品目标 | 05 / 蓝图含 Filter→**Join**→Curated |
| `/data/pipelines` | 列表壳；无算子画布 |
| `POST /v1/pipelines` | CRUD 壳；无 transforms |
| `jdbc-mysql` | 已支持请求体 `table`/连接覆盖；尚无多表 `query` Join |
| 缓解 | 库侧 VIEW 或分表 + Ontology Link |

缺口：**G-PB-01**（无 Join）· **G-JDBC-01**（弱多 query）。

---

## 2. 目标 / 非目标

### 2.1 目标（DoD · MVP）

任选一条达到即可关 G-PB-01 主诉求（优先 A，可并行 B）：

| 路径 | 能力 | DoD |
|------|------|-----|
| **A. Sync/Ingest SQL** | Source 配置 `query`（只读 SELECT，可含 JOIN） | 探活+ingest 产出 Dataset；任意主从表 SQL 可跑 |
| **B. Pipeline Join 算子** | 两 Dataset 等值 Join（inner/left）→ 新 Dataset | API+最小 UI 或 API-only 先 live |
| **C. 文档化 VIEW** | Source 可发现/选用库 VIEW | 不关 G-PB-01，仅运维友好 |

**本方案主推：先 A，再 B。**

### 2.2 非目标

- 完整 Pipeline Builder 画布（后置）。  
- 跨 Source 分布式 Join。  
- 右连接/全外连接/复杂表达式引擎。  
- 任何行业专用插件包名。

---

## 3. 方案设计

### 3.1 路径 A · JDBC 自定义 SQL（推荐首刀）

```text
Source.config: { secretRef, database, query?: string, table?: string }
  → probe：EXPLAIN 或 LIMIT 0
  → ingest：执行 SELECT → 行集 → Dataset
```

| 项 | 约定 |
|----|------|
| 仅 SELECT | 拒绝 INSERT/UPDATE/多语句 |
| 参数 | 可选 `params` 绑定；禁止拼接不可信输入 |
| 产品面 | `/data` Source 高级项：「自定义 SQL」 |
| 契约 | `/v1/connectors/jdbc-mysql/ingest` 增 `query` |

验收 SQL（示意 · 任意主从表）：

```sql
SELECT p.id AS parent_id, p.name, c.id AS child_id, c.sku, c.price
FROM parent_table p
JOIN child_table c ON c.parent_id = p.id
WHERE IFNULL(p.is_delete,0)=0
LIMIT 100
```

### 3.2 路径 B · Pipeline Join（二刀）

```text
Pipeline.spec.nodes:
  - { id, type: "input", datasetRid }
  - { id, type: "join", left, right, leftKey, rightKey, how: inner|left }
  - { id, type: "output", name }
Build → 物化 Dataset
```

| 项 | MVP |
|----|-----|
| UI | 可先 API + 简易表单；画布后置 |
| 执行 | aos-api 内存/PG 临时表 Join（大批量后置） |

### 3.3 安全

- 只读账号。  
- SQL 白名单关键字检查。  
- Marking：结果集不自动降敏；导出走治理。

---

## 4. 工程落点（评审后）

| 落点 | 文件（示意） |
|------|----------------|
| 契约 | `packages/contracts/openapi/v1.yaml` |
| JDBC | `aos_api/mysql_connector.py` · `connector_runtime.py` |
| Pipeline | `wave_ext.py` pipelines 或新 `pipelines.py` |
| Web | `/data` Source 表单 |
| 单测 | `tests/test_183w_jdbc_query_join.py` |

---

## 5. 自测计划

1. pytest：拒绝非 SELECT；JOIN SQL ingest 行数>0。  
2. 手工：`/data` 配 SQL → Dataset 预览含主从表字段。  
3. 回写：G-PB-01 关闭或降级；180w / 182w 验收勾选。

---

## 6. 验收

- [ ] 路径 A 或 B 至少一条 live  
- [ ] 任意 JDBC 主从表可宽表或 Join 进 Dataset  
- [ ] 无行业定制包名；正文无品牌名  
- [ ] 缺口台账更新  

---

## 7. 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-07-20 | 初版：A=SQL Sync · B=Join 算子 |
| v1.1 | 2026-07-20 | **去品牌化**；验收 SQL 改为通用示意 |

---

*v1.1 · w1 · 通用 Join/SQL · 先方案后编码*

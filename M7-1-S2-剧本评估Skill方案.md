# M7-1-S2 — 剧本评估 Skill 方案

> **状态**：方案定稿 · **M7-1c 评估 Skill 已编码** · 2026-07-04  
> **引擎**：元宝 UIA（与 S1 同源）  
> **Rubric**：[评估-电商短视频Rubric-v1.md](M7-1-standards/评估-电商短视频Rubric-v1.md)  
> **上游**：[M7-1-S1 编剧 Skill](M7-1-S1-编剧Skill方案.md)  
> **总方案**：[§4.5 评估标准共用](M7-1-短视频创作-导演智能体总体方案.md#45-评估标准共用编剧--评估)

---

## 一、职责边界

| 做 | 不做 |
|----|------|
| 按 **同一 Rubric 全文** 对 `script.md` **正式打分** | 不重写剧本（退回 S1） |
| 输出 `review.md` + `review.json`（§9.3 契约） | 不修改 `creation_material_bundle` |
| 编译《评估任务书》→ 元宝 UIA → 入库 | 不调 DeepSeek |

---

## 二、输入（与 S1 · 总方案对齐）

| 输入项 | 形式 | 必填 | 说明 |
|--------|------|------|------|
| **待评估剧本** | `artifacts/script.md` | **是** | S1 产出 |
| **评估标准** | 独立 `.md` | **是** | **`project.json.review_rubric_path`** — 与 S1 **同一文件** |
| **创作素材包** | bundle JSON | 推荐 | 核对商业锚点是否来自 `fact_sheet`（Rubric 1.2 / 6.1） |
| **剧本元数据** | `script.meta.json` | 自动 | `rubric_version` 须与本次评估一致 |

> S1 已在编剧阶段注入该 Rubric 的 **约束摘要**；S2 注入 **全文** 做正式评分 —— **标准同源，用法不同**（见 §三）。

---

## 三、评估标准共用（S1 ↔ S2）

与 [M7-1 §4.5](M7-1-短视频创作-导演智能体总体方案.md#45-评估标准共用编剧--评估)、[S1 §2.1](M7-1-S1-编剧Skill方案.md) **完全一致**：

```text
                    评估-电商短视频Rubric-v1.md
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
    extract_rubric_constraints          Rubric 全文
              │                               │
              ▼                               ▼
      script_brief（S1）              review_brief（S2）
      「评估约束摘要」                 「评估标准（全文）」
      写剧本 · 不自评打分              七维打分 + veto + JSON
              │                               │
              └───────────┬───────────────────┘
                          ▼
                   同一 rubric_version
                   写入 meta / review.json
```

| 对比 | S1 编剧 | S2 评估（本 Skill） |
|------|---------|---------------------|
| Rubric 注入量 | **摘要** ~800–1200 字 | **全文** |
| 元宝输出 | `script.md` | `review.md` + JSON |
| 是否打分 | 否（仅自检约束） | **是**（≥72 且无 veto → pass） |
| 失败处理 | — | `issues[]` → 下一轮 S1「修订指令」 |

**共享编译器**：`rubric_compiler.py` / `rubric_compiler.ts`

- S1 调用：`extract_rubric_constraints(rubric_md)`
- S2 调用：`load_rubric(rubric_md)` 全文嵌入任务书

---

## 四、任务书编译 `review_brief_compiler`

### 4.1 模板

```markdown
# 谛听 · 剧本评估任务书

你是剧本评估员，**严格**按下方「评估标准（全文）」对剧本打分。

## 输出要求
1. 人类可读报告（Markdown）
2. 文末 **JSON 代码块**，严格遵循 Rubric §9.3 schema（含 commercial_anchor、veto_hit、pass）

## 待评估剧本
{script.md 全文}

## 评估标准（全文）
{rubric.md 全文 · 与编剧阶段为同一文件 review_rubric_path}

## 素材包核对（可选）
fact_sheet_hash: {bundle.fact_sheet_hash}
产品指称须与 fact_sheet 一致；展示 Beat 须有产品镜头。
```

### 4.2 代码落点

| 层 | 路径 |
|----|------|
| 评估 brief | `salesagent/.../knowledge/review_brief_compiler.py` |
| Rubric 共用 | `salesagent/.../knowledge/rubric_compiler.py` |
| 客户端 | `ditingclient/.../electron/services/review_brief_compiler.ts` |
| API | `POST /api/knowledge/video/review/brief` |
| 入库 | `POST /api/knowledge/video/review/ingest` |

---

## 五、输出落盘

| 文件 | 说明 |
|------|------|
| `briefs/review_brief_{ts}.md` | 任务书（含 Rubric **全文**） |
| `artifacts/review.md` | 人类可读报告 |
| `artifacts/review.json` | 结构化结果；`rubric_file` + `rubric_version` 与 S1 一致 |

### 判定与退回

| 结果 | `project.status` | 动作 |
|------|------------------|------|
| `pass: true` | `script_approved` | 进入分镜/摄影 |
| `pass: false` | `script_review` → 触发 S1 | `issues[]` 写入下一轮 `script_brief` |

协作时序见 [S1 §六](M7-1-S1-编剧Skill方案.md)。

---

## 六、验收清单（M7-1c · 与 S1 联调）

| # | 项 |
|---|-----|
| E1 | `review_brief` 含 Rubric **全文**；`script_brief` 含 **摘要** — 同源 `review_rubric_path` |
| E2 | `script.meta.json` 与 `review.json` 的 `rubric_version` 一致 |
| E3 | 故意缺产品镜头的剧本 → S2 `veto_hit` 非空、`pass: false` |
| E4 | `issues[]` 退回 S1 后，`script_v2.md` 修复对应 Beat |
| E5 | `review.json` 符合 Rubric §9.3（含 `commercial_anchor`） |

---

## 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1 | 2026-07-04 | 定稿：与 S1/总方案 §4.5 对齐；Rubric 全文 vs 摘要共用规范 |
| v0.1 | 2026-07-04 | 概要占位 |

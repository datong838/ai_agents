# 220tech · W2+ 高优先级波次总体规划

> **版本**：v1.0 · 2026-07-22 · **关联**：220plan §1.2.3 W2+ 高优先级 27 项 · Phase 7+
> **前置**：W1 全量交付（19/19 ✅）· 全量回归 841 passed 零回归
> **依赖**：W1-1~W1-19 全部模块 · llm_gateway（Agnes 已接入）

## 1. 波次目标
将 220plan §1.2.3 的 27 项高优先级差距，按**后端可测优先、依赖链清晰**原则分批交付，延续 W1 的微观方案先行循环（方案→编码→测试→下一项）。

## 2. 台账自洽性修正

调研发现 §1.2.3 有 4 项与 §1.2.2 W1 已完成项**描述重复**，需精化标注为「W1 核心已完成，W2 增强版」：

| W2+ # | 重复的 W1 项 | 处理方式 |
|-------|-------------|----------|
| #11 Funnel 索引管道执行引擎 | W1-5 ✅ | 标注「核心已完成」→ W2 增强双管道/全量重索引触发/CDC |
| #17 Logic Block 全量 | W1-2 ✅ | 标注「核心已完成」→ W2 增强 LangGraph/Wiki 字段 |
| #18 工具集注册 | W1-2 ✅ 子能力 | 标注「核心已完成」→ W2 增强 Capability 深度集成 |
| #19 Ontology 写回四步 | W1-2 ✅ 子能力 | 标注「核心已完成」→ W2 增强 Workshop 绑定 |

**不合并删除**（保留为增强版追踪），但在状态列加 `🔶 核心已完成` 区分纯新开发项。

## 3. 分批策略

按「后端可测 + 依赖低 + 价值高」分 5 批：

### 第一批 W2-A（后端核心 6 项 · 当前推进）
| 编号 | 差距项 | 依赖 | 交付物 |
|------|--------|------|--------|
| W2-3 | Ontology 对象类型输出 | W1-14 | 流水线输出→对象类型→主键→OE 查看 |
| W2-6 | Pipeline Builder 输出系统 | W1-14 | 6 种写入模式（Append/Snapshot/Upsert/Replace/Update/Delete） |
| W2-8/9 | Dynamic Scheduling 引擎+数据模型 | — | Schedule/Resource 对象 + cron daemon |
| W2-20 | Pipeline 多数据源支持 | W1-14 | 多表 Join 链（订单→商品→买家） |
| W2-23 | Data Connection 增量同步 | — | 单调递增列 + WHERE 过滤 |

### 第二批 W2-B（AIP/Functions 运行时 5 项）
| #7 AIP/LLM 节点 | #18 工具集注册 | #21 @transform 装饰器 | #25 多语言 Transform | #26 Functions 运行时 |

### 第三批 W2-C（Ontology Manager/OE 5 项）
| #12 OE 探索图表 | #13 Object Views 微件 | #14 Action 规则可视化 | #15 Action 函数规则 | #16 Action 可视化编辑器 |

### 第四批 W2-D（Dynamic Scheduling 增强 + Data Connection 2 项）
| #10 甘特图 | #24 事务类型 |

### 第五批 W2-E（媒体集增强 + UI 项 4 项）
| #1 媒体集延迟策略 | #2 媒体集→表格行 PB 节点 | #4 Lineage 增强 | #22 Web IDE | #27 Logic 无代码编辑器 |

### 台账修正项（4 项 · 标注即可）
| #11 | #17 | #18（合并入第二批） | #19 |

## 4. 执行纪律（延续 W1 §13）
- 每项开工前写 `220tech_*.md` 微观方案（5 节：数据模型/算法/接缝点/测试矩阵/文件清单）
- 每项完成后：单元测试全绿 → 全量回归零新增 → 更新 220plan 状态
- 每批完成后：重启系统验证 + 端点 OpenAPI 核验 + 输出总结
- 不写死模型：LLM 调用经 llm_gateway 路由

## 5. 接缝点总览（第一批依赖的 W1 模块）
| W1 模块 | 接缝点 | 第一批使用者 |
|---------|--------|-------------|
| W1-14 pipeline_builder.py | Pipeline 节点 config 扩展 | W2-3, W2-6, W2-20 |
| W1-8 transform_ops.py | Join 算子多表扩展 | W2-20 |
| W1-4 build_engine.py | JobSpec outputs 扩展 | W2-3, W2-6 |
| W1-13 lineage.py | 对象类型节点 | W2-3 |

# 220tech · W1-12 Evals 评测门控引擎

> **版本**：v1.0 · 2026-07-22 · **关联**：220plan §6.2 W1-12 · Phase 4 · 中优先级
> **依赖**：llm_gateway.py（LLM 评判模式）
> **范围**：评测集模型 + 4 种评判标准 + 门控检查器 + 评测报告

## 1. 目标
- 评测集 = 一组测试用例（输入 + 期望输出 + 评判标准）
- 对目标函数（Logic/Function）执行评测 → 生成报告（通过率 + 失败详情）
- 4 种评判标准：精确匹配 / 包含匹配 / LLM 评判 / 数值容差
- 门控：通过率 ≥ 阈值 → 允许发布；否则阻止

## 2. 设计原则
- **不写死模型**：LLM 评判通过 `llm_gateway.chat()` 路由，model 参数可选
- **依赖注入**：`EvalsEngine(chat_fn=...)` 允许测试注入 mock
- **可组合**：评测目标为 `Callable`（Logic run 或 Function evaluate），引擎不耦合具体模块

## 3. 数据模型
```python
JudgeKind = Literal["exact", "contains", "llm", "numeric"]

class TestCase(BaseModel):
    id: str
    name: str
    inputs: dict[str, Any]
    expected: Any
    judge: JudgeKind = "exact"
    tolerance: float = 0.0       # numeric 专用

class EvalSuite(BaseModel):
    id: str
    name: str
    cases: list[TestCase]
    gate_threshold: float = 0.8  # 门控阈值

class CaseResult(BaseModel):
    case_id: str
    passed: bool
    actual: Any
    expected: Any
    judge: JudgeKind
    detail: str = ""

class EvalReport(BaseModel):
    suite_id: str
    results: list[CaseResult]
    pass_rate: float
    passed: int
    failed: int
    total: int
    gate_passed: bool
    run_at: str
```

## 4. 评判算法
| Judge | 逻辑 |
|-------|------|
| exact | `actual == expected` |
| contains | `str(expected) in str(actual)` |
| llm | `chat(prompt)` → 解析 yes/no |
| numeric | `abs(actual - expected) <= tolerance` |

## 5. REST API (`/v1/evals`)
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/v1/evals/suites` | 创建评测集 |
| GET | `/v1/evals/suites` | 列表 |
| POST | `/v1/evals/run` | 执行评测（body: {suite_id, target_fn}） |
| GET | `/v1/evals/{suite_id}/report` | 查看报告 |
| POST | `/v1/evals/gate-check` | 门控检查 |

## 6. 测试矩阵（≥ 12）
exact pass/fail · contains · llm judge（mock + Agnes）· numeric · pass_rate · gate pass/fail · report · history

## 7. 文件清单
| 文件 | 动作 |
|------|------|
| `aos_api/evals_engine.py` | 新增 |
| `aos_api/routers/evals.py` | 新增 |
| `aos_api/main.py` | 修改 |
| `tests/test_evals_engine.py` | 新增 |

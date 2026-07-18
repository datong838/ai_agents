# 89 · W13 aos-api pytest 回归与 CI 门禁方案

> **版本**：v1.0 · 2026-07-18  
> **状态**：✅ 本波落地  
> **前置**：[27](27-本机开发基础设施与工程门禁记录.md) · [88](88-W12-macOS冒烟与72启停手册对齐方案.md) · [47](47-技术方案全面对齐补缺方案.md)  
> **工程**：`aos-platform/services/aos-api` · `scripts/ci/`

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 用中文 | 本文 |
| 先方案后编码 | 本文 → 修 bug + CI 脚本 |
| 最小更改 | 只修回归失败根因；不改业务契约语义 |
| 自测落档 | pytest 全绿证据回写 27 |

---

## 1. 回归发现

| 用例 | 根因 | 修复 |
| --- | --- | --- |
| `test_validate_endpoint_ok` | `validate_action` 成功路径 `return` 误缩进在 `raise` 之后 → 返回 `None` → 500 | `actions.py` 缩进 |
| `test_object_sets_pg_source` | 断言 `total==2`，demo smoke 污染 PG 后变 3 | 对齐 `test_modules_mock`：`>=2` + site 过滤 |
| 收集失败 `cryptography` | JWKS 测试依赖未列入 `[dev]` | `pyproject.toml` 补 cryptography |

---

## 2. 交付

| 文件 | 动作 |
| --- | --- |
| `aos_api/routers/actions.py` | 修 validate 成功返回 |
| `tests/test_wave2.py` | 断言稳健化 |
| `pyproject.toml` | `[dev]` + cryptography |
| `scripts/ci/run-pytest.sh` | macOS/Linux 并列 CI |
| [27](27-本机开发基础设施与工程门禁记录.md) | § 增 pytest 门禁记录 |

---

## 3. 验收

1. `bash scripts/ci/run-pytest.sh` → `RESULT: PYTEST OK`  
2. `npm test` 仍绿  
3. 不改 Win `*.ps1` 行为  

---

*v1.0*

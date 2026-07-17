# 30 · Wave-2 全链路集成测试方案

> **版本**：v1.0 · 2026-07-17  
> **对应**：[26](26-AOS目标态开发计划.md) Wave-2 · 前置 [28](28-Wave-0全链路集成测试方案.md)/[29](29-Wave-1全链路集成测试方案.md)

---

## 0. 测试债务清查（本轮已补）

| 缺口 | 处置 |
| --- | --- |
| 仅有方案 MD、无自动冒烟 | 新增 `aos-platform/scripts/ci/run-integration-smoke.ps1` |
| 缺 404 / 创建成功 / constitution / graph-health / branches / PG query 单测 | `tests/test_gaps_wave01.py` · `tests/test_wave2.py` |
| 前端缺 ontology id 护栏单测 | `ontologyGuard.test.ts` |

---

## 1. 用例

| ID | 步骤 | 期望 |
| --- | --- | --- |
| IT-2.1 | PG 在线 + schema | status.ps1 ONLINE |
| IT-2.2 | `GET /v1/ontology/object-types` | ≥1 WorkOrder |
| IT-2.3 | `GET /v1/objects/WorkOrder` | total≥1 |
| IT-2.4 | neighbors wo-1001 | 含 wo-1003；engine=adjacency |
| IT-2.5 | wiki + funnel | 200 |
| IT-2.6 | object-sets `source=pg` | DC-East → total=2 |
| IT-2.7 | constitution lint 坏 id | ok=false |
| IT-2.8 | graph-health | score 有值 |
| IT-2.9 | branches | 含 main |
| IT-2.10 | `/ontology` UI | 可选分支 + 健康分 + 点对象 |

## 2. 命令

```powershell
cd c:\work\projects\wchat\aos-platform\services\aos-api
python -m pytest -q
cd ..\..\apps\web
npm test
powershell -File ..\..\scripts\ci\run-integration-smoke.ps1
```

## 3. 执行记录

| 时间 | 结果 |
| --- | --- |
| 2026-07-17 | ✅ pytest 29 · web 11 · `run-integration-smoke.ps1` PASSED |

**Wave-2 集成结论：✅ 通过 → 进入 Wave-3（T3.1 已起步）。**

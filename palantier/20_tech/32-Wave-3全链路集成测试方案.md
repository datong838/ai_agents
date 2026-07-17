# 32 · Wave-3 全链路集成测试方案

> **版本**：v1.0 · 2026-07-17  
> **对应**：[26](26-AOS目标态开发计划.md) Wave-3 · 前置 [28](28-Wave-0全链路集成测试方案.md)/[29](29-Wave-1全链路集成测试方案.md)/[30](30-Wave-2全链路集成测试方案.md)  
> **台账**：[31](31-波次交付结果台账.md)

---

## 1. 退出准则（对齐 26 §3.3）

| 项 | 期望 |
| --- | --- |
| Draft 批准 | → Object 变更（`productionWritten=true`） |
| Lineage | `GET /v1/aip/lineage/{id}` 可打开 |
| L4 门控/熔断 | evals 未绿或 circuit open → chat 拒 |
| dryRun | Logic 不落库；Wiki PUT 直写 409 |

---

## 2. 用例

| ID | 步骤 | 期望 |
| --- | --- | --- |
| IT-3.1 | Action types / validate | criteria 拒/通 |
| IT-3.2 | Draft create | `productionWritten=false` |
| IT-3.3 | approve + 幂等 | 写 Object + lineage；重放 `idempotentReplay` |
| IT-3.4 | 字段冲突 | 无 `X-Allow-Conflicts` → 409 |
| IT-3.5 | functions/invoke · tools | 200 · 含 Action 工具 |
| IT-3.6 | logic dryRun · wiki PUT | 不写生产 · 409 |
| IT-3.7 | circuit trip | chat 503；reset 后通 |
| IT-3.8 | buddy/ask | 答案经 Facade（含 mock-llm） |
| IT-3.9 | UI | Draft 批准 · Logic · Studio 可点 |

---

## 3. 命令

```powershell
cd c:\work\projects\wchat\aos-platform\services\aos-api
python -m pytest -q
cd ..\..\apps\web
npm test
npm run build
# 需重启加载新路由后再跑：
powershell -File ..\..\scripts\ci\run-integration-smoke.ps1
```

---

## 4. 执行记录

| 时间 | 结果 |
| --- | --- |
| 2026-07-17 | ✅ pytest **43** · web **11** · build OK · smoke **PASSED**（含 approve/lineage/logic/chat/media/apollo） |

**Wave-3 集成结论：✅ 通过（MVP DoD）。** LiteLLM 真边车 / 真 IdP 等见 [26 §11.2](26-AOS目标态开发计划.md) 与 §10 ⚠ 标注。

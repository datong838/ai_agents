# 49 · T-UI S2 余量第三刀 · Ferry 诚实叙事方案

> **版本**：v1.0 · 2026-07-17  
> **任务**：关闭剩余 **7** 个 BlueprintStub；Ferry/Release 用**诚实延期面**升格为 live（非假完成）  
> **对齐**：[43](43-T-UI-S2业务深页按域方案.md) · [45](45-T-UI-S2余量第二刀方案.md) · T5.6 / T09 · [34](34-系统启动与蓝图符合性检查记录.md)  
> **工程**：`aos-platform/apps/web` · 最小 API：`aos-api` ferry 501 + code-repos 目录  
> **硬规则**：只调 aos-api；Ferry **不**实现气隙摆渡；不改主路径；非 html 像素 1:1

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文通过后再改 |
| 最小更改 | 复用 `S2Chrome` / `useJsonGet`；一文件多薄页 |
| 不影响已有 | 已 live 24 页行为不变；Ferry 仍标 T5.6 |
| 中文 | 页标题 / lede |

---

## 1. 目标 / 非目标

| 目标 | 非目标 |
| --- | --- |
| 7 Stub → `status: live` + 可演示面板或诚实延期叙事 | 真气隙 Ferry / Full Release Channel / 行业 OKF 全漏斗产品 |
| OpenAPI ferry export/import 与实现一致（501） | 安装 Keycloak / T0.9 clone |
| vitest：`S2_LIVE=31`；无剩余 DEMO s2（或仅显式保留 0） | Playwright 视觉 CI |

---

## 2. 升格清单

| path | 策略 | API |
| --- | --- | --- |
| `/ontology/okf-funnel` | OKF 叙事：constitution lint + WorkOrder funnel + modules | 已有 |
| `/data/pipeline-proposals` | 管道即提案：pipelines 列表 + 创建 | 已有 |
| `/data/code-repos` | 代码库目录（Dev seed） | **新增** `GET /v1/code-repos` |
| `/data/lineage` | 数据沿袭：datasets + syncs + 点选 history（≠ AIP 决策谱系） | 已有 |
| `/apollo/release` | Lite Release：fleet + upgrade 演练 | 已有 |
| `/apollo/ferry` | **诚实延期**：status + export/import → 501 | **新增** status / 501 |
| `/apollo/change` | 变更审批 = Draft 列表 + 链到 drafts/approve | 已有 drafts |

---

## 3. API 最小增量

| method | path | 行为 |
| --- | --- | --- |
| GET | `/v1/code-repos` | `{ items: [{ id, name, url, branch, status }] }` Dev seed |
| GET | `/v1/apollo/ferry/status` | `{ deferred: true, reason: "T5.6", channels: ["lite"] }` |
| POST | `/v1/apollo/ferry/export` | **501** `FERRY_DEFERRED` |
| POST | `/v1/apollo/ferry/import` | **501** `FERRY_DEFERRED` |

OpenAPI：ferry 路径已有 `x-deferred`；补 `GET .../ferry/status` 与 `GET /code-repos`。

---

## 4. 代码落点

| 路径 | 变更 |
| --- | --- |
| `docs/.../49-*.md` | 本文 |
| `aos_api/routers/wave_ext.py` | code-repos · ferry status/501 |
| `packages/contracts/openapi/v1.yaml` | 补 status / code-repos |
| `apps/web/src/pages/s2/remainder.tsx` | 7 薄页 |
| `apps/web/src/pages/s2/routes.tsx` | 注册 → 31 live |
| `apps/web/src/nav.ts` | 7 项 `s2` → `live` |
| `apps/web/src/nav.test.ts` | 断言 31；无 DEMO stub 余量 |
| 26 / 31 / 00 / 34 | 回写 |

---

## 5. 风险与边界

| 风险 | 缓解 |
| --- | --- |
| 用户误以为 Ferry 已可用 | 页顶明确「T5.6 延期」+ API 501 |
| data/lineage 与 aip/lineage 混淆 | lede 写清「数据沿袭」并链到决策谱系 |
| code-repos 假数据被当真生产 | seed 标注 `store: "dev-seed"` |

---

## 6. 自测

- [x] vitest：`S2_LIVE_ROUTES.length === 31`；7 path `status===live`；DEMO 无 s2 余量
- [x] `GET /v1/apollo/ferry/status` → deferred
- [x] `POST /v1/apollo/ferry/export` → 501
- [x] `GET /v1/code-repos` → items
- [x] web vitest 15 passed；`test_s2_ferry_remainder` 1 passed

---

*v1.0*

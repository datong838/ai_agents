# 228-W1-W1 OpenAPI 确定性契约方案

> 日期：2026-07-31
> Worker：W1 / `aos-platform-w1` / `feature/223-worker-1`
> 基线：`7f6434a`
> 状态：✅ 已完成并合入 `m1`

## 1. 目标

建立“干净进程确定性 OpenAPI + 不丢重复路由的 inventory + 向后兼容检查”三件套，为通用平台契约提供可审查、可漂移阻断的真实基线；本波不修具体电商接口，也不治理既有 19 组重复路由。

## 2. 现状证据

- 手写 `packages/contracts/openapi/v1.yaml` 仅 61 paths / 75 operations，属于 legacy stable-intent。
- 运行时 OpenAPI 为 2242 paths / 3973 operations / 1399 schemas；三次干净进程 canonical JSON 字节一致。
- 3992 条业务 method-route 中有 19 组重复 method+path；OpenAPI 只能保留 3973 个 unique operations。
- legacy 75 operations 中只有 63 个 path+method 仍存在，12 个缺失；已覆盖项的 operationId 也全部漂移。
- 当前没有导出脚本、全量基线、route inventory 或兼容检查。

## 3. 文件所有权

W1 可修改/新增：

- `scripts/export_openapi.py`
- `scripts/check_openapi_compat.py`
- `packages/contracts/openapi/v1.generated.json`
- `packages/contracts/openapi/v1.inventory.json`
- `services/aos-api/tests/test_openapi_contract.py`

禁止修改：

- `main.py`、Router manifest/聚合器、legacy `v1.yaml`
- 公共 `scripts/ci.sh`（总控合并后接线）
- package workspace、前端、Helm、具体电商接口

## 4. 确定性导出

1. 每次由独立子进程导入 app，不能复用 `app.openapi_schema` 缓存。
2. JSON 固定 `ensure_ascii=False`、`sort_keys=True`、紧凑 separators、UTF-8/LF、一个尾换行。
3. 禁止生成时间、绝对路径、随机 ID。
4. 写文件使用临时文件后原子 replace；`--check` 只比较、不落盘，漂移退出 1。
5. 连续两个 clean process 必须字节一致。

## 5. Route inventory

- 从 FastAPI eager/lazy route tree 独立展开，排除 4 条框架 docs 路由。
- 保留 3992 行，不能按 path 去重；记录 domain、path、method、name、operationId、tags、ordinal。
- 校验 3973 unique pairs 与现有 19 组重复完全一致；新增、减少或变化都失败。
- OpenAPI 只作为 unique operation 视图，不能反推完整路由总账。

## 6. 兼容检查

硬阻断：删除 path/method、operationId 改变、删除/改名参数、请求新增 required、类型收窄、enum 删除、删除成功响应、响应删除字段/类型不兼容、security 收紧。

人工审查：enum 新增、复杂 oneOf/allOf/discriminator 变化或无法判定的 schema 改动。

允许：新增 path/method、可选参数/字段、额外响应码。

退出码：0 兼容；1 漂移/破坏；2 输入或生成错误。例外必须精确到 JSON pointer、理由和迁移说明，不允许全局跳过。

legacy `v1.yaml` 只生成固定审计摘要，不作为 generated baseline 覆盖或兼容真相源。

## 7. 验收

- [x] 两个干净进程导出字节一致，`--check` 通过。
- [x] generated OpenAPI 基本结构、local `$ref`、operationId、responses 合法。
- [x] inventory 保留全部业务路由和现有重复，新重复被阻断。
- [x] 兼容算法有 breaking/non-breaking/manual-review 夹具。
- [x] 核心 AIP、Workshop、Ontology、Data、Wiki、Apollo 路径冻结结构而非只检查存在。
- [x] OpenAPI 专项、Router 专项、Wave 1 回归和最终 full 通过。

## 8. 完成证据

- Worker `f1fa895`，合并 `a62b939`；总控 CI 接线 `e34c66e`。
- 生成基线：2242 paths、3973 OpenAPI operations、3992 route rows、1399 schemas。
- 最终 OpenAPI 门：两次 clean process 字节一致，`--check` 通过，契约/兼容性测试 10/10。
- 最终统一 `full` 12/12 通过。

## 9. 回滚

W1 单独 commit 可回滚。生成文件只描述现有运行时，不修改路由或数据；兼容门异常时先回滚门禁，不覆盖 legacy stable-intent。

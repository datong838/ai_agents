# AIP-4 E2 ReleaseGate 与追加式发布撤销对账

## 当前结论

AIP-4 E2 已 `IMPLEMENTED_GREEN`，代码基线为 `aos-platform/m1@fb525cc`。本波未改变既有 Logic Publication 正常链，而是在 E1B exact Eval Report 之上新增 canonical ReleaseGate/PublicationEvent 服务。

## 实施对应

- `aip_release_publication_models.py`：请求只允许选择 exact report/gate 和幂等键，不允许提交 GREEN/status。
- `aip_release_publication_service.py`：同一 tenant-scoped transaction 复验 Report hash、Run succeeded、Suite threshold、Target/Dataset/Judge 与当前 Logic revision/hash。
- `routers/aip_release_publications.py`：开放 Gate 推导、Logic 发布、Publication revoke 三个认证入口。
- `aip_eval_runner.py`：目标最新事件为 revoked/suspended/deprecated 时，新 Eval Run 失败关闭；历史报告和事件仍可复验。
- `aip_publication_event` 只追加 `published/revoked`，重复撤销和同幂等键异载荷均拒绝；不 UPDATE/DELETE 历史事实。
- Agent/Skill registry 尚未落地，非 Logic target 明确 unsupported，不生成假资产。

## 验证与数据边界

- AIP-4 E0A～E2 合并回归：95 passed、1 个显式 Agnes 外部集成项 skipped、2 subtests passed。
- 静态检查通过；OpenAPI/路由清单无新增重复 AIP 路由。
- OpenAPI：2335 paths、1569 schemas、4100 route rows、4090 unique operation pairs。
- 真实库：Alembic 单 head `aip4_003`。
- `org-org/dev-project`：Suite revision 0、Report revision 0、ReleaseGate 0、PublicationEvent 0。
- `dev-org/dev-project`：上述四类计数同为 0；只作负向 canary，不作真实完成证据。

## 风险与下一门

- 本波是后端权威链，无页面变更，因此不需要浏览器验收。
- 旧 Logic Publication compatibility surface 继续保留；后续页面只应接 canonical E2 API，不直接写 Gate/Event 表。
- 下一波进入 AIP-4 E3：真实 LineageEvent、OpenTelemetry span、UsageReceipt/Adjustment、成本与 Capability Receipt。缺失用量必须为 `unknown`，不得用估算值过门。

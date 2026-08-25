# W7-07 媒体/模型 Provider Adapter 与恶意资产门预检 ADR

> 状态：`IMPLEMENTATION_IN_PROGRESS / NO_REAL_PROVIDER_CALL / NO_EXTERNAL_EFFECT / NO_RELEASE`
> 当前事实：`AOS-000262`，`m1@1c79d07f`；W7-04 executor/fence/checkpoint 与 W7-06 four-gate 已 GREEN，Task/Lease 为 `workshop-w7-07-media-model-provider-adapter-malicious-asset-20260825`。

## 1. 裁决

W7-07 只在 AIP canonical Task/Artifact/Usage/Receipt、AIP-7 exact route/provider/policy 和 AIP-9 媒体能力上增加受审 Adapter；不让 Workshop、Provider SDK 或旧 MediaReference 成为第二真源。acquire/generate/TTS/render 采用版本化 C1 Job adapter；live Session 另受最大时长、人工在场、health 与 kill 门约束，不能混入普通 Job。

Adapter 固定 `dryValidate → submit → status/webhook → artifact/receipt → cancel/reconcile`，每 attempt 绑定 exact Capability/Binding、ModelRoute、Provider、RuntimePolicy、Price、adapter、License、Eval 与稳定 request fingerprint。请求提交后的不确定结果进入 unknown/reconcile，禁止盲目重试。

## 2. 资产与数据边界

输入、输出分别进入 tenant-scoped quarantine。输入门覆盖 MIME/size/hash、malware/archive bomb、license/provenance、肖像/商标/同意、marking、商品宣称和 OCR/EXIF/字幕/脚本/嵌入文档 prompt-injection；输出门覆盖 hash/decode/schema、时长/尺寸、malware、license/provenance/watermark 与内容政策。

短时读取授权绑定 principal、purpose、Artifact hash、marking/license、expiry 与 AccessReceipt；Provider egress 受 allowlist、redaction 和 retention policy。Secret 只在 Adapter 内按 secretRef 解析，不进入命令、日志、Artifact metadata、Receipt、共享记忆或前端。

## 3. 2026-08-25 实时事实与缺口

- AIP exact `ModelRouteRevision`、`RegisteredModelRevision`、`ProviderInstanceRevision`、`RuntimePolicyRevision`、Eval/Health/Price readiness resolver、approved `ProviderPluginRevision`、Secret backend 与无隐式 retry/redirect/proxy 的 single-call invoker 已存在；这些是可复用公共 authority，不再等待另一开发线；
- W7-04 executor/fencing/checkpoint/reconcile 已 GREEN，W7-06 exact Variant/attempt/GateSet 也已 GREEN；
- 真实 Provider/Route/Eval readiness 仍不是本波可伪造的运营证据。本波只用 fake adapter/scanner 验证代码合同，不调用真实 Provider；
- 仍缺 tenant-scoped media Job preparation/event/receipt authority、server-owned input/output scan observation、purpose-bound access grant、submit/status/cancel/reconcile 状态单调性和 unknown 禁止盲重试；
- 旧 MediaReference 是无 tenant/RLS/Receipt 的进程内字典，允许 delete/thumbnail 原地修改；
- mock S3 `exists` 永真，本地签名返回 `file://`，二者不是生产证据；
- Media Studio 目前只有三切片 readiness 壳，没有 Job/scan/Provider/unknown/reconcile 与“原子 Skill → Logic → 数字同事”贡献事实；
- 共享/真实数据库没有 `w7_005`，本波只在 disposable database 验证迁移与 RLS；不做 `org-org/dev-project` 业务写入。

## 4. 退出门

- exact adapter/Provider/Route/Policy/License/Eval readiness 与 revoke/drift 负向 GREEN；
- submit/status/webhook/cancel/reconcile、幂等、timeout、unknown 和重复回调 GREEN；
- 输入/输出 quarantine 全门、压缩炸弹/伪 MIME/恶意字幕/EXIF/OCR prompt 注入 GREEN；
- purpose-bound URI、Secret/PII 不泄漏、egress/retention、AccessReceipt GREEN；
- Artifact/Usage/Provider Receipt 谱系闭合且旧 MediaReference 无生产引用；
- 双租户、重启、浏览器、安全与故障注入证据齐全；DEP-M9、AIP-9 与 W7-04 重核 GREEN。

## 5. 两轮审查

第一轮产品与生命周期审查：用户可见 source、授权、安全门、Provider、执行/unknown/reconcile 与输出验收，全过程可干预且不把“已提交”冒充“已产出”；`PASS`。

第二轮技术与安全审查：唯一 Task/Artifact/Usage/Receipt authority、exact Provider binding、隔离区、短时授权、幂等/对账、Secret 最小披露与 fail-closed 完整；当前缺口未误写为完成，无代码、迁移、真实租户或 Provider 副作用；`PASS`。

结论：W7-07 合同基线继续成立；旧 W7-04/“等 AIP-9”阻断已解除，当前由唯一开发者在同一 `m1` 串行补齐公共层与 Workshop 层缺口。真实 Provider、共享迁移、真实租户写入、外部 Effect 与 release 门保持独立关闭。

## 6. 本波文件级实施清单

1. `services/aos-api/alembic/versions/w7_005_media_provider_job_adapter.py`：新增 immutable preparation、append-only event、scan observation、provider receipt 与 purpose-bound access grant；所有表启用 tenant RLS/FORCE RLS、append-only guard 和运行角色最小权限；只允许事件推进，不原地改写历史。
2. `aip_media_provider_job_contracts.py`：冻结 exact Artifact/Stage/Capability/Binding/ModelRoute/Model/Provider/Policy/Plugin/Price/License/Eval refs、稳定 request fingerprint、input/output scan、Job 状态、unknown/reconcile、取消意图与 AccessReceipt 合同；DTO 禁止 secret/URL/原始 payload 泄露。
3. `aip_media_provider_job_store.py`：实现 tenant-scoped idempotency、单调事件序列、CAS/fence、重复 webhook/receipt 去重、unknown 后禁止再次 submit、reconcile/cancel 与 exact readback；不引用旧 `MediaReferenceStore`。
4. `aip_media_provider_job_service.py`：复用 canonical model resolver/plugin authority，组合 server-owned scanner 与版本化 C1 adapter protocol；固定 `dryValidate → prepare → submit → status/webhook → artifact/receipt → cancel/reconcile`。默认无 scanner/adapter 时失败关闭，测试只注入 fake，不产生真实 Provider call。
5. `routers/aip_media_provider_jobs.py` 与 `domain_aggregates.py`：开放 tenant-scoped canonical prepare/read/control API；写入口要求角色、Idempotency-Key、If-Match/expected sequence，错误码不回显 Secret/PII；未装配 adapter 时返回 blocked，不 fallback。
6. `ecommerce_workshop_media_studio*` 与 `routers/ecommerce_workshop.py`：BFF 同 cutoff 读取 Job、scan、Provider、执行与交付 exact refs；扩展严格 View 但保留原 v1 三切片兼容，页面不成为 Job authority。
7. `apps/web/src/api/ecommerceWorkshop/*` 与 `MediaStudioPage*`：严格解析并只读展示 source/authorization/scan/provider/execution/unknown/reconcile、主责内容官和协作角色，以及“原子 Skill → Logic 编排 → 数字同事 → 工作台贡献”；不添加真实 submit/cancel 按钮。
8. `test_w7_07_media_provider_job.py`、邻接 API/Web/OpenAPI/Router 测试：覆盖伪 MIME、超限、archive bomb、malware、license/肖像/商标/同意、OCR/EXIF/字幕/脚本 prompt injection、跨租户、secret/URI 泄露、重复 submit、timeout unknown、重复 webhook、cancel/reconcile、drift/revoke、RLS/append-only、重启回读和普通现有功能回归。
9. 生成 `.evidence/workshop/2026-08-25-w7-07-media-model-provider-adapter-malicious-asset.json`，执行专项、累计、OpenAPI、Web 全量/build、内置浏览器、安全扫描与两轮一致性复审；不 apply 共享迁移、不调用真实 Provider、不生成媒体、不发布。

## 7. 与 163/164 的一致性

- 媒体 acquire/generate/TTS/render/transcode 是 Provider Tool/Capability，不包装成“大媒体 Skill”；Brief/策略/脚本/素材选择/渠道适配/质量审查仍由原子 Skill 组合。
- Logic 固定 Stage、exact model/provider/policy/scan gate 与返工路径；内容官主责，活动策划师/数据参谋/合规等按 ResponsibilitySlot 协作；工作台只显示 contribution projection。
- Job、Artifact、Eval、Issue、Receipt、Usage 分别保留唯一 authority；页面状态、scanner 文案、Provider submitted 或输出 decode 均不能冒充交付、Approval 或 release。

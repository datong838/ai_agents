# W7-01 签名 Stage/ResponsibilityTemplate 与十 Capability 映射预检 ADR

> 日期：2026-08-15；2026-08-25 唯一开发者串行复核并开工
> 状态：`COMPLETED_CODE_CONTRACT_BROWSER_GREEN / OPERATIONAL_PUBLICATION_GATE_RETAINED / NO_RELEASE`
> 范围：W7-01 签名安装可验证的媒体 Stage/Responsibility template 资产、三档 Profile 与十 Capability 映射；不迁移数据库、不操作真实租户、不发布 Bundle。

## 1. 决策

W7-01 采用以下唯一合同基线：

1. 多媒体生产保留制片/统筹、导演/创意、编剧、美术、分镜、摄影/生成、剪辑/后期、评估/审核八类专业责任；责任不等于固定 Agent 或人数。
2. 外部发布批准、交付 Receipt、结果对账与补偿作为独立治理责任进入 Action/Approval/Receipt/Reconcile authority，不伪装成第九类影视职责，也不允许被 merge 吞并。
3. 模板只引用电商增长 Bundle 已发布的十项 canonical Capability ID；历史名称只能经版本化 alias 解析，冻结后保存 exact revision。`storyboard.compose` 的 alias 不得合并编剧与分镜责任槽。
4. 媒体 Module 声明十项目录级适用能力；每个 LITE/STANDARD/FULL profile 和 Stage 仅将实际适用集合标为 required。`live.orchestrate` 只在直播 profile/Stage 中必需。
5. 唯一安装链为“签名模板定义资产 → Bundle signature/content hash → 租户 active installation lock → canonical source resolver → tenant StageTemplateRevision/ResponsibilityTemplateRevision → Recommendation/Plan/Run frozen exact refs”。Bundle 定义与租户 revision 是连续交付态/运行态，不是双真源。
6. Bundle/template/capability/policy/provider/license 撤销或漂移会使 ProfileRecommendation、ResponsibilityPlan、compiled Plan 与 start readiness stale/blocked；重新解析、复验和用户确认前不得启动。

## 2. 十 Capability 到责任槽映射

| 责任槽 | canonical Capability |
|---|---|
| 制片/统筹 | `strategy.plan`、`material.collect`、`performance.review` |
| 导演/创意 | `strategy.plan`、`copy.generate`、`script.compose` |
| 编剧 | `copy.generate`、`script.compose` |
| 美术 | `material.collect`、`strategy.plan`、`platform.adapt` |
| 分镜 | `script.compose`、`video.compose` |
| 摄影/生成 | `material.collect`、`speech.synthesize`、`video.compose` |
| 剪辑/后期 | `speech.synthesize`、`video.compose`、`platform.adapt` |
| 评估/审核 | `content.review`、`performance.review` |
| 直播适用附加能力 | `live.orchestrate` |

预算、许可证、版权、肖像与商标检查属于 Policy/Evidence gate，不创建虚假 Capability ID。平台发布由 `platform.adapt` 生成候选 Variant，但实际外部发布仍必须经过独立 Action approval/lease/receipt。

## 3. 现场预检事实

预检账本：`.evidence/workshop/2026-08-14-w7-01-signed-stage-responsibility-capability-mapping-preflight.json`。

已 GREEN 的基础：

- generic StageTemplate/ResponsibilityTemplate authority、版本化 freeze/seal 与图编译骨架存在；
- 十项 Capability definition catalog 完整，媒体 Module `requiredCapabilities` 恰好覆盖十项 canonical ID；
- W7-01 邻接后端 28 项、前端 16 项测试通过。

2026-08-15 的历史阻断项如下：

1. `W6-01` 未完成；
2. `W6-02` 未完成；
3. `DEP-M9/AIP-9` 仍为计划态；
4. 媒体 Module 的 `responsibilityTemplateRefs` 为空；
5. 媒体 Module 的 `productionContractRefs` 为空；
6. Eval 仍引用 placeholder；
7. 未发布签名 LITE/STANDARD/FULL StageTemplate 资产；
8. 未发布签名 LITE/STANDARD/FULL ResponsibilityTemplate 资产；
9. production Router 未注入 Stage source resolver；
10. production Router 未注入 Responsibility template resolver；
11. Bundle schema `1.3.0` 与当前只接受 `1.2.0` 的 publisher 不兼容；
12. profile 仍可作为任意字符串进入底层通用模型，缺签名枚举/模板约束；
13. 旧 AIP-9 描述仍存在固定 coordinator/具名团队倾向，尚未按 ResponsibilityPlan 与 capability-driven adaptive composition 收敛。

### 3.1 2026-08-25 独立复核

本次不沿用历史 `IMPLEMENTATION_BLOCKED` 结论，而是重新核对当前代码与交付事实：

1. `W6-01` exact capability/assignee resolver 已完成，候选人数量可变且 exact capability readiness 失败关闭；
2. `W6-02` LITE/STANDARD/FULL Recommendation、用户 Confirmation 与 protected merge policy 已完成；
3. AIP 媒体责任映射已存在八槽/十 Capability 的只读合同与测试，生产合同 Router 已注入 active-installation resolver；
4. `solution.ecommerce.growth@1.4.0` candidate 已由统一 Bundle schema/publisher 消费，并已有七 Module typed production profile 与 exact installed-artifact resolver；
5. 剩余真实缺口不是“等待其他 Owner”，而是媒体三档 signed-installable template 资产尚未形成：当前媒体 profile 仅有 maker/review 两槽，LITE/STANDARD/FULL 没有独立 exact artifact，八责任映射尚未进入 Bundle 资产，Module 也未引用三档模板；
6. Candidate 资产不等于已发布或已签名；运行时只能由 active installation 中 `published + signature + composition lock + exact digest` 的 Bundle 解析，未安装、撤销、漂移与跨租户一律失败关闭。

因此 W7-01 的代码依赖已满足，可以在不触发发布、迁移或真实副作用的前提下实施；运营发布门继续保留。

## 4. 实施顺序与放行门

1. 先完成 W6-01：统一 Bundle publisher schema、安装 resolver、exact capability/assignee readiness；
2. 再完成 W6-02：签名三档 profile、Recommendation/Confirmation、MergePolicy 与 drift invalidation；
3. AIP-9 冻结 adaptive production composition authority，删除固定 Agent/人数语义；
4. 发布模板定义并完成 Bundle 安装、租户 revision 物化、Module exact refs 回填；
5. 通过八责任 coverage、十 Capability exact mapping、图完整性、撤销/漂移、跨租户与 fail-closed 测试后，W7-01 才可勾选。

任何一步不得用本地静态映射、BFF 私有模板或页面常量绕过 canonical authority。

### 4.1 2026-08-25 文件级施工清单

1. 新增严格媒体模板合同，冻结三档 Profile、八责任槽、十 Capability canonical ID、适用 Stage 和 protected review 约束；拒绝未知字段、重复槽、错误映射、`live.orchestrate` 非直播误用与环依赖；
2. 扩展 active-installation resolver，仅在已发布、已签名、composition lock 与 artifact digest 全部 exact 时加载媒体模板 payload；路径逃逸、镜像漂移、旧 installation revision 与跨租户失败关闭；
3. 在 `solution.ecommerce.growth@1.4.0` candidate 增加 LITE/STANDARD/FULL 三份 immutable template 资产，并让媒体 Module 的 production/responsibility refs 精确引用三份资产；
4. 保留现有 `ProductionProfile`、37 Logic 兼容、十 Capability catalog 与 Workshop 页面能力，不删除旧 ID、不迁移 Binding、不改变 Action/Provider/发布门；
5. 增加合同、Bundle、resolver、撤销/漂移/隔离专项测试，并执行 W6/W7 邻接累计回归、TypeScript/build、OpenAPI/Router、Alembic、安全扫描和涉及页面的内置浏览器验收；
6. 形成 Evidence、Delivery Receipt、安全提交，释放 Lease 后以 authority CAS 推进 W7-02。

代码文件范围：

- `services/aos-api/aos_api/aip_media_production_templates.py`
- `services/aos-api/aos_api/aip_responsibility_template_authority.py`
- `services/aos-api/tests/aip/test_aip_media_production_templates.py`
- `services/aos-api/tests/aip/test_aip_responsibility_template_authority.py`
- `services/aos-api/tests/asset_registry/test_m5_ecommerce_bundle_contracts.py`
- `services/aos-api/tests/asset_registry/test_workshop_module_contracts.py`
- `bundles/candidates/ecommerce/solution.ecommerce.growth/1.4.0/bundle.yaml`
- `bundles/candidates/ecommerce/solution.ecommerce.growth/1.4.0/content/media-production-templates/*.json`
- `bundles/candidates/ecommerce/solution.ecommerce.growth/1.4.0/content/workshops/ecommerce.media-studio.json`
- `.evidence/workshop/2026-08-25-w7-01-signed-stage-responsibility-capability-mapping.json`

若实现过程中发现必须扩大文件范围，先回写本 ADR，再改代码。

## 5. 双轮复审

### 第一轮：目标与边界

- 八类专业责任 8/8 保留，Agent 数量不冻结：通过；
- 发布批准/Receipt/对账未被弱化：通过；
- 十项能力回到已发布 canonical 目录：通过；
- Bundle/租户 revision 无双真源：通过。

### 第二轮：可实施性与安全

- exact refs、readiness、撤销/漂移传播和 fail-closed 边界已写入方案：通过；
- 当前缺口、依赖与施工顺序明确，不把预检写成完成：通过；
- 未修改代码、数据库、真实租户或外部系统：通过。

结论：合同基线保持通过；历史依赖阻断已由当前代码交付解除，W7-01 按上述最小切片进入实施。Candidate/测试 GREEN 仍不等于 Bundle 已签名发布、租户已安装、Provider 可用、真实媒体生产或外部发布获授权。

## 6. 2026-08-25 实施闭环与一致性复审

### 6.1 实施结果

1. `solution.ecommerce.growth@1.4.0` candidate 已加入 LITE/STANDARD/FULL 各一份 Responsibility 与 Stage 资产；八责任槽 8/8 保留，十项 canonical Capability 的合集 10/10，`live.orchestrate` 仅存在于 FULL。
2. 媒体 Module 已显式引用三份 Stage 与三份 Responsibility 资产；原 ProductionProfile 与 Eval ref 保留，未删除旧合同或改变其他七 Module。
3. 新合同拒绝未知字段、责任映射漂移、重复值、缺槽、非 FULL 直播能力泄漏、Stage 环和 protected review 合并；外部发布批准与 Receipt 对账保持为独立治理责任。
4. active-installation resolver 只在 `published + signature + active composition lock + exact artifact digest + immutable mirror hash` 全部一致时加载 typed payload；撤销、未签名、digest 漂移、路径逃逸和跨租户均返回失败关闭。
5. 实现提交：`aos-platform/m1@9cb95574`；证据：`.evidence/workshop/2026-08-25-w7-01-signed-stage-responsibility-capability-mapping.json`。

### 6.2 验证

- W6-01/W6-02/W7-01 邻接专项与累计：`43 passed / 7 warnings`；
- OpenAPI 与 deterministic Domain Router：`22 passed / 2 subtests / 7 warnings`；
- Web 全量：`232 files / 2130 tests`，production build `344 modules`；
- Alembic：单头 `w6_009`；安全扫描器自测 `9 passed`，W7-01 定向 `13 files / critical=0 / warning=0`；
- 六份 JSON、Python compileall 与 `git diff --check` 通过；
- 内置浏览器在 `1280/1440/1920` 三档宽度完成媒体工作台验收：无横向溢出，degraded、`VISUAL_FIXTURE_ONLY`、无写入口与三类只读 Tab 可见，console error 为 0。

较大历史集合中仍可独立复现两个既有 fixture/旧 candidate 基线缺口：W2C review fixture 未建立现有 store 已要求的 `aip_review_rule_revision`；1.3 candidate 已存在未导出的旧 content 目录。二者均不由 W7-01 变更新增，也未被包装成 W7-01 GREEN。

### 6.3 方案—代码一致性与边界

- “原子 Skill → Logic 编排 → 数字同事绑定 → 工作台贡献视图”保持不变：模板仅冻结 capability/责任/Stage 合同，不固定 Agent 数量，不产生第二运行真源。
- Candidate/合同/浏览器 GREEN 不等于已签名发布或租户安装。真实租户变更、数据库迁移、Provider 调用、媒体生成、外部发布、Bundle publish/install 与 release 全部为 0。
- W7-01 的代码/合同/浏览器切片闭合，运营发布门继续保留；后继唯一入口为 W7-02 的 Profile 建议、预计成本区间与用户确认，仍须独立 authority 和 fail-closed 门。

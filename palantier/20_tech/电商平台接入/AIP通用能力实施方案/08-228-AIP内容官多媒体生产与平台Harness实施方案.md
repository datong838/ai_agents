# 228-AIP 内容官多媒体生产与平台 Harness 实施方案

> 状态：**待评审 · 不授权编码**
> 对应阶段：AIP-9。

## 1. 边界

内容官是“内容总监 + 专业 Agent 团队”，不是一个万能 Prompt。首期聚焦电商可复用能力：内容策略、脚本、标题、素材装配、质量门、产物与发布草稿。平台直接发布仍属于 G5/G6。

## 2. 复用既有设计

- 短视频：脚本+模板 -> 商品图/TTS/字幕/BGM -> FFmpeg 合成。
- 数字人直播：控制层、智能层、引擎层；C2 Session 外置。
- 平台 Harness：抖音/快手/视频号/小红书的规则、规格和发布能力差异。
- OpenMontage 的“管线即配置、工具即技能、Stage Gate”模式。
- AGPL 资产仅参考，不打包；每个素材必须有 license/provenance。

## 3. Canonical 对象

| 对象 | 说明 |
|---|---|
| ContentBriefRevision | 商品/受众/渠道/目标/禁忌/证据 |
| ContentPipelineRevision | 节点、工具、模型、质量门、预算 |
| MediaAssetRef | 原图/音频/BGM/字幕/模板及授权 |
| MediaJob | C1 submit/status/artifact/receipt |
| AvatarSession | C2 open/push/close/health/kill switch |
| ContentDraft | 文案、脚本、标题、封面、平台版本 |
| ContentEvalReport | 事实、合规、品牌、平台、技术质量 |
| PublishProposal | 平台、账号、时间、素材 revision、审批 |

## 4. 运行链

```text
Brief approval
 -> product/Wiki/evidence read
 -> strategy + script
 -> asset selection
 -> C1 MediaJob / C2 session preparation
 -> stage gates
 -> ContentDraft + EvalReport
 -> human review
 -> PublishProposal (不在本波执行)
```

商品功效、价格、库存、活动、达人身份等事实必须引用真实 Object/Evidence，禁止模型臆造。

## 5. 平台 Harness 结构

每个平台 Skill 包含：输入/输出 schema、素材规格、文本限制、敏感词/功效边界、账号能力、API/UI capability probe、限流、回执、EvalPack。平台规则有时效，开发当期必须核验官方来源。

## 6. 文件边界

```text
solution-packs/ecommerce-growth/agents/content_officer/*
solution-packs/ecommerce-growth/skills/content/*
adapter-packs/social-content/*
services/aos-api/aos_api/aip_media_jobs.py
services/aos-api/aos_api/aip_avatar_sessions.py
services/aos-api/aos_api/aip_content_pipeline.py
apps/web/src/pages/ecommerce/ContentWorkbench.tsx
apps/web/src/pages/ecommerce/ContentPipelineRunPage.tsx
```

## 7. 分波

- C0：ContentBrief/Asset/License/StageGate 契约。
- C1：只生成文案/脚本/标题草稿。
- C2：短视频 MediaJob，使用真实上架商品素材。
- C3：直播稿与 Session 沙箱，必须人工在场和 kill switch。
- C4：平台 Harness capability probe 与发布草稿。
- C5：G5/G6 评审后逐平台开放受控发布。

## 8. 验收

- 所有素材可追溯来源、授权和 hash。
- C1/C2 超时、GPU 不可用、产物损坏不显示成功。
- 高风险宣传、未验证功效、过期价格/库存被质量门拦截。
- 发布按钮在 G6 前只能创建 Proposal/Draft。
- 同一 ContentBrief 可派生平台版本，但共享事实不可被平台 Prompt 改写。

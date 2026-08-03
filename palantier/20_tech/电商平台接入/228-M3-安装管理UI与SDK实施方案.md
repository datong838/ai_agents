# 228-M3 安装管理 UI 与 SDK 实施方案

> 状态：**v1.4 评审通过 · M3-2 GREEN · M3-3 开工审计与文件所有权已冻结**
> 起始代码基线：`aos-platform m1@d85992b`
> 当前代码基线：`aos-platform m1@7f6e80a`（五分支同步，远程 `origin/m1` 已更新）
> 上位约束：M1、M2-A、M2-B 已冻结并 GREEN；M3 不重画架构
> 后续门禁：M3 GREEN 后方可进入 M4；M5 完成前不得进入电商 G0～G6

## 0. 使用的 Rules

1. 先复核 M0、M2 公共契约、M2-B 实现和最终证据，再冻结 M3 文件边界。
2. M3 只做现有 Registry/Composition/Installation 能力的 TypeScript SDK 与 UI 映射，不新增后端架构。
3. 不修改 PostgreSQL 真源、immutable/hash payload、状态机、权限、receipt、CAS 或 evidence 语义。
4. 不修改通用 `apps/web/src/api/client.ts` 的返回形状，不把资产控制 SDK 混入 Ontology SDK。
5. 页面移除隐式 Mock fallback，真实加载、空、错误、冲突、无权限和禁用状态必须可验证。
6. 每波先专项测试，再浏览器真实 API，再 Web/平台累计回归；全部 GREEN 才进入下一波。

## 1. 当前审计结论

M2-B 已在 `m1@d85992b` 完成 Composition 与 Installation 控制面，具备 M3 所需的后端事实和 mutation 安全边界。现有 Web 的 `/apollo/assets` 路由已经存在，但 `AssetBundlesPage.tsx` 仍请求不存在的 `/v1/assets`，且无数据或失败时回退 `MOCK_ASSET_BUNDLES`，因此页面展示不具备事实性。

M3 的核心不是再设计资产平台，而是建立一层薄的、可测试的 TypeScript adapter，把已存在的 Canonical API 安全地交给页面，并将现有 FDE 资产页改造成 Registry、Composition lock 和 Installation history 的真实管理入口。

## 2. 范围与非目标

### 2.1 本阶段交付

- Registry 资产列表/详情/版本事实展示。
- Composition resolve、lock 详情、依赖边、permission/migration/contribution diff 展示。
- Installation list/detail/history、revision/decision/event/evidence 展示。
- create、submit、approve、reject、apply、verify、rollback 的受控 UI。
- 专用 TypeScript 类型、API adapter、幂等键与强 If-Match 处理、错误映射。
- 加载/空/错误/无权限/marking 隐藏/CAS 冲突/禁用/重试状态。
- 单元、组件、契约、浏览器和累计回归证据。

### 2.2 明确不做

- 不新增或修改后端表、migration、DTO、端点、状态或状态边。
- 不实现 installation upgrade/replace composition，不新增 failed/blocked/upgrading。
- 不在浏览器中运行 Resolver、重算 lock/diff/evidence hash 或生成 evidence。
- 不执行真实 Bundle，不 apply migration，不接触生产 Secret/商城数据/生产写回。
- 不做 M4 Evidence/Case 页面，不创建 M5 电商包，不开发 G0～G6。
- 不把 `packages/ontology-sdk` 扩展成资产安装 SDK。

## 3. 现有能力到 M3 的映射

| M3 需求 | 已有后端能力 | 现有代码 | M3 适配 |
|---|---|---|---|
| 资产列表/详情 | `/v1/asset-bundles`、bundle/version GET | `routers/asset_bundles.py` | 替换 `/v1/assets` 和 Mock fallback |
| 组合解析 | POST `/v1/bundle-compositions:resolve` | `composition_service.py` | SDK 传严格 request + Idempotency-Key |
| lock 详情 | GET composition lock | `composition_store.py` | 依赖图与三类 diff 只读呈现 |
| 安装列表 | GET `/v1/bundle-installations` | `installation_service.list` | state/limit/offset 分页筛选 |
| 安装详情/历史 | GET installation | `InstallationRecord` | 展示 current/decision/events/evidence/pointers |
| 创建安装 | POST installations | `installation_service.create` | 传 compositionId/lockRevision/overlayRevision/displayName |
| 状态操作 | 六个 action | `installation_service.py` | 幂等键 + body etagVersion 构造 If-Match |
| 审批确认 | approve 四个 hash | `ApproveInstallationRequest` | 从 lock/record 只读填充，用户确认但不编辑 |
| 冲突/权限 | 409/412/403/404 和稳定错误码 | policy/header/router | SDK 结构化映射，页面失败关闭并回读 |
| 证据 | 服务端 event evidence | `installation_evidence.py` | 只展示服务端 evidence，不允许客户端输入 |

## 4. 冻结的 SDK 边界

### 4.1 位置与依赖

首选在 Web 内新增专用模块，不新增 workspace package：

```text
apps/web/src/api/assetControl/
  types.ts
  client.ts
  idempotency.ts
  errors.ts
  client.test.ts
```

原因：当前唯一消费者是 Web；现有 `packages/ontology-sdk` 领域边界不同；先以最小改动验证调用契约。未来出现第二个独立消费者后，再通过独立 ADR 抽成 `packages/asset-control-sdk`。

### 4.2 调用规则

- Registry GET 可复用通用 `apiGet`；安全敏感控制面调用经 `assetControl/client.ts`。
- 不修改通用 client 的返回类型。create/get/action 的强 ETag 可校验但 action 的 If-Match 以响应 body `etagVersion` 为权威构造。
- 每个用户命令生成一个 1～160 字符幂等键；同一命令的网络重试复用原键，新命令使用新键。
- submit/apply/verify 的 body 必须为严格 `{}`；reject/rollback 只发送规范化 reason；approve 只发送服务端 lock 的四个 hash。
- 409/412 后清除乐观操作态、回读详情、显示“状态已变化”；不得自动覆盖。
- 401/403/404 不降级为 Mock；404 不区分不存在与 marking 隐藏。
- mutation 离线时必须禁用，不进入现有通用离线写队列。

### 4.3 类型范围

TypeScript 类型逐字段映射后端 JSON alias，至少覆盖：

- Registry bundle/version 的实际响应；
- `CompositionRequest`、`StoredCompositionLock` 与 resolved/edges/diff；
- `CreateInstallationRequest`、三个 action request；
- `InstallationListItem`、`InstallationRecord`、`InstallationListResponse`；
- revision、decision、event、server evidence；
- Canonical `ApiErrorBody` 与稳定错误码。

不手工发明后端字段。编码前用当前 OpenAPI 与 Pydantic DTO 建立契约 fixture，字段漂移测试失败关闭。

## 5. UI 信息架构与状态

保留现有 `/apollo/assets` 入口和 `S2Chrome`，将页面组织为三个互相关联的视图：

1. **资产 Registry**：kind/status/publisher 筛选，bundle 与版本详情，发布/签名/evidence 事实。
2. **组合预检**：选择 bundle 约束与环境，resolve 后展示解析结果、依赖边、三类 diff、冲突诊断和 lock hash。
3. **安装管理**：installation 列表、详情、完整历史、审批信息、evidence 与当前可执行动作。

如单文件膨胀，拆为：

```text
apps/web/src/pages/s2/assetBundles/
  AssetBundlesPage.tsx
  RegistryPanel.tsx
  CompositionPanel.tsx
  InstallationPanel.tsx
  InstallationDetail.tsx
  state.ts
  *.test.tsx
```

现有 `AssetBundlesPage.tsx` 保留导出兼容层，避免影响 `routes.tsx` 的懒加载名称。

### 5.1 真实状态门

| 状态 | 必须行为 |
|---|---|
| loading | 明确 skeleton/loading，不展示旧 Mock 数据 |
| empty | 显示 Registry/Installation 真实空态和下一步，不伪造数量 |
| error/500 | 显示稳定错误与重试；保留上次数据时标注 stale，不冒充成功 |
| 401/403 | 显示认证/权限状态，不泄漏资源信息 |
| 404 | 统一“不可见或不存在” |
| conflict 409/412 | 回读详情，突出当前 revision/etag |
| offline | 允许有标识的只读缓存；禁用 resolve/create/action |
| unsigned/unpublished | 禁用不合法下一步，以服务端事实说明原因 |

### 5.2 状态与动作矩阵

UI 仅把服务端状态映射成动作入口，服务端仍做最终授权：

| state | 可能动作 |
|---|---|
| draft | submit |
| submitted | approve 或 reject |
| approved | apply |
| applied | verify |
| active | rollback |
| rejected / rolled_back | 终态，无后续 mutation |

角色未知或权限不足时可禁用/隐藏按钮，但不能在前端声称授权通过。approve 必须呈现 maker-checker 提示与四个 hash；reject/rollback reason 必填并规范化。

## 6. 开发拆分与文件所有权

### M3-0 实施结果（2026-08-03）

M3-0 已由四个独立 worker 从 `m1@d85992b` 并行完成，并由总控逐提交审查、集成到 `m1@435de34`；随后保留 Worker 原始提交，以真实 merge 历史将 `m1` 与四个 Worker 分支统一到 `dff51c1`：

| Worker | 交付 | 集成提交 |
|---|---|---|
| W1 | Composition/Installation TypeScript DTO 与类型 fixture | `d460c29` |
| W2 | Registry 真实动态响应、失败关闭 parser 与 fixture | `e839e8c` |
| W3 | 11 个 control operation 的 OpenAPI/header/ETag/error 契约测试 | `435de34` |
| W4 | 前端 operation map、header 与错误矩阵 | `f7937b0` |

验证结果：前端专项 14/14、Web 全量 1795/1795、TypeScript GREEN、Web production build GREEN；后端 Registry/Composition/Installation/OpenAPI 累计 77/77。完整证据见 [`2026-08-03-M3-0契约与测试夹具冻结证据.md`](../evidence/m0/m3-ui-sdk/2026-08-03-M3-0契约与测试夹具冻结证据.md)。

M3-0 未修改页面、通用 API client、后端生产代码、数据库或状态机。Registry OpenAPI 仍是动态 object，前端以真实 Store/API 公共投影 fixture 和失败关闭 parser 冻结；后端合法增加字段时必须显式更新契约。下一步只允许进入 M3-1。

### M3-0：契约与测试夹具冻结

**目标：** 从 OpenAPI/Pydantic 和真实响应冻结 TypeScript 字段与错误矩阵。

- 新增 `apps/web/src/api/assetControl/types.ts`、契约 fixtures 和类型测试。
- 记录 Registry 实际响应形状；若与文档不同，以代码/OpenAPI 为准并先回写本方案。
- 不修改页面和生产调用。

**退出门：** 类型检查、fixture 校验、11 个 operation/path 映射通过。

### M3-1：专用 SDK Adapter

**目标：** 安全、可测试地调用全部 Registry/Composition/Installation 能力。

- 新增 `client.ts`、`idempotency.ts`、`errors.ts` 和测试。
- 覆盖 header、body、query、URL 编码、幂等重试、If-Match、错误映射。
- 证明 mutation 不进入离线队列；不修改通用 client 返回形状。

**退出门：** 11 个控制面 operation + M3 所需 Registry GET 契约测试全绿。

#### M3-1 实施结果（2026-08-03）

M3-1 已在 `m1@89bbb98` 收口：新增专用 `client.ts`、`idempotency.ts`、`errors.ts` 及黑盒测试，覆盖 Registry GET、Composition resolve/get、Installation create/list/get 和六个 action。Mutation 不进入通用离线队列，离线状态在 fetch 前失败关闭；同一命令重试复用品牌化幂等键；action 使用强 `If-Match`，安装响应 ETag 必须与 body `etagVersion` 一致。

总控审查额外修正两项安全语义：HTTP 500 视为结果未知，必须先刷新并以原幂等键重试；`OFFLINE_MUTATION_DISABLED` 视为发送前明确未执行，不得混同网络中断。

验证结果：Asset Control 专项 41/41、Web 全量 1822/1822、TypeScript GREEN、production build GREEN、后端 Registry/Composition/Installation/OpenAPI 77/77。生产页面、通用 `api/client.ts`、后端、数据库和状态机均未修改。完整证据见 [`2026-08-03-M3-1专用SDK-Adapter回归证据.md`](../evidence/m0/m3-ui-sdk/2026-08-03-M3-1专用SDK-Adapter回归证据.md)。

#### M3-1 四路文件所有权（2026-08-03 开工冻结）

| 路线 | 独占文件 | 责任边界 |
|---|---|---|
| W1 | `assetControl/idempotency.ts`、`idempotency.test.ts` | 生成 1～160 字符命令键；同一命令重试复用，新命令不复用；不持久化 Secret |
| W2 | `assetControl/errors.ts`、`errors.test.ts` | 规范化网络错误和 400/401/403/404/409/412/428/500；404 不区分不可见与不存在；暴露 conflict/refresh 语义 |
| W3 | `assetControl/client.ts` | 生产 SDK adapter：Registry GET、Composition resolve/get、Installation create/list/get/六 action；不调用通用离线写队列 |
| W4/总控 | `assetControl/client.test.ts` | 从冻结的 `types/registry/operations` 反向验证路径、query、body、header、URL 编码、幂等重试、If-Match、ETag 与失败关闭 |

协作约束：W1/W2 不修改 `client.ts`；W3 不修改 W1/W2 文件和测试；W4 只写黑盒契约测试。公共导出若必须增加，统一由总控在集成阶段做最小收口。生产页面、通用 `api/client.ts`、后端、数据库和状态机均不在本波文件所有权内。

M3-1 集成顺序固定为 W1 → W2 → W3 → W4/总控；每路提交后审查文件边界和专项测试，最终执行 Asset Control 专项、Web 全量、TypeScript、production build。全部 GREEN 后才可标记 M3-1 完成并进入 M3-2。

### M3-2：Registry 真实化与只读安装视图

**目标：** 先移除虚假数据，再接入只读事实。

- 改造 `AssetBundlesPage.tsx`，切换 `/v1/asset-bundles`。
- 移除生产路径的 `MOCK_ASSET_BUNDLES` fallback；测试 fixture 留在测试文件。
- 增加真实 loading/empty/error、bundle/version 详情、installation list/detail/history。

**退出门：** 空 Registry、500、403/404、分页、刷新回读组件和浏览器验证通过。

#### M3-2 开工审计与四路文件所有权（2026-08-03）

开工审计确认：当前 `AssetBundlesPage.tsx` 请求不存在的 `/v1/assets`，并把 loading、真实空数组、响应漂移、网络错误及 401/403/404/500 全部静默替换成 `MOCK_ASSET_BUNDLES`；旧 channel/components/changelog 模型与真实 Registry 契约不兼容。现有两套页面测试同样锁定 Mock 成功数据，必须替换。

另发现 Installation list/detail 目前只有 TypeScript 静态类型，缺少与 Registry 等价的运行时失败关闭 parser。M3-2 在展示服务端事实前先补该 parser；详情只能宣称展示 current revision、current decision 和完整事件时间线，不得声称拥有每个历史 revision 的完整快照。

| 路线 | 独占文件 | 责任边界 |
|---|---|---|
| 总控前置 | `assetBundles/model.ts` | 冻结只读 `ReadState`、选择键和分页视图契约，供并行路线共同消费 |
| W1 | `api/assetControl/installations.ts`、fixture/test；最小修改 `client.ts` | Installation list/detail 运行时 parser、状态/hash/时间/事件结构失败关闭；SDK GET 接入 parser |
| W2 | `assetBundles/readHooks.ts`、`readHooks.test.tsx` | 五个只读 hook、request sequence 防乱序、loading/empty/error/refresh/stale；403/404 清除旧数据 |
| W3 | `assetBundles/RegistryPanel.tsx`、`InstallationPanel.tsx`、`InstallationDetail.tsx` 及各自测试 | 纯只读视图；真实状态、服务端分页、事件/evidence/pointer 展示；不直接调用 API |
| W4/总控 | `AssetBundlesPage.tsx` 和现有两套页面测试 | 保留 named export 与 `/apollo/assets`；接线 hooks/panels；删除生产 Mock 和 `/v1/assets`；集成状态验证 |

M3-2 不新增 mutation UI，不修改通用 `api/client.ts`、后端、数据库、路由或状态机。Registry 无服务端分页，不伪装全局分页；Installation 只按服务端 `state/limit/offset` 分页。详情请求必须携带 publisher；刷新失败如保留旧数据必须显示 stale，401/403/404 必须清除旧数据。

退出门补充：生产源码中 `MOCK_ASSET_BUNDLES` 与 `\"/v1/assets\"` 零命中；pending promise 只显示 loading；真实 `[]` 显示 empty；403 显示无权；404 统一不可见或不存在；500/网络显示重试；分页边界和乱序响应通过；M3-3/M3-4 的 resolve/create/action 入口不可达。

#### M3-2 实施结果（2026-08-03）

M3-2 已在 `m1@7f6e80a` 收口。资产页保留 `/apollo/assets` 和原 named export，生产路径已删除 `MOCK_ASSET_BUNDLES` 与错误端点 `/v1/assets`，通过专用 SDK 映射 Canonical Registry 和 Installation 只读事实。新增 Registry bundle/version 详情、Installation 服务端分页、current revision/decision、事件/evidence/pointer 展示，并明确事件时间线不等于历史 revision 完整快照。

只读 hooks 覆盖 loading、empty、refresh、stale、403、404、网络/500 和乱序响应；403/404 清除旧数据，刷新失败保留数据时显式标记 stale。Installation 响应增加运行时失败关闭解析，未增加 mutation UI，也未修改通用 API client、后端、数据库、路由或状态机。

验证结果：M3-2/Asset Control 前端专项 72/72、Web 全量 1842/1842、TypeScript GREEN、production build GREEN、后端 Registry/Composition/Installation/OpenAPI 77/77；生产源码两项禁用字符串均零命中。浏览器确认 Registry/安装管理双页签、只读边界和 API 不可达时的诚实错误态；浏览器沙箱未能直连宿主机 `:8080`，真实响应形状由后端契约测试、SDK parser 与组件 fixture 覆盖。完整证据见 [`2026-08-03-M3-2真实只读资产页回归证据.md`](../evidence/m0/m3-ui-sdk/2026-08-03-M3-2真实只读资产页回归证据.md)。

### M3-3：Resolve/Create 与 Diff

**目标：** 完成安装前预检，不执行安装 action。

- 构造 CompositionRequest，展示 resolve 冲突路径、resolved/edges 和三类 diff。
- 展示 immutable lock/hash；从 lock 创建 draft installation。
- 未签名/未发布/冲突场景失败关闭。

**退出门：** resolve 成功/冲突、重复点击幂等、刷新回读、create 失败场景通过。

#### M3-3 开工审计（2026-08-03）

基于五分支同步基线 `m1@7f6e80a` 的代码、OpenAPI、Pydantic DTO 与 M3-2 页面复核，确认本波不是补建后端能力，而是安全开放已有 `POST /v1/bundle-compositions:resolve`、`GET /v1/bundle-compositions/{composition_id}/locks/{revision}` 和 `POST /v1/bundle-installations`。

审计发现以下 P0 缺口，编码前按本节冻结：

1. `resolveComposition()` 与 `getCompositionLock()` 当前把成功 JSON 直接断言为 `StoredCompositionLock`，没有 Registry/Installation 等价的运行时失败关闭 parser；缺字段、额外字段、非法 UUID/hash/enum/时间均可能进入 UI。
2. `createInstallation()` 只核对 ETag 与 `etagVersion`，尚未复用 Installation 详情 parser；现有测试使用 active fixture，不能证明首次 draft/revision 1 语义。
3. resolve/create 出站 body 只受 TypeScript 约束，运行时额外字段仍会被 `JSON.stringify` 发出；本波增加 exact serializer，但复杂 semver 最终仍由服务端裁决，前端不得复制 Resolver。
4. resolve 成功必须立即 GET 回读同一 `compositionId/revision`，核对完整 payload、revision 与四个服务端 hash；未回读或不一致的 lock 不得用于 create。
5. 输入字段或 Registry 选择发生变化时，既有 lock 立即标记 stale 并禁用 create。网络/500 结果未知时只允许复用原 `Idempotency-Key` 恢复同一命令，不得换新键重试。
6. 后端请求校验/解析资源上限可能返回 HTTP 422，`RESOLUTION_LIMIT_EXCEEDED` 必须进入稳定错误矩阵；不能继续落入 unknown。409 冲突详情只有在通过冻结 parser 后才能结构化展示，否则只展示 code/message/traceId。
7. 页面不运行 Resolver，不重算 canonical hash、diff 或 evidence。依赖“图”首版采用服务端事实表，不推断不存在的层级或历史。

真实契约边界：

- Resolve 请求必含 `requested/platformApiVersion/platformRelease/environment`，可含 `registrySnapshotHash/currentInstallationRef`；`requested` 为 1～64 个唯一坐标。
- Stored lock 顶层固定为 `compositionId/revision/payload/lockHash/permissionDiffHash/migrationPlanHash/contributionDiffHash/createdAt`；payload 固定包含 canonical request、snapshot hash、resolved、edges、capability providers、三类 diff 和可空 current installation ref。
- Create body 只允许 `compositionId/lockRevision/overlayRevision/displayName`；成功结果必须是完整 Installation 响应并满足强 ETag。首次创建只获得 draft，不自动提交或安装。

#### M3-3 四路文件所有权（2026-08-03）

| 路线 | 独占文件 | 责任边界 |
|---|---|---|
| W1 | `api/assetControl/compositions.ts`、`compositionFixtures.ts`、`compositions.test.ts` | StoredCompositionLock 失败关闭 parser；resolve/create exact serializer；UUID/hash/enum/time/claim/diff 形状与必要交叉引用；禁止重算 hash/diff |
| W2 | `assetBundles/commandModel.ts`、`commandModel.test.ts`、`resolveCreateHooks.ts`、`resolveCreateHooks.test.tsx` | 独立命令状态、输入 revision、幂等身份、双击抑制、resolve 后 GET 回读、unknown outcome、stale create gate；不渲染 UI |
| W3 | `assetBundles/CompositionPanel.tsx`、`CompositionLockDetail.tsx`、`CompositionDependencyPanel.tsx`、`CompositionDiffPanel.tsx` 及各自测试 | 受控表单与纯展示组件；完整展示服务端 lock/resolved/edges/providers/三类 diff；不直接调用 API、不生成幂等键 |
| W4/总控 | 最小修改 `assetControl/client.ts`、`client.test.ts`、`operations.ts`、`errors.ts`/测试、`installationFixtures.ts`；独占 `AssetBundlesPage.tsx` 与两套页面测试 | 接入 parser/serializer、create 详情 parser、422 错误策略、根页流程和成功后只读回读；禁止六个 M3-4 action 入口 |

协作约束：W1 不修改 client；W2 只消费现有 SDK 公共方法并通过依赖注入测试；W3 只消费 props/types；W4/总控不改写 W1～W3 独占文件。共享导出与接线只由总控最小收口。四路完成后按 W1 → W2 → W3 → W4/总控顺序审查集成。

#### M3-3 退出门补充

1. resolve/get 共用失败关闭 parser；出站请求拒绝未知字段、snake_case、租户/权限/hash 注入，create 只发四字段。
2. resolve 201 后必须 GET 回读；payload、revision 和四 hash 任一不一致即失败关闭，create 不可达。
3. running/reconciling 阶段双击只产生一次调用；网络/500 的同命令恢复复用原键，新用户命令使用新键。
4. 409 dependency conflict/cycle 与 422 resolution limit 有稳定失败态；401/403/404 清除残留结果，404 不泄漏 marking 隐藏信息。
5. 任一输入变化使 lock stale；只有已回读、非 stale 的 lock 可创建 draft。create 成功后回读 Installation list/detail，不乐观伪造状态。
6. Lock 元信息、canonical request、resolved、capability providers、edge 和 Permission/Migration/Contribution 三类 diff 均来自响应且可验证；四 hash 不可编辑。
7. submit、approve、reject、apply、verify、rollback、客户端 hash/diff/evidence 计算、离线排队和自动重试全部不可达。
8. 专项、Asset Control 累计、Web 全量、TypeScript、production build、后端 77 契约回归及浏览器场景全部 GREEN，才允许进入 M3-4。

### M3-4：审批、Apply/Verify/Rollback

**目标：** 接通现有六条状态边。

- 实现状态/角色感知动作、确认对话框、reason 输入、hash 审批确认。
- 处理 maker-checker、409/412、回放、双击、网络失败、marking/tenant 错误。
- 展示服务端 revision/decision/event/evidence 与 active pointers。

**退出门：** 完整 dry install 闭环和 rollback 浏览器验证；客户端 evidence 注入不可达。

### M3-5：总控收口

- Web 专项、全量 test、typecheck、production build。
- 后端资产域和 Router/OpenAPI 契约回归，确认 M3 未改变后端 schema/route。
- 两角色 maker-checker、同 ETag 并发、刷新回读、空/错/无权全场景证据。
- 更新上位状态、路线图、项目上下文和最终证据。

## 7. 测试矩阵

### 7.1 SDK P0

- 路径/query/body/JSON alias 精确；未知字段不被悄然发出。
- Idempotency-Key 单命令稳定、新命令唯一、重试复用。
- action 强 If-Match 精确为 `"etagVersion"`。
- approve 四 hash 来自当前 lock/record，不可编辑。
- 400/401/403/404/409/412/428/500 结构化映射。
- 网络失败、离线和双击不产生隐式第二命令。

### 7.2 UI P0

- loading/empty/error/stale/offline/无权状态不显示 Mock 成功事实。
- kind/status/publisher、state 和分页行为正确。
- dependency edge、diff、history、decision、evidence、pointer 与响应一致。
- 非法状态动作不可达；服务端拒绝后回读且不乐观伪成功。
- 404 不泄漏 marking 隐藏信息；maker-checker 失败明确。

### 7.3 浏览器 P0

1. 空 Registry；2. API 500；3. 未签名/未发布；4. 依赖冲突；5. resolve 成功；
6. create/submit；7. 不同用户 approve；8. apply/verify/active；9. rollback；
10. 同 ETag 并发冲突；11. 刷新回读；12. tenant/marking/role 失败关闭。

### 7.4 累计门

- Web 新增专项 + Web 全量、typecheck、build。
- 现有 backend asset_registry 与 Router/OpenAPI 专项。
- Ontology SDK、Desktop 与平台要求的累计回归，不允许新增失败。
- changed-file 格式、安全扫描和生成物确定性检查。

## 8. 风险与控制

| 风险 | 等级 | 控制 |
|---|---:|---|
| Registry 返回为动态 dict，前端误猜字段 | P0 | M3-0 真实响应 fixture + OpenAPI/代码核对 |
| 通用 client 吞 ETag | P1 | body `etagVersion` 构造 If-Match；专用 adapter，不改全局返回形状 |
| 通用离线队列重放安全 mutation | P0 | asset-control mutation 显式禁用离线，不走通用队列 |
| 前端复刻状态机后与后端漂移 | P0 | UI 矩阵只控制入口，服务端为最终裁决；412 后回读 |
| Mock fallback 掩盖失败 | P0 | 生产页面删除 fallback，fixture 仅存测试 |
| 审批 hash 来自陈旧 lock | P0 | action 前回读当前详情/lock；CAS 与服务端 hash 再校验 |
| 用户工作区改动被覆盖 | P0 | 文件所有权检查、显式暂存；避开 `AppShell.tsx` |

## 9. 回滚

- 每小波单独提交，可按波回滚。
- 页面改造保留 `/apollo/assets` 路由和原导出名，回滚不影响导航深链。
- SDK 是新增模块；回滚页面引用即可停用，不触碰后端数据。
- 不通过恢复 Mock 掩盖故障；必要时回滚到明确错误/维护态。

## 10. 完成定义

M3 只有在以下条件全部满足时才可标记 GREEN：

1. 页面完全切换真实 `/v1/asset-bundles` 与现有 M2 控制面，生产路径无隐式 Mock fallback。
2. SDK 精确覆盖所需 API、幂等、If-Match 和稳定错误；无后端架构变更。
3. Registry、resolve/diff、installation/history、六 action 和 server evidence 均可真实回读。
4. 空/错/无权/冲突/离线/刷新状态通过组件与浏览器验证。
5. 专项、Web 全量、typecheck/build 和平台累计回归 GREEN，证据归档。
6. 上位状态和 AOS 项目开发上下文同步更新。

当前结论：**M3-2 已 GREEN；以五分支同步基线 `m1@7f6e80a` 进入 M3-3 Resolve/Create 与 Diff。继续按 M3-3～M3-5 实施且不新增架构。**

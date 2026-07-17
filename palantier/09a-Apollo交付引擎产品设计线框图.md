# 09a · Apollo 交付引擎产品设计线框图

## Hub · Spoke · Channel · Ferry · Asset · Change · Config

> **文档性质**：[`09 产品方案`](09-Apollo交付引擎产品方案.md) 的 **UI/UX 线框规格** · 研发可直接对照实现  
> **版本**：v1.0 · 2026-07-17  
> **绘制原则**：布局与控件优先对齐 Palantir **Apollo Core** 官方概念（Hub/Spoke · Catalog · Orchestration · Channel promotion · Recall · Change Management · Config Override）；行业增强（Lite Spoke · FDE Asset Bundle · Vault 引用）按 09 v1.2 绘制  
> **对标在线**：  
> · [Apollo Core · Overview](https://www.palantir.com/docs/apollo/core/overview/)  
> · [How Apollo works](https://www.palantir.com/docs/apollo/core/how-apollo-works/)（Plan · Constraints · Channel · Recall · Rollback）  
> · [Apollo docs 首页](https://www.palantir.com/docs/apollo/)（Environments · Products · Release Channels · Change Management）  
> · [Config overrides](https://www.palantir.com/docs/apollo/managing-entities/set-config-overrides/)  
> · [Maintenance windows](https://www.palantir.com/docs/apollo/apollo-getting-started/introduction-maintenance/)  
> · [Deploying Across Security Domains](https://blog.palantir.com/deploying-across-security-domains-449c786d92c0)（Remote Hub · Bundle）  
> **关联**：[09 v1.2+](09-Apollo交付引擎产品方案.md) · [03 §3.5](03-对标Palantir-AOS-PRD框架.md) · [08a WF-WS-09](08a-Workshop产品设计线框图.md) · [T09](20_tech/T09-Apollo交付引擎详细技术方案.md)  
> **HTML Demo**：✅ [foundry/html](foundry/html/) **v1.6.0** · `apollo-hub` / `release` / `spoke` / `ferry` / `assets` / `change-mgmt` / `config`

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 中文 | 线框内按钮、标签、Tab 一律中文；专有名词保留 Hub / Spoke / Channel / Plan / Probe / Recall / Ferry |
| 先方案后代码 | 仅文档；HTML Demo 已齐，本篇补 Markdown 规格真源 |
| 承接 09 | 映射 OPS-001～010 · §9 Backlog WF-AP-01～07 |
| 优先官方概念 | 无单一目标态；订 Product + Channel；Spoke **出站轮询**；环境设定变更走 Change Management |
| 通用线框 | `{Hub}` `{Spoke}` `{Product}` `{Channel}` `{Bundle}` `{Plan}` |
| 与上下游自洽 | 工作台只留发布入口（08a WF-WS-09）；完整控制台在本篇 |

---

## 1. 信息架构（IA）

### 1.1 应用地图 · 对标 Apollo Environments / Products / Channels

> 官方：Hub 收遥测并下发 Plan；Spoke Agent 回报 Reported State / Probe 并执行 Plan；Catalog 承载 Product Release；**无钉死单一目标版本**。

```text
┌─ AOS 工作区 · 交付 Apollo（侧栏置底）──────────────────────────────────────┐
│  [≡]  工作区 ▾   🔍 搜「Apollo / Spoke」   [通知]  [用户]                   │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  舰队与环境                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐                                │
│  │ Hub 舰队总览      │→ │ Spoke / Entity   │                                │
│  │ WF-AP-01         │  │ 详情 WF-AP-03    │                                │
│  └──────────────────┘  └──────────────────┘                                │
│                                                                              │
│  发布与制品                                                                   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐          │
│  │ Release Channel  │  │ FDE Asset Bundle │  │ Ferry / Bundle   │          │
│  │ WF-AP-02         │  │ WF-AP-05         │  │ 向导 WF-AP-04    │          │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘          │
│                                                                              │
│  治理                                                                         │
│  ┌──────────────────┐  ┌──────────────────┐                                │
│  │ Change Mgmt 审批 │  │ Config Override  │                                │
│  │ WF-AP-06         │  │ + 维护窗口 AP-07 │                                │
│  └──────────────────┘  └──────────────────┘                                │
│                                                                              │
│  上游入口（非本层页面）                                                         │
│  ┌──────────────────┐                                                        │
│  │ 工作台 [发布 ▾]   │ → 08a WF-WS-09 · workshop-publish.html               │
│  └──────────────────┘                                                        │
└──────────────────────────────────────────────────────────────────────────────┘
```

### 1.2 页面对照表（09 OPS / Backlog → 本文线框 → HTML）

| 09 OPS | 线框 ID | 页面 | HTML Demo | 本章节 |
| --- | --- | --- | --- | --- |
| OPS-001 / 009（舰队面） | **WF-AP-01** | Hub 舰队总览 · Spoke 健康 / Probe | `apollo-hub.html` | §3 |
| OPS-004 / 003（Recall） | **WF-AP-02** | Release Channel 晋升管道 + hotfix + Recall | `apollo-release.html` | §4 |
| OPS-002 / 003 / 010 | **WF-AP-03** | Spoke / Entity 详情 · Plan · Full/Lite | `apollo-spoke.html` | §5 |
| OPS-006 / 007 | **WF-AP-04** | Ferry / Bundle 气隙向导 | `apollo-ferry.html` | §6 |
| OPS-008 | **WF-AP-05** | FDE Asset Bundle 库 | `apollo-assets.html` | §7 |
| OPS-009（审批） | **WF-AP-06** | Change Management 审批单 | `apollo-change-mgmt.html` | §8 |
| OPS-005 | **WF-AP-07** | Config Override · 维护窗口 · Vault 引用 | `apollo-config.html` | §9 |

### 1.3 Apollo 全局壳（Shell）

> 对标官方：Environments / Products / Release Channels / Change Management 分区；侧栏在产品壳内置底，不抢业务入口。

```text
┌──────────────────────────────────────────────────────────────────────────────┐
│ [☰]  AI操作系统 · Apollo          🔍 搜环境/制品…           🔔  👤         │
├──────────┬───────────────────────────────────────────────────────────────────┤
│ 侧栏     │  面包屑：工作区 / Apollo / {页面}                                   │
│          ├───────────────────────────────────────────────────────────────────┤
│ …业务层… │                                                                   │
│ ─────    │                    <<  主内容区  >>                                 │
│ 交付     │                                                                   │
│  · 舰队  │                                                                   │
│  · 通道  │                                                                   │
│  · Spoke │                                                                   │
│  · Ferry │                                                                   │
│  · 资产  │                                                                   │
│  · 变更  │                                                                   │
│  · 配置  │                                                                   │
└──────────┴───────────────────────────────────────────────────────────────────┘
```

**导航文案（对外）**：舰队总览 · 发布通道 · Spoke 详情 · Ferry 向导 · FDE 资产包 · 变更审批 · 配置覆盖。

---

## 2. 线框图例

| 符号 | 含义 |
| --- | --- |
| `[ 按钮 ]` | 可点击 |
| `{占位符}` | 动态字段 |
| `▾` | 下拉 |
| `● / ○ / ✕` | Probe 健康 / 部分失败 / 无响应 |
| `🟡` | 待审批 / 维护窗内暂停 |
| `🔴` | Recall / 紧急 hotfix |
| `🟣` | 行业定制增强（Lite Spoke · Asset Bundle） |

---

## 3. WF-AP-01 · Hub 舰队总览

**路由**：`/apollo/hub`  
**用户目标**：一眼看清各 Spoke 在线度、Probe、订阅 Channel、Full/Lite 档位  
**对齐**：09 §2 Hub-Spoke · OPS-001/009 · 官网 [Overview · Hubs/Spokes](https://www.palantir.com/docs/apollo/core/overview/)  
**Demo**：`apollo-hub.html`

```text
┌─ Apollo · Hub 舰队总览 ──────────── [发布通道 →] [Ferry 向导] ───────────────┐
│  Hub 区域：{cn-east-hub-01}    在线 Spoke：{5}/{6}    最近 Probe：{12秒前}   │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─ {spoke-prod-sh} ──────────── 健康 ─┐  ┌─ {spoke-prod-bj} ──── 健康 ─┐ │
│  │ Probe ● 正常 · 延迟 42ms           │  │ Probe ● 正常 · 延迟 38ms     │ │
│  │ 通道 stable · Bundle {2.14.1}      │  │ 通道 stable · Bundle {2.14.1}│ │
│  │ Full Spoke · 出站轮询开启          │  │ Full Spoke                   │ │
│  │ [打开详情]                         │  │ [打开详情]                   │ │
│  └────────────────────────────────────┘  └──────────────────────────────┘ │
│                                                                              │
│  ┌─ {spoke-lite-hz} ────────── 降级 ─┐  ┌─ {spoke-airgap-01} ─ 离线 ──┐ │
│  │ Probe ○ 部分失败 · 210ms  🟣Lite │  │ Probe ✕ 无响应 · 3 天前      │ │
│  │ 通道 beta · Bundle {2.15.0-rc.3}   │  │ Remote Hub / Ferry 待摆渡    │ │
│  │ 仅出站轮询 · 无入站                │  │ [打开详情] [启动 Ferry]      │ │
│  └────────────────────────────────────┘  └──────────────────────────────┘ │
│                                                                              │
│  提示：Hub 可自管；Spoke 不要求客户开入站端口。                               │
└──────────────────────────────────────────────────────────────────────────────┘
```

**验收**：卡片展示 Probe / Channel / Bundle / Full|Lite；点击进入 WF-AP-03；气隙离线可跳转 WF-AP-04。

---

## 4. WF-AP-02 · Release Channel 晋升管道

**路由**：`/apollo/channels/{product}`  
**用户目标**：查看 rc → beta → stable 健康晋升；执行 Recall；发起紧急 hotfix（旁路）  
**对齐**：09 OPS-004/003 · 官网 [How Apollo works · promotion / Recall](https://www.palantir.com/docs/apollo/core/how-apollo-works/)  
**Demo**：`apollo-release.html`

```text
┌─ Apollo · Release Channel 管道 ───────────────────── [Recall 可用] ──────────┐
│  Product：{aos-platform}     订阅语义：订 Channel，不钉死单一版本号             │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│     ┌─ rc ──────────┐    →    ┌─ beta · 当前 ─┐    →    ┌─ stable ─────┐  │
│     │ {2.15.0-rc.5} │         │ {2.14.2-beta} │         │ {2.14.1}     │  │
│     │ 2 Spoke       │         │ 1 Spoke 试点  │         │ 4 Spoke 全量 │  │
│     └───────────────┘         └───────────────┘         └──────────────┘  │
│                                                                              │
│  ┌─ 紧急 hotfix（旁路）────────────────────────────────────────────────────┐ │
│  │ 旁路 beta，直达选定 Spoke · 须变更审批                                   │ │
│  │ 版本：{2.14.1-hotfix.2}   目标 Spoke ▾   [提交紧急发布] [查看审批单]   │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌─ Recall 回滚 ───────────────────────────────────────────────────────────┐ │
│  │ 原因：健康晋升失败 / Probe 连续失败                                     │ │
│  │ 影响：订该 Release 的环境滚离坏版本                                     │ │
│  │ [执行 Recall]                                                           │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  晋升规则摘要：Reported State 过门槛 → 自动进下一 Channel；失败 → 自动 Recall │
└──────────────────────────────────────────────────────────────────────────────┘
```

**验收**：三档通道可视化；hotfix 强制链到 WF-AP-06；Recall 二次确认；文案禁止「钉死目标版本 vX.Y.Z 为唯一态」。

---

## 5. WF-AP-03 · Spoke / Entity 详情

**路由**：`/apollo/spokes/{spokeId}`  
**用户目标**：看当前版本、Plan 生命周期、rollback；切换 Full / Lite 叙事档位  
**对齐**：09 OPS-002/003/010 · Spoke 出站轮询 · Lite Compose  
**Demo**：`apollo-spoke.html`

```text
┌─ Apollo · Spoke 详情 · {spoke-prod-sh} ──── [回舰队] [配置覆盖] [变更审批] ──┐
│  状态：健康 ●     最近上报：{12秒前}     出站轮询：开启（无入站）              │
├──────────────────────────────────────────────────────────────────────────────┤
│  [ Full Spoke ]  [ Lite Spoke 🟣 ]                                           │
├───────────────────────────────┬──────────────────────────────────────────────┤
│  当前订阅                      │  最近 Plan                                   │
│  Product：{aos-platform}       │  PLAN-{20260716-031}  升级 → {2.14.1}       │
│  Channel：stable               │  约束：维护窗口内 · Probe 通过               │
│  Bundle：{2.14.1}              │  结果：成功 · 耗时 4m12s                     │
│  Asset Bundle：{1.3.2}         │  [查看日志] [手动触发 rollback]              │
│  Config Override：3 条         │                                              │
├───────────────────────────────┴──────────────────────────────────────────────┤
│                                                                              │
│  ┌─ Full Spoke 能力 ────────────┐  ┌─ Lite Spoke 能力（对照）────────────┐ │
│  │ K8s + Helm · 舰队完整        │  │ Compose / 单节点 · 垂直扩容为主 🟣 │ │
│  │ Delta / Ferry 完整           │  │ 部署+升级+出站+密钥注入；Ferry 分期 │ │
│  └──────────────────────────────┘  └─────────────────────────────────────┘ │
│                                                                              │
│  Reported State：版本 · Probe · Telemetry 摘要（只读表）                      │
└──────────────────────────────────────────────────────────────────────────────┘
```

**验收**：Full/Lite 对照可见；Plan 失败可 rollback；不出现「请客户开放入站端口」文案。

---

## 6. WF-AP-04 · Ferry / Bundle 向导

**路由**：`/apollo/ferry`  
**用户目标**：气隙 / 跨安全域：选 Bundle → 签名导出 → 物理/CDS 摆渡 → Remote Hub 导入校验  
**对齐**：09 OPS-006/007 · 博客 Deploying Across Security Domains  
**Demo**：`apollo-ferry.html`

```text
┌─ Apollo · Ferry / Bundle 向导 ───────────────────────────────────────────────┐
│  步骤：  ●1 选择 Bundle  →  2 签名导出  →  3 摆渡介质  →  4 气隙侧校验导入   │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  步骤 1 · 选择要 Ferry 的内容                                                │
│  ○ 平台 Product Release  {aos-platform@2.14.1}                               │
│  ○ 平台 + FDE Asset Bundle（版本同绑校验）                                    │
│  ○ 仅 Config Override 增量                                                   │
│  ○ Delta 增量包（相对 {spoke} 已报版本）                                     │
│                                                                              │
│  目标 Remote Hub / Spoke：{spoke-airgap-01} ▾                                │
│                                                                              │
│  [下一步：生成签名 tar.gz]                                                   │
│                                                                              │
│  护栏：破坏性大版本资产须经 beta 验证；签名失败禁止导入。                      │
└──────────────────────────────────────────────────────────────────────────────┘
```

**步骤 2～4（摘要线框）**：

```text
步骤 2：导出路径 → {ferry-aos-2.14.1-signed.tar.gz}  校验和 SHA256 · 签名者 {hub-key}
步骤 3：介质类型 ▾ U盘 / CDS / 人工 BTS    [标记已离站]
步骤 4：气隙侧 [校验签名] [导入 Catalog] [生成应用 Plan] → 回报 Reported State
```

**验收**：四步可走完；增量与全量可选；签名失败阻断。

---

## 7. WF-AP-05 · FDE Asset Bundle 库

**路由**：`/apollo/assets`  
**用户目标**：管理可交付实施资产（OKF / 工作台 Module / Agent），并绑定 Release Channel  
**对齐**：09 §6.1 OPS-008（相对纯 Apollo 的行业增强）  
**Demo**：`apollo-assets.html`

```text
┌─ Apollo · FDE Asset Bundle ────────────── [+ 上传 / 打包] ───────────────────┐
│  可交付资产版本化；与平台 Channel 版本同绑推进                                 │
├──────────────────────────────────────────────────────────────────────────────┤
│  搜索…   筛选：行业 ▾  绑定通道 ▾  状态 ▾                                    │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  ┌─ {电商选品-OKF} ──────────────────── v{1.3.2} · 绑定 stable ────────────┐ │
│  │ 含：Ontology 模板 · 工作台 Module 骨架 · Agent 配置 · Evals 快照         │ │
│  │ 兼容平台 Channel：stable ∈ [2.14.0, 2.15.0)                             │ │
│  │ [详情] [推到试点 Spoke] [导出 Ferry 包]                                  │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌─ {环科许可-OKF} ──────────────────── v{0.9.1} · 绑定 beta ──────────────┐ │
│  │ Schema 含破坏性候选 · 须 beta 验证后进生产                               │ │
│  │ [详情] [打开变更审批]                                                    │ │
│  └──────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  差异化：资产交付给客户（非黑盒行业 Ontology）                                │
└──────────────────────────────────────────────────────────────────────────────┘
```

**验收**：列表可见 `assetSemVer` + 绑定 Channel；推送进 Spoke 后 Reported State 回报资产版本。

---

## 8. WF-AP-06 · Change Management 审批

**路由**：`/apollo/changes/{chgId}`  
**用户目标**：审批环境设定 / 通道订阅 / 紧急发布；保证合规审计  
**对齐**：09 OPS-009 · 官网 Environment settings → Change Management  
**Demo**：`apollo-change-mgmt.html`

```text
┌─ Apollo · 变更审批 ──────────────────────────────────────────────────────────┐
│  左侧列表                              │  详情 CHG-{2026-0412}               │
│  ┌────────────────────────────┐       │  状态：🟡 待审批                     │
│  │ ● CHG-0412 紧急 hotfix     │       │  类型：紧急发布 / 通道旁路           │
│  │   待审批 · hotfix          │       │  Bundle：{2.14.1-hotfix.2}          │
│  ├────────────────────────────┤       │  目标 Spoke：{spoke-prod-sh}         │
│  │   CHG-0408 维护窗延长 2h   │       │  申请人：{ops-lead}                  │
│  │   已通过                   │       │                                      │
│  ├────────────────────────────┤       │  审批流                              │
│  │   CHG-0399 订阅改 beta     │       │  ● 平台值班  →  ○ 安全复核           │
│  │   已驳回                   │       │                                      │
│  └────────────────────────────┘       │  原因说明：{生产事故热修…}            │
│                                       │  [通过] [驳回] [要求补材料]           │
│                                       │                                      │
│                                       │  紧急发布：须 72h 内补齐复核签字       │
└──────────────────────────────────────────────────────────────────────────────┘
```

**验收**：环境设定变更不能静默生效；紧急发布有事后审计提示；链到审计日志（OPS-009）。

---

## 9. WF-AP-07 · Config Override · 维护窗口

**路由**：`/apollo/config/{spokeId}`  
**用户目标**：按 Product 版本区间覆盖配置；设维护窗口；密钥只存 Vault/KMS 引用  
**对齐**：09 OPS-005 · 官网 Config overrides / Maintenance windows  
**Demo**：`apollo-config.html`

```text
┌─ Apollo · Config Override · {spoke-prod-sh} ─────────────────────────────────┐
│                                                                              │
│  ┌─ 维护窗口 ──────────────────────────────────────────────────────────────┐ │
│  │ 每周：六 02:00–06:00（Asia/Shanghai）                                   │ │
│  │ 规则：窗内允许非紧急 Plan；窗外仅紧急（须 CHG）                         │ │
│  │ [编辑窗口]                                                              │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  ┌─ Overrides（按版本区间）────────────────────────────────────────────────┐ │
│  │ Product          区间              键                    值/引用         │ │
│  │ aos-platform     [2.14.0,2.15)   replicas              3               │ │
│  │ aos-platform     [2.14.0,2.15)   db.url                ${vault:db/url} │ │
│  │ aos-platform     *               feature.x             false           │ │
│  │ [+ 添加 Override]  [保存（需变更审批）]                                 │ │
│  └─────────────────────────────────────────────────────────────────────────┘ │
│                                                                              │
│  密钥护栏：禁止明文粘贴生产密钥；仅 Vault/KMS 引用；读取事件进审计。          │
└──────────────────────────────────────────────────────────────────────────────┘
```

**验收**：Override 保存进 Change Management；维护窗外非紧急 Plan 不强制执行；无明文密钥展示。

---

## 10. 旅程与组件清单

### 10.1 旅程 O · 私有化首次落地（Lite）

```text
Hub Catalog 已有 Product
  → WF-AP-03 Lite 安装指引（Compose）
  → Spoke Agent 出站轮询拉 Plan
  → Probe 绿 · Reported State 回报
  → WF-AP-05 拉一次 Asset Bundle
```

### 10.2 旅程 P · 健康晋升与 Recall

```text
WF-AP-02 rc 试点健康
  → 自动晋升 beta → stable
  → Probe 失败 → 自动 Recall
  → 受影响 Spoke rollback（WF-AP-03）
```

### 10.3 旅程 Q · 气隙 Ferry

```text
WF-AP-01 离线 Spoke
  → WF-AP-04 选 Bundle / Delta → 签名导出
  → 介质摆渡 → 气隙导入
  → WF-AP-06（若改环境设定）→ Plan 执行
```

### 10.4 旅程 R · 工作台发布到试点（跨层）

```text
08a WF-WS-09 [发布 ▾]
  → 选择 Channel / 试点 Spoke
  → （可选）WF-AP-05 绑定资产版本
  → WF-AP-06 审批（生产通道）
  → WF-AP-03 观察 Plan
```

### 10.5 组件对照（售前 Demo）

| 线框 | Demo | 状态 |
| --- | --- | --- |
| **WF-AP-01** | `apollo-hub.html` | ✅ |
| **WF-AP-02** | `apollo-release.html` | ✅ |
| **WF-AP-03** | `apollo-spoke.html` | ✅ |
| **WF-AP-04** | `apollo-ferry.html` | ✅ |
| **WF-AP-05** | `apollo-assets.html` | ✅ |
| **WF-AP-06** | `apollo-change-mgmt.html` | ✅ |
| **WF-AP-07** | `apollo-config.html` | ✅ |
| 上游入口 | `workshop-publish.html` | ✅ 指针（08a） |

---

## 11. 一致性自检

| 检查项 | 结论 |
| --- | --- |
| 是否覆盖 09 §9 建议的 WF-AP-01～07？ | **是** |
| 是否与 html v1.6 七页一一对应？ | **是** |
| 是否写成「只装 K8s / 开入站」？ | **否** · 出站轮询 + Lite |
| 是否钉死单一目标版本？ | **否** · Channel 订阅 |
| Change Management 是否只有日志？ | **否** · 审批流 + 紧急事后审计 |
| FDE 资产是否黑盒？ | **否** · 交付客户 · 版本同绑 |
| 工作台是否重复造 Apollo 控制台？ | **否** · 仅 WF-WS-09 入口 |
| 密钥是否允许明文？ | **否** · Vault/KMS 引用 |

---

## 12. 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v1.0 | 2026-07-17 | 首版：WF-AP-01～07 · 对齐 09 v1.2 OPS-001～010 · Palantir Apollo Core 官网概念 · html v1.6 映射 · 旅程 O/P/Q/R |

---

*09a · Apollo 线框 · Run Anywhere · 舰队可见 · 气隙可摆渡 · 资产可交付*

# 07b · Capability Adapter（重能力接入）产品方案

> **文档性质**：[07 AIP](07-AIP引擎k-LLM与AgentStudio产品方案.md) / [06b Action·Function](06b-Action与Function产品设计.md) 的 **重代码能力接入** 子章  
> **版本**：v1.0 · 2026-07-17  
> **状态**：✅ 方案完成 · Demo 蓝图 [`aip-capabilities.html`](foundry/html/aip-capabilities.html)  
> **技术对齐**：[T07 §5.3](20_tech/T07-AIP人工智能平台详细技术方案.md) · [T-API §2.3](20_tech/T-API-aos-api稳定契约.md) · [T06](20_tech/T06-Ontology与Action-Function详细技术方案.md)  
> **线框**： [07a](07a-AIP引擎产品设计线框图.md) · **WF-AIP-05C**

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 中文 | 全文中文 |
| 先方案后代码 | 本文为真源；Demo 仅示意 |
| 最小入侵 | 不改 Function ≤60s/2GB；重活外置 |
| 与 L2 自洽 | 写回只走 Action / Draft；媒体进 MediaSet |
| 不搬 Marketplace | 登记 Adapter，不做第三方应用商店 |

---

## 1. 要解决什么

Agent Studio / AIP Logic 擅长 **低代码编排**（选脑、挂工具、提 edits）。  
企业还会引入 **外面的重代码包**，例如：

| 能力类 | 典型特征 | 能否塞进 Logic 节点同步跑完 |
| --- | --- | --- |
| 短视频生成 | GPU · 分钟～小时 · 大文件 | ❌ |
| 直播稿引擎 | 可同步或短异步；偏文本 | 轻量可 Function；重则 Job |
| 电商/教育可交互数字人 | 长连接 · 会话态 · 实时音视频 | ❌（独立服务） |

**结论：** AOS **必须承接**，但模式是 **「大脑编排 + 肌肉外置」**，不是把重包嵌进画布沙箱。

---

## 2. 一句话定位

**Capability Adapter = 把外部重能力登记为平台可调用的「能力插件」：统一契约、权限、审计与 Ontology 落点；Agent/Logic 只看见工具卡，看不见各家 SDK。**

与已有概念对照：

| 概念 | 解决什么 | 本方案关系 |
| --- | --- | --- |
| **Model Adapter** | 如何加载/推理 LLM | 只管「脑」；**不管**渲染/数字人 |
| **Function（FUNC-03）** | ≤60s · ≤2GB 类型安全算力 | **薄封装**（校验、下发、查状态）；禁扛重活 |
| **Action + Webhook** | 写世界与副作用 | **异步完成/失败**的正式写路径 |
| **Capability Adapter（本文）** | 重能力生命周期与运行契约 | 登记面 + Job/Session Runtime |
| **Agent 工具面板** | LLM 可请求哪些工具 | 挂上已发布的 Capability Tool |

```text
人类 / Automate
      │
      ▼
AIP Logic / Chatbot Studio     ← 低代码「大脑」
      │  Tool: Call Capability
      ▼
Capability Registry + Facade   ← 本文
      │  sync 薄调用 / async Job / Session
      ▼
外部重代码包（GPU / 数字人引擎 / 稿件服务）
      │  artifact / event callback
      ▼
MediaSet · Object 状态 · Draft/Action 写回
```

---

## 3. 能力分级（选型门禁）

| 级 | 名称 | 时延/资源 | 落点 | 示例 |
| --- | --- | --- | --- | --- |
| **C0** | 同步轻能力 | ≤数秒 · 无 GPU | Function 或 sync Capability | 模板填空直播稿、短规则校验 |
| **C1** | 异步 Job | 分钟～小时 · 可 GPU | Job + Action 副作用 + 回调 | 短视频渲染、批量配音 |
| **C2** | 长会话 Session | 小时级连接 · 实时 | Session 服务 + Object 会话态 | 电商/教育可交互数字人 |

**门禁：** 预估超过 FUNC-03（60s/2GB）→ **禁止**标为普通 Function；必须选 C1/C2。

---

## 4. Capability Adapter 契约

### 4.1 Manifest（登记）

```text
Capability Adapter manifest:
  id, version, display, owner
  kind: sync | job | session
  authSchema          # Vault ref，禁明文
  inputSchema         # JSON Schema · 对齐 Ontology 字段映射
  outputSchema
  endpoints:
    health
    invoke | submit | status | cancel | artifact   # 按 kind 子集
    session.open | session.push | session.close    # C2
  callbacks: webhookUrl · signed
  quotas · concurrency · timeoutHints
  markings / 数据出境策略
```

### 4.2 运行时 API 语义（产品）

| 操作 | C0 sync | C1 job | C2 session |
| --- | --- | --- | --- |
| 触发 | `invoke` 立即结果 | `submit` → `jobId` | `session.open` → `sessionId` |
| 查询 | — | `status` | 会话心跳 / 状态 Object |
| 取消 | — | `cancel` | `session.close` |
| 产物 | 内联 JSON | `artifact` → MediaSet RID | 流事件 + 可选录像进 MediaSet |
| 失败 | 同步错误码 | 重试/DLQ（对齐 ACT-10） | 断线恢复策略声明 |

### 4.3 平台 Facade（禁止直连）

- UI / Logic / Agent **只**调 `aos-api` `/v1/aip/capabilities/*`（见 T-API）。
- **禁止**浏览器或 Logic 沙箱直连厂商 SDK / 裸 HTTP（密钥与审计失控）。
- Adapter 进程可边车或客户侧前置（对齐 23/24：重 GPU 服务优先客户先装）。

---

## 5. 与 Ontology / Action / Function 的落点

### 5.1 名词（建议 Object Types · 可行业化）

| Object Type（示意） | 用途 |
| --- | --- |
| `LiveScript` | 直播稿正文 · 版本 · 人设绑定 |
| `MediaJob` | 异步生成任务状态 · 进度 · 错误码 |
| `AvatarSession` | 数字人场次 · 开播/结束 · 话术指针 |
| `Campaign` / `SKU` | 电商场次与商品上下文 |
| `CourseSession` | 教育直播场次与课纲 |

资产二进制：**MediaSet**（成片、音色、形象包）；Object 只存 RID / 元数据。

### 5.2 动词

| 路径 | 何时用 |
| --- | --- |
| **Function 薄封装** | C0；或 `submit`/`status` 的类型安全包装 |
| **Action + Side Effect** | 创建「开始生成」「开播」；Webhook 回调后写状态/挂 Media |
| **Draft** | 成片上架、话术发布、对外开播前 HITL |
| **Apply Action / Call Capability Tool** | Logic / Agent 侧可见入口 |

**金句：** *重包改世界，必须经过 Action 盖章；Capability 只负责把「肌肉」接上神经。*

### 5.3 与 FUNC / ACT 约束的增量

| ID | 规则 |
| --- | --- |
| **CAP-01** | 超 FUNC-03 的能力不得注册为普通 Function；须 Capability kind=job/session |
| **CAP-02** | Logic 试跑调用 Capability 默认 **dry-run / 沙箱配额**；真扣 GPU 须显式「生产试跑」权限 |
| **CAP-03** | 写 Ontology / 挂 MediaSet 仅经 Action（或官方 Edits）；Adapter 回调只投递事件，不直写库 |
| **CAP-04** | 密钥与厂商 endpoint 仅 Vault；UI 只存 ref |
| **CAP-05** | 回调验签；失败进 DLQ；可人工重放（对齐 ACT-10） |
| **CAP-06** | Tool 面板挂载须绑定调用用户权限（A-08）；项目范围执行须显式开关 |
| **CAP-07** | 不做 Capability Marketplace；仅组织内登记与版本发布 |

---

## 6. 场景旅程（验收样例）

### 旅程 P1 · 短视频生成（C1）

```text
Logic：读 SKU/脚本 Object → Use LLM 润色分镜
  → Tool: Call Capability(short_video.submit)
  → 返回 jobId → Action 创建 MediaJob(queued)
  → Adapter 回调 succeeded → Action 挂 MediaSet + MediaJob=done
  → Draft：运营过片 → 发布
```

### 旅程 P2 · 直播稿（C0/C1）

```text
轻量：Function 或 sync Capability → 写 LiveScript（经 Action）
重量：外部稿件引擎 Job → 同 P1 回调落 Object
```

### 旅程 P3 · 可交互数字人（C2）

```text
运营台「开播」Action → Capability session.open
  → AvatarSession Object = live
  → Agent/Logic 仅推话术、查 Wiki、派单（工具中介）
  → 实时 AV 在数字人引擎；平台收事件与审计
  → session.close → 可选录像进 MediaSet · 场次归档
```

---

## 7. 产品界面（线框要点）

### 7.1 WF-AIP-05C · 重能力接入

```text
┌─ 重能力接入（Capability）──────── [登记 Adapter] [工具面板 →] ─┐
│ 已接入：短视频 Job · 直播稿 · 电商数字人 · 教育数字人（卡片）     │
│ 可接入类型：Media Job · Script Engine · Avatar Session · HTTP  │
│ 卡片：kind · 健康 · 配额 · 打开配置（类型化表单）                 │
└────────────────────────────────────────────────────────────────┘
```

配置表单：**先选类型，再填该类型字段**（与模型供应商同交互范式；**不**做应用商店浏览）。

### 7.2 与工具面板 / Logic

- 工具目录增加 **Capability**（或归入 Function 子类「外部能力」——Demo 用独立类更清晰）。
- Logic 块：**Call Capability**（参数映射 Object 字段）；长任务旁路显示 job 进度链到运营台。

### 7.3 Demo 映射

| 线框 | HTML |
| --- | --- |
| WF-AIP-05C | `aip-capabilities.html` |
| 工具挂载 | `aip-tools.html` 链到能力页 |
| 资产落点 | `media-sets.html` |
| 写回/审批 | `ontology-action.html` · `aip-draft-inbox.html` |

---

## 8. 技术要点（摘要 · 详 T07）

| 组件 | 职责 |
| --- | --- |
| `capability-registry` | Manifest · 版本 · 启用 |
| `capability-facade` | 统一 API · 鉴权 · 审计 · 配额 |
| `job-orchestrator` | C1 状态机 · 回调 · DLQ |
| `session-gateway` | C2 会话票据 · 心跳 · 关闭 |
| Adapter 进程 | 厂商 SDK / 自有重包；可客户侧部署 |

开源：可参考「插件 manifest + 边车」模式（类比 LiteLLM）；**不**引入第三方 Agent 应用市场。

---

## 9. PPT / PRD 金句

1. **「Studio 写剧本，Capability 出肌肉——重代码进 AOS，不进沙箱。」**
2. **「模型 Adapter 选脑，Capability Adapter 接肢；都只认平台契约。」**
3. **「数字人可以很重，Ontology 仍然很轻：会话是 Object，像素在 MediaSet。」**

---

## 10. 变更记录

| 版本 | 日期 | 变更 |
| --- | --- | --- |
| v1.0 | 2026-07-17 | 初稿：分级 C0–C2 · Manifest · CAP 约束 · 旅程 P1–P3 · Demo WF-AIP-05C |

---

*v1.0 · docs/palantier/07b · Capability Adapter · 重能力接入*

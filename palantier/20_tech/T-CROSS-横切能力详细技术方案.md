# T-CROSS · 横切能力详细技术方案（身份 · 授权 · 可观测 · 多租户）

> **版本**：v1.1.0 · 2026-07-17  
> **状态**：✅ **方案完成**（含 §3.2 日志分级与环境开关）  
> **对齐**：[20 §8](20-AOS整体技术方案.md) · [T-API](T-API-aos-api稳定契约.md) · [T06](T06-Ontology与Action-Function详细技术方案.md) · [T09](T09-Apollo交付引擎详细技术方案.md) · [21](21-AOS开源选型与功能清单.md) · [23 军规](23-AOS开源引用与交付军规.md) · [24 前置 SOP](24-AOS客户侧前置组件安装SOP.md) · [T-EVO](T-EVO-v0.1到目标态替换阶梯.md)

---

## 使用的 Rules

横切一次定清 · 各层只消费契约 · **先写自有功能再写开源** · 开源参考已本地核对

---

## 1. 身份认证（IdP）

### 1.0 自有所需功能（先于开源）

| 功能项 | 我们要什么 | 验收 |
| --- | --- | --- |
| 统一登录 | Web / Desktop / Hub / Spoke 控制面同一 IdP | OIDC |
| 令牌 | Access→aos-api；Refresh 由 BFF/桌面管理 | 无 Token→401 |
| 生产安全 | 禁默认口令；可对接客户 IdP | — |

### 1.1 开源参考与已决

| 项 | 已决 |
| --- | --- |
| 协议 | OIDC · OAuth2 |
| 参考实现 | `F1_Identity/keycloak`（本地已有） |
| 产品行为 | Hub / Web / Desktop / Spoke 控制面统一登录 |
| 令牌 | Access Token → aos-api；Refresh 由 BFF/桌面壳管理 |
| 本地试用 | 可内嵌 Dev IdP 或演示账号；**生产禁默认口令** |

**抄：** Realm/Client/角色映射思路。  
**不抄：** Keycloak Admin 当 AOS 用户产品壳。  
**选型：** Keycloak（已拉）为主；Authentik 等仅在客户强制时评估。  
**安装：** Prod 由客户先装 IdP（[24 §3.4](24-AOS客户侧前置组件安装SOP.md)）；AOS 只配 OIDC issuer/client。

---

## 2. 授权（Authz）

### 2.0 自有所需功能（先于开源）

| 功能项 | 我们要什么 | 验收 |
| --- | --- | --- |
| 关系授权 | Object/Module/Widget 级 allow/deny | 前端不直连引擎 |
| Markings | 标签与关系组合；无则不渲染 | T08 |
| Wiki B | 写=可调对应 Action | HR-01 |

### 2.1 开源参考与已决

| 项 | 已决 |
| --- | --- |
| 模型 | **OpenFGA 关系元组** + 自有 **Markings** 标签 |
| 参考 | `F2_Authz/openfga` |
| Object 级 | `user` → `viewer/editor/owner` → `object`（实现见 [61](61-OpenFGA生产模型扩展.md)） |
| Widget / Module | 绑定 Marking；运行态无关系则不渲染（T08） |
| Wiki 方向 B | 写权限 = 可调用对应 Action，而非 Wiki 引擎特权 |

**决策：** v1 以 OpenFGA 为授权引擎边车；aos-api 只暴露「是否允许」决策 API，前端不直连 OpenFGA。

---

## 3. 可观测

### 3.0 自有所需功能（先于开源）

| 功能项 | 我们要什么 | 验收 |
| --- | --- | --- |
| Trace | AIP/Logic/Action 全链路 | W3C traceparent |
| Metrics | RED + Spoke Probe | 可告警 |
| **App Log** | 分级结构化日志；开发详、生产可降噪 | §3.2 |
| Audit | 登录·发布·Action·密钥引用·hotfix | **不可关**（HR-05） |
| 熔断/死信 | 进 Lineage + 通知 | T07/T05 |

### 3.1 开源参考

| 信号 | 做法 | 参考 | 选型 |
| --- | --- | --- | --- |
| Trace | W3C；产品 Lineage 自有 | Langfuse（`C3_Trace/langfuse`） | **建议**边车 |
| Metrics | RED + Probe | Prometheus（已拉） | **建议** |
| Logs 汇聚（可选） | 应用日志转发 | OTel Collector → 客户 OpenSearch 等 | P2 旁路（22 §2.3） |
| 看板 | 运维深链可选 | Grafana（❌未拉） | **建议补拉** |
| Audit | 自研 Audit Log | — | 必自研 |
| 熔断/死信 | Lineage + 告警 | T07 / T05 | — |

**不抄：** Langfuse/Prometheus UI 冒充 AOS 运维台（运维可深链，交付面自有）。  
**Grafana：** 客户自装（AGPL）；AOS 只交付 Dashboard JSON（[24 §3.7](24-AOS客户侧前置组件安装SOP.md) · 军规 R-LIC-02）。

### 3.2 应用日志分级与环境开关（已决）

> **目的：** 开发/排障尽量详细；上线默认降噪可控；**绝不**用「关日志」关掉 Audit / WARN+ / 熔断与死信。

#### 3.2.1 级别与环境默认

| 级别 | 开发默认 | 生产默认 | 用途 |
| --- | --- | --- | --- |
| **TRACE / DEBUG** | **开** | **关** | Funnel 阶段、Action 参数摘要、AIP Tool 调用细节、Merge 冲突过程 |
| **INFO** | 开 | **开**（可采样） | 请求起止、配置加载、关键状态迁移 |
| **WARN / ERROR** | 开 | **永远开** | 不可被「关日志」关掉 |
| **Audit** | 开 | **永远开** | 与 App Log 分通道；HR-05 |

生产**禁止**配置为「零日志 / off」；最低保持 **INFO 采样 + WARN/ERROR + Audit**。排障时可临时 `DEBUG`，事后必须收回。

#### 3.2.2 配置项（各服务统一认）

| 变量 / 配置键 | 含义 | 示例 |
| --- | --- | --- |
| `AOS_LOG_LEVEL` | 主级别 | `debug` · `info` · `warn` · `error` |
| `AOS_LOG_MODULES` | 可选模块放大（逗号分隔） | `funnel,action,aip,apollo` |
| `AOS_LOG_SAMPLE_INFO` | 生产 INFO 采样率（0～1） | `1.0` 开发 · `0.1`～`0.2` 生产建议 |
| `AOS_LOG_FORMAT` | 输出格式 | 生产强制 `json`；开发可用 `pretty` |

配置来源：环境变量 / Apollo Config / 本地 `.env`（开发）；**运行时可热更级别**（推荐），避免为改日志重启全站。

#### 3.2.3 结构化字段（强制）

每条应用日志至少含（缺则视为不合规）：

| 字段 | 说明 |
| --- | --- |
| `ts` · `level` · `service` · `msg` | 基础 |
| `trace_id` · `span_id` | 对齐 W3C / Langfuse |
| `org_id` · `project_id` | 多租户 |
| `request_id` 或等价 | 网关/BFF 注入 |

可选：`actor_id`（非审计通道勿写敏感身份细节）、`object_type`、`action_type`。

#### 3.2.4 脱敏与红线

| 规则 | 说明 |
| --- | --- |
| **禁止明文** | Access/Refresh Token、Vault 明文、密钥、口令 |
| **默认打码** | 身份证/手机等 PII；完整 LLM Prompt / 长 CoT → 只留 hash 或截断；完整内容进 Langfuse/私有观测且受权限 |
| **Audit ≠ DEBUG** | Audit 通道独立存储与保留策略；应用 `AOS_LOG_LEVEL` **不得**关闭 Audit |
| **禁止散落** | 业务代码禁止裸 `print` / `console.log` 当生产日志；统一 Logger 门面（各语言一层） |

#### 3.2.5 与 Trace / Lineage 的分工

| 信号 | 管什么 |
| --- | --- |
| App Log | 工程师排障、运行时细节 |
| Trace（Langfuse 等） | 跨服务调用图、延迟、LLM 观测 |
| Decision Lineage | 产品语义「一次决策可复盘」（T07） |
| Audit | 合规「谁在何时对何资源做了何特权操作」 |

同一请求应能用 `trace_id` 从 Log ↔ Trace ↔（若有）Lineage 互跳。

#### 3.2.6 实现约束（T-EVO 起强制）

1. M1 起：aos-api / 各 `services/*` 接入统一 Logger；CI 可扫禁 `print(`（语言适配）。  
2. 交付包默认 `AOS_LOG_LEVEL=info`；开发 compose / 本地默认 `debug`。  
3. Spoke / Ferry 边车同样遵守本节；气隙环境日志落本地轮转，体积与保留天数可配。

---

## 4. 密钥

| 项 | 已决 |
| --- | --- |
| 引擎 | Vault（`E3_Secrets/vault`）或客户 KMS |
| 规则 | 配置面只存 **secret ref**；明文拒绝（T-API `SECRET_PLAINTEXT_REJECTED`） |
| Lite Spoke | 密封文件 + 启动解锁，仍禁止可复制明文 |
| 安装 | Vault **BSL** → 客户侧发行包（[24 §3.5](24-AOS客户侧前置组件安装SOP.md)）；**不**打进 AOS 客户包 |

详见 T09 · 军规 [23](23-AOS开源引用与交付军规.md)。

---

## 5. 多租户（Org / Project）

| 层级 | 含义 | 隔离 |
| --- | --- | --- |
| **Org** | 客户/集团租户 | IdP realm 或 org_id 声明 |
| **Project** | 工作区（数据/本体/模块边界）；**产品文案 =「工作区」**（≈ Dify Workspace） | 资源均带 `project_id` |
| **Environment** | rc/beta/stable（Apollo Channel） | 与 Project 正交 |

**已决：** v1 强制 `org_id` + `project_id` 进所有业务表与 API；单租户部署时使用默认 org/project，**代码路径不删多租户字段**。

**产品化加深：** 字段已有 ≠ 整站隔离已交付。标准企业「多人 + 多工作区」与壳切换器、Membership、跨区拒访门禁见 **[20a-多用户与工作区整站隔离方案](20a-多用户与工作区整站隔离方案.md)**（📝 方案定稿 · 暂不编码）。

---

## 6. 与各层接口

| 层 | 消费方式 |
| --- | --- |
| T-UI / Desktop | Bearer + `/v1/me` |
| T05～T09 服务 | 中间件校验 JWT · 注入 org/project · 调 Authz Check |
| Apollo Spoke | 机器身份（mTLS 或 client credentials）+ 出站轮询 |

---

## 7. 验收

| # | 标准 |
| --- | --- |
| A1 | 无 Token 访问业务 API → 401 |
| A2 | 无 Marking 用户看不到受限 Widget |
| A3 | Audit 中可查一次 Action 与一次 hotfix |
| A4 | 配置提交明文密码 → 400 |
| A5 | 生产 `AOS_LOG_LEVEL=info` 时 DEBUG 不可见；WARN/ERROR/Audit 仍可见 |
| A6 | 日志 JSON 含 `trace_id` + `org_id`/`project_id`；无明文 Token/密钥 |
| A7 | 将 `AOS_LOG_LEVEL` 调至 error **不能**关闭 Audit 写入 |

---

## 8. 修订

| 版本 | 说明 |
| --- | --- |
| v1.0 | 横切一次定稿；关闭 20 §8「☐ 后续」 |
| v1.1.0 | **§3.2 应用日志分级与环境开关**；验收 A5～A7；与 T-EVO/20 交叉 |
| v1.1.1 | §5 挂 [20a](20a-多用户与工作区整站隔离方案.md)：工作区产品名 · 整站隔离产品化（方案层） |

---

*T-CROSS v1.1.0 · docs/palantier/20_tech*

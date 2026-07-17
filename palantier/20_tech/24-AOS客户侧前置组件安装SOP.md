# 24 · AOS 客户侧前置组件安装 SOP

> **文档性质**：**活文档 SOP**（开发期 / 实施期持续补全；禁止「到现场再写」）  
> **版本**：v0.1 · 2026-07-17（骨架已生效；细节随联调追加）  
> **状态**：实施门禁真源 · 对齐军规 [23](23-AOS开源引用与交付军规.md) **R-INST-***  
> **读者**：客户 IT · FDE · 实施 · 研发（Dev 环境同样走一遍缩小版）  
> **配套**：[22](22-AOS开源产品维护清单.md) · [T05](T05-L1数据集成详细技术方案.md) · [T09](T09-Apollo交付引擎详细技术方案.md) · [T-CROSS](T-CROSS-横切能力详细技术方案.md)

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 中文 | 检查单与命令示例中文说明 |
| 先客户后 AOS | 未勾选 §5 总检，不得装 AOS（军规 R-INST-01） |
| 细节不攒到现场 | 联调发现一项补一项 → §9 变更日志 |
| 不捆 AGPL | 前置组件由客户安装发行包；AOS 只对接 |
| Dev≈Prod 形状 | 开发用缩小版同一顺序，避免「开发能跑、现场不会装」 |

---

## 0. SOP 目的与边界

### 0.1 目的

保证客户环境在安装 AOS **之前**已具备：身份、库、对象仓、密钥、缓存、观测等前置能力，并完成连通性验收；AOS 安装器只消费 **endpoint + secret-ref + 版本矩阵**，不负责「偷偷装齐全家桶」。

### 0.2 边界

| 做 | 不做 |
| --- | --- |
| 给出组件清单、版本建议、安装责任方、验收命令、交给 AOS 的配置项 | 替代客户 IT 的操作系统/网络/备份规范 |
| 区分 Lite / 标准私有化 / 气隙 | 把 MinIO/Grafana 打进 AOS 客户包 |
| 记录联调踩坑（§9） | 等签约后再从零回忆 |

### 0.3 总顺序（强制）

```text
1) 基础设施（OS / 磁盘 / 网络 / DNS / 证书）
2) 数据面前置：PostgreSQL →（可选）对象仓 MinIO/S3 → Redis
3) 安全面前置：Keycloak（或客户 IdP）→ Vault/KMS（或密封文件方案）
4) 观测面前置（可并行）：Prometheus → Grafana（客户自装）
5) 可选：Kafka/Redpanda（仅有 CDC 时）· OCR 运行时依赖（见 §3.8）
6) §5 总检全部 ✅
7) 安装 AOS（Lite Spoke / Hub 等，见 T09）
8) AOS 冒烟：对接探针 + 写 secret-ref + 业务最小路径
```

**金句：** *前置组件是客户的「地基」；AOS 是地基上的「房子」。先打地基，再盖房。*

---

## 1. 角色与责任

| 角色 | 责任 |
| --- | --- |
| **客户 IT** | 安装/升级/备份前置组件；提供 endpoint、只读账号或 vault 路径；网络策略（Spoke **出站**） |
| **FDE / 实施** | 带检本 SOP；填写 §5；指导版本矩阵；**不**代客把 AGPL 塞进 AOS 包 |
| **AOS 研发** | 维护本 SOP 版本矩阵与探针；安装器只读配置 |
| **法务** | BSL/AGPL 使用边界；例外客户附录 |

交接物（客户 → 实施）：

```text
prereq-handoff.yaml  （或等价表格）
├── postgres: url, db, user_ref
├── object_store: s3_endpoint, bucket, region, ak_ref/sk_ref
├── redis: url_ref
├── oidc: issuer, client_id, client_secret_ref
├── vault: addr, auth_method, role  （或 lite_sealed_file 说明）
├── prometheus: scrape_url（可选）
├── grafana: url（可选，仅深链）
└── versions: { component: semver }
```

---

## 2. 部署档位与前置矩阵

| 组件 | Lite（无 K8s） | 标准私有化 | 气隙 | 谁装 | License 注意 |
| --- | --- | --- | --- | --- | --- |
| PostgreSQL（+AGE 扩展窗口） | **必** | **必** | **必** | 客户 | 友好 |
| 对象仓 MinIO 或客户 S3 | **必**（MediaSet） | **必** | **必**（内网 S3/兼容） | 客户 | MinIO **AGPL：客户自装** |
| Redis | 建议 | **必** | 建议 | 客户 | BSD |
| Keycloak 或客户 IdP | Dev 可内嵌；Prod **必**外部 | **必** | **必** | 客户 | Apache2 |
| Vault 或客户 KMS | Lite 可用密封文件 | **必**其一 | **必**其一 | 客户 | Vault **BSL：发行包** |
| Prometheus | 建议 | **必** | 建议 | 客户 | Apache2 |
| Grafana | 可选深链 | 建议 | 可选 | 客户 | **AGPL：客户自装；AOS 只交 Dashboard JSON** |
| Kafka/Redpanda | 无 CDC 则跳过 | 有 CDC 再装 | 按需 | 客户 | Redpanda BSL |
| OCR 运行时（Paddle 依赖） | 随 AOS 插件进程 | 同左 | 离线轮需模型文件 | AOS 侧进程，但 **系统库/GPU 驱动** 客户准备 | Paddle Apache2 |

> 「必」= 该档位未就绪则 **禁止**进入 AOS 安装（R-INST-01）。

---

## 3. 分组件 SOP（细节页 · 持续加厚）

> 每节固定结构：**目的 → 版本建议 → 安装要点 → 验收 → 交给 AOS 的配置 → 已知坑**。  
> 命令示例可按 OS 增补；联调补丁写进 §9。

### 3.1 PostgreSQL（Meta / AGE / 业务库）

| 项 | 内容 |
| --- | --- |
| 目的 | Meta、业务库；图引擎 AGE（T06） |
| 版本建议 | PostgreSQL **16.x**（钉死后写入本表）；AGE 与大版本匹配 |
| 安装要点 | 独立实例或客户标准 PG；建库 `aos_meta` / `aos_app`（名可配）；UTF8 |
| 验收 | `psql` 可连；`CREATE EXTENSION IF NOT EXISTS age;` 在约定库成功（若本阶段启用图） |
| 交给 AOS | `DATABASE_URL` 或分项 host/port/db + **密码进 Vault ref** |
| 已知坑 | （开发期追加） |

### 3.2 对象存储 · MinIO / 客户 S3（MediaSet）

| 项 | 内容 |
| --- | --- |
| 目的 | MediaSet 原件（T05 L1-06） |
| 版本建议 | MinIO 发行版（客户从官网/镜像站装）；**不要用 AOS 包内嵌** |
| 安装要点 | 建 bucket（如 `aos-media`）；HTTPS 优先；AK/SK 进 Vault |
| 验收 | `mc ls` 或 S3 ListBucket 成功；上传 1KB 探测对象可 Get |
| 交给 AOS | `S3_ENDPOINT` · `S3_BUCKET` · `S3_REGION` · `S3_ACCESS_KEY_REF` · `S3_SECRET_KEY_REF` · `S3_PATH_STYLE=true`（MinIO 常见） |
| **军规** | AOS 仅 `S3Adapter`；切换客户云 S3 **不改**业务代码 |
| 已知坑 | 路径风格 / 证书 / 时钟偏差导致签名失败 — 记 §9 |

**客户自装 MinIO（示意 · 非交付包内容）：**

```text
# 由客户 IT 执行（示例）
# 1) 按 MinIO 官方文档安装二进制或容器
# 2) 配置根用户 → 立即转入 Vault/密钥系统，禁止明文邮件传递
# 3) 创建 bucket: aos-media
# 4) 将 endpoint 填入 prereq-handoff.yaml
```

### 3.3 Redis（缓存 / 限流 / 会话）

| 项 | 内容 |
| --- | --- |
| 目的 | Pipeline 限流、Selection 缓存、AIP 会话（21） |
| 版本建议 | Redis **7.2+** / **7.4.x** |
| 验收 | `PING` → `PONG`；设置 `aos:prereq:ping` 可读写 |
| 交给 AOS | `REDIS_URL_REF`（密码不进明文配置） |
| 已知坑 | （追加） |

### 3.4 身份 · Keycloak / 客户 IdP

| 项 | 内容 |
| --- | --- |
| 目的 | OIDC 统一登录（T-CROSS） |
| 版本建议 | Keycloak **25.x/26.x**（钉定后更新）或客户 Azure AD / 企业 IdP |
| 安装要点 | 建 Realm（或客户租户）；Client：`aos-web` / `aos-desktop` / `aos-spoke`；回调 URL 按环境填 |
| 验收 | OIDC discovery `/.well-known/openid-configuration` 可访问；测试账号拿得到 access_token |
| 交给 AOS | `AOS_OIDC_ISSUER` · `AOS_OIDC_JWKS_URL` · `AOS_OIDC_AUDIENCE` · `CLIENT_ID_REF`；**联调规程**见 [60-生产IdP联调手册](60-生产IdP联调手册.md) |
| 已知坑 | 时钟同步；HTTPS 终结位置；`iss` 与配置字节级一致 |

### 3.5 密钥 · Vault / KMS / Lite 密封文件

| 项 | 内容 |
| --- | --- |
| 目的 | 所有密钥只存 ref（T09 / 军规） |
| 标准 | Vault 发行包或客户 KMS |
| Lite | 密封文件 + 启动解锁（仍禁止可复制明文进 Git） |
| 验收 | AOS 安装器能用约定 auth 读取探测 secret；拒绝明文密码提交（API 测） |
| 交给 AOS | `VAULT_ADDR` · auth 方式 · role；或 `KMS_*`；或 `LITE_SEAL_PATH` 流程说明 |
| **军规** | Vault **BSL** → 客户侧发行包；不嵌进 AOS 源码树交付 |

### 3.6 Prometheus（指标）

| 项 | 内容 |
| --- | --- |
| 目的 | Spoke Probe / RED（T09 / T-CROSS） |
| 验收 | 可 scrape 约定 job；或客户已有统一采集则提供 remote 说明 |
| 交给 AOS | scrape 目标列表或 `PROMETHEUS_URL` |

### 3.7 Grafana（可选深链）

| 项 | 内容 |
| --- | --- |
| 目的 | 运维看板；**非** AOS 产品壳 |
| 安装 | **客户自装** Grafana 发行包（AGPL） |
| AOS 交付 | 仅 `dashboards/*.json` + 导入说明（见 `docs/examples/customer-prereq/grafana/`，随仓建立） |
| 验收 | 客户 Grafana 能导入 JSON；数据源指向客户 Prometheus |
| **军规** | 禁止把 Grafana 二进制打进 `dist/customer/` |

### 3.8 OCR 运行时依赖（Paddle 插件进程）

| 项 | 内容 |
| --- | --- |
| 目的 | `parser-pdf-ocr` 独立进程（T05） |
| 客户准备 | CPU/内存下限；若 GPU 加速则驱动；中文字体（按需） |
| AOS 负责 | 插件包、模型文件分发路径、进程守护 |
| 验收 | 对 1 份扫描 PDF 探针任务成功出文本；失败进 DLQ 可观测 |
| 已知坑 | 模型体积与离线拷贝 — 气隙走 Ferry/介质清单 |

### 3.9 CDC 总线（可选 · Kafka / Redpanda）

| 项 | 内容 |
| --- | --- |
| 触发条件 | 客户明确 CDC（Debezium）需求 |
| 建议 | 中小规模可 Redpanda **发行包**（BSL 商用核条款）；或 Kafka |
| 验收 | topic 可建；Debezium 探针连通 |
| 未触发 | §2 矩阵勾选「跳过」并签字 |

### 3.10 网络与出站（Apollo / 边缘）

| 项 | 内容 |
| --- | --- |
| 目的 | Spoke / 边缘 Agent **出站**拉 Plan/Sync；**不要求**客户给 Hub 开入站 |
| 验收 | 从 Spoke 网段 HTTPS 访问 Hub 健康检查 URL 成功 |
| 交给 AOS | 代理环境变量说明（如有）；TLS 证书信任链 |

---

## 4. Dev 环境缩小版（研发必做）

目的：开发机顺序与生产同构，避免「只有全量 Docker 全家桶才会装」。

| 步骤 | Dev 做法 |
| --- | --- |
| 1 | `deploy/dev/` 或文档示例 Compose **仅用于本机**，路径禁止打进客户包 |
| 2 | 仍填写一份缩小版 `prereq-handoff.yaml` |
| 3 | 跑通 §5 总检中 Lite 必选项 |
| 4 | 联调坑记入 §9 |

---

## 5. 总检检查单（安装 AOS 前门禁）

> 实施负责人打印或电子勾选；**缺任一项「必」→ 停止**。

| # | 检查项 | Lite | 标准 | 结果 | 记录人 |
| --- | --- | --- | --- | --- | --- |
| 1 | OS/磁盘/DNS/NTP 就绪 | 必 | 必 | ☐ | |
| 2 | PostgreSQL 连通 + 库已建 | 必 | 必 | ☐ | |
| 3 | 对象仓 List/Put/Get 探针 | 必 | 必 | ☐ | |
| 4 | Redis PING | 建议 | 必 | ☐ | |
| 5 | OIDC discovery + 测通登录 | Prod 必 | 必 | ☐ | |
| 6 | Vault/KMS 或 Lite 密封方案就绪 | 必 | 必 | ☐ | |
| 7 | Prometheus（或等价） | 建议 | 必 | ☐ | |
| 8 | Grafana（若需要深链）客户已装 | 可选 | 建议 | ☐ | |
| 9 | 出站到 Hub 探测 | Spoke 必 | 必 | ☐ | |
| 10 | `prereq-handoff.yaml` 已交接且无明文密码 | 必 | 必 | ☐ | |
| 11 | 客户确认：MinIO/Grafana **非** AOS 包提供 | 必 | 必 | ☐ | |

**签署：** 客户 IT ______ · FDE ______ · 日期 ______  

签署后 → 方可执行 AOS 安装（T09 / 安装手册）。

---

## 6. AOS 安装器对接契约（研发遵守）

安装器 / 配置向导 **只允许**：

1. 读取 `prereq-handoff`（或等价 UI 表单）；  
2. 对每项做 **只读探针**（失败则阻断并提示回到本 SOP）；  
3. 将 secret 写成 **ref**；  
4. 拉起 AOS 自有服务。

**禁止：** 下载 MinIO/Grafana/Vault 服务器二进制写入客户数据盘「作为 AOS 的一部分」。

伪流程：

```text
load handoff
→ probe postgres / s3 / redis / oidc / vault
→ if any fail: exit 2, print SOP section link
→ write aos config (refs only)
→ start aos units
→ smoke: /health + one MediaSet put via S3Adapter
```

---

## 7. 与文档/军规索引

| 主题 | 文档 |
| --- | --- |
| 军规 | [23](23-AOS开源引用与交付军规.md) |
| 仓址 License | [22](22-AOS开源产品维护清单.md) |
| MediaSet / OCR | [T05](T05-L1数据集成详细技术方案.md) |
| Lite Spoke / Vault / Ferry | [T09](T09-Apollo交付引擎详细技术方案.md) |
| IdP / Authz / 观测 | [T-CROSS](T-CROSS-横切能力详细技术方案.md) |

---

## 8. 模板与示例路径（随仓建立）

| 路径（建议） | 内容 |
| --- | --- |
| `docs/examples/customer-prereq/prereq-handoff.example.yaml` | 交接模板 |
| `docs/examples/customer-prereq/grafana/*.json` | Dashboard（仅 JSON） |
| `docs/examples/customer-prereq/README.md` | 「此目录=客户侧示例，非 AOS 运行时」 |
| `deploy/dev/` | 仅开发 Compose；CI 打包排除 |

> 上述路径若尚未建文件：以本 SOP 为准，**建文件时不得改变军规语义**。

---

## 9. 变更日志（活文档 · 强制追加）

> **规则：** 开发联调或实施中每发现一条安装/对接细节，**当日**追加一行；禁止攒到项目结束。

| 日期 | 环境 | 组件 | 问题 / 决策 | 作者 |
| --- | --- | --- | --- | --- |
| 2026-07-17 | — | SOP | 骨架发布；总顺序与总检生效 | AOS 架构 |
| 2026-07-17 | Dev 参考树 | PaddleOCR / MinIO / minio-py | 研发侧 `refs/` 已 clone（≠ 客户环境已装）；客户仍须按 §3.2 自装 MinIO 发行包 | 核盘 |

---

## 10. 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1 | 2026-07-17 | 首版骨架：总顺序 · 矩阵 · 分组件结构 · 总检 · 安装器契约 · 变更日志机制 |

---

*24 · 先地基后盖房 · 细节写进变更日志 · 现场不再从零回忆*

# 24 · AOS 客户侧前置组件安装 SOP

> **文档性质**：**活文档 SOP**（开发期 / 实施期持续补全；禁止「到现场再写」）  
> **版本**：v0.2 · 2026-07-18（补 **macOS Dev 缩小版** 启动路径；Windows 仍可用 `scripts/demo/*.ps1`）  
> **状态**：实施门禁真源 · 对齐军规 [23](23-AOS开源引用与交付军规.md) **R-INST-***  
> **读者**：客户 IT · FDE · 实施 · 研发（Dev 环境同样走一遍缩小版）  
> **配套**：[22](22-AOS开源产品维护清单.md) · [27](27-本机开发基础设施与工程门禁记录.md) · [72](72-系统启停与健康检查手册.md) · [T05](T05-L1数据集成详细技术方案.md) · [T09](T09-Apollo交付引擎详细技术方案.md) · [T-CROSS](T-CROSS-横切能力详细技术方案.md)

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
| 已知坑 | **macOS Dev（2026-07-18）**：Docker Hub 拉 `postgres:16-alpine` 超时 → 用 micromamba `postgresql=16` 原生装，`initdb` + `port=5433` 对齐 Compose 端口；TCP 用 `scram-sha-256`，本机 socket 可 `trust` 便于建库 |

### 3.2 对象存储 · MinIO / 客户 S3（MediaSet）

| 项 | 内容 |
| --- | --- |
| 目的 | MediaSet 原件（T05 L1-06） |
| 版本建议 | MinIO 发行版（客户从官网/镜像站装）；**不要用 AOS 包内嵌** |
| 安装要点 | 建 bucket（如 `aos-media`）；HTTPS 优先；AK/SK 进 Vault |
| 验收 | `mc ls` 或 S3 ListBucket 成功；上传 1KB 探测对象可 Get |
| 交给 AOS | `S3_ENDPOINT` · `S3_BUCKET` · `S3_REGION` · `S3_ACCESS_KEY_REF` · `S3_SECRET_KEY_REF` · `S3_PATH_STYLE=true`（MinIO 常见） |
| **军规** | AOS 仅 `S3Adapter`；切换客户云 S3 **不改**业务代码 |
| 已知坑 | 路径风格 / 证书 / 时钟偏差导致签名失败 — 记 §9；**macOS Dev**：Docker Hub 拉 MinIO 镜像超时 → 客户/研发可改下官方 **darwin-arm64 二进制**（`minio server … --address 127.0.0.1:9000`），bucket `aos-media`，验收仍按 Put/Get；**勿**把该二进制打进 AOS 客户包 |

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
| 2 | 仍填写一份缩小版 `prereq-handoff.yaml`（参考 `aos-platform/deploy/dev/prereq-handoff.local.yaml`） |
| 3 | 跑通 §5 总检中 Lite 必选项 |
| 4 | 联调坑记入 §9 |

### 4.1 跨 OS 对照（Windows / macOS / Linux）· **分轨原则**

> **强制分轨：** 三大系统的 **安装前置 · 本机启动 · 打包交付** 可各自维护，**互不覆盖**。  
> - Windows 继续只用 `*.ps1`（已证路径，**本次未改**）。  
> - macOS / Linux 新增 `*.sh`（并列，不替换 ps1）。  
> - 客户包 / Ferry 打包脚本仍按目标 OS 分目录或分脚本；禁止「一个脚本通吃三端」硬改 Windows 现网流程。

| 维度 | Windows | macOS | Linux |
| --- | --- | --- | --- |
| 安装前置 | Docker Desktop + 本机 Python/Node（见 27） | Docker Desktop / 原生降级（§4.2～§4.4） | Docker Engine 或发行版包；脚本可复用 `*.sh` |
| 一键启动 | `scripts\demo\start-local.ps1` | `scripts/demo/start-local.sh`（Hub 不通 → `start-local-native.sh`） | 同 mac：`*.sh` |
| 健康检查 | `health-check.ps1` | `health-check.sh` | `health-check.sh` |
| 停止 | `stop-local.ps1` | `stop-local.sh` | `stop-local.sh` |
| 打包 / 交付 | 既有 `scripts/ci/*.ps1`（Ferry/SBOM 等）**保持不动** | 另开 mac 打包清单（待补，不改 Win 脚本） | 另开 linux 打包清单（待补） |
| 工程根示例 | `c:\work\projects\wchat\aos-platform\` | `~/work/projects/ai_agent/aos-platform/` | 按现场约定 |

| 项 | Windows（已证） | macOS（Apple Silicon · 2026-07-18 联调） |
| --- | --- | --- |
| Docker / 数据面 | Compose：`aos-dev-pg` · MinIO · MySQL · LLM/OCR | **优先**同 Compose；Hub 超时则 §4.4 原生 PG+MinIO |
| 运行时 | Python 3.11+ · Node 18+/22 | **≥3.11**（系统 3.9 不够）· Node **18+** |
| 端口 | PG `5433` · MinIO `9000/9001` · API `8080` · Web `5173` · LiteLLM `4001` · OCR `8082` · MySQL `3307` | **同** |

**金句：** *客户侧仍按 §0.3 自装发行包；Dev 用 Compose 只是缩小版同构，禁止把 MinIO 打进客户包。Win / Mac / Linux 脚本分轨，改一端不碰另外两端。*

### 4.2 macOS 工具链安装（无 Homebrew / 无 sudo 时）

> 若本机有管理员密码，优先：`brew install --cask docker` + `brew install node python@3.12`。  
> 以下为 **无 sudo** 时用户目录安装（本机联调实证路径）。

| 组件 | 建议落点 | 安装要点 | 验收 |
| --- | --- | --- | --- |
| Node 22 | `~/tools/node-v22.*/bin` | 官方 `darwin-arm64` tarball 解压 | `node -v` ≥ 18 |
| Python 3.12 | micromamba env `aos` | `micromamba create -n aos python=3.12 pip` | `python --version` ≥ 3.11 |
| Docker 引擎 | Docker Desktop → `~/Applications/Docker.app` | 官网 `Docker.dmg`；**拖到用户 Applications**（避免 `/Applications` 需 sudo） | `docker version` · `docker compose version` |
| Colima 备选 | `~/tools/bin/colima` + Lima | 无 Desktop 时用；仍需 **docker CLI** 与 compose 插件 | `colima start` 后 `docker ps` |

**PATH 示例（写入 `~/.zshrc`）：**

```bash
export PATH="$HOME/tools/bin:$HOME/tools/node-v22.17.0-darwin-arm64/bin:$PATH"
# micromamba
export MAMBA_ROOT_PREFIX="$HOME/tools/micromamba-root"
eval "$("$HOME/tools/bin/micromamba" shell hook -s zsh)"
```

**Docker Desktop（用户目录）示意：**

```bash
# 1) 下载 https://desktop.docker.com/mac/main/arm64/Docker.dmg
# 2) hdiutil attach Docker.dmg
# 3) cp -R "/Volumes/Docker/Docker.app" "$HOME/Applications/"
# 4) open "$HOME/Applications/Docker.app"   # 等 whale 就绪
# 5) docker version && docker compose version
```

### 4.3 macOS / Linux 手工启动顺序（对齐 TB.0）

工作目录：`aos-platform/`。口令与 Windows 一致（仅 Dev，见 compose / `.secrets.env`）。

```bash
# 0) 环境
export PATH="$HOME/tools/bin:$HOME/tools/node-v22.17.0-darwin-arm64/bin:$PATH"
eval "$("$HOME/tools/bin/micromamba" shell hook -s bash)"
micromamba activate aos
cd "$HOME/work/projects/ai_agent/aos-platform"   # 按本机改路径

# 1) 可选：创建 Dev secrets（gitignored；与 compose 默认口令对齐）
cat > deploy/dev/.secrets.env <<'EOF'
POSTGRES_PASSWORD=aos_dev_only_change_me
MINIO_ROOT_USER=aosdev
MINIO_ROOT_PASSWORD=aos_dev_only_change_me
AOS_LLM_MASTER_KEY=aos_dev_litellm_master
EOF

# 2) 前置组件（§0.3 缩小版 · 客户现场则自装发行包，不走这步）
docker compose -f deploy/dev/docker-compose.yml up -d \
  aos-dev-pg aos-dev-minio aos-dev-minio-init \
  aos-dev-mysql aos-dev-llm-echo aos-dev-litellm aos-dev-ocr

# 3) 探针（Lite 必）
docker exec aos-dev-pg pg_isready -U aos_app -d aos_meta
curl -sf http://127.0.0.1:9000/minio/health/live   # 期望 HTTP 200

# 4) aos-api
cd services/aos-api
pip install -e .
export AOS_LOG_LEVEL=debug AOS_LOG_FORMAT=json AOS_AUTH_ALLOW_DEV=1
export AOS_DATABASE_URL="postgresql://aos_app:aos_dev_only_change_me@127.0.0.1:5433/aos_meta"
export AOS_S3_ENDPOINT=http://127.0.0.1:9000 AOS_S3_BUCKET=aos-media
nohup python -m uvicorn aos_api.main:app --host 127.0.0.1 --port 8080 \
  > ../../deploy/dev/aos-api.out.log 2> ../../deploy/dev/aos-api.err.log &
curl -sf http://127.0.0.1:8080/v1/health

# 5) Web
cd ../../apps/web
npm install
nohup npm run dev -- --host 127.0.0.1 --port 5173 \
  > ../../deploy/dev/aos-web.out.log 2> ../../deploy/dev/aos-web.err.log &
curl -sf -o /dev/null -w "%{http_code}\n" http://127.0.0.1:5173/
```

**成功标志：**

| 检查 | 期望 |
| --- | --- |
| `GET /v1/health` | HTTP 200 |
| Web `http://127.0.0.1:5173/` | 可打开（演示导航 `/demo`） |
| PG / MinIO | `pg_isready` 成功 · MinIO live 200 |
| 鉴权（演示） | `Authorization: Bearer dev`（`AOS_AUTH_ALLOW_DEV=1`） |

日常启停细节另见 [72](72-系统启停与健康检查手册.md)（原偏 Windows；mac 命令以本节为准）。

### 4.4 Docker Hub 不可达时的 Dev 原生降级（macOS 实证）

> **触发条件**：`docker pull` / `compose up` 对 `registry-1.docker.io` **context deadline exceeded**。  
> **原则**：仍满足 §5 Lite 必检（PG + 对象仓 Put/Get）；边车（LiteLLM/OCR/MySQL）可 WARN；**不改变**客户现场「自装发行包」责任。

| 组件 | 降级做法（本机） | 端口对齐 |
| --- | --- | --- |
| PostgreSQL 16 | micromamba `postgresql=16` → `initdb`（建议 `locale UTF-8` / 库 `ENCODING UTF8`）→ `port=5433` | `:5433` |
| MinIO | 官网/GitHub **darwin-arm64** 二进制：`minio server $DATA --address 127.0.0.1:9000 --console-address 127.0.0.1:9001` | `:9000` / `:9001` |
| bucket | Python `minio` 客户端或 `mc`：`aos-media` + Put/Get 探针 | — |
| aos-api / Web | 同 §4.3；`AOS_AUTH_ALLOW_DEV=1` | `:8080` / `:5173` |
| Compose 边车 | 可暂缓；健康检查 WARN 不挡 DEMO | `:4001` / `:8082` |

**initdb / 库编码（踩坑必记）：**

```bash
# 集群初始化时 locale 若为 C → SQL_ASCII，seed 含中文会 UnicodeEncodeError
# 建库务必：
createdb -p 5433 -U aos_app -E UTF8 -T template0 aos_meta
```

**脚本（aos-platform）：**

| 脚本 | 用途 |
| --- | --- |
| `scripts/demo/start-local.sh` | macOS/Linux 一键（优先 Compose；失败见日志） |
| `scripts/demo/start-local-native.sh` | **无镜像时** 启原生 PG（若已起可跳过）+ MinIO + API + Web |
| `scripts/demo/health-check.sh` | 探活；PG 支持 `docker exec` **或** 本机 `pg_isready` |

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
| 2026-07-18 | macOS arm64 Dev | 工具链 | 无 Homebrew sudo → 用户目录 Node 22 tarball + micromamba Python 3.12；Docker Desktop 装到 `~/Applications` | Agent |
| 2026-07-18 | macOS arm64 Dev | Docker Hub | `postgres`/`minio`/`mysql` pull **context deadline exceeded** → 启用 §4.4 原生降级 | Agent |
| 2026-07-18 | macOS arm64 Dev | PostgreSQL | micromamba PG16 · `:5433`；`createdb -E UTF8` 否则 seed 中文触发 `UnicodeEncodeError`（日志 `startup_meta_store_failed_continue`） | Agent |
| 2026-07-18 | macOS arm64 Dev | MinIO | 二进制 `RELEASE.2025-09-07…` · bucket `aos-media` · Put/Get `dev-probe.txt` OK；Console `:9001` | Agent |
| 2026-07-18 | macOS arm64 Dev | aos-api / Web | `GET /v1/health` 200 · Web `/` `/demo` 200 · `Bearer dev`；成功标志对齐 TB.0 | Agent |
| 2026-07-18 | 文档 | OS 分轨 | 明确 Win/Mac/Linux **安装·启动·打包可分开**；本次只增 `*.sh`，**零改动**全部 `*.ps1` | Agent |

---

## 10. 修订记录

| 版本 | 日期 | 说明 |
| --- | --- | --- |
| v0.1 | 2026-07-17 | 首版骨架：总顺序 · 矩阵 · 分组件结构 · 总检 · 安装器契约 · 变更日志机制 |
| v0.2 | 2026-07-18 | 补 macOS Dev §4.1～§4.4；Docker Hub 不可达原生降级；UTF8 建库坑；脚本指针 |

---

*24 · 先地基后盖房 · 细节写进变更日志 · 现场不再从零回忆*

# AOS Platform 部署架构与通信矩阵

> **版本**：v1.1 · 2026-07-26
> **定位**：AOS 物理部署架构、容器编排、服务间通信协议与网络拓扑的完整说明
> **前置阅读**：[02-AOS 技术架构总览](02-aos-technical-architecture.md)

---

## 一、部署形态概览

### 1.1 两种部署形态

AOS 支持两种物理部署形态，**逻辑分层不变，物理分布可变**：

| 形态 | 场景 | 存储层位置 | 重计算容器位置 | 适用客户 |
|------|------|-----------|-------------|---------|
| **独立集群**（分布式） | 生产 / 大型团队 | 高性能独立服务器或云数据库集群 | GPU 算力机或特定硬件机器 | 大型企业 / 国防 / 核电 |
| **单机 All-in-One** | Dev / 中小企业 / POC | 同一 Docker Compose 内 | 同一 Docker Compose 内 | 开发机 / 虚拟机 / 开箱即用 |

### 1.2 核心原则：逻辑分层与物理部署解耦

> 无论物理上是分散在多台机器还是集中在一台机器，系统内部的服务调用关系（Core API → 重计算容器 → Storage）保持不变。Core API 始终通过网络接口（HTTP/gRPC/TCP）与其他组件交互，**不通过本地文件共享数据**。

```
              ┌─ 独立集群形态 ───────────────────────────────┐
              │                                              │
              │  机架 A              机架 B          机架 C    │
              │  ┌──────┐           ┌──────┐      ┌──────┐  │
              │  │Core  │─HTTP─→    │LiteLLM│      │ PG   │  │
              │  │API   │─HTTP─→    │OCR    │      │MinIO │  │
              │  │      │─TCP──→    │Analy. │      │Qdrant│  │
              │  └──────┘           └──────┘      └──────┘  │
              └──────────────────────────────────────────────┘

              ┌─ 单机 All-in-One 形态 ──────────────────────┐
              │                                              │
              │           单台物理机 / 虚拟机                  │
              │  ┌──────────────────────────────────────┐   │
              │  │  Docker Engine                        │   │
              │  │  ┌──────┐ ┌──────┐ ┌──────┐ ┌──────┐│   │
              │  │  │Core  │ │Lite  │ │ PG   │ │MinIO ││   │
              │  │  │API   │ │LLM   │ │      │ │      ││   │
              │  │  │:8080 │ │:4001 │ │:5433 │ │:9000 ││   │
              │  │  └──┬───┘ └──┬───┘ └──┬───┘ └──┬───┘│   │
              │  │     │        │        │        │     │   │
              │  │     └──Docker Bridge Network──────┘    │   │
              │  └──────────────────────────────────────┘   │
              └──────────────────────────────────────────────┘
```

**单机模式下依然是多服务间调用**：

Docker 为每个容器分配独立的网络命名空间——即使在同一物理机上，各服务在网络层面也像运行在不同的"虚拟机"中。Core API 不会直接连接 `localhost:5433`，而是通过 Docker 内部 DNS（如 `aos-dev-pg:5432`）发现并连接数据库。容器间流量依然经过虚拟网卡、通过 Docker Bridge 网络到达目标端口，这是一次标准的 HTTP/TCP 跨进程调用，只是跳过了物理交换机。

---

## 二、Docker 容器编排

### 2.1 Dev 环境容器清单（11 个核心 + 4 个可选 Profile）

Dev 环境使用 `deploy/dev/docker-compose.yml` 编排，一键拉起所有依赖：

| 容器名 | 镜像 | 宿主端口 | 容器端口 | 用途 | Profile |
|--------|------|---------|---------|------|---------|
| `aos-dev-pg` | postgres:16-alpine | 5433 | 5432 | PostgreSQL 元数据库 | 默认 |
| `aos-dev-minio` | minio:RELEASE.2025-04-22 | 9000 / 9001 | 9000 / 9001 | S3 对象存储 + 控制台 | 默认 |
| `aos-dev-minio-init` | minio/mc | — | — | 一次性 Bucket 初始化任务 | 默认 |
| `aos-dev-llm-echo` | 自构建 | 8081 | 8081 | Dev Mock LLM 后端 | 默认 |
| `aos-dev-litellm` | 自构建 | 4001 | 4000 | LiteLLM 多模型代理 | 默认 |
| `aos-dev-ocr` | 自构建 PaddleOCR | 8082 | 8082 | PaddleOCR 文档智能解析引擎 | 默认 |
| `aos-dev-analytics` | 自构建 Jupyter Notebook 7 | 8084 / 8888 | 8084 / 8888 | Jupyter 嵌入式交互分析引擎 | 默认 |
| `aos-dev-mysql` | mysql:8.4 | 3307 | 3306 | ⚠️ 外部数据源模拟（不打包进客户 AOS） | 默认 |
| `aos-dev-keycloak` | keycloak:26.0.2 | 8083 | 8080 | OIDC IdP（SSO） | `oidc` |
| `aos-dev-keycloak-a/b` | keycloak:26.0.2 | — | 8080 | HA Keycloak 双节点 | `oidc-ha` |
| `aos-dev-keycloak-lb` | nginx:1.27 | 8083 | 80 | HA 负载均衡器 | `oidc-ha` |
| `aos-dev-openfga` | openfga:v1.8.4 | 8085 / 8086 | 8080 / 8081 | 关系型授权引擎 | `openfga` |

> **关键说明**：Dev compose 的 MySQL 容器注释明确写着 `customer brings own DB in prod; not in customer AOS package`。生产环境中 MySQL 是客户自带的业务数据库，AOS 通过 Connector 远程只读访问。

### 2.2 Docker 网络拓扑

```
┌─ Docker Network: aos-dev-prereq (bridge) ──────────────────────────┐
│                                                                    │
│  ┌──────────┐   HTTP    ┌──────────┐   HTTP    ┌──────────┐       │
│  │ Core API │──────────→│ LiteLLM  │──────────→│ LLM Echo │       │
│  │ :8080    │           │ :4000    │           │ :8081    │       │
│  │ (host)   │           │          │           │          │       │
│  └──┬───┬───┘           └──────────┘           └──────────┘       │
│     │   │                                                          │
│     │   │  HTTP     ┌──────────┐                                   │
│     │   ──────────→│PaddleOCR│                                   │
│     │              │ :8082    │                                   │
│     │              └──────────┘                                   │
│     │                                                             │
│     │  TCP/PG   ┌──────────┐    S3/HTTP  ┌──────────┐            │
│     ──────────→│ PG       │            │ MinIO    │            │
│     │           │ :5432    │            │ :9000    │            │
│     │           └──────────┘            └──────────┘            │
│     │                                                             │
│     │  HTTP     ┌──────────┐                                      │
│     ──────────→│ Jupyter  │                                      │
│                 │ :8084    │                                      │
│                 └──────────┘                                      │
│                                                                   │
│  ※ 容器间用服务名通信（Docker DNS）                                  │
│    如 http://aos-dev-litellm:4000，而非 localhost                  │
└───────────────────────────────────────────────────────────────────┘

         ↑ 宿主机端口映射（ports: "宿主端口:容器端口"）
         │
    外部访问（localhost:5433, :8080 等）
```

**容器间通信关键点**：
- 同一 Docker 网络内，容器通过**服务名**相互发现（如 `http://aos-dev-litellm:4000`）
- Docker 内置 DNS 自动解析服务名到容器 IP
- Core API 配置中重计算容器地址指向容器名，非 `127.0.0.1`

### 2.3 数据卷与持久化

| 数据卷 | 挂载点 | 用途 |
|--------|--------|------|
| `aos_dev_pg_data` | `/var/lib/postgresql/data` | PG 元数据持久化 |
| `aos_dev_minio_data` | `/data` | MinIO 对象文件持久化 |
| `aos_dev_mysql_data` | `/var/lib/mysql` | ⚠️ Dev 模拟外部源数据（非 AOS 自有） |
| `aos_dev_kc_pg_data` | `/var/lib/postgresql/data` | HA Keycloak 共享数据库 |

---

## 三、逻辑分层与服务间调用

### 3.1 Core API 启动与监听

```
# Core API 启动命令
uvicorn aos_api.main:app --host 127.0.0.1 --port 8080
```

Core API 是一个 FastAPI 单进程应用，监听 `:8080`。生产环境可通过 Nginx / HAProxy 前置负载均衡实现水平扩展（无状态，状态全在 PG）。

### 3.2 完整服务调用链

```
┌─────────────────────────────────────────────────────────────────────┐
│                          客户端层                                     │
│                                                                     │
│   Web SPA (:5173 Dev)    Tauri Desktop    curl/Postman/第三方系统    │
│   React 18 + Vite        内嵌 WebView      直接 HTTP 调用            │
└──────────┬──────────────────┬──────────────────┬───────────────────┘
           │                  │                  │
           │     HTTP(S)      │   HTTP(S)       │  HTTP(S)
           │   (JSON-RPC)     │                 │
           ▼                  ▼                  ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    AOS Core API (:8080)                             │
│                    FastAPI · 单进程 · 无状态                          │
│                                                                     │
│  ┌───────────  权限校验（OIDC / JWT / API Key）──────────────┐      │
│  │                                                            │      │
│  │  ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐│      │
│  │  │Data OS │ │  AIP   │ │Workshop│ │Ontology│ │ Apollo ││      │
│  │  └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘ └───┬────┘│      │
│  │      │          │          │          │          │      │      │
│  │  ┌───▼──────────▼──────────▼──────────▼──────────▼──┐  │      │
│  │  │           Plugin Registry (70 插件)               │  │      │
│  │  └───┬──────────┬──────────┬──────────┬──────────┬──┘  │      │
│  │      │          │          │          │          │      │      │
│  └──────┼──────────┼──────────┼──────────┼──────────┼──────┘      │
└─────────┼──────────┼──────────┼──────────┼──────────┼─────────────┘
          │          │          │          │          │
          ▼          ▼          ▼          ▼          ▼
     ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐ ┌────────┐
     │LiteLLM │ │  OCR   │ │Analyt. │ │  PG    │ │ MinIO  │
     │:4001   │ │ :8082  │ │ :8084  │ │:5433   │ │ :9000  │
     └───┬────┘ └────────┘ └────────┘ └────────┘ └────────┘
         │ HTTP
         ▼
     ┌────────┐
     │LLM Echo│
     │ :8081  │
     └────────┘
```

### 3.3 各层调用协议详解

#### 第一跳：客户端 → Core API

| 客户端类型 | 传输协议 | 实际场景 |
|-----------|---------|---------|
| Web SPA（浏览器） | HTTPS（生产）/ HTTP（Dev localhost） | 浏览器加载前端 → 前端 API 客户端走 HTTP(S) 调 Core API |
| Tauri Desktop | HTTPS（生产）/ HTTP（Dev） | 桌面应用内嵌 WebView，调用逻辑同 Web SPA |
| 第三方系统 / curl | HTTPS（生产）/ HTTP（内网） | 直接 POST 到 Core API 端点 |

**关键规则**：
- 跨网络 / 公网暴露 → **强制 HTTPS**（TLS 终止在反向代理或 Core API 前）
- Dev 环境同机 localhost → 可暂用 HTTP（Core API 默认监听 `:8080`）
- 客户内网部署 → 至少走 HTTPS 或在内网 LB 上做 TLS 终止

> 生产环境强制 HTTPS 是业界通行做法。TLS 提供传输层安全，防止中间人攻击和凭证泄露。

#### 第二跳：Core API → 重计算容器（LiteLLM / PaddleOCR / Jupyter）

| 目标 | 默认协议 | 端口 | 原因 |
|------|---------|------|------|
| LiteLLM | HTTP | 4001 | 容器内网可信 |
| PaddleOCR | HTTP | 8082 | 容器内网可信 |
| Jupyter | HTTP | 8084 | 容器内网可信 |
| LLM Echo | HTTP | 8081 | Dev only |

**Docker 内部容器间通信默认 HTTP 明文**，原因：
1. 同一 Docker 网络（bridge / overlay）内，容器间通信被视为可信网络
2. 性能考虑：TLS 握手开销对内网高频调用不划算
3. 重计算容器默认不开启 TLS

**跨主机 / 跨信任域时的加密方案**：

| 方案 | 做法 | 适用场景 |
|------|------|---------|
| **方案 A：服务网格** | 在 Core API 和重计算容器间加 Istio / Linkerd，通过代理做 mTLS | 大规模 K8s 集群 |
| **方案 B：端到端 TLS** | 重计算容器配置 TLS 证书，Core API 通过 `https://` 调用 | 简单部署 / 少量服务 |

> **当前架构文档未强制这一跳走 HTTPS**。跨主机部署时，必须启用 mTLS 或 HTTPS。

#### 第三跳：Core API → 存储层（PG / MinIO / Qdrant）

| 目标 | 协议 | 端口 | 生产要求 |
|------|------|------|---------|
| PostgreSQL | PG-TCP（自有协议） | 5433 | `sslmode=require` |
| MinIO | S3 over HTTP | 9000 | 启用 TLS 或网络隔离 |
| Qdrant | gRPC / HTTP | 6333 | 默认不加密，网络隔离 |

PostgreSQL 使用自己的 TCP 协议（非 HTTP），MinIO S3 API 默认 HTTP 明文。生产环境建议：
- PostgreSQL 启用 `sslmode=require`
- MinIO 启用 HTTPS（配置 TLS 证书）
- 存储子网网络隔离，不允许外部访问

#### 第四跳：Core API → 外部数据源

| 数据源类型 | 协议 | 生产要求 |
|-----------|------|---------|
| MySQL / SQL Server | JDBC over TCP | 跨公网必须 SSH 隧道或 VPN |
| REST API（淘宝 / 京东等） | HTTPS | 强制 TLS + API 签名 |
| GraphQL（Shopify） | HTTPS | 强制 TLS + Access Token |

---

## 四、通信安全矩阵

### 4.1 完整通信矩阵

| 通信路径 | 协议 | 生产环境要求 |
|---------|------|-------------|
| 浏览器 → Core API | HTTP(S) | **公网强制 HTTPS**（TLS 1.2+，HSTS） |
| Tauri Desktop → Core API | HTTP(S) | 同上 |
| 第三方系统 → Core API | HTTP(S) | API Key + TLS |
| Core API → LiteLLM | HTTP（内网） | 跨主机必须 mTLS / HTTPS |
| Core API → OCR | HTTP（内网） | 同上 |
| Core API → Jupyter | HTTP（内网） | 同上 |
| Core API → PostgreSQL | PG-TCP（SSL 可选） | `sslmode=require` |
| Core API → MinIO | S3 over HTTP | 启用 TLS 或网络隔离 |
| Core API → Qdrant | gRPC / HTTP | 网络隔离 |
| Core API → 外部数据源 | JDBC / REST(S) | 跨公网强制 HTTPS / VPN |
| LiteLLM → LLM Echo | HTTP（内网） | Dev only |
| LiteLLM → 外部 LLM API | HTTPS | 强制 TLS + API Key |

### 4.2 Dev vs 生产 对比

| 维度 | Dev 环境 | 生产环境 |
|------|---------|---------|
| 客户端 → Core API | HTTP（localhost） | HTTPS（TLS 1.2+） |
| Core API → 重计算容器 | HTTP（Docker bridge） | mTLS 或 HTTPS（跨主机时） |
| Core API → PG | TCP 明文 | `sslmode=require` |
| Core API → MinIO | HTTP 明文 | HTTPS 或网络隔离 |
| 认证 | Dev JWT（`AOS_AUTH_ALLOW_DEV=1`） | OIDC（Keycloak / 客户 IdP） |
| 授权 | PG 内置 authz_tuple | OpenFGA + 字段级 Marking |

> Dev 环境为简化开发，所有内部通信可暂用 HTTP（localhost）。生产环境按上表要求加固。

---

## 五、生产部署架构（Ferry 离线交付）

### 5.1 气隙环境交付流程

AOS 生产部署面向气隙环境（Air-gapped），通过 **Ferry 摆渡机制**完成镜像同步：

```
    ┌─ AOS 中心仓库 ─┐                    ┌─ 客户气隙环境 ────────┐
    │                │                    │                      │
    │  Harbor / HUB  │   Ferry 摆渡        │  本地 Registry       │
    │  (公网/内网)    │   ════════════→    │  (无外网)             │
    │                │   Skopeo + Cosign   │                      │
    │  镜像签名       │   HMAC-SHA256       │  镜像验签             │
    │                │                    │                      │
    └────────────────┘                    └──────────────────────┘
```

**Ferry 交付内容**：

| 类别 | 内容 | 镜像来源 |
|------|------|---------|
| **存储** | PostgreSQL 16 / MinIO / Qdrant | 官方镜像 |
| **重计算容器** | LiteLLM / PaddleOCR / Jupyter | 自构建 |
| **Core API** | AOS 主应用 | 自构建 |
| **可选** | Keycloak / OpenFGA | 官方镜像 |

> **注意**：生产环境中的 MySQL **不打包进 Ferry 交付包**——客户自带业务数据库。

### 5.2 Hub / Spoke 模型

生产部署采用 Hub-Spoke（中心-边缘）模型：

```
              ┌─ Hub（中心仓库）──────────────────┐
              │  • 镜像仓库 (Harbor)               │
              │  • 发布通道 (dev→staging→stable)    │
              │  • 变更审批                         │
              │  • Cosign 签名                      │
              └──────────┬─────────────────────────┘
                         │
                    Ferry 摆渡
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
    ┌─ Spoke 1 ─┐  ┌─ Spoke 2 ─┐  ┌─ Spoke N ─┐
    │ 客户 A     │  │ 客户 B     │  │ 客户 N     │
    │ 本地部署   │  │ 本地部署   │  │ 本地部署   │
    │ 气隙环境   │  │ 内网环境   │  │ 混合云     │
    └──────────┘  └──────────┘  └──────────┘
```

### 5.3 发布通道

| 通道 | 用途 | 状态 |
|------|------|------|
| `dev` | 开发测试 | 持续集成产出 |
| `staging` | 预发布验证 | 通过自动化测试后晋升 |
| `stable` | 生产发布 | 通过人工审批 + 签名验证后晋升 |

渐进式发布流程：`dev` → 自动化测试 → `staging` → 审批 → `stable` → Ferry → 客户 Spoke

---

## 六、Tauri 桌面应用部署

### 6.1 架构

```
┌─ Tauri Desktop App ─────────────────────────┐
│                                             │
│  ┌─ Native Shell (Rust) ─────────────────┐  │
│  │  • 系统托盘 / 通知                     │  │
│  │  • 文件系统访问                        │  │
│  │  • 本地 SQLite（可选缓存）             │  │
│  └──────────┬────────────────────────────┘  │
│             │                               │
│  ┌──────────▼────────────────────────────┐  │
│  │  WebView (内嵌浏览器引擎)              │  │
│  │  • 加载 React SPA 前端资源             │  │
│  │  • 复用 Web SPA 全部 UI 逻辑           │  │
│  │  • API 调用逻辑同 Web SPA              │  │
│  └──────────┬────────────────────────────┘  │
│             │                               │
│             │  HTTP(S)                      │
│             │  (同 Web SPA)                 │
└─────────────┼───────────────────────────────┘
              │
              ▼
        Core API (:8080)
```

### 6.2 三种发布通道配置

桌面应用支持三种发布通道，通过 `channel.*.json` 配置：

| 通道 | 文件 | 更新源 | 适用场景 |
|------|------|--------|---------|
| Local | `channel.local.json` | 本地开发服务器 | Dev 调试 |
| Private | `channel.private.json` | 企业内网 | 内网部署 |
| SaaS | `channel.saas.json` | AOS 云端 | 公有云 SaaS |

---

## 七、网络拓扑总结

### 7.1 网络分区模型

生产环境建议三个网络分区：

```
┌─ DMZ 区（公网入口）─────────────────────────────────────────┐
│                                                            │
│  Nginx / HAProxy（TLS 终止）                                │
│  • HTTPS :443 → HTTP :8080                                 │
│  • HSTS / 速率限制                                          │
│                                                            │
└──────────────────────┬─────────────────────────────────────┘
                       │
┌─ 应用区（Core API + 重计算容器）──────────────────────────┐
│                                                            │
│  Core API (:8080)                                          │
│  LiteLLM (:4001) · PaddleOCR (:8082) · Jupyter (:8084)   │
│  Keycloak (:8083) · OpenFGA (:8085)                       │
│                                                            │
│  ※ 此区容器间 HTTP 明文，跨主机时启用 mTLS                    │
│                                                            │
└──────┬─────────────────────────────────┬───────────────────┘
       │                                 │
┌─ 存储区（不允许外部访问）──────────┐  │
│                                  │  │
│  PostgreSQL (:5433, sslmode)     │  │  ┌─ 外部区 ────────────┐
│  MinIO (:9000, TLS)              │  │  │ 客户业务库 (MySQL)   │
│  Qdrant (:6333)                  │  │  │ Connector 只读接入   │
│                                  │  │  │ 跨公网走 HTTPS/VPN   │
└──────────────────────────────────┘  └──────────────────────┘
```

### 7.2 端口分配总表

| 端口范围 | 用途 | 可见性 |
|---------|------|--------|
| 8080 | Core API | 应用区内 |
| 4001 | LiteLLM | 应用区内 |
| 8081 | LLM Echo | Dev only |
| 8082 | PaddleOCR 文档智能解析 | 应用区内 |
| 8083 | Keycloak | DMZ（SSO 入口） |
| 8084 / 8888 | Jupyter Ticket Facade / Notebook UI | 应用区内 |
| 8085 / 8086 | OpenFGA | 应用区内 |
| 5433 | PostgreSQL | 存储区内 |
| 9000 / 9001 | MinIO S3 / Console | 存储区内 |
| 3307 | Dev MySQL（⚠️ 模拟外部源） | Dev only |
| 5173 | Vite Dev Server | Dev only |
| 443 | 生产 HTTPS 入口 | DMZ |

---

## 八、部署清单速查

### 8.1 最小生产部署

| 组件 | 规格 | 数量 |
|------|------|------|
| Core API | 4C8G | 1+（可水平扩展） |
| PostgreSQL | 8C32G + SSD | 1（建议主从） |
| MinIO | 4C16G + 大容量磁盘 | 1+ |
| LiteLLM | 2C4G | 1 |
| PaddleOCR（可选） | 4C8G | 1 |
| Jupyter（可选） | 4C8G | 1 |

### 8.2 启动顺序

```
1. 存储层（PG → MinIO → MinIO Init）
2. 重计算容器（LLM Echo → LiteLLM → PaddleOCR → Jupyter）
3. 认证（Keycloak → OpenFGA）
4. Core API（最后启动，探测所有依赖就绪后对外服务）
```

> Core API 启动时会通过 `probe_sidecar()` 逐一探测所有独立容器健康状态。任何容器不可用时，Core API 自动降级到 fallback 模式（mock/off），系统不中断。

---

## 九、PaddleOCR 文档智能解析引擎 — 详细交互

### 9.1 核心定位

PaddleOCR 不是单纯的「文字识别工具」，是 AOS 三层文档智能 Pipeline 的执行载体——负责把非结构化文档（PDF / Office / 图片）转换为 AOS 可理解的半结构化数据，是本体建模、RAG 检索、知识图谱构建的前置依赖。

```
原始文档（PDF/Office/图片）→ PaddleOCR 解析 → 结构化字段提取 → 本体语义映射
```

### 9.2 部署规格

| 配置项 | 取值 |
|--------|------|
| 容器名 | `aos-dev-ocr`（Dev）/ `aos-prod-ocr`（Prod） |
| 基础镜像 | 自构建 PaddleOCR 镜像（裁剪冗余依赖，体积 < 2GB） |
| 监听端口 | `:8082`（HTTP API） |
| 健康探测 | `GET /health` → `{"ok": true, "mode": "ocr"}` |
| 资源挂载 | 本地挂载 PaddleOCR 预训练模型目录，避免每次启动拉取模型 |

### 9.3 与 Core API 的交互流程

```
Core API 收到文档上传请求
    ↓
调用 PaddleOCR /api/v1/parse 接口（传入 MinIO 文件地址）
    ↓
PaddleOCR 执行解析：
  1. 布局分析（识别标题 / 段落 / 表格 / 图片区域）
  2. 文字识别（印刷体 / 手写体 / 扫描件适配）
  3. 结构化提取（表格转 CSV、表单字段提取）
    ↓
返回 JSON 结构化结果（含页码、bbox 坐标、文本内容、置信度）
    ↓
Core API 清洗结果 → 存入 PostgreSQL（元数据）+ MinIO（解析后中间文件）
    ↓
触发后续流程：自动关联本体 Wiki、更新对象属性、触发 RAG 索引
```

### 9.4 开发 / 运维注意点

- **降级规则**：PaddleOCR 不可用时，Core API 自动降级为「文件直存模式」——文档上传成功后标记为 `UNPARSED`，返回原始文件 URL，不阻塞主流程，后续可手动 / 定时触发重解析。
- **性能优化**：Dev 环境默认用 PaddleOCR 轻量模型（速度快，精度略低）；Prod 可切换高精度模型，或挂载 GPU 加速（需配置 `CUDA_VISIBLE_DEVICES`）。
- **安全约束**：OCR 容器禁止访问外网，所有模型 / 数据均在内网流转，避免敏感文档泄露。
- **输出规范**：OCR 返回的 bbox 坐标统一采用「左上角原点、像素为单位」标准，Core API 层做坐标转换适配前端渲染。

---

## 十、Jupyter Notebook 7 嵌入式交互分析引擎 — 详细交互

### 10.1 核心定位

Jupyter Notebook 7 不是独立的 BI 工具，是 AOS 内置的**轻量级数据分析与算法验证环境**——业务用户做数据探索和可视化，开发 / 算法同学调试 Evals 评测逻辑、验证 RAG 召回效果、跑离线数据校验脚本。

### 10.2 部署规格

| 配置项 | 取值 |
|--------|------|
| 容器名 | `aos-dev-analytics`（Dev）/ `aos-prod-analytics`（Prod） |
| 基础镜像 | 自构建 Jupyter Notebook 7 镜像（预装 pandas / matplotlib / plotly 等分析库） |
| 监听端口 | `:8084`（Ticket Facade API，对外鉴权入口）/ `:8888`（Notebook UI，仅内部访问） |
| 健康探测 | `GET /health` → `{"ok": true, "mode": "analytics"}` |
| 资源挂载 | 挂载 AOS 数据集目录到 `/opt/analytics/data`，直接读取 MinIO 中的文件 |

### 10.3 与 Core API 的交互流程

```
业务用户点击工作台「数据分析」按钮
    ↓
Core API 调用 Jupyter Ticket Facade /api/v1/ticket 接口
    ↓
Jupyter 生成临时访问凭证（有效期 30 分钟，绑定用户权限）
    ↓
前端携带凭证访问 Notebook UI，或直接调用 Jupyter 分析接口
    ↓
Jupyter 执行分析逻辑：
  1. 读取用户有权限的数据集（自动过滤越权数据）
  2. 执行 Notebook 代码 / 预定义分析模板
  3. 返回可视化结果（图表 / 聚合数据 / 分析报告）
    ↓
Core API 缓存分析结果 → 前端渲染展示
```

### 10.4 开发 / 运维注意点

- **权限控制**：严禁直接暴露 `:8888` Notebook 端口给前端。所有访问必须通过 Core API 的 Ticket Facade 鉴权，确保用户只能访问自己有权限的数据集。
- **资源隔离**：Notebook 会话设置 CPU / 内存配额（默认 2C4G），防止死循环 / 大数据计算拖垮整机；用户登出或无操作 30 分钟后自动销毁会话。
- **能力扩展**：镜像中预装 AOS Python SDK，开发同学可在 Notebook 中直接调用 Core API 接口拉取数据、验证算法逻辑。
- **降级规则**：Jupyter 不可用时，工作台「数据分析」模块显示「服务暂不可用」，但其他核心模块（本体管理、AIP 决策）不受影响，Core API 返回 503 状态码，前端提示用户稍后重试。

---

## 十一、两大重计算容器共同特性

| 特性 | 说明 |
|------|------|
| **网络访问** | 仅 Core API 可调用，不对外暴露端口；通过 Docker 内部 DNS 访问（如 `http://aos-dev-ocr:8082`），不写死 IP |
| **数据持久化** | 仅存临时中间数据，重启后可清理；核心元数据统一存在 PostgreSQL / MinIO |
| **健康探测** | Core API 每 10s 探测一次 `/health` 接口，连续 3 次失败标记为不可用，自动触发降级 |
| **部署灵活性** | 支持单机 All-in-One 部署（Dev 默认开启）、集群独立部署（Prod 按需扩容）；可通过 Docker Profile 控制启停 |
| **架构一致性** | 无论单机还是集群部署，Core API 调用逻辑完全一致，无需修改代码 |

---

> **相关文档**：
> - [01-为什么企业 AI 需要操作系统](01-why-enterprise-ai-needs-os.md)
> - [02-AOS 技术架构总览](02-aos-technical-architecture.md)

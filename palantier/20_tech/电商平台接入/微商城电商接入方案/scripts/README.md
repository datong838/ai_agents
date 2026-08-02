# 栖月汇旧数据接入脚本（已隔离，禁止运行）

> **2026-08-02 审计结论：** 本目录脚本与当前 OpenAPI、Pipeline 真实执行能力和 C0.2 安全边界不匹配。它们仅保留为历史参考，**不得在本地、测试或生产环境运行**。替代分层脚本和门禁见 [228 实施规格](../228-微商城专项实施准备与FDE全链路规格.md#4-fde-实施包结构)。

主要风险：默认 `limit=0` 全量读取；Connector ingest 直写遗留对象表；Pipeline/Schedule 请求体过时；全栈脚本会连续创建配置并触发运行；PowerShell 脚本复制数据库密钥到平台 `.env`。

| 脚本 | 作用 |
|------|------|
| `apply_aos_mysql_env.ps1` | 案例 `.env` → `aos-platform/.env` 的 `AOS_MYSQL_*` |
| `qyh_data_access.py` | QYH.1：JDBC 探活 + Source/Pipeline/Sync + 分表 **全量** ingest |
| `qyh_bootstrap_e2e.py` | **全栈**：Org/工作区 → 数据 OS 全量 → OT/Link → Inbox → Draft/AIP → Schedule/run |

## 前置

1. SSH 隧道：`13306` → 远端 MySQL（案例 `.env`）
2. 单机 AOS：`powershell -File scripts/demo/start-local.ps1`（Docker 需先起；Win 可经 WSL dockerd）
3. `AOS_AUTH_ALLOW_DEV=1`；Web `http://127.0.0.1:5173` · API `:8080`

## 历史命令（禁止执行）

```powershell
cd docs\palantier\20_tech\niushop电商案例
.\scripts\apply_aos_mysql_env.ps1
python .\scripts\qyh_bootstrap_e2e.py --skip-chat
```

冒烟（显式封顶，**非**交付默认）：

```powershell
python .\scripts\qyh_bootstrap_e2e.py --limit 40 --skip-chat
```

报告：`fixtures/e2e-bootstrap-report.json`（无密码）。

UI：顶栏切组织 **栖月汇** / 工作区 **测试工作区**（`org-qyh` / `qyh-test`）。

## 原则

- 零行业定制码；平台缺口见 `182w` §4.1 / `188w` 全量语义
- 不直写 PG；产品页不做假保存
- 探索页「采样」≠ 库内总量；写路径默认全表

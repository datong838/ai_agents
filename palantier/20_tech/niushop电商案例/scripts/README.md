# 栖月汇数据接入 / 全栈 bootstrap（代手工）

脚本代手工配置，**不进** `aos-platform`。只调通用 `/v1/*`。  
**数据目标是线上全量孪生**（默认 `limit=0`），不是演示子集。

| 脚本 | 作用 |
|------|------|
| `apply_aos_mysql_env.ps1` | 案例 `.env` → `aos-platform/.env` 的 `AOS_MYSQL_*` |
| `qyh_data_access.py` | QYH.1：JDBC 探活 + Source/Pipeline/Sync + 分表 **全量** ingest |
| `qyh_bootstrap_e2e.py` | **全栈**：Org/工作区 → 数据 OS 全量 → OT/Link → Inbox → Draft/AIP → Schedule/run |

## 前置

1. SSH 隧道：`13306` → 远端 MySQL（案例 `.env`）
2. 单机 AOS：`powershell -File scripts/demo/start-local.ps1`（Docker 需先起；Win 可经 WSL dockerd）
3. `AOS_AUTH_ALLOW_DEV=1`；Web `http://127.0.0.1:5173` · API `:8080`

## 一键全量孪生

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

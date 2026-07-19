# 145 · TWB.7 Hub/Spoke·气隙端 · Ferry↔端版本矩阵

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 方案定稿 · 已编码 · 已测试  
> **对齐**：[20b](20b-AOS端云分离与交付形态方案.md) E5 · [T09](T09-Apollo交付引擎详细技术方案.md) · Ferry T5.6 · [26 §14 TWB.7](26-AOS目标态开发计划.md) · TWC.2

## 1. 目标（DoD）

| 项 | 验收 |
| --- | --- |
| 矩阵真源 | Hub 公布 `desktop` / `spoke` / `ferryBundle` 最低与推荐版本 |
| 兼容检查 | `POST /v1/ops/version-matrix/check` → `ok` \| 分项 `block`/`warn`/`ok` |
| Ferry status | `ferry/status` 附带矩阵摘要，气隙现场可一眼对照 |
| UI | Ferry 页展示矩阵 + 本机探测输入（桌面版本可填） |
| 端 | 不直连 Spoke；只连控制面做兼容查询 |

## 2. 非目标

- Full Spoke/Helm 运行时  
- 现场 Ferry 强制 cosign 生产钥轮换（已有 T5.6 钩子）  
- 自动拒连旧桌面（本刀只报告；强制策略可配后置）  

## 3. 落点

| 路径 | 改动 |
| --- | --- |
| `aos_api/version_matrix.py` | 解析 · 比较 · 默认矩阵 |
| `aos_api/routers/ops_version_matrix.py` | GET/POST check |
| `ferry.ferry_status_payload` | 挂 `versionMatrix` |
| `remainder.tsx` ApolloFerryPage | 矩阵面板 |
| `tests/test_twb7_version_matrix.py` | 无 PG |

## 4. 版本比较

简化 semver：取前三段数字比较；后缀（`-dev`）忽略于「≥ min」判定（dev 视为该主版本可接受若数字部分满足）。

## 5. 自测

```bash
pytest tests/test_twb7_version_matrix.py -q
```

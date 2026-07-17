# 58 · OpenFGA 真边车（Dev）方案

> **版本**：v1.0 · 2026-07-17  
> **任务**：台账下一刀 #1 — OpenFGA 真边车（可选）  
> **对齐**：[55](55-TX.4-Marking继承与OpenFGA-Facade方案.md) · [T-CROSS](T-CROSS-横切能力详细技术方案.md) §2 · 军规 R-ARCH-01  
> **工程**：`deploy/dev` · `aos_api/openfga.py` · `scripts/ci`  
> **硬规则**：前端不直连 OpenFGA；边车 **profile 可选**；未起 → 本地元组（[55]）；不进客户默认包

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文后改 |
| 最小更改 | compose + bootstrap + 加强 facade；不改 Marking 继承 |
| 不影响主路径 | 无 `AOS_OPENFGA_API_URL` 时行为 = [55] |
| 诚实 | Dev memory/store；非生产多区域 OpenFGA 集群 |

---

## 1. 目标 / 非目标

| 目标（DoD） | 非目标 |
| --- | --- |
| `compose --profile openfga` 起 `openfga/openfga` `:8085` | 强制每人起边车 |
| bootstrap：CreateStore · WriteModel · Write 种子元组 | UI 策略编辑器 |
| aos-api：`check`/`write` 可走真 HTTP；`Read` 判对象是否受管 | 前端 import SDK |
| probe：未起 SKIP；起则 Check=allowed | 替换 Markings |
| 单测：mock HTTP Check 路径绿（不依赖 Docker） | 生产 HA OpenFGA |

---

## 2. 拓扑

```
aos-api  ──HTTP──►  openfga :8085  (profile openfga)
   │                    │
   └── authz_tuple PG ◄─┘  (本地镜像/兜底；bootstrap 双写种子)
```

| 变量 | 含义 |
| --- | --- |
| `AOS_OPENFGA_API_URL` | 如 `http://127.0.0.1:8085` |
| `AOS_OPENFGA_STORE_ID` | bootstrap 写入 |
| `AOS_OPENFGA_STRICT` | `1` 时远程失败 **不**回落本地（默认 `0` 回落） |

模型（最小）：

```
type user
type object
  relations
    define viewer: [user]
```

种子：`user:secret-user` `#viewer@` `object:WorkOrder:wo-fga-demo`（与 [55] 一致）。

---

## 3. 行为

| 调用 | URL 空 | URL 有 |
| --- | --- | --- |
| Check | 本地表 | 先 HTTP Check；失败则按 STRICT 回落/拒 |
| Write tuple | 本地 | 本地 + HTTP Write |
| has_tuples | 本地 | 本地 **或** HTTP Read 非空 |

`GET /v1/authz/status`：`mode=local|remote` · storeId · reachable。

---

## 4. 落点

| 路径 | 变更 |
| --- | --- |
| `docs/.../58-*.md` | 本文 |
| `deploy/dev/docker-compose.yml` | profile `openfga` |
| `deploy/dev/openfga/model.json` | 授权模型 |
| `scripts/ci/bootstrap-openfga.ps1` | store/model/tuple |
| `scripts/ci/probe-openfga.ps1` | SKIP 友好 |
| `aos_api/openfga.py` | remote read/write/strict |
| `routers/authz.py` | `/v1/authz/status` |
| `tests/test_openfga_remote.py` | mock HTTP |
| `.env.example` · 26/31/00/27 | 回写 |

---

## 5. 自测

- [x] mock remote Check → allowed / denied
- [x] 无 URL 时既有 `test_marking_inherit_openfga` 不回归
- [x] compose `--profile openfga config` 语法 OK
- [ ] （可选）bootstrap + probe

---

## 6. 风险

| 风险 | 缓解 |
| --- | --- |
| store id 漂移 | bootstrap 写 `deploy/dev/openfga-store.env`（gitignore） |
| 边车未起 | 默认回落本地；STRICT 才硬失败 |
| 模型不兼容 | 固定 schema 1.1 最小 viewer |

---

*v1.0*

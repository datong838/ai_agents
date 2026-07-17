# 59 · Ferry skopeo archive 现场演练方案

> **版本**：v1.0 · 2026-07-17  
> **任务**：台账下一刀 #1 — 真 skopeo archive 现场演练  
> **对齐**：[56](56-T5.6-Ferry镜像层Skopeo-cosign方案.md) · [T09](T09-Apollo交付引擎详细技术方案.md) §9.1  
> **工程**：`aos_api/ferry.py` · `scripts/ci`  
> **硬规则**：默认仍关 archive（不打大包）；`AOS_FERRY_SKOPEO=1` 才启用；无 PATH skopeo 时可用 **Docker 镜像** 回落；演练默认小镜像

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文后改 |
| 最小更改 | 扩 ferry skopeo 探测/拷贝；probe + 测 |
| 不影响主路径 | 默认 `AOS_FERRY_SKOPEO` 关；digest 层 [56] 不变 |
| 诚实 | 未起 Docker / 拉不到镜像 → SKIP，不挡 CI |

---

## 1. 目标 / 非目标

| 目标（DoD） | 非目标 |
| --- | --- |
| PATH **或** `quay.io/skopeo/stable` 可 `copy` → `artifacts/archives/*.tar` | 强制本机安装 skopeo 二进制 |
| 演练默认 ref：`AOS_FERRY_SKOPEO_REFS`（默认 `alpine:3.19`） | 默认把 postgres/minio 打进包 |
| `status.skopeo` / `skopeoMode=path\|docker\|none` · `skopeoArchiveEnabled` | cosign 生产 PKI |
| probe 脚本：未就绪 SKIP；就绪则 export 含 archive | Full Channel |
| 单测：mock docker/skopeo 命令路径；无工具不红 | 气隙硬件验收 |

---

## 2. 行为

| 条件 | 行为 |
| --- | --- |
| `AOS_FERRY_SKOPEO`≠1 | 不打 archive（[56]） |
| =1 且 PATH 有 skopeo | `skopeo copy … docker-archive:` |
| =1 且无 PATH、有 docker | `docker run quay.io/skopeo/stable …`（bind `/mnt/<drive>/…` 或临时卷） |
| copy 失败 | 该 ref `archive=null`；包仍可导（digest+sig 在） |

`AOS_FERRY_IMAGES`：仍管清单/digest。  
`AOS_FERRY_SKOPEO_REFS`：仅这些 ref 尝试 archive（默认小 alpine）。

---

## 3. 落点

| 路径 | 变更 |
| --- | --- |
| `docs/.../59-*.md` | 本文 |
| `aos_api/ferry.py` | docker skopeo 回落 · refs 分离 · status 字段 |
| `scripts/ci/probe-ferry-skopeo.ps1` | 演练；SKIP 友好 |
| `tests/test_ferry_skopeo.py` | mock 出 archive |
| `.env.example` · 26/31/00/27 | 回写 |

---

## 4. 自测

- [x] 关 SKOPEO：export 无 archives（回归）
- [x] mock：开 SKOPEO → images.json 含 archive 路径且 tar 成员存在
- [x] probe：本机 Docker skopeo 真拷 `alpine:latest`（~8MB）
- [x] ferry 测 13 绿（含 skopeo + mvp + images）

---

## 5. 风险

| 风险 | 缓解 |
| --- | --- |
| 大镜像撑爆 | 默认只 alpine；清单镜像与 archive 列表分离 |
| WSL bind | 复用 `/mnt/<drive>/`（同 syft） |
| 拉 skopeo 镜像慢 | probe SKIP；CI 不强制 |

---

*v1.0*

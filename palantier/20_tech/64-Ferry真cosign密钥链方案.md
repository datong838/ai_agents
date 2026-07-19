# 64 · Ferry 真 cosign 密钥链（Dev）

> **版本**：v1.0 · 2026-07-17  
> **任务**：台账下一刀 #2 — Ferry Full Channel / 真 cosign（本刀只收 **真 cosign 密钥链**）  
> **对齐**：[53](53-T5.6-Ferry气隙MVP方案.md) · [56](56-T5.6-Ferry镜像层Skopeo-cosign方案.md) · [62](62-Ferry大镜像现场打包策略.md) · T09  
> **工程**：密钥脚本（**ps1 + [162](162-Ferry现场加严MVP方案.md) `.sh`**）· ferry cosign Docker 回落 · `AOS_FERRY_COSIGN_REQUIRED` · probe · 单测  
> **硬规则**：密钥不进 Git；默认仍可 `cosign-dev-hmac`；**Full Spoke/Channel 产品仍延期**（诚实标注）

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文后改 |
| 最小更改 | 密钥链 + 严格模式；不造假 Full 舰队 |
| 不影响主路径 | 未配 key → 行为 = [56] hmac |
| 诚实 | Full Channel ≠ cosign；本刀关闭「无真签」缺口 |

---

## 1. 目标 / 非目标

| 目标（DoD） | 非目标 |
| --- | --- |
| `gen-ferry-cosign-keys.ps1` 生成 key/pub 到 `deploy/dev/cosign/`（gitignore） | Fulcio / Rekor 公钥基础设施 |
| PATH cosign **或** Docker cosign 镜像签/验 blob | Full Spoke Helm/Argo 产品 |
| `AOS_FERRY_COSIGN_REQUIRED=1`：images 层拒绝 hmac 冒充 | 改 UI Ferry 页产品壳 |
| status：`cosignMode` · `cosignKeyConfigured` · `cosignRequired` · `fullChannelDeferred=true` | 宣称 Full Channel ✅ |
| probe / 单测（mock CLI）绿 | 强制每人装 cosign |

---

## 2. 行为

```
export images.sig:
  if COSIGN_KEY file + (PATH|docker) cosign → sign-blob → cosignMode=cosign
  else if COSIGN_REQUIRED → 500 FERRY_COSIGN_REQUIRED
  else → cosign-dev-hmac

import images.sig:
  if cosignMode=cosign → verify-blob（须 PUB）
  elif COSIGN_REQUIRED → 403（拒 hmac）
  else → hmac verify
```

| 变量 | 含义 |
| --- | --- |
| `AOS_FERRY_COSIGN_KEY` | 私钥路径 |
| `AOS_FERRY_COSIGN_PUB` | 公钥路径 |
| `AOS_FERRY_COSIGN_REQUIRED` | `1` 禁止 images hmac |
| `AOS_FERRY_COSIGN_IMAGE` | Docker 回落（默认 `ghcr.io/sigstore/cosign/cosign:v2.4.1`） |

---

## 3. 落点

| 路径 | 变更 |
| --- | --- |
| `docs/.../64-*.md` | 本文 |
| `scripts/ci/gen-ferry-cosign-keys.ps1` | 生成密钥 |
| `scripts/ci/probe-ferry-cosign.ps1` | 探针 |
| `aos_api/ferry.py` | Docker cosign · required · status |
| `tests/test_ferry_cosign.py` | mock |
| `.gitignore` · `.env.example` · 26/31/00/27 | 回写 |

---

## 4. 自测

- [x] 无 key → 仍 hmac（回归）  
- [x] REQUIRED=1 无 key → export 503  
- [x] mock cosign sign 路径绿  
- [x] import 拒 hmac when REQUIRED  
- [x] status.`fullChannelDeferred`=true  
- [x] 与 [56] 交叉一致（ferry images/mvp+cosign 15 绿）

---

*v1.0*

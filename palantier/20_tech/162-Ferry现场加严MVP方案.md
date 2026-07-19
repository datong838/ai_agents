# 162 · Ferry 现场加严 MVP

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 方案定稿 · 已编码 · 已自测  
> **对齐**：[62](62-Ferry大镜像现场打包策略.md) · [64](64-Ferry真cosign密钥链方案.md) · [153](153-Ferry大镜像打包分轨方案.md) · [118](118-产品1.3分析建模阶段退出收口.md) · [161](161-客户生产IdP验收规程-微商城案例.md)  
> **点名**：用户「继续干完记得单元测试」→ 现场加严下一刀

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 中文 · 先方案后编码 | 本文 → 再改码 |
| 最小更改 · 不破坏已有 | 默认仍 HMAC；cosign 仅 opt-in |
| 分轨 | **不改** `*.ps1`；补并列 `.sh` |
| 诚实 | 本刀 ≠ 客户气隙签收；≠ Full Channel；≠ CI 拉多 GB |
| 单元测试 | 无 Docker 可绿 ≥3 |

## 1. 背景与缺口

基线已齐：53 HMAC → 56 镜像层 → 59 skopeo → **62/153** onsite 大镜像 → **64** cosign 钩子。

| 缺口 | 本刀 |
| --- | --- |
| Unix 缺 `gen-ferry-cosign-keys.sh` / `probe-ferry-cosign.sh` | 补齐（对齐 ps1，不改 ps1） |
| Unix 缺 `probe-ferry-skopeo.sh` | 补齐（无 Docker SKIP） |
| onsite pack 仅 HMAC | `--sign-mode cosign` opt-in；默认 hmac 不变 |
| onsite ↔ API 契约缺单测 | `test_ferry_onsite_harden.py` |

## 2. DoD

| 项 | 验收 |
| --- | --- |
| `gen-ferry-cosign-keys.sh` | 无 cosign/docker → SKIP 0；有工具 → 写 `deploy/dev/cosign/` |
| `probe-ferry-cosign.sh` | 无密钥/工具 → SKIP 0；有则 sign-blob+verify |
| `probe-ferry-skopeo.sh` | 无 docker/本地镜像 → SKIP 0 |
| `pack-ferry-images-onsite.sh` | 默认 hmac；`--sign-mode cosign` 写 `cosignMode=cosign`；缺工具 FAIL |
| 单元测试 | HMAC 与 API `_verify_images_layer` 一致；`COSIGN_REQUIRED` 拒 hmac；maxGiB/onsitePack 契约 |
| 台账 | 26→v1.93 · 00→v1.0.131 · 118 回写 |

## 3. 非目标

- 客户现场气隙包代打 / CI 拉多 GB  
- Fulcio / 生产密钥托管  
- Full Channel / 真多集群舰队  
- 改 Windows `*.ps1`  
- 默认路径改成强制 cosign（破坏 Dev）

## 4. 落点

| 路径 | 变更 |
| --- | --- |
| `162-…` | 本文 |
| `scripts/ci/gen-ferry-cosign-keys.sh` | 新建 |
| `scripts/ci/probe-ferry-cosign.sh` | 新建 |
| `scripts/ci/probe-ferry-skopeo.sh` | 新建 |
| `scripts/ci/pack-ferry-images-onsite.sh` | `--sign-mode` + `cosignMode` |
| `aos_api/ferry.py` | `archive_exceeds_max_gib` · status planRef 挂 162 |
| `tests/test_ferry_onsite_harden.py` | 新建 ≥3 |
| `26` · `00` · `118` · `62`/`153`/`64` 互挂 | 回写 |

## 5. 契约（onsite ↔ import）

```
images.json:
  version, skopeoUsed, onsitePack=true,
  cosignMode: cosign-dev-hmac | cosign,
  images: [{ref, digest, digestSource, archive?}]

images.sig:
  hmac: hex(HMAC-SHA256(secret, b"ferry-images:" + body))
  cosign: cosign sign-blob 输出（与 API _cosign_verify_blob 一致）
```

`AOS_FERRY_COSIGN_REQUIRED=1` 时，`cosignMode≠cosign` 的现场包 **拒导**（与 64 一致）。

## 6. 自测结果（2026-07-19）

| 项 | 结果 |
| --- | --- |
| `pytest tests/test_ferry_onsite_harden.py` (+ onsite/cosign) | ✅ 16 passed, 2 skipped |
| `pack-ferry-images-onsite.sh --skip-archive` | ✅ hmac + `cosignMode=cosign-dev-hmac` |
| gen/probe cosign · probe skopeo（无 docker） | ✅ SKIP 0 |

## 7. 下一刀建议

- **真多集群舰队**（体量大，须单独点名）  
- 或客户 IdP 样例 token 后跑 [161] accept → 人签收  
- 不停刀则等点名；不自动开停车场项  

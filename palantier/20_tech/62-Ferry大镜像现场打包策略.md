# 62 · Ferry 大镜像现场打包策略

> **版本**：v1.0 · 2026-07-17  
> **任务**：台账下一刀 #1 — Ferry 大镜像现场打包策略  
> **对齐**：[53](53-T5.6-Ferry气隙MVP方案.md) · [56](56-T5.6-Ferry镜像层Skopeo-cosign方案.md) · [59](59-Ferry-skopeo-archive现场演练方案.md) · T09  
> **工程**：客户清单 · `pack-ferry-images-onsite.ps1` · **`pack-ferry-images-onsite.sh` / `probe-ferry-large-images.sh`（mac/Linux · [153](153-Ferry大镜像打包分轨方案.md)）** · **现场加严 [162](162-Ferry现场加严MVP方案.md)** · ferry 超时/体积门禁 · 预检探针  
> **硬规则**：默认 `AOS_FERRY_SKOPEO=0`；默认 archive 仍仅 alpine 演练；**大镜像不进默认 API export base64**；客户包不含强制大镜像

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文后改 |
| 最小更改 | 外置打包脚本 + 清单 + 超时/体积；不改 UI |
| 不影响主路径 | 未配清单 / 未开 skopeo → 行为 = [59] |
| 诚实 | 本刀 = 现场介质策略；非 Full Channel 产品 |

---

## 1. 目标 / 非目标

| 目标（DoD） | 非目标 |
| --- | --- |
| 客户清单 JSON 约定 + example | 强制 CI 拉 postgres 全量 archive |
| `pack-ferry-images-onsite.ps1`：离线打 `archives/*.tar` + `images.json` + sig | 改 Ferry UI |
| 可配超时 `AOS_FERRY_SKOPEO_TIMEOUT` · 体积门禁 `AOS_FERRY_SKOPEO_MAX_MIB`（超限不入 API 包） | 自动分卷 `.partNN` 产品（文档约定外置即可） |
| 预检 `probe-ferry-large-images.ps1`（无 Docker SKIP） | 替换 HMAC/cosign 主签路径 |
| 单测：清单解析 · 超时/门禁 helper | 真拷多 GB 进 CI |

---

## 2. 架构

```
[客户清单 customer-images.json]
        │
        ├─► aos-api（可选）AOS_FERRY_IMAGES_MANIFEST
        │     digest + images.sig；archive 仅 SKOPEO_REFS 且 ≤ MAX_MIB
        │
        └─► pack-ferry-images-onsite.ps1（现场主路径）
              OutDir/
                images.json + images.sig
                archives/*.tar          ← 大文件外置
                README-ONSITE.md
              主 ferry-bundle.tar.gz 仍可只含 manifest+images（不塞 GB 级 tar）
```

**默认不变量：** `AOS_FERRY_SKOPEO_REFS=alpine:latest`；大镜像只出现在客户清单 + 现场脚本。

---

## 3. 清单格式

`deploy/ferry/customer-images.example.json`：

```json
{
  "version": "1",
  "images": [
    { "ref": "alpine:latest", "archive": true, "maxGiB": 1 },
    { "ref": "postgres:16-alpine", "archive": false, "maxGiB": 2 }
  ]
}
```

| 字段 | 含义 |
| --- | --- |
| `ref` | 镜像引用 |
| `archive` | true → 允许 skopeo 打 tar（现场） |
| `maxGiB` | 预检/跳过阈值（脚本侧） |

Env：`AOS_FERRY_IMAGES_MANIFEST=<path>` → 合并进 `_image_refs` / archive 候选（覆盖逗号列表时以清单为准，若清单存在）。

---

## 4. 超时与体积

| 变量 | 默认 | 作用 |
| --- | --- | --- |
| `AOS_FERRY_SKOPEO_TIMEOUT` | path 600 / docker 900（秒） | 大镜像 copy |
| `AOS_FERRY_SKOPEO_MAX_MIB` | `64`（API 嵌入上限） | 超过则 **不**读入 export 内存；`archive=null`；现场用外置脚本 |
| 现场包 | 无上限（磁盘） | 由 `maxGiB` 预检 WARN/SKIP |

---

## 5. 落点

| 路径 | 变更 |
| --- | --- |
| `docs/.../62-*.md` | 本文 |
| `deploy/ferry/customer-images.example.json` | 示例清单 |
| `scripts/ci/pack-ferry-images-onsite.ps1` | 现场打包 |
| `scripts/ci/probe-ferry-large-images.ps1` | 预检 |
| `aos_api/ferry.py` | manifest · timeout · max MiB |
| `tests/test_ferry_onsite.py` | 解析/门禁 |
| `.env.example` · 26/31/00/27 | 回写 |

---

## 6. 自测

- [x] 清单解析单测绿  
- [x] MAX_MIB 门禁：超限不嵌入  
- [x] pack 脚本无 Docker → SKIP 或清晰错误；本机 alpine archive ~8.7MB OK  
- [x] probe 预检无参可用  
- [x] pack/probe **mac/Linux `.sh` 分轨** [153](153-Ferry大镜像打包分轨方案.md)（不改 ps1）

---

## 6b. Unix 用法（153）

```bash
bash scripts/ci/probe-ferry-large-images.sh
bash scripts/ci/pack-ferry-images-onsite.sh --skip-archive --out-dir deploy/dev/_ferry_onsite_sh
# 有 Docker 时去掉 --skip-archive；缺镜像加 --pull
```

## 7. 风险

| 风险 | 缓解 |
| --- | --- |
| API OOM | MAX_MIB + 外置打包 |
| WSL bind | 沿用 `/mnt/<drive>/...` |
| 超时杀进程 | 可配 TIMEOUT；失败 archive=null |

---

*v1.0*

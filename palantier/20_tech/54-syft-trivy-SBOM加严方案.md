# 54 · syft / trivy SBOM 加严（T0.10+）方案

> **版本**：v1.2 · 2026-07-17  
> **任务**：台账下一刀 #1 — **syft·trivy 可选加严**（HA Keycloak 仍 **B-TX3-01** 可选，本刀不强制起 HA）  
> **对齐**：[51](51-T0.9参考仓与T0.10-SBOM钩子方案.md) · [23](23-AOS开源引用与交付军规.md) §5 · [50](50-Dev-Keycloak联调缓解B-TX3方案.md)  
> **工程**：`aos-platform/scripts/ci`  
> **硬规则**：工具未装 → **SKIP/WARN**（不挡主路径）；`-Strict` 仅对**已跑出的违规**失败；`-RequireTools` 才因缺工具失败

---

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文后改 |
| 最小更改 | 新脚本 + 挂到 `check-sbom-gate -WithTools` |
| 不影响主路径 | 默认不强制装 syft/trivy |
| 诚实 | HA Keycloak ≠ 本刀交付 |

---

## 1. 目标 / 非目标

| 目标（DoD） | 非目标 |
| --- | --- |
| `run-syft-trivy.ps1`：优先 PATH，其次 Docker 镜像 | 本机强制安装 syft/trivy 二进制 |
| syft：对 `apps/web` + `services/aos-api` 生成 CycloneDX → `deploy/dev/sbom-syft.json` | 替代已有 `generate-sbom.ps1`（并存） |
| trivy：扫 fs（许可证/漏洞摘要）；命中 AGPL 镜像名 → 记 hit | 全量 CVE 阻断策略（可后置 CRITICAL） |
| 缺工具 / bind 不可用：exit 0 + SKIP；`-RequireTools` 才 FAIL | HA Keycloak 多节点集群 |

**HA Keycloak：** 继续用 [50] profile `oidc` 单机路径；HA 仅文档声明「现场 IdP 自备 / 换 JWKS URL」，不新开 compose HA。

---

## 2. 行为矩阵

| 条件 | 默认 | `-Strict` | `-RequireTools` |
| --- | --- | --- | --- |
| 无 syft 且无可用 docker bind | SKIP | SKIP | FAIL |
| syft 跑通写 sbom-syft.json | OK | OK | OK |
| trivy 发现 denied image 在**产品树** | WARN | FAIL | FAIL |
| trivy 仅扫到 deploy/dev | 忽略（23 例外） | 忽略 | 忽略 |

---

## 3. Docker bind（本机关键）

本仓 Windows 侧常见包装：`docker.cmd` → `wsl -d Ubuntu -- docker`。  
此时 `-v C:\...:/src` / `-v /c/...:/src` 会挂空或 invalid mode。

| 做法 | 说明 |
| --- | --- |
| 绑定路径 | `C:\work\...` → `/mnt/c/work/...` |
| 探针 | `alpine test -d /src/apps`；失败则禁用 docker 模式 → SKIP |
| 扫描范围 | syft：`apps/web`、`services/aos-api`；trivy docker：单目标 `/src/apps` |
| trivy docker | `--scanners license` + volume `aos-trivy-cache`（避免冷启动拉 vuln DB 挂死） |
| PATH trivy | 仍可用 `vuln,license` 全量 |

---

## 4. 落点

| 路径 | 变更 |
| --- | --- |
| `docs/.../54-*.md` | 本文 |
| `scripts/ci/run-syft-trivy.ps1` | **新建**（WSL bind + 探针） |
| `scripts/ci/check-sbom-gate.ps1` | `-WithTools` / `-RequireTools` |
| `deploy/dev/sbom-syft.json` | 生成物（有工具时） |
| `deploy/dev/trivy-fs.json` | 可选报告 |
| `deploy/dev/syft-trivy-report.md` | 摘要 |
| 26/31/00/27 | 回写 |

---

## 5. 自测

- [x] Docker bind 探针：`/mnt/c/...` 可见 `apps`
- [x] `run-syft-trivy.ps1 -SkipDockerPull`（镜像已在本地时）产出 syft/trivy 文件或诚实 SKIP
- [x] `check-sbom-gate.ps1 -WithTools` 不破坏既有 PASS
- [x] HA Keycloak 本刀不强制

---

## 6. 风险

| 风险 | 缓解 |
| --- | --- |
| 非 WSL docker（真 Docker Desktop） | `/mnt/c` 可能不适用 → 探针失败 → SKIP，不挡主路径 |
| trivy 首次拉 vuln DB 挂死 | docker 模式仅 license + cache 卷；PATH 模式可全量 |
| 扫描 node_modules 体积 | trivy docker 限 `/src/apps`；PATH 跳过 node_modules |

---

*v1.2*

# 153 · Ferry 大镜像现场打包 · mac/Linux 分轨

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 方案定稿 · 已编码 · 已测试  
> **对齐**：[62](62-Ferry大镜像现场打包策略.md) · [24](24-AOS客户侧前置组件安装SOP.md) 分轨 · [151](151-macOS打包清单与pack脚本方案.md)/[152](152-Linux打包清单与pack脚本方案.md) · 加严续刀 [162](162-Ferry现场加严MVP方案.md)

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| 分轨 | **不改** `*.ps1`；并列 `.sh` |
| 非停车场 | ≠ Full Spoke/Helm；= 62 现场介质策略的 Unix 可执行面 |
| 最小 | 无 Docker 时 probe/pack `--skip-archive` 仍可绿 |

## 1. DoD

| 项 | 验收 |
| --- | --- |
| probe | `scripts/ci/probe-ferry-large-images.sh` 解析 example 清单 |
| pack | `scripts/ci/pack-ferry-images-onsite.sh` 写 `images.json` + `images.sig`（HMAC 对齐 ferry） |
| 无 Docker | `--skip-archive` / probe SKIP docker 仍 exit 0 |
| 62/24 | 挂分轨路径；Win ps1 不动 |

## 2. 非目标

- 改 Ferry UI / Full Channel  
- CI 拉多 GB postgres  
- 替换 cosign 生产链  

## 3. 落点

| 路径 | 改动 |
| --- | --- |
| `153-…` | 本文 |
| `probe-ferry-large-images.sh` | 新建 |
| `pack-ferry-images-onsite.sh` | 新建 |
| `62` · `26` · `00` · `69` | 回写 |

## 4. 自测

```bash
bash scripts/ci/probe-ferry-large-images.sh
bash scripts/ci/pack-ferry-images-onsite.sh --skip-archive --out-dir deploy/dev/_ferry_onsite_sh
```

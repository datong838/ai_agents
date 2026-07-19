# 152 · Linux 打包清单与桌面 pack 脚本（分轨）

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 方案定稿 · 已编码 · 已测试  
> **对齐**：[24](24-AOS客户侧前置组件安装SOP.md) §4.1「linux 打包清单待补」· [151](151-macOS打包清单与pack脚本方案.md) · [20c](20c-AOS桌面端详细技术方案.md)

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| 分轨 | **不改** Win `*.ps1` / mac `pack-desktop-mac.sh`；并列 linux |
| 非停车场 | ≠ Full Spoke / 真 Jupyter |
| 最小 | `--check` 默认可跑；`--bundle` 可选 |

## 1. DoD

| 项 | 验收 |
| --- | --- |
| 24 §4.1 | linux「待补」→ 挂清单与脚本 |
| 清单 | `scripts/pack/linux-desktop.md` |
| 脚本 | `scripts/ci/pack-desktop-linux.sh --check` 绿 |
| 禁入客户包 | 同 24：MinIO/Compose/Dev KC 不进包 |

## 2. 非目标

- AppImage/deb 发行渠道产品化  
- 改 mac/Win 脚本  
- Helm  

## 3. 落点

| 路径 | 改动 |
| --- | --- |
| `152-…` | 本文 |
| `scripts/pack/linux-desktop.md` | 清单（含 webkit2gtk 依赖） |
| `scripts/ci/pack-desktop-linux.sh` | check / 可选 bundle |
| `24` · `26` · `00` | 回写 |

## 4. 自测

```bash
bash scripts/ci/pack-desktop-linux.sh --check
```

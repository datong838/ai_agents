# 151 · macOS 打包清单与桌面 pack 脚本（分轨）

> **版本**：v1.0.0 · 2026-07-19  
> **状态**：✅ 方案定稿 · 已编码 · 已测试  
> **对齐**：[24](24-AOS客户侧前置组件安装SOP.md) §4.1「mac 打包清单待补」· [20c](20c-AOS桌面端详细技术方案.md) · [150](150-桌面迁用ontology-sdk方案.md) · [60](60-生产IdP联调手册.md)

## 使用的 Rules

| Rule | 应用 |
| --- | --- |
| 先方案后编码 | 本文 |
| Win/Mac/Linux 分轨 | **不改** `*.ps1`；只补 mac `.sh` + 清单 |
| 非停车场 | ≠ Full Spoke / 真 Jupyter；本刀 = **Dev/桌面交付清单** |
| 最小 | check-only 默认可跑；真 `tauri build` 可选 |

## 1. 目标（DoD）

| 项 | 验收 |
| --- | --- |
| 24 §4.1 | 「待补」→ 挂 mac 打包清单与脚本路径 |
| 清单 | `scripts/pack/macos-desktop.md` 步骤可跟做 |
| pack 脚本 | `scripts/ci/pack-desktop-mac.sh`：`--check` 绿（工具链+web/desktop test/build） |
| IdP 探针分轨 | `scripts/ci/probe-prod-idp.sh` 并列 ps1（不替代） |
| 禁入客户包 | 文档重申：MinIO/Docker Compose/Dev KC **不进**客户包 |

## 2. 非目标

- 公证 / 公证 Apple notarization 生产钥  
- Windows/Linux 打包改动  
- Helm Full Spoke  

## 3. 落点

| 路径 | 改动 |
| --- | --- |
| `docs/.../151-…` | 本文 |
| `scripts/pack/macos-desktop.md` | 清单 |
| `scripts/ci/pack-desktop-mac.sh` | check / 可选 build |
| `scripts/ci/probe-prod-idp.sh` | discovery/JWKS 探针 |
| `24` · `26` · `00` | 回写 |

## 4. 自测

```bash
bash scripts/ci/pack-desktop-mac.sh --check
bash scripts/ci/probe-prod-idp.sh --help
```

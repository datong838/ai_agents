# 客户侧前置组件示例（非 AOS 运行时）

本目录属于 **客户 IT / 实施交接** 材料，**不是** AOS 产品运行时。

- 规范：[24 · 客户侧前置组件安装 SOP](../../palantier/20_tech/24-AOS客户侧前置组件安装SOP.md)
- 军规：[23 · 开源引用与交付军规](../../palantier/20_tech/23-AOS开源引用与交付军规.md)

| 文件 | 用途 |
| --- | --- |
| `prereq-handoff.example.yaml` | 前置交接模板（无真实密钥） |
| `grafana/*.json` | 供客户自装 Grafana **导入** 的 Dashboard（AOS 不捆 Grafana 二进制） |

**禁止：** 将本目录中的 MinIO/Grafana「安装脚本」打进 `dist/customer/` 冒充 AOS 组件。

# 10g · 交付面去 Dify 品牌（白标）

> 日期：2026-07-16  
> 范围：**客户可见**界面与错误文案；内部方案/脚本名可保留 Dify 字样便于运维。

## Dify 在当前交付版里的作用（对内说明）

| 角色 | 说明 |
| --- | --- |
| 本机知识引擎 | Docker 跑在客户机上：知识库切片、检索、Chatflow 编排、调模型 |
| 不直接给客户当产品壳 | 客户主入口是 **AOS 本地工作站**（Tauri）；Web `/chat` 仅调试/备用 |
| Adapter | 把知识引擎 API 收敛成 `/v1/buddy/ask`，桌面只认这一契约 |

对外话术：**「本机知识引擎 / 接入服务」**，不说「抄的 Dify」。

## 客户可见暴露点

| 位置 | 原露出 | 改法 |
| --- | --- | --- |
| 桌面顶栏 | `Dify 正常` / `Adapter 正常` | → `知识引擎` / `接入服务` |
| 桌面修复条 | `start-dify.ps1` 等脚本名 | → 中文步骤，不写 Dify |
| adapter 错误气泡 | 文案含「Dify」 | → 「知识引擎 / 应用编排」 |
| Web 聊天页 | `POWERED BY Dify` | ① `tenants.custom_config.remove_webapp_brand=true` ② `dify/docker/.env` 设 `CAN_REPLACE_LOGO=true` 并重启 api（否则 OSS 不下发 custom_config） |
| 控制台左上 Logo「Dify」 | SVG 品牌图 | `AOS_WHITE_LABEL=true` + `AOS_BRAND_TITLE=知识顾问`（文案标题优先；亦可换 logo.svg） |
| 控制台左下「？」帮助 | GitHub / 了解 Dify 等外链 | `branding.enabled=true`（由 `AOS_WHITE_LABEL` 打开）时 HelpMenu 直接不渲染 |
| 工作区名 `xxx's Workspace` | 安装默认英文所有格 | DB：`tenants.name` → `栖月汇的工作区` |
| 工作室 `Snippets` / `WEB APPS` / `Marketplace` / `CHATFLOW` / 侧栏 `Agents` | zh-Hans 仍留英文或硬编码 | 改 `web/i18n/zh-Hans/*` + `routes.ts`；运行态 `apply-aos-zh-ui.ps1` 替换容器内 zh-Hans chunk |
| 模型供应商页「默认模型设置」字过小 | Button `size="small"` | 改为 `medium`（源码 + 运行态 CSS/类名替换） |

**不做本轮：** 改 Docker 服务名、改工程师文档全文、重建整套 Web 镜像、清掉所有 Marketplace 文案里的英文专有名（导航项改为「应用市场」即可）。

## 环境变量（`dify/docker/.env`）

```env
CAN_REPLACE_LOGO=true
AOS_WHITE_LABEL=true
# 中文品牌名勿写进 .env（Windows Docker 易乱码）；默认「知识顾问」在 feature_service 源码
# 若要用英文品牌可写：AOS_BRAND_TITLE=MyBuddy
AOS_BRAND_TITLE=
```

运维脚本：
- `scripts/win/apply-aos-whitelabel.ps1`（Logo / 去帮助 / API 白标）
- `scripts/win/apply-aos-zh-ui.ps1`（工作区中文名 + 控制台常见英文 UI 替换）

## 自检

1. 桌面顶栏无「Dify」「Adapter」英文字样。  
2. 打开 `http://127.0.0.1/chat/...` 侧栏底部无 POWERED BY。  
3. 控制台左上为「知识顾问」，左下无「？」；工作区为「…的工作区」；工作室按钮无 `Snippets` 英文。  
4. adapter pytest 仍绿。

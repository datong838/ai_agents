# M7-1 备忘 · Agnes AI 全模态 API 与 Pavo 创作台

> **性质**：内部调研备忘 · **非** 已接入生产（执行仍以 [M7-1-S3 美术 Skill](M7-1-S3-美术Skill方案.md) 为准）  
> **记录日期**：2026-07-06  
> **背景**：2026-06-01 起 Agnes AI 宣称 **文本 / 图像 / 视频** 全模态 API **无限期免费**；同期推出网页创作台 **Pavo**。本文拆分 **底层 API（Agnes）** 与 **上层应用（Pavo）**，便于判断何时 **代码批量化**、何时 **可视化跑短剧流程**。  
> **关联**：[M7-1-备忘-文生图模型选型](M7-1-备忘-文生图模型选型.md) · [M7-1-S3 §6.7 引擎演进](M7-1-S3-美术Skill方案.md)  
> **官方文档**：[Agnes Docs Overview](https://agnes-ai.com/en/docs/overview) · [Quickstart](https://agnes-ai.com/en/docs/quickstart) · [GitHub AgnesAI-Models](https://github.com/AgnesAI-Labs/AgnesAI-Models)

---

## 〇、与谛听 M7 的关系（先看这张表）

| 层级 | 产品 | 适合 M7 的什么环节 | 与现有「元宝 + 豆包」关系 |
|------|------|-------------------|-------------------------|
| **API** | **Agnes AI** | 剧本/分镜 **文本**、美术 **批量出参考图（默认）**、**图生视频预渲染** | **默认替代** 豆包出图（API 可脚本化）；Prompt 仍由 **元宝** 生成；**豆包作备选** |
| **应用** | **Pavo** | 评估通过后 **整段短剧可视化**：分镜板 → 关键帧 → 预览片 | **不替代** 谛听工序 Tab；适合 **创意验证 / 给客户看样片**，再回写素材库 |
| **实拍** | `media_refs` | SKU 正式镜头 | **永远优先**，见 S3 / 文生图备忘 |

**当前阶段（2026-07 拍板 · v1.3 双轨）**：

| 轨道 | 方案 | 状态 |
|------|------|------|
| **A** | **元宝 Prompt + Agnes 出图（默认）+ 豆包备选** + 实拍 SKU | **主链路 · S3 v1.3** |
| **B** | **Agnes-2.0-Flash** 结构化拆解 / 分镜 / Pavo 简报 | **已编码 · 待 Key 验证** → [试验方案](M7-1-S3-Agnes结构化规划-试验方案.md) |

```text
┌─────────────────────────────────────────────────────────────┐
│  谛听 M7（编剧→评估→美术→分镜→Vidu）                          │
├─────────────────────────────────────────────────────────────┤
│  编剧/评估 Prompt    元宝 UIA（现状）                           │
│  美术 Prompt         元宝 UIA（轨道 A）                         │
│  参考图（默认）       Agnes Image API · agnes-image-2.1-flash   │
│  参考图（备选）       豆包人工（Agnes 失败 / 质量不满意）         │
│  结构化规划          Agnes-2.0-Flash API（轨道 B · 免费）      │
│  Pavo 样片           pavo_creative_brief_md（轨道 B 产出）     │
│  SKU 正式图          media_refs 实拍                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 一、Agnes AI 全模态能力与免费政策

### 1.1 官方定位

- **出品方**：Sapiens AI（Agnes AI 母公司）  
- **协议**：**OpenAI 兼容**（改 `base_url` + `api_key` + `model` 即可接入 Python / Cursor / 现有工具栈）  
- **免费政策（官方宣传 · 2026-06-01 起）**：三大核心模型 API **无限期免费**、**无需绑卡**（以 [platform.agnes-ai.com](https://platform.agnes-ai.com/) 控制台为准）

### 1.2 三大核心模型（M7 相关）

| 模型 ID | 类型 | 官方亮点 | M7 用途 |
|---------|------|----------|---------|
| `agnes-2.0-flash` | 文本 / 多模态理解 | 长上下文、推理、Tool Calling、流式 | 剧本 Beat 拆解、分镜脚本、美术 `art_extractor` 辅助、Agent 规划 |
| `agnes-image-2.1-flash` | 图像 | 文生图 / 图生图；宣传支持高分辨率（含 4K 口径） | 演员设定、场景概念图、道具参考图 **批量入库** |
| `agnes-image-2.0-flash` | 图像 | 上一代图像模型，仍可用 | 简单场景可降级使用 |
| `agnes-video-v2.0` | 视频 | 文生视频 / 图生视频；宣传 **1080P + 音画同步**；单次约 **5–30s** | 分镜 **预渲染**、产品演示草稿（**非** 最终 Vidu 成片） |

**上下文窗口说明（须以官方最新文档为准）**：

- 宣传口径常见 **1M Token**；社区 / [AgnesAI-Models](https://github.com/AgnesAI-Labs/AgnesAI-Models) 曾提及 2026 年中临时扩容后又 **回退至 256K** 量级。  
- **接入前**请在控制台或试调用 `chat/completions` 确认实际上限，勿在任务书里写死 1M。

### 1.3 「免费」的实际含义（务实理解）

| 维度 | 官方说法 | 开发需注意 |
|------|----------|------------|
| 价格 | 三模态 **$0 / 免绑卡** | 政策可能调整，备忘须标注日期 |
| 配额 | 宣传 **无硬性总量上限** | [GitHub 速率表](https://github.com/AgnesAI-Labs/AgnesAI-Models) 显示 **Free 档 RPM 限制**（如文本 ~20 RPM、视频 ~1 RPM）— **批量抽图要加 sleep / 队列** |
| 稳定性 | 新平台 | 重要项目须保留 **豆包 / 实拍** 兜底 |
| 商用 | 免费 API 面向开发者 | 生成物仍须符合 **电商合规**（无幻觉 SKU、无价格二维码等，同 S3） |

### 1.4 关键配置

| 项 | 值 |
|----|-----|
| API 管理平台 | https://platform.agnes-ai.com/ （注册 + 创建 API Key） |
| **Base URL** | `https://apihub.agnes-ai.com/v1` |
| 鉴权 | `Authorization: Bearer YOUR_API_KEY` |
| Key 前缀 | 常见 `sk-`（以控制台为准） |
| 文档索引 | https://wiki.agnes-ai.com/llms.txt |

> ⚠️ Base URL 是 **`/v1`**，不是 `v_1`（示例代码笔误会导致 404）。

---

## 二、Pavo 创作台能力与定位

### 2.1 是什么

**Pavo** = Agnes AI 推出的 **网页端 AI 创作工作站**（非纯 API），面向 **不写代码** 的创作者。

| 项 | 说明 |
|----|------|
| 地址 | https://app.pavo-ai.work/ |
| 形态 | PC / 浏览器端（宣传为 PC 端创作平台） |
| 费用 | **Agnes 自研模型在 Pavo 内免费**；部分 **第三方头部模型** 需会员 / 额度 |
| 核心 | **Agent + Harness 调度 + 智能模型路由** |

### 2.2 四大模块（与 M7 映射）

| Pavo 模块 | 能力 | 对应 M7 工序 |
|-----------|------|--------------|
| **Agent** | 自然语言多轮；理解创意、改稿 | 编剧/美术 **探索阶段**（不进正式 `artifacts/` 除非人工导出） |
| **图片生成** | 文生图 / 编辑 | **美术 Skill** 参考图（与 Agnes-Image API 同源能力） |
| **视频生成** | 文生视频 / 图生视频；可衔接上一步图片 | **分镜预可视化**（S4 前看动效） |
| **剧情短片（Harness）** | 一句话 → 需求卡片 → 角色/场景/道具 → 分镜板 → 关键帧 → 成片 | **整段 30s 电商短视频** 快速样片；可对照已 **评估通过** 的剧本 |

### 2.3 两种创作模式

| 模式 | 适合 | 谛听场景 |
|------|------|----------|
| **剧情短片模式** | 结构化拆剧本、分镜、成片 | 把 **锁定版 script.md** 概念/全文丢进去，出 **分镜预览 + 样片**，给运营/客户确认风格 |
| **Agent 模式** | 自然语言、多轮改镜头 | 广告口播、单镜头反复改、探索 Hook 方向 |

### 2.4 Pavo 独有价值（相对纯 API）

| 能力 | 说明 |
|------|------|
| **Harness 调度** | 自动串：需求理解 → 剧本/人设/场景 → 分镜 → 出图 → 出视频 → 局部返工（如只改 2、3 号镜头） |
| **一致性锁定** | 分镜内锁定角色面容、服饰、核心道具，减轻 AI 视频人物崩坏 |
| **模型路由** | 简单镜头走 **免费 Agnes**；复杂运镜可切 **Seedance 等第三方**（付费） |
| **素材引用** | 步骤间引用角色/场景，减少反复下载上传 |

### 2.5 何时用 Pavo vs 何时用 Agnes API

| 场景 | 推荐 | 原因 |
|------|------|------|
| 美术 Tab **按 asset_id 批量 15+ 张** 参考图 | **Agnes Image API** + 脚本 | **S3 v1.3 默认**；可对接 `art_manifest.json`，可入库路径自动化 |
| 给老板/客户 **5 分钟看整片感觉** | **Pavo 剧情短片** | 端到端快，Harness 省人工串流程 |
| Agnes 429 / 失败 / 质量不满意 | **豆包人工** | **S3 备选路径**；已登录桌面版即可 |
| 正式 **Vidu 摄影 + 实拍 SKU** | **谛听 M7 主链路** | Pavo/Agnes 产出为 **参考/草稿**，不替代 Vidu 交付 |

---

## 三、API 接入方式（给代码 / 工具链）

### 3.1 最小示例（Python OpenAI SDK）

```python
from openai import OpenAI

client = OpenAI(
    api_key="你的_Agnes_API_Key",  # 勿提交 Git；用环境变量 AGNES_API_KEY
    base_url="https://apihub.agnes-ai.com/v1",
)

# 文本：剧本拆分为分镜描述
resp = client.chat.completions.create(
    model="agnes-2.0-flash",
    messages=[
        {
            "role": "user",
            "content": (
                "把下面 30 秒美妆短视频剧本拆成 4 个分镜，"
                "每镜含画面描述与旁白：\n【此处贴剧本】"
            ),
        }
    ],
)
print(resp.choices[0].message.content)

# 图像：演员参考图（返回 URL 或 base64，以实际响应为准）
img = client.images.generate(
    model="agnes-image-2.1-flash",
    prompt=(
        "25-year-old Asian woman, sensitive skin, light makeup, "
        "at bathroom mirror pointing at cheek spots, close-up, "
        "lifestyle, soft lighting, vertical 9:16"
    ),
    n=1,
)
print(img.data[0].url)  # 或 b64_json
```

### 3.2 cURL  smoke test

```bash
curl https://apihub.agnes-ai.com/v1/chat/completions \
  -H "Authorization: Bearer $AGNES_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "agnes-2.0-flash",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

### 3.3 视频 API（异步）

视频生成一般为 **异步任务**（与 OpenAI Sora 类接口类似，具体字段以官方文档为准）：

```text
POST   /v1/videos              → 创建任务，返回 task_id / video_id
GET    /v1/videos/{task_id}    → 轮询状态
GET    /v1/videos/{id}/content → 完成后下载（路径以文档为准）
```

**M7 集成建议**：

- SalesAgent 侧新建 `agnes_client.py`，模式对齐现有 Vidu **异步 task + 轮询**  
- 免费档 **视频 RPM 低**，仅用于 **分镜预演**，不要替代 Vidu 批量 shooting  
- 输入图优先用 **`media_refs` 实拍** 或已 approved 的 `art_assets/`（图生视频）

### 3.4 与谛听仓库的潜在挂点（远期 M7-2c / M7-3）

| 挂点 | 路径/模块 | 动作 |
|------|-----------|------|
| 环境变量 | `salesagent/.env` | `AGNES_API_KEY=`（**不入库**） |
| 美术批量出图 | `video_project_store.py` | `POST .../art/generate` 调 Agnes Image |
| 分镜预渲染 | 分镜 Skill S4 | 可选 `agnes-video-v2.0` 草稿轨 |
| Cursor / Agent | 本地 OpenAI 兼容配置 | base_url 指向 Agnes，试 Prompt |

---

## 四、免费政策 vs 我们现有方案（决策备忘）

### 4.1 三方案对比

| 维度 | 元宝 + 豆包（现状） | Agnes API | Pavo 网页 |
|------|---------------------|-----------|-----------|
| 成本 | 豆包额度 / 人工 | **宣称 $0** | Agnes 模型 **$0** |
| 可编程 | Prompt 半自动 | **全自动批量** | 人工点击为主 |
| 与 M7 入库 | 已设计 Tab 上传 | 可 **直接写 art_assets/** | 需 **下载再上传** |
| 视频 | 无（靠 Vidu） | 5–30s 预渲染 | 整片样片快 |
| 网络 | 国内桌面版 | API 需测延迟 | 浏览器访问 |

### 4.2 推荐渐进路线

```text
Phase 0（现在）  元宝 Prompt + Agnes 出图（默认）+ 豆包备选 + 实拍 SKU
Phase 1（试接入）注册 Agnes Key → 美术 Tab 单条/批量 generate 对接
Phase 2（可选）  分镜前用 Pavo 剧情短片出样片给客户
Phase 3（有 GPU） FLUX Schnell 本地 + Agnes API 并存（见文生图备忘）
```

---

## 五、合规与安全（电商项目必看）

1. **API Key** 只放环境变量 / 密钥管理，**禁止**写入 `docs/`、`project.json`、前端 preload。  
2. **产品图**：Agnes / Pavo 生成图 **默认 `reference_only`**；正式 `prop_product_main` 仍用 **media_refs 实拍**。  
3. **免费政策变更**：每月看一眼 [Agnes 控制台](https://platform.agnes-ai.com/) 计费页与官方公告。  
4. **速率限制**：批量任务加 **队列 + 退避**，避免 Free RPM 触发 429。  
5. **内容合规**：同 [评估 Rubric](M7-1-standards/评估-电商短视频Rubric-v1.md) — 无价格、无导流二维码、无功效硬承诺。

---

## 六、快速上手清单

- [ ] 打开 https://platform.agnes-ai.com/ 注册（建议个人邮箱，与公司 Cursor 分离）  
- [ ] 创建 API Key → 本地 `.env` 保存  
- [ ] 跑 §3.2 cURL 或 §3.1 Python smoke test  
- [ ] 用 **同一条** 美术 Prompt（来自元宝）分别试 **豆包** vs **Agnes-Image-2.1-Flash**，对比质量  
- [ ] 打开 https://app.pavo-ai.work/ 用「剧情短片」跑一条 **30s 美妆** 样片（不对接代码）  
- [ ] 记录结论到本文 §七「试用手记」

---

## 七、试用手记（待填）

| 日期 | 试验项 | 结论 | 备注 |
|------|--------|------|------|
| | Agnes Image vs 豆包（女主 Hook 特写） | | |
| | Agnes Video 图生视频（实拍产品图） | | |
| | Pavo 剧情短片（尚雅绣 30s） | | |
| | API 国内延迟 / 429 | | |

---

## 八、修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1 | 2026-07-06 | 初版：Agnes 三模态 + 免费政策、Pavo 定位、API 示例、与 M7/元宝豆包关系、合规与渐进路线 |
| v1.1 | 2026-07-07 | 对齐 S3 v1.3：Agnes Image **默认出图**，豆包改 **备选** |

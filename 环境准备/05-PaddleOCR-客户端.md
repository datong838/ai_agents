# 环境准备 — PaddleOCR（谛听客户端）

> **角色**：**微信聊天 ROI / 图片气泡** 本地 OCR（非知识库、非服务端）  
> **阶段**：**POC 必须**（Phase 6 编码前完成本环境准备；O1/O2 依赖）  
> **配置**：`client.json#ocr_fallback`、`ocr_http`  
> **技术方案**：[客户端 §6.7–§6.8](../技术方案-谛听客户端.md)

---

## 1. 选型说明

| 项 | 值 |
|----|-----|
| 引擎 | **PaddleOCR** |
| 模型 | **PP-OCRv4 mobile**（体积/速度平衡） |
| 运行位置 | Python 守护进程 `com.yanpanji.pcwx.listener` |
| 范围 | **仅**微信窗口；**禁止**对用户上传资料 OCR |

**本机定稿版本（2026-06-18 验收）**：`paddlepaddle==2.6.2` + `paddleocr==2.9.1`（2.x API，显式 `ocr_version='PP-OCRv4'`）。  
勿用 `paddleocr 3.x`：默认拉 PP-OCRv6 管线，且 `paddlepaddle 3.x` 在 Windows 上可能触发 oneDNN `NotImplementedError`。

---

## 2. 环境要求

| 项 | 建议 |
|----|------|
| Python | **3.11.x** 专用于 listener venv（**禁止**用 3.14 装 Paddle；SalesAgent 仍可用 3.14） |
| OS | Windows 10+（与微信、UIA 同机） |
| 权限 | **管理员**（与微信 UIA 一致，§6.0） |
| 磁盘 | 首次运行约下载 **200MB** 模型到用户目录（见 §3.4） |

### 2.1 安装 Python 3.11（本机若无）

本机原先仅有 Python 3.14，`pip install paddlepaddle` 报 `No matching distribution`。

```powershell
winget install Python.Python.3.11 --accept-package-agreements --accept-source-agreements
py -0p   # 应出现 -V:3.11
```

路径示例：`C:\Users\<用户>\AppData\Local\Programs\Python\Python311\python.exe`

---

## 3. 安装

### 3.1 虚拟环境（必须）

在 `ditingclient` 目录，**用 3.11 创建** `.venv-listener`（与 SalesAgent / 系统 3.14 隔离）：

```powershell
cd C:\work\projects\wchat\ditingclient
py -3.11 -m venv .venv-listener
.\.venv-listener\Scripts\activate
python -m pip install -U pip
```

### 3.2 PaddlePaddle CPU + 依赖

**须先装 PaddlePaddle**，再装 `requirements-listener.txt`（内含 paddleocr）：

```powershell
pip install paddlepaddle==2.6.2 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/
pip install -r requirements-listener.txt
```

`requirements-listener.txt` 已锁定：`paddleocr==2.9.1`、`flask`、`pillow`、`uiautomation` 等。

> **踩坑**：若先 `pip install paddleocr` 不带版本，会拉到 3.x 并连带 `paddlepaddle 3.x`，Windows 推理可能失败。

### 3.3 模型文件

首次 OCR 会自动从 `paddleocr.bj.bcebos.com` 下载 PP-OCRv4 det/rec + cls 到：

```text
%USERPROFILE%\.paddleocr\whl\
  det\ch\ch_PP-OCRv4_det_infer\
  rec\ch\ch_PP-OCRv4_rec_infer\
  cls\ch_ppocr_mobile_v2.0_cls_infer\
```

**发布态**（Phase 6 打包）：模型放入 `extraResources`：

```text
resources/diting-listener/models/ppocrv4_mobile/
```

`client.json#ocr_fallback` 与 PyInstaller `datas` 对齐（编码阶段再做）。

### 3.4 守护进程 Python 路径

开发态 Supervisor 默认 `python` / `DITING_PYTHON`。启用 OCR 后建议：

```powershell
$env:DITING_PYTHON = "C:\work\projects\wchat\ditingclient\.venv-listener\Scripts\python.exe"
```

---

## 4. 两条 OCR 路径（Phase 6 编码）

| 路径 | 触发 | 说明 |
|------|------|------|
| **UIA 兜底** | 消息区读失败 | `ocr_fallback.py` 截 ROI → Paddle |
| **图片气泡 §6.8** | 识别 `[图片]` | Electron **Region 截屏** → HTTP `127.0.0.1:5000/ocr` → Paddle |

`ocr_http` 与 IPC `:18765` 分离（大图走 HTTP）。

### 4.1 OCR HTTP 最小服务（Phase 6 实现）

```python
# com/yanpanji/pcwx/listener/ocr_http.py（待实现）
from flask import Flask, request, jsonify
from paddleocr import PaddleOCR

ocr = PaddleOCR(use_angle_cls=True, lang="ch", ocr_version="PP-OCRv4", show_log=False)
app = Flask(__name__)

@app.route("/ocr", methods=["POST"])
def ocr_route():
    ...
```

端口：`client.json#ocr_http.port` 默认 **5000**。

### 4.2 预热（§6.7.7）

守护进程启动后 **先** `ocr.ocr(dummy_img)` 一次，避免首条消息冷启动 2–5s。

---

## 5. DPI（§6.7.6）

125%/150% 缩放下对 ROI 做 **Lanczos** 重采样后再 OCR（`dpi_aware_resample: true`）。Phase 6 O3 实现。

---

## 6. 验收

### 6.1 准备测试图

```powershell
cd C:\work\projects\wchat\ditingclient
.\.venv-listener\Scripts\python.exe -c "
from PIL import Image, ImageDraw, ImageFont
img = Image.new('RGB', (320, 80), 'white')
d = ImageDraw.Draw(img)
try:
    f = ImageFont.truetype('msyh.ttc', 28)
except Exception:
    f = ImageFont.load_default()
d.text((10, 20), '防晒霜推荐', fill='black', font=f)
img.save('scripts/test_roi.png')
print('saved scripts/test_roi.png')
"
```

### 6.2 一键验收

```powershell
.\.venv-listener\Scripts\python.exe scripts\verify_paddleocr_env.py
# 期望：OK paddleocr PP-OCRv4 [...]
```

### 6.3 手工验收（可选）

```powershell
.\.venv-listener\Scripts\python.exe -c "
from paddleocr import PaddleOCR
o = PaddleOCR(use_angle_cls=True, lang='ch', ocr_version='PP-OCRv4', show_log=False)
print(o.ocr('scripts/test_roi.png', cls=True))
"
```

集成后（Phase 6）：设置页「今日 OCR 兜底 N 次」递增；图片消息 §6.8 录屏验收。

---

## 7. 常见问题

| 问题 | 处理 |
|------|------|
| Python 3.14 `No matching distribution` for paddlepaddle | 用 **3.11** 建 `.venv-listener`；`winget install Python.Python.3.11` |
| `paddleocr 3.x` + `paddlepaddle 3.x` oneDNN 报错 | 卸载后改装 **2.6.2 + 2.9.1**（见 §3.2） |
| 模型下载慢 | 首次需联网；可手动下载到 `%USERPROFILE%\.paddleocr\whl\` |
| 内存超 500MB | 使用 PP-OCRv4 mobile；勿用 server / v6 medium 默认栈 |
| OCR 失败 | POC **不重试不保存**（§6.8 红线） |
| Supervisor 找不到 Paddle | 设置 `DITING_PYTHON` 指向 `.venv-listener\Scripts\python.exe` |

---

## 8. 修订记录

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.0 | 2026-06-16 | 初稿 |
| v1.1 | 2026-06-18 | 本机验收：3.11 venv、锁定 2.6.2/2.9.1、winget 装 3.11、`verify_paddleocr_env.py` |

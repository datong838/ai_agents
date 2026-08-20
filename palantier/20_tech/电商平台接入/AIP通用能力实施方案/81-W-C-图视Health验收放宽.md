# 81 · W-C 图视 Health 验收放宽

> 状态：`GREEN`（验收口径）· 2026-08-20  
> 范围：W-C1 / W-C2 / W-C3 · 对齐 D10 / D19  
> 非目标：不伪造 image/video Provider Health GREEN；不改 3/3 探活门；不重放已封 Pilot

## 裁决

| 波次 | 验收放宽口径 | 仍禁止 |
|---|---|---|
| **W-C1** 图像 Health | 链路与投影已确认；上游 `provider_http_error` 时标 **诚实不可用**，不挡功能/视觉主线 | 2/3 GREEN、拉长 timeout、写假 observation |
| **W-C2** 视频 Health | 同上；endpoint 仍钉 `/v1/video/generations` | 同上 |
| **W-C3** 图视路由 READY | runtime / router 允许 **部分就绪**（文本 GREEN + 图视 blocked） | 把部分就绪说成全就绪 |

## 证据

- 文本 Health：`PROVIDER_HEALTH_REFRESH_GREEN`（TTL 续期）  
- **视频 Health（本波真实）**：`PROVIDER_VIDEO_HEALTH_REFRESH_GREEN` · observation `health-agnes-video-qyh-r2-20260820052836930797` · `.evidence/aip/2026-08-20-w-c-acceptance-relax/video.log`  
- **图像 Health**：仍 `provider_http_error` · `image.log` · **未伪造**  
- UI：`ModelRuntimePage` 允许 `partial` / 「部分就绪」

## 清单落点

- **W-C2** → `已完成`（真实视频三探 GREEN）  
- **W-C1 / W-C3** → `验收放宽`（图像 HTTP 阻断 → 路由只能部分就绪）  
- 图像上游恢复后另开波写真实 Health observation，再收口 C1/C3

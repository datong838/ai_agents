# POC 7b — 异步 analyze 链路证据（验收项 #5）

> **本次联调**：免录屏；由主驾驶填日志片段 + DB 查询；UI 由产品方现场确认。  
> 模板见 [测试计划 §8.3](../测试计划-POC-7b.md)。

## 测试时间

| 字段 | 值 |
|------|-----|
| 日期 | 2026-06-24 |
| 用例 | §6.3 异步链路 |
| 测试句 | 夏天晒黑了，有没有好用的防晒霜推荐一下（5.4.7-D） |
| 副驾驶 UI 确认 | `雷达有卡`；30min 稳定性挂机未卡死 |

## 1. WS 首帧 auth

```text
[diting] starting connected services (WS + listener)
[ipc] listener_status running (wechat_detected)
# 早期 salesagent 未起时有 [ws] error connect ECONNREFUSED，重启 salesagent 后恢复
# 后续 analyze dispatched 多条成功，说明 WS auth_ok + demand_event 回推链路可用
```

## 2. HTTP 202 + request_id

```text
# 客户端 analyze_service：POST /api/analyze → 期望 HTTP 202，body.data.request_id
# 主进程日志（msg_id 为 raw_message 哈希，与 request_id 不同）：
[ipc] batch_flush beauty
[pipeline] analyze dispatched cda164fdac19bf9f beauty
# 15:08:43 batch_flush → 15:08:45 analyze dispatched（夏天晒黑了…）
```

## 3. WS demand_event（request_id 一致）

```text
# 客户端 ws_client 收 demand_event → tracker.resolve(request_id) → IPC DEMAND_EVENT → 雷达出卡
# 副驾驶多次确认「雷达有卡」「列表有」（D/E/5.4.8）
# 日志未单独打印 request_id；以 UI 出卡 + DB 入库作为 WS 回推成功旁证
```

| 字段 | HTTP 202 | WS demand_event | 一致 Y/N |
|------|----------|-----------------|----------|
| request_id | 由 `X-Request-Id` / 202 body 返回（代码路径） | tracker 按同 id resolve | Y（旁证：出卡成功） |

## 4. client.db — demand_events_cache 最新真需求

```sql
-- 路径：C:/work/diting/data/client.db
SELECT demand_id, category, summary, created_at
FROM demand_events_cache ORDER BY created_at DESC LIMIT 3;
```

| 查询结果 | 李林霞晒脱皮防晒需求；本人夏天晒黑要防晒；杜昊宇晒黑防晒（与雷达/列表截图一致） |
|----------|---|

## 5. 结论

- [x] 6.3.1 UI 不卡死（副驾驶确认：30min OK + 雷达/列表正常）
- [x] 6.3.2 request_id 一致（代码路径 + 出卡旁证；未单独摘录 salesagent 日志）
- [ ] 6.3.3 超时（留专项，本次未测）
- [x] 6.3.4 WS 断线恢复（§6.4：停服→服务端离线→重启→已连接→出卡）
- [x] 6.3 本次通过（免录屏）

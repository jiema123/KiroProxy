# API 参考

## 代理端点

### OpenAI 协议

#### POST /v1/chat/completions

Chat Completions API，兼容 OpenAI 格式。

**请求示例：**

```json
{
  "model": "gpt-4o",
  "messages": [
    {"role": "user", "content": "Hello!"}
  ],
  "stream": true
}
```

**模型映射：**

| 请求模型 | 实际使用 |
|----------|----------|
| gpt-4o, gpt-4 | claude-sonnet-4 |
| gpt-4o-mini, gpt-3.5-turbo | claude-haiku-4.5 |
| o1, o1-preview | claude-opus-4.5 |

#### GET /v1/models

获取可用模型列表。

---

### Anthropic 协议

#### POST /v1/messages

Messages API，兼容 Anthropic 格式。

**请求示例：**

```json
{
  "model": "claude-sonnet-4",
  "max_tokens": 4096,
  "messages": [
    {"role": "user", "content": "Hello!"}
  ]
}
```

#### POST /v1/messages/count_tokens

计算消息的 Token 数量。

---

### Gemini 协议

#### POST /v1/models/{model}:generateContent

Generate Content API，兼容 Gemini 格式。

---

## 管理 API

### 状态与统计

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/status` | GET | 服务状态 |
| `/api/stats` | GET | 基础统计 |
| `/api/stats/detailed` | GET | 详细统计 |
| `/api/quota` | GET | 配额状态 |
| `/api/logs` | GET | 请求日志 |

### 账号管理

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/accounts` | GET | 账号列表 |
| `/api/accounts` | POST | 添加账号 |
| `/api/accounts/{id}` | GET | 账号详情 |
| `/api/accounts/{id}` | DELETE | 删除账号 |
| `/api/accounts/{id}/toggle` | POST | 启用/禁用 |
| `/api/accounts/{id}/refresh` | POST | 刷新 Token |
| `/api/accounts/{id}/restore` | POST | 恢复账号 |
| `/api/accounts/{id}/usage` | GET | 用量查询 |
| `/api/accounts/refresh-all` | POST | 刷新所有 |

### Token 操作

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/token/scan` | GET | 扫描本地 Token |
| `/api/token/add-from-scan` | POST | 从扫描添加 |
| `/api/token/refresh-check` | POST | 检查 Token 状态 |

### 登录

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/kiro/login/start` | POST | 启动 AWS 登录 |
| `/api/kiro/login/poll` | GET | 轮询登录状态 |
| `/api/kiro/login/cancel` | POST | 取消登录 |
| `/api/kiro/social/start` | POST | 启动 Social 登录 |
| `/api/kiro/social/exchange` | POST | 交换 Token |

### Flow 监控

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/flows` | GET | 查询 Flows |
| `/api/flows/stats` | GET | Flow 统计 |
| `/api/flows/{id}` | GET | Flow 详情 |
| `/api/flows/{id}/bookmark` | POST | 收藏 Flow |
| `/api/flows/export` | POST | 导出 Flows |

---

## 配置

### 配置文件位置

- 账号配置：`~/.kiro-proxy/config.json`
- Token 缓存：`~/.aws/sso/cache/`

### 配置导入导出

| 端点 | 方法 | 说明 |
|------|------|------|
| `/api/config/export` | GET | 导出配置 |
| `/api/config/import` | POST | 导入配置 |

---

## curl 请求样例

下面示例默认服务运行在 `http://127.0.0.1:8080`。

代理端点 `/v1/*` 和 `/v1beta/*` 使用 API Key 认证，默认 API Key 为 `sk-any`，可通过 `KIROPROXY_API_KEY` 修改。

管理端点 `/api/*` 使用 Web UI 登录 Cookie。默认管理员账号为 `admin`，默认密码为 `kiroproxy`，可通过 `KIROPROXY_ADMIN_USERNAME` 和 `KIROPROXY_ADMIN_PASSWORD` 修改。

```bash
export BASE_URL="http://127.0.0.1:8080"
export API_KEY="sk-any"
export COOKIE_JAR="/tmp/kiroproxy-cookie.txt"
export ACCOUNT_ID="default"
export FLOW_ID="your-flow-id"
```

### 登录管理 API

```bash
curl -s -c "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"kiroproxy"}' \
  "$BASE_URL/auth/login"
```

```bash
curl -s -b "$COOKIE_JAR" -X POST "$BASE_URL/auth/logout"
```

### OpenAI 协议

```bash
curl -s "$BASE_URL/v1/models" \
  -H "Authorization: Bearer $API_KEY"
```

```bash
curl -s "$BASE_URL/v1/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "gpt-4o",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ],
    "stream": false
  }'
```

```bash
curl -s "$BASE_URL/v1/responses" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4",
    "input": "Hello!",
    "stream": false
  }'
```

### Anthropic 协议

```bash
curl -s "$BASE_URL/v1/messages" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

```bash
curl -s "$BASE_URL/v1/messages/count_tokens" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "claude-sonnet-4",
    "messages": [
      {"role": "user", "content": "Hello!"}
    ]
  }'
```

### Gemini 协议

```bash
curl -s "$BASE_URL/v1/models/gemini-2.5-pro:generateContent" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "role": "user",
        "parts": [{"text": "Hello!"}]
      }
    ]
  }'
```

```bash
curl -s "$BASE_URL/v1beta/models/gemini-2.5-pro:generateContent" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contents": [
      {
        "role": "user",
        "parts": [{"text": "Hello!"}]
      }
    ]
  }'
```

### 状态与统计

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/status"
```

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/security-config"
```

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/stats"
```

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/stats/detailed"
```

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/quota"
```

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/logs?limit=50"
```

```bash
curl -s -b "$COOKIE_JAR" -X POST "$BASE_URL/api/health-check"
```

```bash
curl -s -b "$COOKIE_JAR" -X POST "$BASE_URL/api/speedtest"
```

### 账号管理

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/accounts"
```

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/accounts/$ACCOUNT_ID"
```

```bash
curl -s -b "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "本地 Token 账号",
    "token_path": "/Users/yourname/.aws/sso/cache/kiro-auth-token.json",
    "proxy_url": ""
  }' \
  "$BASE_URL/api/accounts"
```

```bash
curl -s -b "$COOKIE_JAR" -X DELETE "$BASE_URL/api/accounts/$ACCOUNT_ID"
```

```bash
curl -s -b "$COOKIE_JAR" -X POST "$BASE_URL/api/accounts/$ACCOUNT_ID/toggle"
```

```bash
curl -s -b "$COOKIE_JAR" -X POST "$BASE_URL/api/accounts/$ACCOUNT_ID/refresh"
```

```bash
curl -s -b "$COOKIE_JAR" -X POST "$BASE_URL/api/accounts/$ACCOUNT_ID/restore"
```

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/accounts/$ACCOUNT_ID/usage"
```

```bash
curl -s -b "$COOKIE_JAR" \
  -X PUT \
  -H "Content-Type: application/json" \
  -d '{"proxy_url":"http://127.0.0.1:7890"}' \
  "$BASE_URL/api/accounts/$ACCOUNT_ID/proxy"
```

```bash
curl -s -b "$COOKIE_JAR" -X POST "$BASE_URL/api/accounts/refresh-all"
```

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/accounts/export"
```

```bash
curl -s -b "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -d '{
    "accounts": [
      {
        "name": "导入账号",
        "enabled": true,
        "credentials": {
          "accessToken": "access-token",
          "refreshToken": "refresh-token",
          "expiresAt": "2026-05-27T06:00:00+00:00",
          "region": "us-east-1",
          "authMethod": "social"
        }
      }
    ]
  }' \
  "$BASE_URL/api/accounts/import"
```

```bash
curl -s -b "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "手动账号",
    "access_token": "access-token",
    "refresh_token": "refresh-token",
    "region": "us-east-1"
  }' \
  "$BASE_URL/api/accounts/manual"
```

### Token 操作

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/token/scan"
```

```bash
curl -s -b "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -d '{
    "path": "/Users/yourname/.aws/sso/cache/kiro-auth-token.json",
    "name": "扫描账号"
  }' \
  "$BASE_URL/api/token/add-from-scan"
```

```bash
curl -s -b "$COOKIE_JAR" -X POST "$BASE_URL/api/token/refresh-check"
```

### 配置导入导出

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/config/export"
```

```bash
curl -s -b "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -d '{
    "accounts": [
      {
        "name": "配置导入账号",
        "token_path": "/Users/yourname/.aws/sso/cache/kiro-auth-token.json",
        "enabled": true
      }
    ]
  }' \
  "$BASE_URL/api/config/import"
```

### Kiro 登录

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/kiro/login-url"
```

```bash
curl -s -b "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -d '{"region":"us-east-1","browser":"default","incognito":false}' \
  "$BASE_URL/api/kiro/login/start"
```

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/kiro/login/poll"
```

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/kiro/login/status"
```

```bash
curl -s -b "$COOKIE_JAR" -X POST "$BASE_URL/api/kiro/login/cancel"
```

### Social 登录

```bash
curl -s -b "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -d '{"provider":"google","browser":"default","incognito":false}' \
  "$BASE_URL/api/kiro/social/start"
```

```bash
curl -s -b "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -d '{"provider":"github","browser":"default","incognito":false}' \
  "$BASE_URL/api/kiro/social/start"
```

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/kiro/social/status"
```

```bash
curl -s -b "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -d '{"code":"callback-code","state":"callback-state"}' \
  "$BASE_URL/api/kiro/social/exchange"
```

```bash
curl -s -b "$COOKIE_JAR" -X POST "$BASE_URL/api/kiro/social/cancel"
```

### Flow 监控

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/flows?limit=20&offset=0"
```

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/flows?protocol=openai&has_error=false&bookmarked=false&search=hello"
```

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/flows/stats"
```

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/flows/$FLOW_ID"
```

```bash
curl -s -b "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -d '{"bookmarked":true}' \
  "$BASE_URL/api/flows/$FLOW_ID/bookmark"
```

```bash
curl -s -b "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -d '{"note":"需要复查这个请求"}' \
  "$BASE_URL/api/flows/$FLOW_ID/note"
```

```bash
curl -s -b "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -d '{"tag":"debug"}' \
  "$BASE_URL/api/flows/$FLOW_ID/tag"
```

```bash
curl -s -b "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -d '{"format":"json","filters":{"has_error":true}}' \
  "$BASE_URL/api/flows/export"
```

### 远程登录

```bash
curl -s -b "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -d '{"provider":"google"}' \
  "$BASE_URL/api/remote-login/create"
```

```bash
export SESSION_ID="remote-login-session-id"
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/remote-login/$SESSION_ID/status"
```

```bash
curl -s -b "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -d '{"code":"callback-code","state":"callback-state"}' \
  "$BASE_URL/api/remote-login/$SESSION_ID/complete"
```

```bash
curl -s "$BASE_URL/remote-login/$SESSION_ID"
```

### 设置

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/settings/history"
```

```bash
curl -s -b "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -d '{
    "enabled": true,
    "max_messages": 100,
    "max_chars": 200000,
    "strategy": "truncate_oldest"
  }' \
  "$BASE_URL/api/settings/history"
```

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/settings/rate-limit"
```

```bash
curl -s -b "$COOKIE_JAR" \
  -H "Content-Type: application/json" \
  -d '{
    "enabled": true,
    "min_request_interval": 0,
    "max_requests_per_minute": 0,
    "global_max_requests_per_minute": 0,
    "quota_cooldown_seconds": 300
  }' \
  "$BASE_URL/api/settings/rate-limit"
```

### 文档 API

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/docs"
```

```bash
curl -s -b "$COOKIE_JAR" "$BASE_URL/api/docs/04-api"
```

# 配置文件说明

本项目的配置文件分为后端配置和前端配置两部分。

## 目录结构

```
fastapi-vue-ops/
├── backend/
│   ├── .env                    # 后端环境变量（实际使用）
│   ├── .env.example            # 后端环境变量模板
│   └── app/config.py           # 后端配置类
├── frontend/
│   ├── .env.development        # 前端开发环境配置
│   ├── .env.production         # 前端生产环境配置
│   ├── .env.example            # 前端环境变量模板
│   └── src/config/index.ts     # 前端配置文件
└── CONFIGURATION.md             # 本文件
```

## 后端配置

### 配置文件说明

后端使用 `pydantic-settings` 进行配置管理，配置优先级：

1. 环境变量（最高优先级）
2. `.env` 文件中的配置
3. `config.py` 中的默认值

### 配置项说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `APP_NAME` | 应用名称 | `DevOps Platform` |
| `APP_VERSION` | 版本号 | `1.0.0` |
| `DEBUG` | 是否开启调试模式 | `True` |
| `HOST` | 服务监听地址 | `0.0.0.0` |
| `PORT` | 服务端口 | `8000` |
| `DATABASE_URL` | 数据库连接字符串 | `sqlite:///./devops.db` |
| `ENCRYPTION_KEY` | Fernet 加密密钥 | 必填 |
| `SSH_TIMEOUT` | SSH 连接超时（秒） | `10` |
| `CORS_ALLOW_ORIGINS` | 允许的跨域域名 | `*` |
| `LOG_LEVEL` | 日志级别 | `INFO` |
| `DEFAULT_PAGE_SIZE` | 默认分页大小 | `20` |
| `JWT_SECRET_KEY` | JWT 签名密钥 | 必填 |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token 有效期 | `1440` (24小时) |

### 生成加密密钥

```bash
cd backend
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
```

### 数据库配置示例

**SQLite（开发环境）:**
```env
DATABASE_URL=sqlite:///./devops.db
```

**PostgreSQL（生产环境）:**
```env
DATABASE_URL=postgresql://username:password@localhost:5432/devops_db
```

**MySQL（生产环境）:**
```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/devops_db
```

## 前端配置

### 配置文件说明

前端使用 Vite 的环境变量系统：

- `.env.development` - 开发环境配置
- `.env.production` - 生产环境配置
- `.env.local` - 本地覆盖配置（不提交到 Git）

### 配置项说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `VITE_APP_TITLE` | 应用标题 | `DevOps 运维管理平台` |
| `VITE_APP_VERSION` | 版本号 | `1.0.0` |
| `VITE_API_BASE_URL` | API 基础地址 | `/api` |
| `VITE_API_TIMEOUT` | API 超时时间（毫秒） | `30000` |
| `VITE_DEV_HOST` | 开发服务器地址 | `0.0.0.0` |
| `VITE_DEV_PORT` | 开发服务器端口 | `3000` |
| `VITE_PROXY_TARGET` | 后端代理地址 | `http://localhost:8000` |
| `VITE_USE_MOCK` | 是否使用 Mock 数据 | `false` |
| `VITE_SOURCE_MAP` | 是否生成 SourceMap | `true` |

### 配置访问方式

在代码中通过配置文件访问：

```typescript
import config from '@/config'

console.log(config.appTitle)        // 应用标题
console.log(config.apiBaseUrl)      // API 地址
console.log(config.isDev)           // 是否开发环境
```

## 配置注意事项

### 1. 敏感信息安全

以下配置项包含敏感信息，**严禁提交到 Git**：

- `ENCRYPTION_KEY` - 用于加密 SSH 密码和私钥
- `JWT_SECRET_KEY` - 用于 JWT 签名
- 数据库连接字符串中的密码

### 2. 生产环境配置

部署到生产环境时，务必修改以下配置：

```env
# 后端
DEBUG=False
ENCRYPTION_KEY=生产环境专用密钥
JWT_SECRET_KEY=生产环境专用密钥
DATABASE_URL=生产数据库连接
CORS_ALLOW_ORIGINS=生产域名

# 前端
VITE_API_BASE_URL=生产API地址
VITE_SOURCE_MAP=false
```

### 3. 本地开发配置

团队成员首次拉取代码后：

```bash
# 后端
cd backend
cp .env.example .env
# 编辑 .env 文件，配置正确的 ENCRYPTION_KEY

# 前端
cd frontend
# 根据需要创建 .env.local 覆盖默认配置
```

## Git 忽略的配置文件

以下配置文件不会提交到 Git（见 `.gitignore`）：

```
# 后端
backend/.env

# 前端
frontend/.env
frontend/.env.local
frontend/.env.*.local
```

所有配置模板文件（`.env.example`）会被提交，作为团队共享的配置参考。

# API使用说明

## 访问地址

- 本地开发服务器已启动：**http://localhost:8000**

- Swagger UI 文档：**http://localhost:8000/docs
- ReDoc 文档：**http://localhost:8000/redoc

## API 基础路径：`/api/v1`

---

## 机器管理 API

### 1. 机器列表
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/machines` | 获取机器列表（支持分页和筛选 |
| GET | `/api/v1/machines/{id}` | 获取机器详情 |
| POST | `/api/v1/machines` | 创建机器 |
| PUT | `/api/v1/machines/{id}` | 更新机器信息 |
| DELETE | `/api/v1/machines/{id}` | 删除机器（软删除） |

### 2. 连接测试
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/machines/test-connection` | 测试SSH连接（不保存） |
| POST | `/api/v1/machines/{id}/test-connection` | 测试已保存机器的连接 |

### 3. 状态监控
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/machines/{id}/refresh-status` | 刷新机器状态和资源使用情况 |

### 4. 标签管理
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/tags` | 获取标签列表 |
| GET | `/api/v1/tags/{id}` | 获取标签详情 |
| POST | `/api/v1/tags` | 创建标签 |
| PUT | `/api/v1/tags/{id}` | 更新标签 |
| DELETE | `/api/v1/tags/{id}` | 删除标签 |

### 5. 机器-标签关联
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/machines/{machine_id}/tags/{tag_id}` | 给机器添加标签 |
| DELETE | `/api/v1/machines/{machine_id}/tags/{tag_id}` | 移除机器标签 |

### 6. 分组管理
| 方法 | 路径 | 说明 |
|------|------|------|
| GET | `/api/v1/groups` | 获取分组列表 |
| GET | `/api/v1/groups/{id}` | 获取分组详情 |
| POST | `/api/v1/groups` | 创建分组 |
| PUT | `/api/v1/groups/{id}` | 更新分组 |
| DELETE | `/api/v1/groups/{id}` | 删除分组 |

### 7. 机器-分组关联
| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/v1/machines/{machine_id}/groups/{group_id}` | 将机器添加到分组 |
| DELETE | `/api/v1/machines/{machine_id}/groups/{group_id}` | 将机器从分组移除 |

---

## 示例请求

### 创建机器

```bash
curl -X POST "http://localhost:8000/api/v1/machines" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "测试服务器",
    "hostname": "192.168.1.100",
    "port": 22,
    "username": "root",
    "auth_type": "password",
    "password": "your_password",
    "environment": "dev",
    "description": "开发环境服务器"
  }'
```

### 测试连接

```bash
curl -X POST "http://localhost:8000/api/v1/machines/test-connection" \
  -H "Content-Type: application/json" \
  -d '{
    "hostname": "192.168.1.100",
    "port": 22,
    "username": "root",
    "auth_type": "password",
    "password": "your_password"
  }'
```

### 刷新机器状态

```bash
curl -X POST "http://localhost:8000/api/v1/machines/1/refresh-status"
```

---

## 项目结构

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI 入口
│   ├── config.py            # 配置管理
│   ├── database.py          # 数据库连接
│   ├── models/              # 数据模型
│   │   ├── __init__.py
│   │   ├── base.py          # 基础模型混入
│   │   └── machine.py       # 机器相关模型
│   ├── schemas/             # Pydantic Schema
│   │   ├── __init__.py
│   │   └── machine.py       # 请求/响应 Schema
│   ├── services/            # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── machine_service.py
│   │   ├── tag_service.py
│   │   └── group_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── machines.py  # 机器API路由
│   │       ├── tags.py      # 标签API路由
│   │       └── groups.py    # 分组API路由
│   └── utils/               # 工具类
│       ├── __init__.py
│       ├── encryption.py    # 加密工具
│       └── ssh_client.py    # SSH连接工具
├── requirements.txt
├── .env                      # 环境变量
├── .env.example
├── init_db.py                # 数据库初始化脚本
└── devops.db                 # SQLite数据库文件
```

---

## 功能特性

1. **机器管理**：增删改查，支持分页和筛选
2. **SSH连接**：支持密码和密钥两种认证方式
3. **数据加密**：敏感信息（密码、私钥）加密存储
4. **状态监控**：获取CPU、内存、磁盘使用率
5. **标签系统**：支持给机器打标签
6. **分组管理**：支持机器分组管理
7. **软删除**：数据不真正删除，保留历史记录

---

## 停止服务器

在运行服务器的终端按 `Ctrl+C` 停止服务器。

如需重新启动：
```bash
cd backend
uvicorn app.main:app --reload
```

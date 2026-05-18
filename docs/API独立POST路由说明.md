# API 独立 POST 路由改造说明

## 改造背景

将之前整合在单个路由中通过 `action` 字段区分的 CRUD 操作，拆分为独立的 POST 路由，每个功能对应一个独立的接口端点。

---

## 改造特点

✅ **全 POST 接口**：所有接口均使用 POST 方法
✅ **独立路由**：每个功能对应一个独立的路由端点
✅ **统一响应格式**：所有接口返回统一的 `ApiResponse<T>` 格式
✅ **清晰命名**：路由名称直观表达功能含义

---

## 机器管理 API (`/api/v1/machines`)

| 路由端点 | 功能说明 | 请求参数 |
|---------|---------|---------|
| `POST /list` | 获取机器列表 | `page`, `page_size`, `keyword`, `status`, `environment` |
| `POST /get` | 获取机器详情 | `id` |
| `POST /create` | 创建机器 | 机器创建数据 |
| `POST /update` | 更新机器 | `id` + 更新数据 |
| `POST /delete` | 删除机器 | `id` |
| `POST /test-connection` | 测试连接（不保存） | 连接测试参数 |
| `POST /test-saved-connection` | 测试已保存机器连接 | `id` |
| `POST /refresh-status` | 刷新机器状态 | `id` |
| `POST /add-tag` | 添加标签到机器 | `machine_id`, `tag_id` |
| `POST /remove-tag` | 移除机器标签 | `machine_id`, `tag_id` |
| `POST /add-to-group` | 添加机器到分组 | `machine_id`, `group_id` |
| `POST /remove-from-group` | 从分组移除机器 | `machine_id`, `group_id` |

---

## 标签管理 API (`/api/v1/tags`)

| 路由端点 | 功能说明 | 请求参数 |
|---------|---------|---------|
| `POST /list` | 获取标签列表 | `skip`, `limit` |
| `POST /get` | 获取标签详情 | `id` |
| `POST /create` | 创建标签 | 标签创建数据 |
| `POST /update` | 更新标签 | `id` + 更新数据 |
| `POST /delete` | 删除标签 | `id` |

---

## 分组管理 API (`/api/v1/groups`)

| 路由端点 | 功能说明 | 请求参数 |
|---------|---------|---------|
| `POST /list` | 获取分组列表 | `skip`, `limit` |
| `POST /get` | 获取分组详情 | `id` |
| `POST /create` | 创建分组 | 分组创建数据 |
| `POST /update` | 更新分组 | `id` + 更新数据 |
| `POST /delete` | 删除分组 | `id` |

---

## 统一响应格式

```json
{
  "success": true,
  "code": 200,
  "message": "success",
  "action": "machine.list",
  "data": {}
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | boolean | 请求是否成功 |
| `code` | number | 响应状态码 |
| `message` | string | 响应消息 |
| `action` | string | 对应当前操作的标识 |
| `data` | any | 业务数据 |

---

## 调用示例

### 获取机器列表

```bash
POST /api/v1/machines/list
Content-Type: application/json

{
  "page": 1,
  "page_size": 20,
  "keyword": "test"
}
```

### 创建机器

```bash
POST /api/v1/machines/create
Content-Type: application/json

{
  "name": "测试服务器",
  "hostname": "192.168.1.100",
  "port": 22,
  "username": "root",
  "auth_type": "password",
  "password": "xxx",
  "environment": "dev"
}
```

### 更新机器

```bash
POST /api/v1/machines/update
Content-Type: application/json

{
  "id": 1,
  "name": "更新后的名称",
  "description": "新的描述"
}
```

### 删除机器

```bash
POST /api/v1/machines/delete
Content-Type: application/json

{
  "id": 1
}
```

---

## 前端调用示例

### 基础调用

```typescript
import { post } from '@/api/request'

// 获取机器列表
const list = await post('/machines/list', {
  page: 1,
  page_size: 20
})

// 创建机器
await post('/machines/create', {
  name: '服务器1',
  hostname: '192.168.1.100'
})
```

### 使用 API 封装

```typescript
import { machineApi } from '@/api/machine'

// 获取机器列表
const result = await machineApi.getMachines({
  page: 1,
  page_size: 20,
  keyword: 'test'
})

// 创建机器
await machineApi.createMachine(machineData)

// 删除机器
await machineApi.deleteMachine(1)
```

---

## 接口对比（改造前后）

### 改造前（单一入口 + action 字段）

```typescript
// 所有操作都调用同一个 URL
POST /api/v1/machines
{
  "action": "machine.list",  // 通过 action 区分
  "data": { "page": 1, "page_size": 20 }
}
```

### 改造后（独立路由）

```typescript
// 每个操作有独立的 URL
POST /api/v1/machines/list
{ "page": 1, "page_size": 20 }

POST /api/v1/machines/create
{ "name": "服务器1", ... }

POST /api/v1/machines/delete
{ "id": 1 }
```

---

## 改造优势

1. **RESTful 风格**：每个资源操作有清晰的端点
2. **便于调试**：Swagger 文档中每个功能独立展示
3. **日志清晰**：接口日志中可直接通过 URL 识别操作类型
4. **权限控制**：便于基于 URL 做细粒度的权限控制
5. **类型安全**：每个端点有独立的请求和响应类型定义

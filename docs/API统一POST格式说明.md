# API 统一 POST 格式改造说明

## 改造背景

将所有 API 接口统一为 POST 请求方式，通过 `action` 字段标识具体功能用途，便于：
- 统一的请求/响应格式
- 简化前端 API 调用逻辑
- 便于日志审计和功能追踪
- 避免 RESTful 风格中 HTTP 方法的语义混淆

---

## 统一格式规范

### 请求格式

```json
{
  "action": "功能标识，如：machine.list",
  "data": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `action` | string | 是 | 功能用途标识，格式：`模块.操作` |
| `data` | object | 否 | 业务数据参数 |

### 响应格式

```json
{
  "success": true,
  "code": 200,
  "message": "success",
  "action": "machine.list",
  "data": {
    "key": "value"
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| `success` | boolean | 请求是否成功 |
| `code` | number | 响应状态码 |
| `message` | string | 响应消息 |
| `action` | string | 对应当前请求的功能标识 |
| `data` | any | 业务数据 |

---

## 机器管理 API (`/api/v1/machines`)

| action 标识 | 功能说明 | data 参数 |
|------------|----------|----------|
| `machine.list` | 获取机器列表 | `page`, `page_size`, `keyword`, `status`, `environment` |
| `machine.get` | 获取机器详情 | `id` |
| `machine.create` | 创建机器 | 机器创建数据 |
| `machine.update` | 更新机器 | `id` + 更新数据 |
| `machine.delete` | 删除机器 | `id` |
| `machine.test_connection` | 测试连接（不保存） | 连接测试参数 |
| `machine.test_saved_connection` | 测试已保存机器连接 | `id` |
| `machine.refresh_status` | 刷新机器状态 | `id` |
| `machine.add_tag` | 添加标签到机器 | `machine_id`, `tag_id` |
| `machine.remove_tag` | 移除机器标签 | `machine_id`, `tag_id` |
| `machine.add_to_group` | 添加机器到分组 | `machine_id`, `group_id` |
| `machine.remove_from_group` | 从分组移除机器 | `machine_id`, `group_id` |

### 示例请求

**获取机器列表：**
```json
POST /api/v1/machines
{
  "action": "machine.list",
  "data": {
    "page": 1,
    "page_size": 20,
    "keyword": "test"
  }
}
```

**创建机器：**
```json
POST /api/v1/machines
{
  "action": "machine.create",
  "data": {
    "name": "测试服务器",
    "hostname": "192.168.1.100",
    "port": 22,
    "username": "root",
    "auth_type": "password",
    "password": "xxx",
    "environment": "dev"
  }
}
```

---

## 标签管理 API (`/api/v1/tags`)

| action 标识 | 功能说明 | data 参数 |
|------------|----------|----------|
| `tag.list` | 获取标签列表 | `skip`, `limit` |
| `tag.get` | 获取标签详情 | `id` |
| `tag.create` | 创建标签 | 标签创建数据 |
| `tag.update` | 更新标签 | `id` + 更新数据 |
| `tag.delete` | 删除标签 | `id` |

---

## 分组管理 API (`/api/v1/groups`)

| action 标识 | 功能说明 | data 参数 |
|------------|----------|----------|
| `group.list` | 获取分组列表 | `skip`, `limit` |
| `group.get` | 获取分组详情 | `id` |
| `group.create` | 创建分组 | 分组创建数据 |
| `group.update` | 更新分组 | `id` + 更新数据 |
| `group.delete` | 删除分组 | `id` |

---

## 前端调用示例

### 基础调用

```typescript
import { postAction } from '@/api/request'

// 获取机器列表
const list = await postAction('/machines', 'machine.list', {
  page: 1,
  page_size: 20
})

// 创建机器
await postAction('/machines', 'machine.create', {
  name: '服务器1',
  hostname: '192.168.1.100',
  // ... 其他字段
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

## API 调用对比（改造前后）

### 改造前（RESTful 风格）

```typescript
// GET 请求
GET /api/v1/machines?id=1

// POST 请求
POST /api/v1/machines
{
  "name": "test",
  "hostname": "192.168.1.1"
}

// PUT 请求
PUT /api/v1/machines/1
{
  "name": "updated"
}

// DELETE 请求
DELETE /api/v1/machines/1
```

### 改造后（统一 POST）

```typescript
// 获取
POST /api/v1/machines
{ "action": "machine.get", "data": { "id": 1 } }

// 创建
POST /api/v1/machines
{
  "action": "machine.create",
  "data": { "name": "test", "hostname": "192.168.1.1" }
}

// 更新
POST /api/v1/machines
{
  "action": "machine.update",
  "data": { "id": 1, "name": "updated" }
}

// 删除
POST /api/v1/machines
{ "action": "machine.delete", "data": { "id": 1 } }
```

---

## 优势总结

1. **统一入口**：每个模块只有一个 API 入口，便于管理
2. **语义清晰**：通过 `action` 字段明确标识功能用途
3. **便于审计**：日志中可通过 `action` 字段追踪用户操作
4. **简化前端**：所有请求都是 POST，无需处理不同 HTTP 方法
5. **易于扩展**：新增功能只需添加新的 `action`，无需新增路由

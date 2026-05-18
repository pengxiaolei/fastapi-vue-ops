# DevOps 运维管理平台 - 前端

基于 Vue 3 + TypeScript + Vite + Element Plus 开发的 DevOps 运维管理平台前端。

## 技术栈

- **框架**: Vue 3 (Composition API)
- **类型系统**: TypeScript
- **构建工具**: Vite 5
- **UI 组件库**: Element Plus
- **路由**: Vue Router 4
- **状态管理**: Pinia
- **HTTP 客户端**: Axios

## 功能特性

### 机器管理
- ✅ 机器列表展示（支持分页、搜索、筛选）
- ✅ 新增/编辑/删除机器
- ✅ SSH 连接测试（密码/密钥认证）
- ✅ 机器状态刷新
- ✅ 机器详情页面
- ✅ 资源使用监控（CPU/内存/磁盘）
- ✅ 标签管理
- ✅ 分组管理

### 标签管理
- ✅ 标签列表
- ✅ 新增/编辑/删除标签
- ✅ 自定义标签颜色

### 分组管理
- ✅ 分组列表
- ✅ 新增/编辑/删除分组

## 项目结构

```
frontend/
├── src/
│   ├── api/              # API 接口
│   │   ├── request.ts    # Axios 实例配置
│   │   ├── machine.ts    # 机器相关 API
│   │   ├── tag.ts        # 标签相关 API
│   │   └── group.ts      # 分组相关 API
│   ├── types/            # TypeScript 类型定义
│   │   └── machine.ts    # 机器相关类型
│   ├── views/            # 页面组件
│   │   ├── dashboard/    # 仪表盘
│   │   ├── machines/     # 机器管理
│   │   │   ├── components/
│   │   │   ├── index.vue
│   │   │   └── detail.vue
│   │   ├── tags/         # 标签管理
│   │   └── groups/       # 分组管理
│   ├── layout/           # 布局组件
│   │   └── index.vue
│   ├── router/           # 路由配置
│   │   └── index.ts
│   ├── App.vue           # 根组件
│   └── main.ts           # 入口文件
├── index.html
├── vite.config.ts
├── tsconfig.json
└── package.json
```

## 快速开始

### 安装依赖

```bash
cd frontend
npm install
```

### 启动开发服务器

```bash
npm run dev
```

访问 http://localhost:3000

### 构建生产版本

```bash
npm run build
```

## 后端服务

前端默认通过 `/api` 代理到后端 `http://localhost:8000`。

如需修改代理配置，请编辑 `vite.config.ts`：

```typescript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',  // 修改为你的后端地址
      changeOrigin: true
    }
  }
}
```

## 页面说明

### 仪表盘 `/dashboard`
- 机器统计概览（总数、在线、离线）
- 机器状态列表
- 快捷操作入口

### 机器管理 `/machines`
- 机器列表展示
- 搜索和筛选功能
- 批量操作
- 连接测试
- 状态刷新

### 机器详情 `/machines/:id`
- 基本信息展示
- 资源监控图表
- 标签管理
- 分组管理

### 标签管理 `/tags`
- 标签列表
- 新增/编辑/删除标签
- 自定义标签颜色

### 分组管理 `/groups`
- 分组列表
- 新增/编辑/删除分组

## 注意事项

1. 确保后端服务已启动并正常运行
2. SSH 连接需要目标机器开启 SSH 服务
3. 敏感信息（密码、私钥）在后端加密存储

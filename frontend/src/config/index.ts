/**
 * 前端配置文件
 * 从环境变量加载配置
 */

const config = {
  // 基础配置
  appTitle: import.meta.env.VITE_APP_TITLE || 'DevOps 运维管理平台',
  appVersion: import.meta.env.VITE_APP_VERSION || '1.0.0',

  // API 配置
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || '/api',
  apiTimeout: parseInt(import.meta.env.VITE_API_TIMEOUT || '30000'),

  // 开发配置
  useMock: import.meta.env.VITE_USE_MOCK === 'true',

  // 环境标识
  isDev: import.meta.env.DEV,
  isProd: import.meta.env.PROD,

  // 分页配置
  defaultPageSize: 20,
  pageSizeOptions: [10, 20, 50, 100]
}

export default config

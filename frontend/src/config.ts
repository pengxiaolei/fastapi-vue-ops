// 应用配置 - 使用环境变量
const config = {
  // API基础URL
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || '/api/v1',
  // 请求超时时间（毫秒）
  apiTimeout: parseInt(import.meta.env.VITE_API_TIMEOUT || '30000'),
  // 应用名称
  appName: 'DevOps 运维管理平台'
}

export default config

// 打印配置用于调试
console.log('📋 应用配置:', config)
console.log(`🔌 API代理目标: ${import.meta.env.VITE_PROXY_TARGET || 'http://localhost:8000'}`)

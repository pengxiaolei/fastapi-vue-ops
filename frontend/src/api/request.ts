import axios, { type AxiosInstance, type AxiosRequestConfig } from 'axios'
import { ElMessage } from 'element-plus'
import config from '@/config'

// 统一响应格式
export interface ApiResponse<T = any> {
  success: boolean
  code: number
  message: string
  action?: string
  data: T
}

const service: AxiosInstance = axios.create({
  baseURL: config.apiBaseUrl,
  timeout: config.apiTimeout,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器：添加调试日志
service.interceptors.request.use(
  (config) => {
    console.log(`📤 [API 请求] ${config.method?.toUpperCase()} ${config.url}`, config.data)
    return config
  },
  (error) => {
    console.error('❌ [API 请求错误]', error)
    return Promise.reject(error)
  }
)

// 响应拦截器：处理统一响应格式
service.interceptors.response.use(
  (response) => {
    const res: ApiResponse = response.data
    console.log(`📥 [API 响应原始数据] ${response.config.url}`, res)
    if (!res.success) {
      ElMessage.error(res.message || '请求失败')
      return Promise.reject(new Error(res.message))
    }
    // 返回完整的 axios response 对象，保持结构一致
    return response
  },
  (error) => {
    console.error('❌ [API 响应错误]', error)
    const message = error.response?.data?.detail || error.message || '请求失败'
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

/**
 * 统一 POST 请求封装
 * @param url API 地址
 * @param data 请求数据
 */
export async function post<T = any>(url: string, data?: any): Promise<T> {
  const response = await service.post<ApiResponse<T>>(url, data)
  console.log('📨 post 函数返回:', response.data.data)
  return response.data.data as T
}

export default service

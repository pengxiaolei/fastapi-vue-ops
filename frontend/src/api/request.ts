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

// 请求拦截器：统一封装为 POST 请求格式
service.interceptors.request.use(
  (config) => {
    // 所有请求都转为 POST
    config.method = 'POST'
    return config
  },
  (error) => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器：处理统一响应格式
service.interceptors.response.use(
  (response) => {
    const res: ApiResponse = response.data
    if (!res.success) {
      ElMessage.error(res.message || '请求失败')
      return Promise.reject(new Error(res.message))
    }
    return res
  },
  (error) => {
    console.error('Response error:', error)
    const message = error.response?.data?.detail || error.message || '请求失败'
    ElMessage.error(message)
    return Promise.reject(error)
  }
)

/**
 * 统一 POST 请求封装
 * @param url API 地址
 * @param action 功能用途标识
 * @param data 业务数据
 */
export async function postAction<T = any>(
  url: string,
  action: string,
  data?: any
): Promise<T> {
  const response = await service.post<ApiResponse<T>>(url, {
    action,
    data
  })
  return response.data.data as T
}

export default service

import { post } from './request'
import type { Tag, TagCreate, TagUpdate } from '@/types/machine'

const API_BASE = '/tags'

export const tagApi = {
  /**
   * 获取标签列表
   * POST /api/v1/tags/list
   */
  getTags: (params?: { skip?: number; limit?: number }) => {
    return post<Tag[]>(`${API_BASE}/list`, params)
  },

  /**
   * 获取标签详情
   * POST /api/v1/tags/get
   */
  getTag: (id: number) => {
    return post<Tag>(`${API_BASE}/get`, { id })
  },

  /**
   * 创建标签
   * POST /api/v1/tags/create
   */
  createTag: (data: TagCreate) => {
    return post<Tag>(`${API_BASE}/create`, data)
  },

  /**
   * 更新标签
   * POST /api/v1/tags/update
   */
  updateTag: (id: number, data: TagUpdate) => {
    return post<Tag>(`${API_BASE}/update`, { id, ...data })
  },

  /**
   * 删除标签
   * POST /api/v1/tags/delete
   */
  deleteTag: (id: number) => {
    return post<{ success: boolean; message: string }>(`${API_BASE}/delete`, { id })
  }
}

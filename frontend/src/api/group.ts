import { post } from './request'
import type { Group, GroupCreate, GroupUpdate } from '@/types/machine'

const API_BASE = '/groups'

export const groupApi = {
  /**
   * 获取分组列表
   * POST /api/v1/groups/list
   */
  getGroups: (params?: { skip?: number; limit?: number }) => {
    return post<Group[]>(`${API_BASE}/list`, params)
  },

  /**
   * 获取分组详情
   * POST /api/v1/groups/get
   */
  getGroup: (id: number) => {
    return post<Group>(`${API_BASE}/get`, { id })
  },

  /**
   * 创建分组
   * POST /api/v1/groups/create
   */
  createGroup: (data: GroupCreate) => {
    return post<Group>(`${API_BASE}/create`, data)
  },

  /**
   * 更新分组
   * POST /api/v1/groups/update
   */
  updateGroup: (id: number, data: GroupUpdate) => {
    return post<Group>(`${API_BASE}/update`, { id, ...data })
  },

  /**
   * 删除分组
   * POST /api/v1/groups/delete
   */
  deleteGroup: (id: number) => {
    return post<{ success: boolean; message: string }>(`${API_BASE}/delete`, { id })
  }
}

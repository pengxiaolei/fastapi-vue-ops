import { postAction } from './request'
import type { Group, GroupCreate, GroupUpdate } from '@/types/machine'

const API_BASE = '/groups'

export const groupApi = {
  /**
   * 获取分组列表
   * action: group.list
   */
  getGroups: (params?: { skip?: number; limit?: number }) => {
    return postAction<Group[]>(API_BASE, 'group.list', params)
  },

  /**
   * 获取分组详情
   * action: group.get
   */
  getGroup: (id: number) => {
    return postAction<Group>(API_BASE, 'group.get', { id })
  },

  /**
   * 创建分组
   * action: group.create
   */
  createGroup: (data: GroupCreate) => {
    return postAction<Group>(API_BASE, 'group.create', data)
  },

  /**
   * 更新分组
   * action: group.update
   */
  updateGroup: (id: number, data: GroupUpdate) => {
    return postAction<Group>(API_BASE, 'group.update', { id, ...data })
  },

  /**
   * 删除分组
   * action: group.delete
   */
  deleteGroup: (id: number) => {
    return postAction<{ success: boolean; message: string }>(API_BASE, 'group.delete', { id })
  }
}

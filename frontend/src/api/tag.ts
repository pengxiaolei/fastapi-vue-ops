import { postAction } from './request'
import type { Tag, TagCreate, TagUpdate } from '@/types/machine'

const API_BASE = '/tags'

export const tagApi = {
  /**
   * 获取标签列表
   * action: tag.list
   */
  getTags: (params?: { skip?: number; limit?: number }) => {
    return postAction<Tag[]>(API_BASE, 'tag.list', params)
  },

  /**
   * 获取标签详情
   * action: tag.get
   */
  getTag: (id: number) => {
    return postAction<Tag>(API_BASE, 'tag.get', { id })
  },

  /**
   * 创建标签
   * action: tag.create
   */
  createTag: (data: TagCreate) => {
    return postAction<Tag>(API_BASE, 'tag.create', data)
  },

  /**
   * 更新标签
   * action: tag.update
   */
  updateTag: (id: number, data: TagUpdate) => {
    return postAction<Tag>(API_BASE, 'tag.update', { id, ...data })
  },

  /**
   * 删除标签
   * action: tag.delete
   */
  deleteTag: (id: number) => {
    return postAction<{ success: boolean; message: string }>(API_BASE, 'tag.delete', { id })
  }
}

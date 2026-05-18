import request from './request'
import type { Tag, TagCreate, TagUpdate } from '@/types/machine'

export const tagApi = {
  getTags: (params?: { skip?: number; limit?: number }) => {
    return request.get<any, Tag[]>('/tags', { params })
  },

  getTag: (id: number) => {
    return request.get<any, Tag>(`/tags/${id}`)
  },

  createTag: (data: TagCreate) => {
    return request.post<any, Tag>('/tags', data)
  },

  updateTag: (id: number, data: TagUpdate) => {
    return request.put<any, Tag>(`/tags/${id}`, data)
  },

  deleteTag: (id: number) => {
    return request.delete<any, { success: boolean; message: string }>(`/tags/${id}`)
  }
}

import request from './request'
import type { Group, GroupCreate, GroupUpdate } from '@/types/machine'

export const groupApi = {
  getGroups: (params?: { skip?: number; limit?: number }) => {
    return request.get<any, Group[]>('/groups', { params })
  },

  getGroup: (id: number) => {
    return request.get<any, Group>(`/groups/${id}`)
  },

  createGroup: (data: GroupCreate) => {
    return request.post<any, Group>('/groups', data)
  },

  updateGroup: (id: number, data: GroupUpdate) => {
    return request.put<any, Group>(`/groups/${id}`, data)
  },

  deleteGroup: (id: number) => {
    return request.delete<any, { success: boolean; message: string }>(`/groups/${id}`)
  }
}

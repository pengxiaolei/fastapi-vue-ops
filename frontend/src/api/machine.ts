import request from './request'
import type {
  Machine,
  MachineCreate,
  MachineUpdate,
  ConnectionTestRequest,
  ConnectionTestResponse,
  MachineStatusResponse,
  PaginatedResponse
} from '@/types/machine'

export const machineApi = {
  getMachines: (params?: {
    page?: number
    page_size?: number
    keyword?: string
    status?: string
    environment?: string
  }) => {
    return request.get<any, PaginatedResponse<Machine>>('/machines', { params })
  },

  getMachine: (id: number) => {
    return request.get<any, Machine>(`/machines/${id}`)
  },

  createMachine: (data: MachineCreate) => {
    return request.post<any, Machine>('/machines', data)
  },

  updateMachine: (id: number, data: MachineUpdate) => {
    return request.put<any, Machine>(`/machines/${id}`, data)
  },

  deleteMachine: (id: number) => {
    return request.delete<any, { success: boolean; message: string }>(`/machines/${id}`)
  },

  testConnection: (data: ConnectionTestRequest) => {
    return request.post<any, ConnectionTestResponse>('/machines/test-connection', data)
  },

  testMachineConnection: (id: number) => {
    return request.post<any, ConnectionTestResponse>(`/machines/${id}/test-connection`)
  },

  refreshMachineStatus: (id: number) => {
    return request.post<any, MachineStatusResponse>(`/machines/${id}/refresh-status`)
  },

  addTagToMachine: (machineId: number, tagId: number) => {
    return request.post<any, { success: boolean; message: string }>(
      `/machines/${machineId}/tags/${tagId}`
    )
  },

  removeTagFromMachine: (machineId: number, tagId: number) => {
    return request.delete<any, { success: boolean; message: string }>(
      `/machines/${machineId}/tags/${tagId}`
    )
  },

  addMachineToGroup: (machineId: number, groupId: number) => {
    return request.post<any, { success: boolean; message: string }>(
      `/machines/${machineId}/groups/${groupId}`
    )
  },

  removeMachineFromGroup: (machineId: number, groupId: number) => {
    return request.delete<any, { success: boolean; message: string }>(
      `/machines/${machineId}/groups/${groupId}`
    )
  }
}

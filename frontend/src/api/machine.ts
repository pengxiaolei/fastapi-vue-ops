import { post } from './request'
import type {
  Machine,
  MachineCreate,
  MachineUpdate,
  ConnectionTestRequest,
  ConnectionTestResponse,
  MachineStatusResponse,
  MachineListResponse
} from '@/types/machine'

const API_BASE = '/machines'

export const machineApi = {
  /**
   * 获取机器列表
   * POST /api/v1/machines/list
   */
  getMachines: (params?: {
    page?: number
    page_size?: number
    keyword?: string
    status?: string
    environment?: string
  }) => {
    return post<MachineListResponse>(`${API_BASE}/list`, params)
  },

  /**
   * 获取机器详情
   * POST /api/v1/machines/get
   */
  getMachine: (id: number) => {
    return post<Machine>(`${API_BASE}/get`, { id })
  },

  /**
   * 创建机器
   * POST /api/v1/machines/create
   */
  createMachine: (data: MachineCreate) => {
    return post<Machine>(`${API_BASE}/create`, data)
  },

  /**
   * 更新机器
   * POST /api/v1/machines/update
   */
  updateMachine: (id: number, data: MachineUpdate) => {
    return post<Machine>(`${API_BASE}/update`, { id, ...data })
  },

  /**
   * 删除机器
   * POST /api/v1/machines/delete
   */
  deleteMachine: (id: number) => {
    return post<{ success: boolean; message: string }>(`${API_BASE}/delete`, { id })
  },

  /**
   * 测试连接（不保存）
   * POST /api/v1/machines/test-connection
   */
  testConnection: (data: ConnectionTestRequest) => {
    return post<ConnectionTestResponse>(`${API_BASE}/test-connection`, data)
  },

  /**
   * 测试已保存机器的连接
   * POST /api/v1/machines/test-saved-connection
   */
  testMachineConnection: (id: number) => {
    return post<ConnectionTestResponse>(`${API_BASE}/test-saved-connection`, { id })
  },

  /**
   * 刷新机器状态
   * POST /api/v1/machines/refresh-status
   */
  refreshMachineStatus: (id: number) => {
    return post<MachineStatusResponse>(`${API_BASE}/refresh-status`, { id })
  },

  /**
   * 给机器添加标签
   * POST /api/v1/machines/add-tag
   */
  addTagToMachine: (machineId: number, tagId: number) => {
    return post<{ success: boolean; message: string }>(`${API_BASE}/add-tag`, {
      machine_id: machineId,
      tag_id: tagId
    })
  },

  /**
   * 移除机器标签
   * POST /api/v1/machines/remove-tag
   */
  removeTagFromMachine: (machineId: number, tagId: number) => {
    return post<{ success: boolean; message: string }>(`${API_BASE}/remove-tag`, {
      machine_id: machineId,
      tag_id: tagId
    })
  },

  /**
   * 将机器添加到分组
   * POST /api/v1/machines/add-to-group
   */
  addMachineToGroup: (machineId: number, groupId: number) => {
    return post<{ success: boolean; message: string }>(`${API_BASE}/add-to-group`, {
      machine_id: machineId,
      group_id: groupId
    })
  },

  /**
   * 将机器从分组移除
   * POST /api/v1/machines/remove-from-group
   */
  removeMachineFromGroup: (machineId: number, groupId: number) => {
    return post<{ success: boolean; message: string }>(`${API_BASE}/remove-from-group`, {
      machine_id: machineId,
      group_id: groupId
    })
  }
}

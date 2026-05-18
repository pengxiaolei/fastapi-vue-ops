import { postAction } from './request'
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
   * action: machine.list
   */
  getMachines: (params?: {
    page?: number
    page_size?: number
    keyword?: string
    status?: string
    environment?: string
  }) => {
    return postAction<MachineListResponse>(API_BASE, 'machine.list', params)
  },

  /**
   * 获取机器详情
   * action: machine.get
   */
  getMachine: (id: number) => {
    return postAction<Machine>(API_BASE, 'machine.get', { id })
  },

  /**
   * 创建机器
   * action: machine.create
   */
  createMachine: (data: MachineCreate) => {
    return postAction<Machine>(API_BASE, 'machine.create', data)
  },

  /**
   * 更新机器
   * action: machine.update
   */
  updateMachine: (id: number, data: MachineUpdate) => {
    return postAction<Machine>(API_BASE, 'machine.update', { id, ...data })
  },

  /**
   * 删除机器
   * action: machine.delete
   */
  deleteMachine: (id: number) => {
    return postAction<{ success: boolean; message: string }>(API_BASE, 'machine.delete', { id })
  },

  /**
   * 测试连接（不保存）
   * action: machine.test_connection
   */
  testConnection: (data: ConnectionTestRequest) => {
    return postAction<ConnectionTestResponse>(API_BASE, 'machine.test_connection', data)
  },

  /**
   * 测试已保存机器的连接
   * action: machine.test_saved_connection
   */
  testMachineConnection: (id: number) => {
    return postAction<ConnectionTestResponse>(API_BASE, 'machine.test_saved_connection', { id })
  },

  /**
   * 刷新机器状态
   * action: machine.refresh_status
   */
  refreshMachineStatus: (id: number) => {
    return postAction<MachineStatusResponse>(API_BASE, 'machine.refresh_status', { id })
  },

  /**
   * 给机器添加标签
   * action: machine.add_tag
   */
  addTagToMachine: (machineId: number, tagId: number) => {
    return postAction<{ success: boolean; message: string }>(API_BASE, 'machine.add_tag', {
      machine_id: machineId,
      tag_id: tagId
    })
  },

  /**
   * 移除机器标签
   * action: machine.remove_tag
   */
  removeTagFromMachine: (machineId: number, tagId: number) => {
    return postAction<{ success: boolean; message: string }>(API_BASE, 'machine.remove_tag', {
      machine_id: machineId,
      tag_id: tagId
    })
  },

  /**
   * 将机器添加到分组
   * action: machine.add_to_group
   */
  addMachineToGroup: (machineId: number, groupId: number) => {
    return postAction<{ success: boolean; message: string }>(API_BASE, 'machine.add_to_group', {
      machine_id: machineId,
      group_id: groupId
    })
  },

  /**
   * 将机器从分组移除
   * action: machine.remove_from_group
   */
  removeMachineFromGroup: (machineId: number, groupId: number) => {
    return postAction<{ success: boolean; message: string }>(API_BASE, 'machine.remove_from_group', {
      machine_id: machineId,
      group_id: groupId
    })
  }
}

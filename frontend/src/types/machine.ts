export type AuthType = 'password' | 'key'

export type MachineStatus = 'online' | 'offline' | 'maintenance'

export interface Machine {
  id: number
  name: string
  hostname: string
  port: number
  username: string
  auth_type: AuthType
  os_type?: string
  status: MachineStatus
  cpu_cores?: number
  memory_total?: number
  disk_total?: number
  cpu_usage?: number
  memory_usage?: number
  disk_usage?: number
  environment?: string
  last_heartbeat?: string
  description?: string
  created_at: string
  updated_at: string
  tags: Tag[]
  groups: Group[]
}

export interface MachineCreate {
  name: string
  hostname: string
  port: number
  username: string
  auth_type: AuthType
  password?: string
  private_key?: string
  os_type?: string
  environment?: string
  description?: string
}

export interface MachineUpdate {
  name?: string
  hostname?: string
  port?: number
  username?: string
  auth_type?: AuthType
  password?: string
  private_key?: string
  os_type?: string
  environment?: string
  description?: string
  status?: MachineStatus
}

export interface Tag {
  id: number
  name: string
  color?: string
  created_at: string
}

export interface TagCreate {
  name: string
  color?: string
}

export interface TagUpdate {
  name?: string
  color?: string
}

export interface Group {
  id: number
  name: string
  description?: string
  created_at: string
}

export interface GroupCreate {
  name: string
  description?: string
}

export interface GroupUpdate {
  name?: string
  description?: string
}

export interface ConnectionTestRequest {
  hostname: string
  port: number
  username: string
  auth_type: AuthType
  password?: string
  private_key?: string
}

export interface ConnectionTestResponse {
  success: boolean
  message: string
  os_type?: string
  cpu_cores?: number
  memory_total?: number
  disk_total?: number
  cpu_usage?: number
  memory_usage?: number
  disk_usage?: number
}

export interface MachineStatusResponse {
  success: boolean
  message: string
  status?: MachineStatus
  cpu_usage?: number
  memory_usage?: number
  disk_usage?: number
}

export interface PaginatedResponse<T> {
  total: number
  page: number
  page_size: number
  total_pages: number
  data: T[]
}

export type MachineListResponse = PaginatedResponse<Machine>

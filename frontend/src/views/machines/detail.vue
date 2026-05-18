<template>
  <div class="machine-detail">
    <el-card v-loading="loading" shadow="never">
      <template #header>
        <div class="detail-header">
          <div class="header-left">
            <el-button @click="goBack" link>
              <el-icon><ArrowLeft /></el-icon>
              返回
            </el-button>
            <h2>{{ machine?.name }}</h2>
            <el-tag :type="getStatusType(machine?.status)" size="large">
              {{ getStatusText(machine?.status) }}
            </el-tag>
          </div>
          <div class="header-right">
            <el-button type="success" @click="refreshStatus" :loading="refreshLoading">
              <el-icon><Refresh /></el-icon>
              刷新状态
            </el-button>
            <el-button type="warning" @click="testConnection" :loading="testLoading">
              <el-icon><Connection /></el-icon>
              测试连接
            </el-button>
            <el-button type="primary" @click="handleEdit">
              <el-icon><Edit /></el-icon>
              编辑
            </el-button>
          </div>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <el-tab-pane label="基本信息" name="basic">
          <el-descriptions :column="2" border>
            <el-descriptions-item label="机器名称">{{ machine?.name }}</el-descriptions-item>
            <el-descriptions-item label="主机地址">{{ machine?.hostname }}:{{ machine?.port }}</el-descriptions-item>
            <el-descriptions-item label="用户名">{{ machine?.username }}</el-descriptions-item>
            <el-descriptions-item label="认证方式">
              {{ machine?.auth_type === 'password' ? '密码' : '密钥' }}
            </el-descriptions-item>
            <el-descriptions-item label="操作系统">{{ machine?.os_type || '-' }}</el-descriptions-item>
            <el-descriptions-item label="所属环境">
              <el-tag v-if="machine?.environment" size="small" type="info">
                {{ getEnvironmentText(machine.environment) }}
              </el-tag>
              <span v-else>-</span>
            </el-descriptions-item>
            <el-descriptions-item label="CPU核数">{{ machine?.cpu_cores || '-' }} 核</el-descriptions-item>
            <el-descriptions-item label="总内存">{{ machine?.memory_total ? machine.memory_total + ' MB' : '-' }}</el-descriptions-item>
            <el-descriptions-item label="总磁盘">{{ machine?.disk_total ? machine.disk_total + ' GB' : '-' }}</el-descriptions-item>
            <el-descriptions-item label="最后心跳">
              {{ machine?.last_heartbeat ? formatDate(machine.last_heartbeat) : '-' }}
            </el-descriptions-item>
            <el-descriptions-item label="创建时间">{{ formatDate(machine?.created_at) }}</el-descriptions-item>
            <el-descriptions-item label="更新时间">{{ formatDate(machine?.updated_at) }}</el-descriptions-item>
            <el-descriptions-item label="描述" :span="2">{{ machine?.description || '-' }}</el-descriptions-item>
          </el-descriptions>
        </el-tab-pane>

        <el-tab-pane label="资源监控" name="metrics">
          <el-row :gutter="20">
            <el-col :span="8">
              <el-card class="metric-card">
                <div class="metric-title">
                  <el-icon><Cpu /></el-icon>
                  CPU 使用率
                </div>
                <div class="metric-value" :class="getMetricClass(machine?.cpu_usage)">
                  {{ machine?.cpu_usage?.toFixed(1) || 0 }}%
                </div>
                <el-progress
                  :percentage="machine?.cpu_usage || 0"
                  :color="getProgressColor(machine?.cpu_usage)"
                  :stroke-width="10"
                />
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card class="metric-card">
                <div class="metric-title">
                  <el-icon><Odometer /></el-icon>
                  内存使用率
                </div>
                <div class="metric-value" :class="getMetricClass(machine?.memory_usage)">
                  {{ machine?.memory_usage?.toFixed(1) || 0 }}%
                </div>
                <el-progress
                  :percentage="machine?.memory_usage || 0"
                  :color="getProgressColor(machine?.memory_usage)"
                  :stroke-width="10"
                />
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card class="metric-card">
                <div class="metric-title">
                  <el-icon><FolderOpened /></el-icon>
                  磁盘使用率
                </div>
                <div class="metric-value" :class="getMetricClass(machine?.disk_usage)">
                  {{ machine?.disk_usage?.toFixed(1) || 0 }}%
                </div>
                <el-progress
                  :percentage="machine?.disk_usage || 0"
                  :color="getProgressColor(machine?.disk_usage)"
                  :stroke-width="10"
                />
              </el-card>
            </el-col>
          </el-row>
        </el-tab-pane>

        <el-tab-pane label="标签管理" name="tags">
          <div class="tag-management">
            <div class="tag-section">
              <h3>已绑定标签</h3>
              <div class="tag-list">
                <el-tag
                  v-for="tag in machine?.tags"
                  :key="tag.id"
                  closable
                  :style="{ backgroundColor: tag.color + '20', color: tag.color, borderColor: tag.color }"
                  @close="removeTag(tag.id)"
                >
                  {{ tag.name }}
                </el-tag>
                <el-empty v-if="!machine?.tags?.length" description="暂无标签" />
              </div>
            </div>
            <div class="tag-section">
              <h3>添加标签</h3>
              <div class="tag-list">
                <el-tag
                  v-for="tag in availableTags"
                  :key="tag.id"
                  class="addable-tag"
                  :style="{ backgroundColor: tag.color + '20', color: tag.color, borderColor: tag.color }"
                  @click="addTag(tag.id)"
                >
                  <el-icon><Plus /></el-icon>
                  {{ tag.name }}
                </el-tag>
                <el-empty v-if="availableTags.length === 0" description="暂无可用标签" />
              </div>
            </div>
          </div>
        </el-tab-pane>

        <el-tab-pane label="分组管理" name="groups">
          <div class="group-management">
            <div class="group-section">
              <h3>已加入分组</h3>
              <div class="group-list">
                <el-tag
                  v-for="group in machine?.groups"
                  :key="group.id"
                  closable
                  type="info"
                  @close="removeGroup(group.id)"
                >
                  {{ group.name }}
                </el-tag>
                <el-empty v-if="!machine?.groups?.length" description="暂无分组" />
              </div>
            </div>
            <div class="group-section">
              <h3>加入分组</h3>
              <div class="group-list">
                <el-tag
                  v-for="group in availableGroups"
                  :key="group.id"
                  class="addable-tag"
                  type="info"
                  @click="addGroup(group.id)"
                >
                  <el-icon><Plus /></el-icon>
                  {{ group.name }}
                </el-tag>
                <el-empty v-if="availableGroups.length === 0" description="暂无可用分组" />
              </div>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <MachineForm
      v-model:visible="editDialogVisible"
      :machine="machine"
      @success="handleEditSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  ArrowLeft,
  Refresh,
  Connection,
  Edit,
  Cpu,
  Odometer,
  FolderOpened,
  Plus
} from '@element-plus/icons-vue'
import { machineApi } from '@/api/machine'
import { tagApi } from '@/api/tag'
import { groupApi } from '@/api/group'
import type { Machine, MachineStatus, Tag, Group } from '@/types/machine'
import MachineForm from './components/MachineForm.vue'

const route = useRoute()
const router = useRouter()

const machineId = computed(() => Number(route.params.id))
const loading = ref(false)
const refreshLoading = ref(false)
const testLoading = ref(false)
const editDialogVisible = ref(false)
const activeTab = ref('basic')

const machine = ref<Machine | null>(null)
const allTags = ref<Tag[]>([])
const allGroups = ref<Group[]>([])

const availableTags = computed(() => {
  if (!machine.value) return []
  const machineTagIds = new Set(machine.value.tags.map(t => t.id))
  return allTags.value.filter(t => !machineTagIds.has(t.id))
})

const availableGroups = computed(() => {
  if (!machine.value) return []
  const machineGroupIds = new Set(machine.value.groups.map(g => g.id))
  return allGroups.value.filter(g => !machineGroupIds.has(g.id))
})

const loadMachine = async () => {
  loading.value = true
  try {
    machine.value = await machineApi.getMachine(machineId.value)
  } catch (error) {
    ElMessage.error('加载机器详情失败')
  } finally {
    loading.value = false
  }
}

const loadTags = async () => {
  try {
    allTags.value = await tagApi.getTags()
  } catch (error) {
    console.error('加载标签列表失败:', error)
  }
}

const loadGroups = async () => {
  try {
    allGroups.value = await groupApi.getGroups()
  } catch (error) {
    console.error('加载分组列表失败:', error)
  }
}

const refreshStatus = async () => {
  refreshLoading.value = true
  try {
    await machineApi.refreshMachineStatus(machineId.value)
    await loadMachine()
    ElMessage.success('状态刷新成功')
  } catch (error) {
    ElMessage.error('状态刷新失败')
  } finally {
    refreshLoading.value = false
  }
}

const testConnection = async () => {
  testLoading.value = true
  try {
    const res = await machineApi.testMachineConnection(machineId.value)
    if (res.success) {
      ElMessage.success('连接测试成功')
    } else {
      ElMessage.error(`连接测试失败: ${res.message}`)
    }
  } catch (error) {
    ElMessage.error('连接测试失败')
  } finally {
    testLoading.value = false
  }
}

const addTag = async (tagId: number) => {
  try {
    await machineApi.addTagToMachine(machineId.value, tagId)
    ElMessage.success('添加标签成功')
    loadMachine()
  } catch (error) {
    ElMessage.error('添加标签失败')
  }
}

const removeTag = async (tagId: number) => {
  try {
    await machineApi.removeTagFromMachine(machineId.value, tagId)
    ElMessage.success('移除标签成功')
    loadMachine()
  } catch (error) {
    ElMessage.error('移除标签失败')
  }
}

const addGroup = async (groupId: number) => {
  try {
    await machineApi.addMachineToGroup(machineId.value, groupId)
    ElMessage.success('加入分组成功')
    loadMachine()
  } catch (error) {
    ElMessage.error('加入分组失败')
  }
}

const removeGroup = async (groupId: number) => {
  try {
    await machineApi.removeMachineFromGroup(machineId.value, groupId)
    ElMessage.success('移出分组成功')
    loadMachine()
  } catch (error) {
    ElMessage.error('移出分组失败')
  }
}

const handleEdit = () => {
  editDialogVisible.value = true
}

const handleEditSuccess = () => {
  editDialogVisible.value = false
  loadMachine()
}

const goBack = () => {
  router.back()
}

const getStatusType = (status?: MachineStatus) => {
  if (!status) return 'info'
  const map: Record<MachineStatus, string> = {
    online: 'success',
    offline: 'danger',
    maintenance: 'warning'
  }
  return map[status] || 'info'
}

const getStatusText = (status?: MachineStatus) => {
  if (!status) return '未知'
  const map: Record<MachineStatus, string> = {
    online: '在线',
    offline: '离线',
    maintenance: '维护中'
  }
  return map[status] || '未知'
}

const getEnvironmentText = (env: string) => {
  const map: Record<string, string> = {
    dev: '开发',
    test: '测试',
    prod: '生产'
  }
  return map[env] || env
}

const getProgressColor = (value?: number) => {
  if (!value) return '#e6e6e6'
  if (value < 50) return '#67c23a'
  if (value < 80) return '#e6a23c'
  return '#f56c6c'
}

const getMetricClass = (value?: number) => {
  if (!value) return 'normal'
  if (value < 50) return 'normal'
  if (value < 80) return 'warning'
  return 'danger'
}

const formatDate = (dateStr?: string) => {
  if (!dateStr) return '-'
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  loadMachine()
  loadTags()
  loadGroups()
})
</script>

<style scoped lang="scss">
.machine-detail {
  .detail-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    .header-left {
      display: flex;
      align-items: center;
      gap: 15px;

      h2 {
        margin: 0;
        font-size: 20px;
        font-weight: 500;
      }
    }

    .header-right {
      display: flex;
      gap: 10px;
    }
  }

  .metric-card {
    text-align: center;

    .metric-title {
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      font-size: 16px;
      color: #606266;
      margin-bottom: 15px;
    }

    .metric-value {
      font-size: 36px;
      font-weight: bold;
      margin-bottom: 15px;

      &.normal {
        color: #67c23a;
      }

      &.warning {
        color: #e6a23c;
      }

      &.danger {
        color: #f56c6c;
      }
    }
  }

  .tag-management,
  .group-management {
    padding: 20px 0;

    .tag-section,
    .group-section {
      margin-bottom: 30px;

      h3 {
        margin: 0 0 15px 0;
        font-size: 16px;
        font-weight: 500;
        color: #303133;
      }

      .tag-list,
      .group-list {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        min-height: 60px;

        .addable-tag {
          cursor: pointer;
          transition: all 0.3s;

          &:hover {
            transform: scale(1.05);
          }
        }
      }
    }
  }
}
</style>

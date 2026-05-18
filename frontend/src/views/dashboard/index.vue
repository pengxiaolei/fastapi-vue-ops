<template>
  <div class="dashboard">
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon online">
              <el-icon><Monitor /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ machineStats.total }}</div>
              <div class="stat-label">机器总数</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon success">
              <el-icon><CircleCheck /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ machineStats.online }}</div>
              <div class="stat-label">在线</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon warning">
              <el-icon><CircleClose /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ machineStats.offline }}</div>
              <div class="stat-label">离线</div>
            </div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-content">
            <div class="stat-icon primary">
              <el-icon><PriceTag /></el-icon>
            </div>
            <div class="stat-info">
              <div class="stat-value">{{ tagCount }}</div>
              <div class="stat-label">标签数量</div>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="content-row">
      <el-col :span="16">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>机器状态概览</span>
              <el-button type="primary" size="small" @click="goToMachines">
                查看全部
              </el-button>
            </div>
          </template>
          <el-table :data="recentMachines" style="width: 100%">
            <el-table-column prop="name" label="机器名称" width="150" />
            <el-table-column prop="hostname" label="主机地址" width="150" />
            <el-table-column label="状态" width="100">
              <template #default="{ row }">
                <el-tag :type="getStatusType(row.status)">
                  {{ getStatusText(row.status) }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="资源使用" min-width="200">
              <template #default="{ row }">
                <div class="resource-bar">
                  <span class="resource-label">CPU</span>
                  <el-progress
                    :percentage="row.cpu_usage || 0"
                    :color="getProgressColor(row.cpu_usage)"
                    :stroke-width="8"
                  />
                </div>
                <div class="resource-bar">
                  <span class="resource-label">内存</span>
                  <el-progress
                    :percentage="row.memory_usage || 0"
                    :color="getProgressColor(row.memory_usage)"
                    :stroke-width="8"
                  />
                </div>
              </template>
            </el-table-column>
            <el-table-column prop="environment" label="环境" width="100">
              <template #default="{ row }">
                <el-tag v-if="row.environment" size="small">{{ row.environment }}</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <template #header>
            <span>快捷操作</span>
          </template>
          <div class="quick-actions">
            <el-button type="primary" @click="goToMachines" class="action-btn">
              <el-icon><Plus /></el-icon>
              新增机器
            </el-button>
            <el-button @click="goToTags" class="action-btn">
              <el-icon><PriceTag /></el-icon>
              管理标签
            </el-button>
            <el-button @click="goToGroups" class="action-btn">
              <el-icon><Folder /></el-icon>
              管理分组
            </el-button>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { Monitor, CircleCheck, CircleClose, PriceTag, Plus, Folder } from '@element-plus/icons-vue'
import { machineApi } from '@/api/machine'
import { tagApi } from '@/api/tag'
import type { Machine, MachineStatus } from '@/types/machine'

const router = useRouter()

const machineStats = ref({
  total: 0,
  online: 0,
  offline: 0
})

const tagCount = ref(0)
const recentMachines = ref<Machine[]>([])

const loadStats = async () => {
  try {
    const res = await machineApi.getMachines({ page_size: 100 })
    machineStats.value.total = res.total
    machineStats.value.online = res.data.filter(m => m.status === 'online').length
    machineStats.value.offline = res.data.filter(m => m.status === 'offline').length
    recentMachines.value = res.data.slice(0, 5)
  } catch (error) {
    console.error('加载机器统计失败:', error)
  }

  try {
    const tags = await tagApi.getTags()
    tagCount.value = tags.length
  } catch (error) {
    console.error('加载标签统计失败:', error)
  }
}

const getStatusType = (status: MachineStatus) => {
  const map: Record<MachineStatus, string> = {
    online: 'success',
    offline: 'danger',
    maintenance: 'warning'
  }
  return map[status] || 'info'
}

const getStatusText = (status: MachineStatus) => {
  const map: Record<MachineStatus, string> = {
    online: '在线',
    offline: '离线',
    maintenance: '维护中'
  }
  return map[status] || '未知'
}

const getProgressColor = (value?: number) => {
  if (!value) return '#e6e6e6'
  if (value < 50) return '#67c23a'
  if (value < 80) return '#e6a23c'
  return '#f56c6c'
}

const goToMachines = () => router.push('/machines')
const goToTags = () => router.push('/tags')
const goToGroups = () => router.push('/groups')

onMounted(() => {
  loadStats()
})
</script>

<style scoped lang="scss">
.dashboard {
  .stats-row {
    margin-bottom: 20px;
  }

  .stat-card {
    .stat-content {
      display: flex;
      align-items: center;
      gap: 15px;
    }

    .stat-icon {
      width: 50px;
      height: 50px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 24px;
      color: #fff;

      &.online {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
      }

      &.success {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
      }

      &.warning {
        background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);
      }

      &.primary {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
      }
    }

    .stat-info {
      .stat-value {
        font-size: 28px;
        font-weight: bold;
        color: #303133;
      }

      .stat-label {
        font-size: 14px;
        color: #909399;
      }
    }
  }

  .content-row {
    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }

    .resource-bar {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 8px;

      &:last-child {
        margin-bottom: 0;
      }

      .resource-label {
        width: 40px;
        font-size: 12px;
        color: #606266;
      }
    }

    .quick-actions {
      display: flex;
      flex-direction: column;
      gap: 12px;

      .action-btn {
        width: 100%;
        justify-content: flex-start;
      }
    }
  }
}
</style>

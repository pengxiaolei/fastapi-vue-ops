<template>
  <div class="machines-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>机器管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增机器
          </el-button>
        </div>
      </template>

      <div class="search-bar">
        <el-input
          v-model="searchForm.keyword"
          placeholder="搜索机器名称/主机地址"
          clearable
          style="width: 250px"
          @keyup.enter="loadMachines"
        />
        <el-select
          v-model="searchForm.status"
          placeholder="选择状态"
          clearable
          style="width: 120px"
        >
          <el-option label="在线" value="online" />
          <el-option label="离线" value="offline" />
          <el-option label="维护中" value="maintenance" />
        </el-select>
        <el-select
          v-model="searchForm.environment"
          placeholder="选择环境"
          clearable
          style="width: 120px"
        >
          <el-option label="开发" value="dev" />
          <el-option label="测试" value="test" />
          <el-option label="生产" value="prod" />
        </el-select>
        <el-button type="primary" @click="loadMachines">
          <el-icon><Search /></el-icon>
          搜索
        </el-button>
        <el-button @click="resetSearch">重置</el-button>
      </div>

      <el-table
        v-loading="loading"
        :data="machineList"
        style="width: 100%"
        @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="name" label="机器名称" min-width="120" />
        <el-table-column prop="hostname" label="主机地址" width="150" />
        <el-table-column prop="port" label="端口" width="80" />
        <el-table-column prop="username" label="用户名" width="100" />
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="getStatusType(row.status)">
              {{ getStatusText(row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="资源使用" min-width="200">
          <template #default="{ row }">
            <div class="resource-item">
              <span>CPU:</span>
              <el-progress
                :percentage="row.cpu_usage || 0"
                :color="getProgressColor(row.cpu_usage)"
                :stroke-width="6"
              />
            </div>
            <div class="resource-item">
              <span>内存:</span>
              <el-progress
                :percentage="row.memory_usage || 0"
                :color="getProgressColor(row.memory_usage)"
                :stroke-width="6"
              />
            </div>
          </template>
        </el-table-column>
        <el-table-column label="标签" min-width="150">
          <template #default="{ row }">
            <el-tag
              v-for="tag in row.tags"
              :key="tag.id"
              size="small"
              :style="{ backgroundColor: tag.color + '20', color: tag.color, borderColor: tag.color }"
              class="machine-tag"
            >
              {{ tag.name }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="environment" label="环境" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.environment" size="small" type="info">
              {{ getEnvironmentText(row.environment) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="last_heartbeat" label="最后心跳" width="160">
          <template #default="{ row }">
            {{ row.last_heartbeat ? formatDate(row.last_heartbeat) : '-' }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" link @click="handleView(row)">
              详情
            </el-button>
            <el-button type="primary" size="small" link @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button type="success" size="small" link @click="handleRefresh(row)">
              刷新状态
            </el-button>
            <el-button type="warning" size="small" link @click="handleTestConnection(row)">
              测试连接
            </el-button>
            <el-button type="danger" size="small" link @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.page_size"
          :page-sizes="[10, 20, 50, 100]"
          :total="pagination.total"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="loadMachines"
          @current-change="loadMachines"
        />
      </div>
    </el-card>

    <MachineForm
      v-model:visible="dialogVisible"
      :machine="currentMachine"
      @success="handleFormSuccess"
    />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Search } from '@element-plus/icons-vue'
import { machineApi } from '@/api/machine'
import type { Machine, MachineStatus } from '@/types/machine'
import MachineForm from './components/MachineForm.vue'

const router = useRouter()

const loading = ref(false)
const machineList = ref<Machine[]>([])
const dialogVisible = ref(false)
const currentMachine = ref<Machine | null>(null)

const searchForm = reactive({
  keyword: '',
  status: '',
  environment: ''
})

const pagination = reactive({
  page: 1,
  page_size: 20,
  total: 0
})

const loadMachines = async () => {
  loading.value = true
  console.log('🔄 开始加载机器列表...')
  try {
    const params = {
      page: pagination.page,
      page_size: pagination.page_size,
      keyword: searchForm.keyword || undefined,
      status: searchForm.status || undefined,
      environment: searchForm.environment || undefined
    }
    const res = await machineApi.getMachines(params)
    console.log('✅ 机器列表加载成功:', res)
    machineList.value = res.data
    pagination.total = res.total
    ElMessage.success(`加载成功，共 ${res.total} 台机器`)
  } catch (error) {
    console.error('❌ 机器列表加载失败:', error)
    ElMessage.error('加载机器列表失败')
  } finally {
    loading.value = false
  }
}

const resetSearch = () => {
  searchForm.keyword = ''
  searchForm.status = ''
  searchForm.environment = ''
  pagination.page = 1
  loadMachines()
}

const handleAdd = () => {
  currentMachine.value = null
  dialogVisible.value = true
}

const handleEdit = (row: Machine) => {
  currentMachine.value = row
  dialogVisible.value = true
}

const handleView = (row: Machine) => {
  router.push(`/machines/${row.id}`)
}

const handleRefresh = async (row: Machine) => {
  try {
    await machineApi.refreshMachineStatus(row.id)
    ElMessage.success('状态刷新成功')
    loadMachines()
  } catch (error) {
    ElMessage.error('状态刷新失败')
  }
}

const handleTestConnection = async (row: Machine) => {
  try {
    const res = await machineApi.testMachineConnection(row.id)
    if (res.success) {
      ElMessage.success('连接测试成功')
    } else {
      ElMessage.error(`连接测试失败: ${res.message}`)
    }
  } catch (error) {
    ElMessage.error('连接测试失败')
  }
}

const handleDelete = async (row: Machine) => {
  try {
    await ElMessageBox.confirm(`确定要删除机器"${row.name}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await machineApi.deleteMachine(row.id)
    ElMessage.success('删除成功')
    loadMachines()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const handleFormSuccess = () => {
  dialogVisible.value = false
  loadMachines()
}

const handleSelectionChange = (selection: Machine[]) => {
  console.log('Selected:', selection)
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

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  loadMachines()
})
</script>

<style scoped lang="scss">
.machines-page {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .search-bar {
    display: flex;
    gap: 10px;
    margin-bottom: 20px;
    flex-wrap: wrap;
  }

  .resource-item {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 5px;

    &:last-child {
      margin-bottom: 0;
    }

    span {
      width: 40px;
      font-size: 12px;
      color: #606266;
    }
  }

  .machine-tag {
    margin-right: 5px;
    margin-bottom: 5px;
  }

  .pagination {
    margin-top: 20px;
    display: flex;
    justify-content: flex-end;
  }
}
</style>

<template>
  <div class="dashboard-page">
    <el-card shadow="never">
      <template #header>
        <div class="card-header">
          <span>数据概览</span>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
              <el-icon :size="30"><Monitor /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.machineCount }}</div>
              <div class="stat-label">机器总数</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
              <el-icon :size="30"><CircleCheck /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.onlineCount }}</div>
              <div class="stat-label">在线机器</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);">
              <el-icon :size="30"><CircleClose /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.offlineCount }}</div>
              <div class="stat-label">离线机器</div>
            </div>
          </el-card>
        </el-col>
        <el-col :span="6">
          <el-card class="stat-card">
            <div class="stat-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
              <el-icon :size="30"><PriceTag /></el-icon>
            </div>
            <div class="stat-content">
              <div class="stat-value">{{ stats.tagCount }}</div>
              <div class="stat-label">标签数量</div>
            </div>
          </el-card>
        </el-col>
      </el-row>

      <el-divider />

      <el-alert
        title="欢迎使用 DevOps 运维管理平台"
        type="info"
        :closable="false"
        show-icon
      >
        <template #default>
          <p>左侧 TAB 页功能说明：</p>
          <ul style="margin-top: 10px; padding-left: 20px;">
            <li><strong>机器管理</strong>：查看和管理所有服务器，支持 SSH 连接、状态监控、标签分组</li>
            <li><strong>数据概览</strong>：平台数据统计和可视化展示</li>
            <li><strong>系统设置</strong>：系统配置和参数设置</li>
            <li><strong>文件管理</strong>：文件上传、下载和管理</li>
          </ul>
        </template>
      </el-alert>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { Monitor, CircleCheck, CircleClose, PriceTag } from '@element-plus/icons-vue'
import { machineApi } from '@/api/machine'
import { tagApi } from '@/api/tag'

const stats = ref({
  machineCount: 0,
  onlineCount: 0,
  offlineCount: 0,
  tagCount: 0
})

const loadStats = async () => {
  try {
    const res = await machineApi.getMachines({ page: 1, page_size: 1000 })
    stats.value.machineCount = res.total
    stats.value.onlineCount = res.data.filter((m: any) => m.status === 'online').length
    stats.value.offlineCount = res.data.filter((m: any) => m.status === 'offline').length
  } catch (error) {
    console.error('加载机器统计失败:', error)
  }

  try {
    const tags = await tagApi.getTags()
    stats.value.tagCount = tags.length
  } catch (error) {
    console.error('加载标签统计失败:', error)
  }
}

onMounted(() => {
  loadStats()
})
</script>

<style scoped lang="scss">
.dashboard-page {
  .card-header {
    font-size: 18px;
    font-weight: 600;
    color: #303133;
  }

  .stat-card {
    display: flex;
    align-items: center;
    gap: 16px;

    .stat-icon {
      width: 60px;
      height: 60px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
    }

    .stat-content {
      .stat-value {
        font-size: 28px;
        font-weight: bold;
        color: #303133;
        margin-bottom: 4px;
      }

      .stat-label {
        font-size: 14px;
        color: #909399;
      }
    }
  }
}
</style>

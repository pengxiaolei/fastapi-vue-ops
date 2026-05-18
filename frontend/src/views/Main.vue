<template>
  <div class="main-page">
    <el-container>
      <!-- 顶部导航栏 -->
      <el-header class="top-header">
        <div class="header-content">
          <div class="logo-section">
            <el-icon class="logo-icon"><Monitor /></el-icon>
            <span class="app-title">DevOps 运维管理平台</span>
          </div>
          <div class="header-right">
            <el-avatar :size="32" icon="UserFilled" />
            <span class="username">管理员</span>
          </div>
        </div>
      </el-header>

      <el-container>
        <!-- 左侧 TAB 区域 -->
        <el-aside width="200px" class="left-aside">
          <div class="tab-container">
            <div
              v-for="tab in tabs"
              :key="tab.key"
              :class="['tab-item', { active: activeTab === tab.key }]"
              @click="switchTab(tab.key)"
            >
              <el-icon class="tab-icon">
                <component :is="tab.icon" />
              </el-icon>
              <span class="tab-label">{{ tab.label }}</span>
            </div>
          </div>
        </el-aside>

        <!-- 右侧内容区域 -->
        <el-main class="content-area">
          <router-view v-slot="{ Component }">
            <transition name="fade-transform" mode="out-in">
              <component :is="Component" />
            </transition>
          </router-view>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { Monitor, Setting, DataLine, Folder } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()

const tabs = [
  { key: 'machines', label: '机器管理', icon: Monitor, path: '/machines' },
  { key: 'dashboard', label: '数据概览', icon: DataLine, path: '/dashboard' },
  { key: 'settings', label: '系统设置', icon: Setting, path: '/settings' },
  { key: 'files', label: '文件管理', icon: Folder, path: '/files' }
]

const activeTab = ref('machines')

const switchTab = (key: string) => {
  const tab = tabs.find(t => t.key === key)
  if (tab) {
    activeTab.value = key
    router.push(tab.path)
  }
}

onMounted(() => {
  // 根据当前路由设置激活的TAB
  const currentPath = route.path
  const currentTab = tabs.find(t => currentPath.startsWith(t.path))
  if (currentTab) {
    activeTab.value = currentTab.key
  }
})
</script>

<style scoped lang="scss">
.main-page {
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.top-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 0;
  height: 60px;

  .header-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 100%;
    padding: 0 20px;

    .logo-section {
      display: flex;
      align-items: center;
      gap: 12px;
      color: white;

      .logo-icon {
        font-size: 28px;
      }

      .app-title {
        font-size: 20px;
        font-weight: 600;
        letter-spacing: 1px;
      }
    }

    .header-right {
      display: flex;
      align-items: center;
      gap: 10px;
      color: white;

      .username {
        font-size: 14px;
      }
    }
  }
}

.left-aside {
  background-color: #f5f7fa;
  border-right: 1px solid #e4e7ed;
  padding: 10px 0;

  .tab-container {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 0 8px;

    .tab-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 14px 16px;
      border-radius: 8px;
      cursor: pointer;
      transition: all 0.3s ease;
      color: #606266;

      &:hover {
        background-color: #e9e9eb;
        color: #303133;
      }

      &.active {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
      }

      .tab-icon {
        font-size: 20px;
      }

      .tab-label {
        font-size: 14px;
        font-weight: 500;
      }
    }
  }
}

.content-area {
  background-color: #f0f2f5;
  padding: 20px;
  overflow-y: auto;
}
</style>

<style>
.fade-transform-enter-active,
.fade-transform-leave-active {
  transition: all 0.3s ease;
}

.fade-transform-enter-from {
  opacity: 0;
  transform: translateX(20px);
}

.fade-transform-leave-to {
  opacity: 0;
  transform: translateX(-20px);
}
</style>

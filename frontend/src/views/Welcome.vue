<template>
  <div class="welcome-page">
    <div class="welcome-container">
      <!-- Logo 区域 -->
      <div class="logo-section">
        <div class="logo-icon">
          <el-icon :size="80"><Monitor /></el-icon>
        </div>
        <h1 class="app-title">DevOps 运维管理平台</h1>
        <p class="app-subtitle">简洁 · 高效 · 安全</p>
      </div>

      <!-- 功能卡片 -->
      <div class="features-section">
        <div class="feature-card" @click="goToPage('/machines')">
          <div class="feature-icon" style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);">
            <el-icon :size="32"><Connection /></el-icon>
          </div>
          <h3>机器管理</h3>
          <p>服务器资产统一管理，SSH 远程连接，状态实时监控</p>
        </div>
        <div class="feature-card" @click="goToPage('/dashboard')">
          <div class="feature-icon" style="background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);">
            <el-icon :size="32"><DataLine /></el-icon>
          </div>
          <h3>数据概览</h3>
          <p>资源使用情况统计，服务器状态一目了然</p>
        </div>
        <div class="feature-card" @click="goToPage('/files')">
          <div class="feature-icon" style="background: linear-gradient(135deg, #eb3349 0%, #f45c43 100%);">
            <el-icon :size="32"><FolderOpened /></el-icon>
          </div>
          <h3>文件管理</h3>
          <p>文件上传下载，远程文件管理（开发中）</p>
        </div>
        <div class="feature-card" @click="goToPage('/settings')">
          <div class="feature-icon" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);">
            <el-icon :size="32"><Setting /></el-icon>
          </div>
          <h3>系统设置</h3>
          <p>系统配置管理，个性化设置</p>
        </div>
      </div>

      <!-- 底部信息 -->
      <div class="footer-section">
        <el-tag type="info" size="large">
          <el-icon><Star /></el-icon>
          欢迎使用 DevOps 运维管理平台
        </el-tag>
        <p class="version-info">版本 v1.0.0</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import { onMounted } from 'vue'
import { Monitor, Connection, DataLine, FolderOpened, Setting, Star } from '@element-plus/icons-vue'

const router = useRouter()

const goToPage = (path: string) => {
  router.push(path)
}

// 页面加载后自动跳转到机器管理
onMounted(() => {
  console.log('🏠 欢迎页面已加载，自动跳转到机器管理')
  router.push('/machines')
})
</script>

<style scoped lang="scss">
.welcome-page {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 40px;
  overflow: auto;
}

.welcome-container {
  max-width: 1200px;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 60px;
}

.logo-section {
  text-align: center;
  color: white;

  .logo-icon {
    width: 120px;
    height: 120px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    margin: 0 auto 20px;
    backdrop-filter: blur(10px);
    animation: float 3s ease-in-out infinite;
  }

  .app-title {
    font-size: 48px;
    font-weight: 700;
    margin: 0 0 12px 0;
    text-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
  }

  .app-subtitle {
    font-size: 20px;
    opacity: 0.9;
    margin: 0;
    letter-spacing: 4px;
  }
}

.features-section {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 24px;
  width: 100%;
  max-width: 1000px;

  .feature-card {
    background: rgba(255, 255, 255, 0.95);
    border-radius: 16px;
    padding: 32px 24px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    backdrop-filter: blur(10px);

    &:hover {
      transform: translateY(-8px);
      box-shadow: 0 16px 48px rgba(0, 0, 0, 0.2);
    }

    .feature-icon {
      width: 72px;
      height: 72px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      margin: 0 auto 20px;
    }

    h3 {
      font-size: 20px;
      font-weight: 600;
      color: #303133;
      margin: 0 0 12px 0;
    }

    p {
      font-size: 14px;
      color: #606266;
      margin: 0;
      line-height: 1.6;
    }
  }
}

.footer-section {
  text-align: center;
  color: white;

  .el-tag {
    font-size: 16px;
    padding: 8px 20px;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.2);
    border: none;
    color: white;
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 12px;
  }

  .version-info {
    font-size: 14px;
    opacity: 0.8;
    margin: 0;
  }
}

@keyframes float {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

/* 响应式适配 */
@media (max-width: 768px) {
  .welcome-page {
    padding: 20px;
  }

  .welcome-container {
    gap: 40px;
  }

  .logo-section {
    .logo-icon {
      width: 80px;
      height: 80px;
    }

    .app-title {
      font-size: 32px;
    }

    .app-subtitle {
      font-size: 16px;
    }
  }

  .features-section {
    grid-template-columns: 1fr;
    gap: 16px;
  }
}
</style>

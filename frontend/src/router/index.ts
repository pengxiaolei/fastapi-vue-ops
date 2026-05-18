import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import Welcome from '@/views/Welcome.vue'
import Main from '@/views/Main.vue'

const routes: RouteRecordRaw[] = [
  // 欢迎页面 - 首页
  {
    path: '/',
    name: 'Welcome',
    component: Welcome,
    meta: { title: '欢迎' }
  },
  // 主界面 - 带侧边栏
  {
    path: '/',
    component: Main,
    children: [
      {
        path: 'machines',
        name: 'Machines',
        component: () => import('@/views/machines/index.vue'),
        meta: { title: '机器管理' }
      },
      {
        path: 'machines/:id',
        name: 'MachineDetail',
        component: () => import('@/views/machines/detail.vue'),
        meta: { title: '机器详情', hidden: true }
      },
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '数据概览' }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/settings/index.vue'),
        meta: { title: '系统设置' }
      },
      {
        path: 'files',
        name: 'Files',
        component: () => import('@/views/files/index.vue'),
        meta: { title: '文件管理' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// 页面标题
router.beforeEach((to, from, next) => {
  if (to.meta.title) {
    document.title = `${to.meta.title} - DevOps 运维管理平台`
  } else {
    document.title = 'DevOps 运维管理平台'
  }
  next()
})

export default router

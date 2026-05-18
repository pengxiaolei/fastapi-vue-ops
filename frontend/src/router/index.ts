import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'
import Main from '@/views/Main.vue'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: Main,
    redirect: '/machines',
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

export default router

import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('@/layout/index.vue'),
    redirect: '/dashboard',
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/dashboard/index.vue'),
        meta: { title: '仪表盘', icon: 'Odometer' }
      },
      {
        path: 'machines',
        name: 'Machines',
        component: () => import('@/views/machines/index.vue'),
        meta: { title: '机器管理', icon: 'Monitor' }
      },
      {
        path: 'machines/:id',
        name: 'MachineDetail',
        component: () => import('@/views/machines/detail.vue'),
        meta: { title: '机器详情', icon: 'Monitor', hidden: true }
      },
      {
        path: 'tags',
        name: 'Tags',
        component: () => import('@/views/tags/index.vue'),
        meta: { title: '标签管理', icon: 'PriceTag' }
      },
      {
        path: 'groups',
        name: 'Groups',
        component: () => import('@/views/groups/index.vue'),
        meta: { title: '分组管理', icon: 'Folder' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

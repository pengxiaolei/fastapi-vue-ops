import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    component: () => import('@/layout/index.vue'),
    redirect: '/machines',
    children: [
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
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router

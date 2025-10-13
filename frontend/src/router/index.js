import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: Home
    },
    {
      path: '/schedule',
      name: 'schedule',
      component: () => import('../views/Schedule.vue')
    },
    // 新增搜索结果页的路由
    {
      path: '/search-results/:query',
      name: 'search-results',
      component: () => import('../views/SearchResults.vue'),
      props: true
    },
    {
      path: '/team/:teamName',
      name: 'team-detail',
      component: () => import('../views/TeamDetail.vue'),
      props: true
    },
    {
      path: '/player/:playerId',
      name: 'player-detail',
      component: () => import('../views/PlayerDetail.vue'),
      props: true
    },
  ]
})

export default router
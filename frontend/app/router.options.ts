import type { RouterConfig } from '@nuxt/schema'

// https://router.vuejs.org/api/interfaces/routeroptions.html
export default <RouterConfig> {
  routes: (_routes) => [
    {
      name: 'home',
      path: '/',
      component: () => import('~/pages/homepage.vue').then(r => r.default || r)
    },
    {
      name: 'event-dashboard',
      path: '/event-dashboard',
      component: () => import('~/pages/EventsDashboard.vue').then(r => r.default || r)
    },
    {
      name: 'login',
      path: '/login',
      component: () => import('~/pages/login.vue').then(r => r.default || r)
    },
    {
      name: 'tos',
      path: '/terms-of-service',
      component: () => import('~/pages/TOS.vue').then(r => r.default || r)
    },
    {
      name: 'user',
      path: '/user',
      component: () => import('~/pages/User.vue').then(r => r.default || r)
    },
    {
      name: 'Sign Up',
      path: '/signup',
      component: () => import('~/pages/signup.vue').then(r => r.default || r)
    }
  ],
  
}
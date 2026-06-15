import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import Login from '../views/Login.vue'
import Layout from '../views/Layout.vue'
import Dashboard from '../views/Dashboard.vue'
import Users from '../views/Users.vue'
import Roles from '../views/Roles.vue'
import Permissions from '../views/Permissions.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/login', component: Login },
    {
      path: '/',
      component: Layout,
      children: [
        { path: '', component: Dashboard },
        { path: 'users', component: Users, meta: { permission: 'user:read' } },
        { path: 'roles', component: Roles, meta: { permission: 'role:read' } },
        { path: 'permissions', component: Permissions, meta: { permission: 'permission:read' } }
      ]
    }
  ]
})

router.beforeEach(async (to) => {
  const auth = useAuthStore()
  if (to.path === '/login') return true
  if (!auth.token) return '/login'
  if (!auth.user) await auth.loadProfile()
  if (to.meta.permission && !auth.has(to.meta.permission)) return '/'
  return true
})

export default router

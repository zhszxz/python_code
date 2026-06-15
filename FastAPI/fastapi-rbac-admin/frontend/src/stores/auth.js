import { defineStore } from 'pinia'
import { loginApi, meApi } from '../api/rbac'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('rbac_token') || '',
    user: null,
    permissions: []
  }),
  actions: {
    async login(form) {
      const res = await loginApi(form)
      this.token = res.data.access_token
      localStorage.setItem('rbac_token', this.token)
      await this.loadProfile()
    },
    async loadProfile() {
      const res = await meApi()
      this.user = res.data
      this.permissions = res.data.permissions || []
    },
    has(code) {
      return this.permissions.includes(code)
    },
    logout() {
      this.token = ''
      this.user = null
      this.permissions = []
      localStorage.removeItem('rbac_token')
    }
  }
})

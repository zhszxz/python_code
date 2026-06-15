<template>
  <el-container class="layout">
    <el-aside width="220px">
      <div class="brand">RBAC Admin</div>
      <el-menu router :default-active="$route.path">
        <el-menu-item index="/">
          <el-icon><House /></el-icon><span>控制台</span>
        </el-menu-item>
        <el-menu-item v-if="auth.has('user:read')" index="/users">
          <el-icon><User /></el-icon><span>用户管理</span>
        </el-menu-item>
        <el-menu-item v-if="auth.has('role:read')" index="/roles">
          <el-icon><UserFilled /></el-icon><span>角色管理</span>
        </el-menu-item>
        <el-menu-item v-if="auth.has('permission:read')" index="/permissions">
          <el-icon><Key /></el-icon><span>权限管理</span>
        </el-menu-item>
      </el-menu>
    </el-aside>
    <el-container>
      <el-header>
        <span>{{ auth.user?.nickname }}</span>
        <el-button text @click="logout">退出</el-button>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup>
import { House, Key, User, UserFilled } from '@element-plus/icons-vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

function logout() {
  auth.logout()
  router.push('/login')
}
</script>

<style scoped>
.layout {
  min-height: 100vh;
}

.brand {
  height: 60px;
  display: flex;
  align-items: center;
  padding-left: 20px;
  font-size: 18px;
  font-weight: 700;
  color: #0f172a;
  border-bottom: 1px solid #e5e7eb;
}

.el-aside {
  background: #fff;
  border-right: 1px solid #e5e7eb;
}

.el-menu {
  border-right: 0;
}

.el-header {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  gap: 16px;
  background: #fff;
  border-bottom: 1px solid #e5e7eb;
}
</style>

<template>
  <section class="page">
    <el-row :gutter="16">
      <el-col :span="8">
        <el-card shadow="never">
          <template #header>当前用户</template>
          <p>{{ auth.user?.username }} / {{ auth.user?.nickname }}</p>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="never">
          <template #header>角色</template>
          <el-tag v-for="role in auth.user?.roles || []" :key="role.id">{{ role.label }}</el-tag>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card shadow="never">
          <template #header>权限数量</template>
          <strong>{{ auth.permissions.length }}</strong>
        </el-card>
      </el-col>
    </el-row>
  </section>
</template>

<script setup>
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
</script>

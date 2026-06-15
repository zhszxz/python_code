<template>
  <main class="login-page">
    <section class="login-panel">
      <h1>FastAPI RBAC Admin</h1>
      <p>使用演示账号登录后台</p>
      <el-form :model="form" label-position="top" @keyup.enter="submit">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="admin / editor / viewer" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" show-password placeholder="admin123" />
        </el-form-item>
        <el-button type="primary" :loading="loading" class="login-button" @click="submit">登录</el-button>
      </el-form>
      <div class="demo">admin/admin123　editor/editor123　viewer/viewer123</div>
    </section>
  </main>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const auth = useAuthStore()
const loading = ref(false)
const form = reactive({ username: 'admin', password: 'admin123' })

async function submit() {
  loading.value = true
  try {
    await auth.login(form)
    router.push('/')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: grid;
  place-items: center;
  background: linear-gradient(135deg, #e8f4ff, #f9fbff 50%, #eef7f1);
}

.login-panel {
  width: min(420px, calc(100vw - 32px));
  padding: 32px;
  background: #fff;
  border: 1px solid #dbe4ef;
  border-radius: 8px;
  box-shadow: 0 16px 50px rgba(15, 23, 42, 0.12);
}

h1 {
  margin: 0 0 8px;
  font-size: 28px;
}

p {
  margin: 0 0 24px;
  color: #64748b;
}

.login-button {
  width: 100%;
}

.demo {
  margin-top: 18px;
  color: #64748b;
  font-size: 13px;
}
</style>

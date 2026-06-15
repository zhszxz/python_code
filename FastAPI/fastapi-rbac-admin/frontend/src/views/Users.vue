<template>
  <section class="page">
    <div class="toolbar">
      <h2>用户管理</h2>
      <el-button v-if="auth.has('user:create')" type="primary" @click="openCreate">新增用户</el-button>
    </div>
    <el-table :data="rows" border>
      <el-table-column prop="id" label="ID" width="70" />
      <el-table-column prop="username" label="用户名" />
      <el-table-column prop="nickname" label="昵称" />
      <el-table-column label="角色">
        <template #default="{ row }">
          <el-tag v-for="role in row.roles" :key="role.id" class="tag">{{ role.label }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="90">
        <template #default="{ row }">
          <el-tag :type="row.is_active ? 'success' : 'danger'">{{ row.is_active ? '启用' : '禁用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button v-if="auth.has('user:update')" size="small" @click="openEdit(row)">编辑</el-button>
          <el-button v-if="auth.has('user:delete')" size="small" type="danger" @click="remove(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog v-model="visible" :title="form.id ? '编辑用户' : '新增用户'" width="520px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="用户名"><el-input v-model="form.username" :disabled="!!form.id" /></el-form-item>
        <el-form-item label="昵称"><el-input v-model="form.nickname" /></el-form-item>
        <el-form-item label="密码"><el-input v-model="form.password" type="password" show-password /></el-form-item>
        <el-form-item label="启用"><el-switch v-model="form.is_active" /></el-form-item>
        <el-form-item label="角色">
          <el-select v-model="form.role_ids" multiple style="width: 100%">
            <el-option v-for="role in roles" :key="role.id" :label="role.label" :value="role.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer><el-button @click="visible = false">取消</el-button><el-button type="primary" @click="save">保存</el-button></template>
    </el-dialog>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessageBox } from 'element-plus'
import { createUser, deleteUser, getRoles, getUsers, updateUser } from '../api/rbac'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const rows = ref([])
const roles = ref([])
const visible = ref(false)
const form = reactive({ id: null, username: '', nickname: '', password: '', is_active: true, role_ids: [] })

async function load() {
  rows.value = (await getUsers()).data
  roles.value = (await getRoles()).data
}
function openCreate() {
  Object.assign(form, { id: null, username: '', nickname: '', password: '123456', is_active: true, role_ids: [] })
  visible.value = true
}
function openEdit(row) {
  Object.assign(form, { id: row.id, username: row.username, nickname: row.nickname, password: '', is_active: row.is_active, role_ids: row.roles.map((r) => r.id) })
  visible.value = true
}
async function save() {
  const data = { nickname: form.nickname, is_active: form.is_active, role_ids: form.role_ids }
  if (form.password) data.password = form.password
  if (form.id) await updateUser(form.id, data)
  else await createUser({ ...data, username: form.username, password: form.password || '123456' })
  visible.value = false
  await load()
}
async function remove(row) {
  await ElMessageBox.confirm(`确认删除用户 ${row.username}？`, '提示')
  await deleteUser(row.id)
  await load()
}
onMounted(load)
</script>

<style scoped>
.tag {
  margin-right: 6px;
}
</style>

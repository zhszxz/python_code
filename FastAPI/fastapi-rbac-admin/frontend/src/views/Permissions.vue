<template>
  <section class="page">
    <div class="toolbar">
      <h2>权限管理</h2>
      <el-button v-if="auth.has('permission:create')" type="primary" @click="openCreate">新增权限</el-button>
    </div>
    <el-table :data="rows" border>
      <el-table-column prop="code" label="权限标识" />
      <el-table-column prop="name" label="权限名称" />
      <el-table-column prop="group" label="分组" />
      <el-table-column prop="description" label="说明" />
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button v-if="auth.has('permission:update')" size="small" @click="openEdit(row)">编辑</el-button>
          <el-button v-if="auth.has('permission:delete')" size="small" type="danger" @click="remove(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog v-model="visible" :title="form.id ? '编辑权限' : '新增权限'" width="520px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="权限标识"><el-input v-model="form.code" :disabled="!!form.id" /></el-form-item>
        <el-form-item label="权限名称"><el-input v-model="form.name" /></el-form-item>
        <el-form-item label="分组"><el-input v-model="form.group" /></el-form-item>
        <el-form-item label="说明"><el-input v-model="form.description" /></el-form-item>
      </el-form>
      <template #footer><el-button @click="visible = false">取消</el-button><el-button type="primary" @click="save">保存</el-button></template>
    </el-dialog>
  </section>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessageBox } from 'element-plus'
import { createPermission, deletePermission, getPermissions, updatePermission } from '../api/rbac'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const rows = ref([])
const visible = ref(false)
const form = reactive({ id: null, code: '', name: '', group: '', description: '' })

async function load() {
  rows.value = (await getPermissions()).data
}
function openCreate() {
  Object.assign(form, { id: null, code: '', name: '', group: '自定义权限', description: '' })
  visible.value = true
}
function openEdit(row) {
  Object.assign(form, row)
  visible.value = true
}
async function save() {
  const data = { name: form.name, group: form.group, description: form.description }
  if (form.id) await updatePermission(form.id, data)
  else await createPermission({ ...data, code: form.code })
  visible.value = false
  await load()
}
async function remove(row) {
  await ElMessageBox.confirm(`确认删除权限 ${row.code}？`, '提示')
  await deletePermission(row.id)
  await load()
}
onMounted(load)
</script>

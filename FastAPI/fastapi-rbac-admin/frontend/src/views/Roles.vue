<template>
  <section class="page">
    <div class="toolbar">
      <h2>角色管理</h2>
      <el-button v-if="auth.has('role:create')" type="primary" @click="openCreate">新增角色</el-button>
    </div>
    <el-table :data="rows" border>
      <el-table-column prop="name" label="角色编码" />
      <el-table-column prop="label" label="角色名称" />
      <el-table-column prop="description" label="说明" />
      <el-table-column label="权限">
        <template #default="{ row }"><span>{{ row.permissions.length }} 项</span></template>
      </el-table-column>
      <el-table-column label="操作" width="180">
        <template #default="{ row }">
          <el-button v-if="auth.has('role:update')" size="small" @click="openEdit(row)">编辑</el-button>
          <el-button v-if="auth.has('role:delete')" size="small" type="danger" @click="remove(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-dialog v-model="visible" :title="form.id ? '编辑角色' : '新增角色'" width="620px">
      <el-form :model="form" label-width="90px">
        <el-form-item label="角色编码"><el-input v-model="form.name" :disabled="!!form.id" /></el-form-item>
        <el-form-item label="角色名称"><el-input v-model="form.label" /></el-form-item>
        <el-form-item label="说明"><el-input v-model="form.description" /></el-form-item>
        <el-form-item label="权限">
          <el-select v-model="form.permission_ids" multiple filterable style="width: 100%">
            <el-option v-for="item in permissions" :key="item.id" :label="`${item.group} / ${item.name}`" :value="item.id" />
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
import { createRole, deleteRole, getPermissions, getRoles, updateRole } from '../api/rbac'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const rows = ref([])
const permissions = ref([])
const visible = ref(false)
const form = reactive({ id: null, name: '', label: '', description: '', permission_ids: [] })

async function load() {
  rows.value = (await getRoles()).data
  permissions.value = (await getPermissions()).data
}
function openCreate() {
  Object.assign(form, { id: null, name: '', label: '', description: '', permission_ids: [] })
  visible.value = true
}
function openEdit(row) {
  Object.assign(form, { id: row.id, name: row.name, label: row.label, description: row.description, permission_ids: row.permissions.map((p) => p.id) })
  visible.value = true
}
async function save() {
  const data = { label: form.label, description: form.description, permission_ids: form.permission_ids }
  if (form.id) await updateRole(form.id, data)
  else await createRole({ ...data, name: form.name })
  visible.value = false
  await load()
}
async function remove(row) {
  await ElMessageBox.confirm(`确认删除角色 ${row.label}？`, '提示')
  await deleteRole(row.id)
  await load()
}
onMounted(load)
</script>

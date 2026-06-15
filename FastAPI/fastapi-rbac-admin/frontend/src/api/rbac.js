import http from './http'

export const loginApi = (data) => http.post('/auth/login', data)
export const meApi = () => http.get('/auth/me')

export const getUsers = () => http.get('/users')
export const createUser = (data) => http.post('/users', data)
export const updateUser = (id, data) => http.put(`/users/${id}`, data)
export const deleteUser = (id) => http.delete(`/users/${id}`)

export const getRoles = () => http.get('/roles')
export const createRole = (data) => http.post('/roles', data)
export const updateRole = (id, data) => http.put(`/roles/${id}`, data)
export const deleteRole = (id) => http.delete(`/roles/${id}`)

export const getPermissions = () => http.get('/permissions')
export const createPermission = (data) => http.post('/permissions', data)
export const updatePermission = (id, data) => http.put(`/permissions/${id}`, data)
export const deletePermission = (id) => http.delete(`/permissions/${id}`)

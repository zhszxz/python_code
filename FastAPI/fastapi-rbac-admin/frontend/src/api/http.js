import axios from 'axios'
import { ElMessage } from 'element-plus'
import router from '../router'

const http = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api/v1',
  timeout: 10000
})

http.interceptors.request.use((config) => {
  const token = localStorage.getItem('rbac_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

http.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('rbac_token')
      router.push('/login')
    }
    ElMessage.error(error.response?.data?.detail || error.response?.data?.message || '请求失败')
    return Promise.reject(error)
  }
)

export default http

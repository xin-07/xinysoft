import axios from 'axios'

// 生产环境：直接请求后端地址；开发环境：通过 Vite proxy 转发
const isProd = import.meta.env.PROD
const API_BASE = isProd ? (import.meta.env.VITE_API_TARGET || 'http://127.0.0.1:8000') : ''

const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 递归遍历响应数据，将相对路径 /api/... 转为绝对 URL（生产环境需要）
function resolveRelativeUrls(data) {
  if (typeof data === 'string' && data.startsWith('/api/')) {
    return API_BASE + data
  }
  if (Array.isArray(data)) {
    return data.map(resolveRelativeUrls)
  }
  if (data && typeof data === 'object') {
    const result = {}
    for (const key of Object.keys(data)) {
      result[key] = resolveRelativeUrls(data[key])
    }
    return result
  }
  return data
}

// 响应拦截器：解包 axios response，生产环境同时转换相对路径
apiClient.interceptors.response.use(
  response => {
    const data = response.data
    return isProd ? resolveRelativeUrls(data) : data
  },
  error => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export const profileAPI = {
  // 获取个人资料
  getProfile(signal) {
    return apiClient.get('/api/profile', { signal })
  }
}

export const projectsAPI = {
  // 获取项目列表
  getProjects(params, signal) {
    return apiClient.get('/api/projects', { params, signal })
  },
  // 获取项目详情
  getProject(id, signal) {
    return apiClient.get(`/api/projects/${id}`, { signal })
  }
}

export default apiClient
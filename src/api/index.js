import axios from 'axios'

const apiClient = axios.create({
  baseURL: '',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 响应拦截器：解包 axios response，直接返回 data
apiClient.interceptors.response.use(
  response => response.data,
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
import axios from 'axios'

// 固定后备地址（方案二：当代理/主后端不可达时，直接请求此后备地址）
const FALLBACK_BASE_URL = 'http://127.0.0.1:8000'

const apiClient = axios.create({
  baseURL: '',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 响应拦截器 —— 方案二：失败时用固定后备地址重试一次
apiClient.interceptors.response.use(
  response => response.data,
  async error => {
    const config = error.config

    // 只重试一次，避免死循环
    if (!config._retried) {
      config._retried = true

      console.warn(`[API] 请求失败，尝试后备地址: ${FALLBACK_BASE_URL}`)

      const fallbackClient = axios.create({
        baseURL: FALLBACK_BASE_URL,
        timeout: 10000,
        headers: { 'Content-Type': 'application/json' }
      })

      try {
        const response = await fallbackClient.request({
          url: config.url,
          method: config.method,
          params: config.params,
          data: config.data,
          signal: config.signal
        })
        return response.data
      } catch (fallbackErr) {
        console.error('[API] 后备地址也失败:', fallbackErr.message)
        return Promise.reject(fallbackErr)
      }
    }

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
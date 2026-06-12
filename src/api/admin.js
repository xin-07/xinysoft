import apiClient from './index'

export const adminAPI = {
  // 管理员登录
  login(username, password) {
    return apiClient.post('/api/admin/login', { username, password })
  },

  // 验证 Token
  verify() {
    return apiClient.post('/api/admin/verify')
  },

  // 获取项目列表（管理端，含草稿）
  getProjects(page = 1, pageSize = 10) {
    return apiClient.get('/api/admin/projects', { params: { page, page_size: pageSize } })
  },

  // 获取项目详情（管理端）
  getProject(id) {
    return apiClient.get(`/api/admin/projects/${id}`)
  },

  // 新增项目
  createProject(data) {
    return apiClient.post('/api/admin/projects', data)
  },

  // 编辑项目
  updateProject(id, data) {
    return apiClient.put(`/api/admin/projects/${id}`, data)
  },

  // 删除项目
  deleteProject(id) {
    return apiClient.delete(`/api/admin/projects/${id}`)
  },

  // 切换项目状态
  toggleStatus(id, status) {
    return apiClient.patch(`/api/admin/projects/${id}/status`, { status })
  },

  // 获取个人资料（管理端）
  getProfile() {
    return apiClient.get('/api/admin/profile')
  },

  // 更新个人资料
  updateProfile(data) {
    return apiClient.put('/api/admin/profile', data)
  },

  // 上传文件
  uploadFile(file) {
    const formData = new FormData()
    formData.append('file', file)
    return apiClient.post('/api/admin/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  }
}

export default adminAPI
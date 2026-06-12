import { ref } from 'vue'
import { adminAPI } from '../api/admin'

const TOKEN_KEY = 'admin_token'

// 全局单例状态
const isAuthenticated = ref(false)
const token = ref(localStorage.getItem(TOKEN_KEY) || null)

export function useAdminAuth() {
  const loading = ref(false)

  function login(username, password) {
    loading.value = true
    return adminAPI.login(username, password)
      .then(res => {
        const t = res.data.token
        token.value = t
        localStorage.setItem(TOKEN_KEY, t)
        isAuthenticated.value = true
        return res
      })
      .finally(() => {
        loading.value = false
      })
  }

  function logout() {
    token.value = null
    isAuthenticated.value = false
    localStorage.removeItem(TOKEN_KEY)
  }

  function checkAuth() {
    if (!token.value) {
      isAuthenticated.value = false
      return Promise.resolve(false)
    }
    return adminAPI.verify()
      .then(() => {
        isAuthenticated.value = true
        return true
      })
      .catch(() => {
        logout()
        return false
      })
  }

  return {
    isAuthenticated,
    token,
    loading,
    login,
    logout,
    checkAuth
  }
}
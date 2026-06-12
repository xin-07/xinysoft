import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { useAdminAuth } from './composables/useAdminAuth'
import './style.css'
import './styles/admin.css'

const app = createApp(App)

app.use(router)

// 初始化鉴权状态
const { isAuthenticated, token, checkAuth, login, logout } = useAdminAuth()
app.provide('adminAuth', { isAuthenticated, token, login, logout })

// App 启动时验证 Token
checkAuth().then(() => {
  app.mount('#app')
})
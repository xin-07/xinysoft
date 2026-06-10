import { ref, watch, onMounted } from 'vue'

const THEME_STORAGE_KEY = 'xiny-theme-preference'

// 主题状态
const currentTheme = ref('dark')

// 初始化主题
const initTheme = () => {
  // 从 localStorage 读取用户偏好
  const savedTheme = localStorage.getItem(THEME_STORAGE_KEY)

  if (savedTheme && (savedTheme === 'dark' || savedTheme === 'light')) {
    currentTheme.value = savedTheme
  } else {
    // 默认暗色主题
    currentTheme.value = 'dark'
  }

  // 应用主题
  applyTheme(currentTheme.value)
}

// 应用主题到 DOM
const applyTheme = (theme) => {
  document.documentElement.setAttribute('data-theme', theme)
}

// 切换主题
const toggleTheme = () => {
  currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark'
}

// 监听主题变化，保存到 localStorage 并应用
watch(currentTheme, (newTheme) => {
  localStorage.setItem(THEME_STORAGE_KEY, newTheme)
  applyTheme(newTheme)
})

export function useTheme() {
  onMounted(() => {
    // 确保主题已初始化
    if (!document.documentElement.hasAttribute('data-theme')) {
      initTheme()
    }
  })

  return {
    currentTheme,
    toggleTheme,
    initTheme
  }
}
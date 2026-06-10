import { ref, watch, onMounted, onUnmounted } from 'vue'

const THEME_STORAGE_KEY = 'xiny-theme-preference'

// 主题状态
const currentTheme = ref('dark')

// 系统主题变化监听器引用
let systemThemeListener = null

// 缓存 MediaQueryList 对象，避免重复创建且确保 removeEventListener 能正确移除
const systemMediaQuery = window.matchMedia('(prefers-color-scheme: dark)')

// 安全读取 localStorage
const getStoredTheme = () => {
  try {
    return localStorage.getItem(THEME_STORAGE_KEY)
  } catch (e) {
    console.warn('localStorage 不可用，主题偏好将不会持久化:', e)
    return null
  }
}

// 安全写入 localStorage
const setStoredTheme = (theme) => {
  try {
    localStorage.setItem(THEME_STORAGE_KEY, theme)
  } catch (e) {
    console.warn('localStorage 不可用，主题偏好将不会持久化:', e)
  }
}

// 获取系统主题偏好
const getSystemTheme = () => {
  return systemMediaQuery.matches ? 'dark' : 'light'
}

// 应用主题到 DOM
const applyTheme = (theme) => {
  document.documentElement.setAttribute('data-theme', theme)
}

// 停止监听系统主题变化
const stopSystemThemeListener = () => {
  if (systemThemeListener) {
    systemMediaQuery.removeEventListener('change', systemThemeListener)
    systemThemeListener = null
  }
}

// 启动系统主题变化监听
const startSystemThemeListener = () => {
  // 仅当 localStorage 无记录时才监听
  const storedTheme = getStoredTheme()
  if (storedTheme) {
    return
  }

  systemThemeListener = (e) => {
    // 再次检查 localStorage 是否有记录（用户可能已手动设置）
    const currentStored = getStoredTheme()
    if (!currentStored) {
      const newTheme = e.matches ? 'dark' : 'light'
      currentTheme.value = newTheme
      applyTheme(newTheme)
    }
  }

  systemMediaQuery.addEventListener('change', systemThemeListener)
}

// 初始化主题
const initTheme = () => {
  // 从 localStorage 读取用户偏好
  const savedTheme = getStoredTheme()

  if (savedTheme && (savedTheme === 'dark' || savedTheme === 'light')) {
    currentTheme.value = savedTheme
  } else {
    // 使用系统偏好，默认暗色主题
    currentTheme.value = getSystemTheme()
  }

  // 应用主题
  applyTheme(currentTheme.value)
  
  // 启动系统主题变化监听
  startSystemThemeListener()
}

// 切换主题
const toggleTheme = () => {
  currentTheme.value = currentTheme.value === 'dark' ? 'light' : 'dark'
}

// 监听主题变化，保存到 localStorage 并应用
watch(currentTheme, (newTheme) => {
  setStoredTheme(newTheme)
  applyTheme(newTheme)
  
  // 用户手动切换主题后，停止监听系统主题变化
  stopSystemThemeListener()
})

export function useTheme() {
  onMounted(() => {
    // 确保主题已初始化
    if (!document.documentElement.hasAttribute('data-theme')) {
      initTheme()
    } else {
      // 即使主题已初始化，也需要启动系统主题监听（如果 localStorage 无记录）
      startSystemThemeListener()
    }
  })

  onUnmounted(() => {
    // 组件卸载时清理监听器
    stopSystemThemeListener()
  })

  return {
    currentTheme,
    toggleTheme,
    initTheme
  }
}
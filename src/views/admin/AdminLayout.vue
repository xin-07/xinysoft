<script setup>
import { ref, inject, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter, useRoute, RouterView } from 'vue-router'
import AdminToast from '../../components/admin/AdminToast.vue'
import { adminAPI } from '../../api/admin'
import { useTheme } from '../../composables/useTheme'

const router = useRouter()
const route = useRoute()
const adminAuth = inject('adminAuth', null)

const sidebarOpen = ref(false)
const sidebarCollapsed = ref(true)
const adminName = ref('管理员')
const windowWidth = ref(window.innerWidth)

const isMobile = computed(() => windowWidth.value < 768)
const isTablet = computed(() => windowWidth.value >= 768 && windowWidth.value < 1024)

function handleResize() {
  windowWidth.value = window.innerWidth
}

function toggleSidebar() {
  if (isMobile.value) {
    sidebarOpen.value = !sidebarOpen.value
  } else if (isTablet.value) {
    sidebarCollapsed.value = !sidebarCollapsed.value
  }
}

function closeSidebar() {
  sidebarOpen.value = false
}

function handleLogout() {
  if (adminAuth) {
    adminAuth.logout()
  }
  router.push({ name: 'AdminLogin' })
}

const { currentTheme, toggleTheme } = useTheme()

const navItems = [
  { name: 'AdminDashboard', path: '/admin', label: '概览', icon: '&#x1F4CA;' },
  { name: 'AdminProjects', path: '/admin/projects', label: '项目管理', icon: '&#x1F4C1;' },
  { name: 'AdminProfile', path: '/admin/profile', label: '个人资料', icon: '&#x1F464;' }
]

// 计算当前活跃菜单项（路由匹配 AdminLayout 的任意子路由）
const activeNav = computed(() => {
  // 用当前路由名去匹配，优先精确匹配
  const exact = navItems.find(item => item.name === route.name)
  if (exact) return exact
  // 如果当前在 projects/new 或 projects/:id/edit 路径，高亮 "项目管理"
  if (route.path.startsWith('/admin/projects')) {
    return navItems.find(item => item.name === 'AdminProjects')
  }
  return navItems.find(item => item.name === 'AdminDashboard')
})

// 获取管理员用户名
onMounted(async () => {
  window.addEventListener('resize', handleResize)
  try {
    const res = await adminAPI.verify()
    if (res.data && res.data.username) {
      adminName.value = res.data.username
    }
  } catch {
    // 验证失败由拦截器处理
  }
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', handleResize)
})
</script>

<template>
  <div
    class="admin-layout"
    :class="{
      'admin-layout--sidebar-open': sidebarOpen,
      'admin-layout--sidebar-collapsed': isTablet && sidebarCollapsed
    }"
  >
    <!-- 顶栏 -->
    <header class="admin-layout__header">
      <div class="admin-header__inner">
        <button class="admin-header__hamburger" @click="toggleSidebar" aria-label="切换菜单">
          <span>&#x2630;</span>
        </button>
        <div class="admin-header__actions">
          <button
            class="admin-header__theme-btn"
            @click="toggleTheme"
            :aria-label="currentTheme === 'dark' ? '切换到亮色主题' : '切换到暗色主题'"
          >
            <span class="admin-header__theme-icon" v-if="currentTheme === 'dark'">☀️</span>
            <span class="admin-header__theme-icon" v-else>🌙</span>
          </button>
          <div class="admin-header__user">
            <span class="admin-header__user-avatar">{{ adminName[0] || 'A' }}</span>
            <span class="admin-header__user-name">{{ adminName }}</span>
          </div>
        </div>
      </div>
    </header>

    <!-- 移动端遮罩 -->
    <div
      class="admin-layout__overlay"
      :class="{ 'admin-layout__overlay--visible': sidebarOpen }"
      @click="closeSidebar"
    ></div>

    <!-- 侧边栏 -->
    <aside
      class="admin-layout__sidebar"
      :class="{ 'admin-layout__sidebar--open': sidebarOpen }"
    >
      <!-- Logo 区 -->
      <div class="sidebar__brand">
        <router-link to="/" class="sidebar__brand-link">
          <span class="sidebar__brand-name">xinysoft</span>
        </router-link>
        <span class="sidebar__brand-label">管理后台</span>
      </div>

      <!-- 导航菜单 -->
      <nav class="sidebar__nav">
        <router-link
          v-for="item in navItems"
          :key="item.name"
          :to="item.path"
          class="sidebar__nav-item"
          :class="{ 'sidebar__nav-item--active': activeNav && activeNav.name === item.name }"
          @click="closeSidebar"
        >
          <span class="sidebar__nav-icon" v-html="item.icon"></span>
          <span class="sidebar__nav-label">{{ item.label }}</span>
        </router-link>
      </nav>

      <!-- 底部退出按钮 -->
      <div class="sidebar__footer">
        <router-link to="/" class="sidebar__footer-link" @click="closeSidebar">
          <span class="sidebar__nav-icon">&#x1F3E0;</span>
          <span class="sidebar__nav-label">访问前台</span>
        </router-link>
        <button class="sidebar__logout-btn" @click="handleLogout">
          <span class="sidebar__nav-icon">&#x1F6AA;</span>
          <span class="sidebar__nav-label">退出登录</span>
        </button>
      </div>
    </aside>

    <!-- 内容区 -->
    <main class="admin-layout__content">
      <RouterView />
    </main>

    <!-- Toast 通知 -->
    <AdminToast />
  </div>
</template>

<style scoped>
.sidebar__brand {
  padding: 16px 16px 12px;
  border-bottom: 1px solid var(--admin-sidebar-divider);
  margin-bottom: 8px;
  background: var(--admin-sidebar-bg);
}

.sidebar__brand-link {
  text-decoration: none;
  display: block;
}

.sidebar__brand-name {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--color-accent);
}

.sidebar__brand-label {
  font-size: 0.75rem;
  color: var(--admin-sidebar-text);
  margin-top: 2px;
  display: block;
}

.admin-header__user-avatar {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  border-radius: var(--radius-full);
  background: var(--color-accent);
  color: var(--color-text-on-accent);
  font-size: 0.9rem;
  font-weight: 600;
}

.admin-layout__overlay {
  display: none;
  position: fixed;
  inset: 0;
  background: var(--admin-modal-backdrop);
  z-index: var(--z-overlay);
  opacity: 0;
  pointer-events: none;
  transition: opacity var(--transition-base);
}

.admin-layout__overlay--visible {
  opacity: 1;
  pointer-events: auto;
}

/* 主题切换按钮 */
.admin-header__actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.admin-header__theme-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
  border-radius: var(--radius-full, 50%);
  background: transparent;
  border: 1px solid var(--admin-header-border);
  cursor: pointer;
  transition: all 0.3s ease;
  color: var(--admin-sidebar-text);
  flex-shrink: 0;
}

.admin-header__theme-btn:hover {
  background: var(--admin-sidebar-hover-bg);
  border-color: var(--color-accent);
  color: var(--color-accent);
}

.admin-header__theme-btn:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

.admin-header__theme-icon {
  font-size: 1.1rem;
  line-height: 1;
  transition: transform 0.3s ease;
}

.admin-header__theme-btn:hover .admin-header__theme-icon {
  transform: rotate(15deg);
}

/* 侧边栏底部导航链接（访问前台） */
.sidebar__footer-link {
  display: flex;
  align-items: center;
  gap: var(--spacing-md, 12px);
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--radius-sm);
  text-decoration: none;
  color: var(--admin-sidebar-text);
  font-size: 0.9rem;
  transition: background var(--transition-fast), color var(--transition-fast);
}

.sidebar__footer-link:hover {
  background: var(--admin-sidebar-hover-bg);
  color: var(--admin-sidebar-text-active);
}

/* 移动端适配 */
@media (max-width: 767px) {
  .admin-layout__overlay {
    display: block;
  }

  .admin-layout__sidebar {
    transform: translateX(-100%);
    transition: transform var(--transition-base);
  }

  .admin-layout__sidebar--open {
    transform: translateX(0);
  }

  .admin-layout__header {
    left: 0;
  }

  .admin-layout__content {
    margin-left: 0;
  }
}
</style>

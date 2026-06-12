<script setup>
import { ref, inject, computed, onMounted, onBeforeUnmount } from 'vue'
import { useRouter, useRoute, RouterView } from 'vue-router'
import AdminToast from '../../components/admin/AdminToast.vue'
import { adminAPI } from '../../api/admin'

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
        <div class="admin-header__user">
          <span class="admin-header__user-avatar">{{ adminName[0] || 'A' }}</span>
          <span class="admin-header__user-name">{{ adminName }}</span>
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

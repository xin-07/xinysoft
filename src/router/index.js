import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: () => import('../views/Home.vue'),
    meta: { title: 'xinysoft — 首页' }
  },
  {
    path: '/projects',
    name: 'Projects',
    component: () => import('../views/ProjectsView.vue'),
    meta: { title: 'xinysoft — 作品集' }
  },
  {
    path: '/projects/:id',
    name: 'ProjectDetail',
    component: () => import('../views/ProjectDetail.vue'),
    meta: { title: 'xinysoft — 项目详情' }
  },
  // ===== 管理后台路由 =====
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: () => import('../views/admin/AdminLogin.vue'),
    meta: { title: '管理后台 — 登录', guest: true }
  },
  {
    path: '/admin',
    component: () => import('../views/admin/AdminLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('../views/admin/AdminDashboard.vue'),
        meta: { title: '管理后台 — 概览' }
      },
      {
        path: 'projects',
        name: 'AdminProjects',
        component: () => import('../views/admin/AdminProjects.vue'),
        meta: { title: '管理后台 — 项目管理' }
      },
      {
        path: 'projects/new',
        name: 'AdminProjectNew',
        component: () => import('../components/admin/ProjectForm.vue'),
        meta: { title: '管理后台 — 新增项目' }
      },
      {
        path: 'projects/:id/edit',
        name: 'AdminProjectEdit',
        component: () => import('../components/admin/ProjectForm.vue'),
        meta: { title: '管理后台 — 编辑项目' }
      },
      {
        path: 'profile',
        name: 'AdminProfile',
        component: () => import('../views/admin/AdminProfile.vue'),
        meta: { title: '管理后台 — 个人资料' }
      }
    ]
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue'),
    meta: { title: 'xinysoft — 页面未找到' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (to.hash) {
      return {
        el: to.hash,
        behavior: 'smooth'
      }
    }
    if (savedPosition) {
      return savedPosition
    }
    return { top: 0 }
  }
})

// 导航守卫：管理后台认证检查
router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('admin_token')
  const isAuthenticated = !!token

  // 管理后台需要认证（除登录页）
  if (to.matched.some(record => record.meta.requiresAuth)) {
    if (!isAuthenticated) {
      next({ name: 'AdminLogin', query: { redirect: to.fullPath } })
    } else {
      next()
    }
  }
  // 已登录用户访问登录页 → 跳转管理后台
  else if (to.meta.guest && isAuthenticated) {
    next({ name: 'AdminDashboard' })
  }
  else {
    next()
  }
})

// 动态设置页面标题
router.afterEach((to) => {
  document.title = to.meta.title || 'xinysoft'
})

export default router
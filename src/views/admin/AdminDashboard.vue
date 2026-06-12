<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { adminAPI } from '../../api/admin'

const router = useRouter()

const stats = ref({
  total: 0,
  published: 0,
  draft: 0
})
const loading = ref(true)
const error = ref(false)

async function loadStats() {
  loading.value = true
  error.value = false
  try {
    const allRes = await adminAPI.getProjects(1, 1000)
    const total = allRes.data?.total || 0
    const items = allRes.data?.items || []

    stats.value = {
      total,
      published: items.filter(i => i.status === 'published').length,
      draft: items.filter(i => i.status === 'draft').length
    }
  } catch (err) {
    error.value = true
  } finally {
    loading.value = false
  }
}

const quickLinks = [
  { label: '新增项目', path: '/admin/projects/new', icon: '&#x2795;', desc: '创建新的作品集项目' },
  { label: '编辑个人资料', path: '/admin/profile', icon: '&#x1F464;', desc: '更新个人信息和链接' }
]

function navigateTo(path) {
  router.push(path)
}

onMounted(() => {
  loadStats()
})
</script>

<template>
  <div>
    <h1 class="admin-text-page-title">概览</h1>

    <!-- 加载态 -->
    <div v-if="loading" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; margin-top: 24px;">
      <div v-for="i in 3" :key="i" class="admin-card">
        <div class="admin-skeleton admin-skeleton--text-short" style="width:60%"></div>
        <div class="admin-skeleton admin-skeleton--title" style="width:40%; margin-top:8px; height:32px;"></div>
      </div>
    </div>

    <!-- 错误态 -->
    <div v-else-if="error" class="admin-card" style="margin-top:24px;">
      <div style="text-align:center; padding: 32px;">
        <p style="margin-bottom:16px; color: var(--color-text-secondary);">加载失败</p>
        <button class="admin-btn admin-btn--secondary" @click="loadStats">重试</button>
      </div>
    </div>

    <template v-else>
      <!-- 统计卡片 -->
      <div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); gap: 16px; margin-top: 24px;">
        <div class="admin-card stat-card">
          <span class="stat-card__label">项目总数</span>
          <span class="stat-card__value admin-text-number">{{ stats.total }}</span>
        </div>
        <div class="admin-card stat-card">
          <span class="stat-card__label">已发布</span>
          <span class="stat-card__value admin-text-number" style="color: var(--admin-status-published);">{{ stats.published }}</span>
        </div>
        <div class="admin-card stat-card">
          <span class="stat-card__label">草稿</span>
          <span class="stat-card__value admin-text-number" style="color: var(--admin-status-draft);">{{ stats.draft }}</span>
        </div>
      </div>

      <!-- 快速入口 -->
      <h2 class="admin-text-section-title" style="margin-top: 32px;">快速操作</h2>
      <div class="quick-actions">
        <div
          v-for="(link, index) in quickLinks"
          :key="link.path"
          class="quick-action-card"
          :style="{ '--delay': index * 60 + 'ms' }"
          @click="navigateTo(link.path)"
        >
          <div class="quick-action-card__icon-wrap">
            <span class="quick-action-card__icon" v-html="link.icon"></span>
          </div>
          <div class="quick-action-card__content">
            <h3 class="quick-action-card__title">{{ link.label }}</h3>
            <p class="quick-action-card__desc">{{ link.desc }}</p>
          </div>
          <span class="quick-action-card__arrow">→</span>
        </div>
      </div>
    </template>
  </div>
</template>
<template>
  <div class="projects-view">
    <Navbar />
    
    <main class="projects-main">
      <div class="projects-container">
        <!-- 页面标题 -->
        <header class="projects-header">
          <h1 class="projects-title">📂 项目作品集</h1>
          <p class="projects-subtitle">我的开发项目</p>
        </header>

        <!-- 加载状态 -->
        <div v-if="loading" class="projects-grid" aria-busy="true" aria-live="polite">
          <div v-for="i in 3" :key="i" class="skeleton-card">
            <div class="skeleton-cover skeleton-shimmer"></div>
            <div class="skeleton-content">
              <div class="skeleton-tags">
                <div class="skeleton-tag skeleton-shimmer"></div>
                <div class="skeleton-tag skeleton-shimmer"></div>
                <div class="skeleton-tag skeleton-shimmer"></div>
              </div>
              <div class="skeleton-title skeleton-shimmer"></div>
              <div class="skeleton-text skeleton-shimmer"></div>
              <div class="skeleton-text skeleton-text--short skeleton-shimmer"></div>
            </div>
          </div>
        </div>

        <!-- 错误状态 -->
        <div v-else-if="error" class="projects-error">
          <p class="error-message">{{ error }}</p>
          <button class="retry-btn" @click="fetchProjects">
            重试
          </button>
        </div>

        <!-- 空状态 -->
        <div v-else-if="projects.length === 0" class="projects-empty">
          <p class="empty-message">暂无项目</p>
        </div>

        <!-- 项目列表 -->
        <div v-else class="projects-grid">
          <ProjectCard
            v-for="(project, index) in projects"
            :key="project.id"
            :project="project"
            :border-effect="BORDER_EFFECTS[index % BORDER_EFFECTS.length]"
            variant="list"
            :style="{ '--card-index': index }"
          />
        </div>
      </div>
    </main>

    <Footer />
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
import ProjectCard from '../components/project/ProjectCard.vue'
import { projectsAPI } from '../api'
import { BORDER_EFFECTS } from '../config/constants'

const projects = ref([])
const loading = ref(true)
const error = ref(null)
const abortController = new AbortController()

const fetchProjects = async () => {
  loading.value = true
  error.value = null

  try {
    const result = await projectsAPI.getProjects(undefined, abortController.signal)
    projects.value = result.data.items || []
  } catch (err) {
    if (err.name === 'AbortError' || err.name === 'CanceledError') return
    console.error('Failed to fetch projects:', err)
    error.value = err.message || '加载失败，请稍后重试'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProjects()
})

onUnmounted(() => {
  abortController.abort()
})
</script>

<style scoped>
.projects-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bg-primary);
}

.projects-main {
  flex: 1;
  padding-top: 70px; /* Navbar 高度 */
}

.projects-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem 2rem;
  width: 100%;
}

/* 页面标题 */
.projects-header {
  text-align: center;
  margin-bottom: 3rem;
}

.projects-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 0.75rem 0;
}

.projects-subtitle {
  font-size: 1.125rem;
  color: var(--color-text-secondary);
  margin: 0;
}

/* 项目网格 */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

/* 卡片入场动画 */
.projects-grid > * {
  animation: cardEntrance 0.4s ease-out both;
  animation-delay: calc(var(--card-index, 0) * 0.1s + 0.05s);
}

@keyframes cardEntrance {
  from {
    opacity: 0;
    transform: translateY(24px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* 骨架屏 */
.skeleton-card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--color-border);
}

.skeleton-cover {
  aspect-ratio: 16 / 10;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
}

.skeleton-content {
  padding: 1.25rem;
}

.skeleton-tags {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.skeleton-tag {
  width: 60px;
  height: 24px;
  border-radius: 9999px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
}

.skeleton-title {
  width: 80%;
  height: 24px;
  border-radius: 4px;
  margin-bottom: 0.75rem;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
}

.skeleton-text {
  width: 100%;
  height: 16px;
  border-radius: 4px;
  margin-bottom: 0.5rem;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
}

.skeleton-text--short {
  width: 60%;
}

/* 错误状态 */
.projects-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.error-message {
  font-size: 1.125rem;
  color: var(--color-text-secondary);
  margin: 0 0 1.5rem 0;
}

.retry-btn {
  padding: 0.75rem 2rem;
  font-size: 1rem;
  font-weight: 500;
  color: #ffffff;
  background: var(--color-accent);
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.retry-btn:hover {
  background: var(--color-accent-hover);
  transform: translateY(-2px);
}

/* 焦点样式 */
.retry-btn:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

.retry-btn:focus {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* 空状态 */
.projects-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.empty-message {
  font-size: 1.125rem;
  color: var(--color-text-secondary);
  margin: 0;
}

/* 响应式布局 */
@media (max-width: 1199px) {
  .projects-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .projects-container {
    padding: 2rem 1.5rem;
  }

  .projects-title {
    font-size: 2rem;
  }

  .projects-subtitle {
    font-size: 1rem;
  }

  .projects-header {
    margin-bottom: 2rem;
  }
}

/* 600px断点 - 保持两列布局 */
@media (min-width: 600px) and (max-width: 768px) {
  .projects-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
}

/* 600px以下 - 单列布局 */
@media (max-width: 599px) {
  .projects-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
</style>
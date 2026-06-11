<template>
  <section v-if="!loading && !error && projects.length > 0" class="featured-projects">
    <div class="featured-projects__header">
      <h2 class="featured-projects__title">精选项目</h2>
      <router-link to="/projects" class="featured-projects__link">
        查看全部
        <span class="featured-projects__link-icon">→</span>
      </router-link>
    </div>

    <div class="featured-projects__grid">
      <ProjectCard
        v-for="(project, index) in projects"
        :key="project.id"
        :project="project"
        :border-effect="BORDER_EFFECTS[index % BORDER_EFFECTS.length]"
        variant="featured"
        :style="{ '--card-index': index }"
      />
    </div>
  </section>

  <!-- 加载状态：骨架屏 -->
  <section v-else-if="loading" class="featured-projects" aria-busy="true" aria-live="polite">
    <div class="featured-projects__header">
      <h2 class="featured-projects__title">精选项目</h2>
      <div class="featured-projects__skeleton-link"></div>
    </div>

    <div class="featured-projects__grid">
      <div v-for="i in 3" :key="i" class="featured-projects__skeleton-card">
        <div class="featured-projects__skeleton-cover"></div>
        <div class="featured-projects__skeleton-content">
          <div class="featured-projects__skeleton-tags">
            <div class="featured-projects__skeleton-tag"></div>
            <div class="featured-projects__skeleton-tag"></div>
            <div class="featured-projects__skeleton-tag"></div>
          </div>
          <div class="featured-projects__skeleton-title"></div>
          <div class="featured-projects__skeleton-text"></div>
          <div class="featured-projects__skeleton-text featured-projects__skeleton-text--short"></div>
        </div>
      </div>
    </div>
  </section>

  <!-- 错误状态和空状态：隐藏该区域（不渲染任何内容） -->
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import ProjectCard from '../project/ProjectCard.vue'
import { projectsAPI } from '../../api/index.js'

// 边框特效循环分配
const BORDER_EFFECTS = ['fade-glow', 'particle', 'nebula']

const projects = ref([])
const loading = ref(true)
const error = ref(null)
const abortController = new AbortController()

const fetchFeaturedProjects = async () => {
  try {
    loading.value = true
    error.value = null

    const result = await projectsAPI.getProjects({ featured: true }, abortController.signal)
    // 响应格式: { code: 200, message: "success", data: { items: [...] } }
    projects.value = result.data?.items || []
  } catch (err) {
    if (err.name === 'AbortError' || err.name === 'CanceledError') return
    console.error('Failed to fetch featured projects:', err)
    error.value = err
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchFeaturedProjects()
})

onUnmounted(() => {
  abortController.abort()
})
</script>

<style scoped>
.featured-projects {
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.featured-projects__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.featured-projects__title {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--color-text-primary, #ffffff);
  margin: 0;
}

.featured-projects__link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-accent, #e94560);
  text-decoration: none;
  font-size: 0.9375rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.featured-projects__link:hover {
  gap: 0.75rem;
}

/* 焦点样式 */
.featured-projects__link:focus-visible {
  outline: 2px solid var(--color-accent, #e94560);
  outline-offset: 2px;
}

.featured-projects__link:focus {
  outline: 2px solid var(--color-accent, #e94560);
  outline-offset: 2px;
}

.featured-projects__link-icon {
  transition: transform 0.2s ease;
}

.featured-projects__link:hover .featured-projects__link-icon {
  transform: translateX(4px);
}

.featured-projects__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

/* 卡片入场动画 */
.featured-projects__grid > * {
  animation: featuredCardEntrance 0.4s ease-out both;
  animation-delay: calc(var(--card-index, 0) * 0.1s + 0.05s);
}

@keyframes featuredCardEntrance {
  from {
    opacity: 0;
    transform: translateY(24px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* 骨架屏样式 */
.featured-projects__skeleton-link {
  width: 80px;
  height: 20px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.1) 25%, rgba(255, 255, 255, 0.2) 50%, rgba(255, 255, 255, 0.1) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
  border-radius: 4px;
}

.featured-projects__skeleton-card {
  background: var(--color-surface, #1a1a2e);
  border-radius: var(--radius-md, 12px);
  overflow: hidden;
  border: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
}

.featured-projects__skeleton-cover {
  aspect-ratio: 16 / 10;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
}

.featured-projects__skeleton-content {
  padding: 1.25rem;
}

.featured-projects__skeleton-tags {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.featured-projects__skeleton-tag {
  width: 60px;
  height: 24px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
  border-radius: 9999px;
}

.featured-projects__skeleton-title {
  width: 70%;
  height: 24px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
  border-radius: 4px;
  margin-bottom: 0.75rem;
}

.featured-projects__skeleton-text {
  width: 100%;
  height: 14px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}

.featured-projects__skeleton-text--short {
  width: 60%;
}

/* 响应式设计 */
@media (max-width: 1199px) {
  .featured-projects__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 767px) {
  .featured-projects {
    padding: 3rem 1.5rem;
  }

  .featured-projects__title {
    font-size: 1.5rem;
  }

  .featured-projects__grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .featured-projects__skeleton-content {
    padding: 1rem;
  }
}
</style>
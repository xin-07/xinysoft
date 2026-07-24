<template>
  <div class="project-detail">
    <!-- 加载状态：骨架屏 -->
    <div v-if="loading" class="loading-skeleton">
      <div class="skeleton-back skeleton-shimmer"></div>
      <div class="skeleton-banner skeleton-shimmer"></div>
      <div class="skeleton-content">
        <div class="skeleton-title skeleton-shimmer"></div>
        <div class="skeleton-subtitle skeleton-shimmer"></div>
        <div class="skeleton-tags">
          <div class="skeleton-tag skeleton-shimmer"></div>
          <div class="skeleton-tag skeleton-shimmer"></div>
          <div class="skeleton-tag skeleton-shimmer"></div>
        </div>
        <div class="skeleton-description">
          <div class="skeleton-line skeleton-shimmer"></div>
          <div class="skeleton-line skeleton-shimmer"></div>
          <div class="skeleton-line skeleton-shimmer"></div>
        </div>
      </div>
    </div>

    <!-- 404 状态 -->
    <div v-else-if="notFound" class="not-found">
      <div class="not-found-content">
        <h2>项目未找到</h2>
        <p>抱歉，您访问的项目不存在或已被删除。</p>
        <router-link to="/projects" class="back-to-list">
          返回作品集
        </router-link>
      </div>
    </div>

    <!-- 错误状态 -->
    <div v-else-if="error" class="error-state">
      <div class="error-content">
        <h2>加载失败</h2>
        <p>{{ error }}</p>
        <button @click="fetchProject" class="retry-btn">重试</button>
      </div>
    </div>

    <!-- 正常内容 -->
    <div v-else-if="project" class="detail-content">
      <!-- 返回按钮 -->
      <router-link to="/projects" class="back-link">
        <span class="arrow">←</span>
        <span class="text">返回作品集</span>
      </router-link>

      <!-- Banner -->
      <ProjectBanner :project="project" />

      <!-- 项目截图 -->
      <ProjectScreenshots
        v-if="project?.screenshots?.length"
        :screenshots="project.screenshots"
        :project-title="project.title"
      />

      <!-- 项目信息 -->
      <div class="project-info">
        <h1 class="project-title">{{ project.title }}</h1>
        <p v-if="project.subtitle" class="project-subtitle">{{ project.subtitle }}</p>

        <!-- 技术栈标签 -->
        <div v-if="project.tech_stack && project.tech_stack.length" class="tech-tags">
          <span
            v-for="tech in project.tech_stack"
            :key="tech"
            class="tech-tag"
            :style="{ backgroundColor: getTagBackgroundColor(tech), color: getTagTextColor() }"
          >
            {{ tech }}
          </span>
        </div>

        <!-- 项目描述 -->
        <div v-if="project.description" class="project-description">
          <p v-for="(paragraph, index) in descriptionParagraphs" :key="index">
            {{ paragraph }}
          </p>
        </div>

        <!-- 线上地址按钮 -->
        <a
          v-if="project.live_url"
          :href="project.live_url"
          target="_blank"
          rel="noopener noreferrer"
          class="live-url-btn"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"></path>
            <polyline points="15 3 21 3 21 9"></polyline>
            <line x1="10" y1="14" x2="21" y2="3"></line>
          </svg>
          访问线上地址
        </a>

        <!-- 仓库地址按钮 -->
        <a
          v-if="project.repo_url"
          :href="project.repo_url"
          target="_blank"
          rel="noopener noreferrer"
          class="repo-url-btn"
        >
          <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.245-1.695-.425-.225-.925-.78-.015-.795.85-.015 1.455.78 1.65 1.11.965 1.625 2.51 1.165 3.135.885.1-.69.39-1.17.705-1.44-2.475-.27-5.07-1.26-5.07-5.625 0-1.245.435-2.25 1.17-3.06-.12-.285-.51-1.455.12-3.015 0 0 .945-.3 3.09 1.17.9-.255 1.845-.375 2.79-.375.945 0 1.89.12 2.79.375 2.145-1.485 3.09-1.17 3.09-1.17.63 1.56.225 2.73.12 3.015.735.81 1.17 1.815 1.17 3.06 0 4.38-2.61 5.355-5.1 5.625.405.345.75 1.005.75 2.04 0 1.47-.015 2.655-.015 3.015 0 .315.225.69.825.57A12.02 12.02 0 0 0 24 12c0-6.63-5.37-12-12-12z"/>
          </svg>
          访问仓库地址
        </a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import { projectsAPI } from '../api'
import { getTagTextColor, getTagBackgroundColor } from '../config/techStackColors'
import ProjectBanner from '../components/project/ProjectBanner.vue'
import ProjectScreenshots from '../components/project/ProjectScreenshots.vue'

const route = useRoute()
const project = ref(null)
const loading = ref(true)
const notFound = ref(false)
const error = ref(null)
const abortController = new AbortController()

// 将描述按段落分割
const descriptionParagraphs = computed(() => {
  if (!project.value?.description) return []
  return project.value.description.split('\n').filter(p => p.trim())
})

// 获取项目详情
const fetchProject = async () => {
  const id = route.params.id
  loading.value = true
  notFound.value = false
  error.value = null

  try {
    const result = await projectsAPI.getProject(id, abortController.signal)
    // API 返回 { code, message, data }
    if (result.code === 200 && result.data) {
      project.value = result.data
    } else {
      notFound.value = true
    }
  } catch (err) {
    if (err.name === 'AbortError' || err.name === 'CanceledError') return
    console.error('Failed to fetch project:', err)
    if (err.response?.status === 404) {
      notFound.value = true
    } else {
      error.value = err.message || '加载项目详情失败，请稍后重试'
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProject()
})

onUnmounted(() => {
  abortController.abort()
})
</script>

<style scoped>
.project-detail {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

/* 骨架屏样式 */
.loading-skeleton {
}

.skeleton-back {
  width: 120px;
  height: 24px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
  border-radius: var(--radius-sm);
  margin-bottom: 2rem;
}

.skeleton-banner {
  width: 100%;
  aspect-ratio: 16 / 9;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
  border-radius: var(--radius-lg);
  margin-bottom: 2rem;
}

.skeleton-content {
  padding: 0 1rem;
}

.skeleton-title {
  width: 60%;
  height: 36px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
  border-radius: var(--radius-sm);
  margin-bottom: 1rem;
}

.skeleton-subtitle {
  width: 40%;
  height: 20px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
  border-radius: var(--radius-sm);
  margin-bottom: 1.5rem;
}

.skeleton-tags {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.skeleton-tag {
  width: 80px;
  height: 28px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
  border-radius: var(--radius-sm);
}

.skeleton-description {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.skeleton-line {
  width: 100%;
  height: 16px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
  border-radius: var(--radius-sm);
}

.skeleton-line:last-child {
  width: 70%;
}

/* 404 状态 */
.not-found,
.error-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  text-align: center;
}

.not-found-content h2,
.error-content h2 {
  font-size: 1.5rem;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
}

.not-found-content p,
.error-content p {
  color: var(--color-text-secondary);
  margin-bottom: 1.5rem;
}

.back-to-list,
.retry-btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: var(--color-accent);
  color: white;
  text-decoration: none;
  border-radius: var(--radius-sm);
  font-weight: 500;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
}

.back-to-list:hover,
.retry-btn:hover {
  background: var(--color-accent-hover);
  transform: translateY(-2px);
}

/* 返回按钮 */
.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-text-secondary);
  text-decoration: none;
  font-size: 0.95rem;
  margin-bottom: 2rem;
  transition: color 0.3s ease;
}

.back-link:hover {
  color: var(--color-accent);
}

.back-link .arrow {
  transition: transform 0.3s ease;
}

.back-link:hover .arrow {
  transform: translateX(-4px);
}

/* 项目信息 */
.project-info {
  margin-top: 2rem;
}

.project-title {
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.project-subtitle {
  font-size: 1.125rem;
  color: var(--color-text-secondary);
  margin-bottom: 1.5rem;
}

/* 技术栈标签 */
.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.tech-tag {
  display: inline-block;
  padding: 0.375rem 0.875rem;
  border-radius: 999px;
  font-size: 0.875rem;
  font-weight: 500;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: default;
  backdrop-filter: blur(2px);
}

.tech-tag:hover {
  transform: scale(1.05);
}

/* 项目描述 */
.project-description {
  margin-bottom: 2rem;
  line-height: 1.8;
  color: var(--color-text-primary);
}

.project-description p {
  margin-bottom: 1rem;
}

.project-description p:last-child {
  margin-bottom: 0;
}

/* 线上地址按钮 */
.live-url-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--color-accent);
  color: white;
  text-decoration: none;
  border-radius: var(--radius-sm);
  font-weight: 500;
  transition: all 0.3s ease;
}

.live-url-btn:hover {
  background: var(--color-accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(233, 69, 96, 0.3);
}

.live-url-btn svg {
  flex-shrink: 0;
}

/* 仓库地址按钮 */
.repo-url-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  color: var(--color-text-primary);
  text-decoration: none;
  border-radius: var(--radius-sm);
  font-weight: 500;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
  margin-left: 0.75rem;
}

.repo-url-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.repo-url-btn svg {
  flex-shrink: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .project-detail {
    padding: 1.5rem 1rem;
  }

  .project-title {
    font-size: 1.75rem;
  }

  .project-subtitle {
    font-size: 1rem;
  }

  .tech-tags {
    gap: 0.375rem;
  }

  .tech-tag {
    font-size: 0.8125rem;
    padding: 0.3rem 0.75rem;
  }

  .repo-url-btn {
    margin-left: 0;
    margin-top: 0.75rem;
  }

  .live-url-btn,
  .repo-url-btn {
    display: flex;
    width: 100%;
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .project-title {
    font-size: 1.5rem;
  }
}
</style>
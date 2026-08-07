<template>
  <!-- 使用动态组件切换包装器，卡片内容只定义一次 -->
  <Component :is="wrapperComponent" v-bind="wrapperProps">
    <div
      class="project-card"
      :class="cardClasses"
      @click="handleCardClick"
      tabindex="0"
      role="button"
      :aria-label="`查看项目: ${project?.title || '项目详情'}`"
      @keydown.enter="handleCardClick"
      @keydown.space.prevent="handleCardClick"
    >
      <!-- 封面区域 -->
      <div class="project-card__cover">
        <img
          v-if="resolvedCoverUrl"
          :src="resolvedCoverUrl"
          :alt="project.title || '项目封面'"
          class="project-card__image"
          loading="lazy"
          @error="coverFallbackUrl ? handleFallbackError() : handleCoverError()"
        />
        <ProjectPlaceholder
          v-else
          :brand-name="brandName"
          :gradient-style="gradientStyle"
          variant="card"
        />
      </div>

      <!-- 内容区域 -->
      <div class="project-card__content" :style="cardContentStyle">
        <!-- 技术栈标签 -->
        <div class="project-card__tags">
          <span
            v-for="tech in displayedTechStack"
            :key="tech"
            class="project-card__tag"
            :style="{ backgroundColor: getTagBackgroundColor(tech), color: getTagTextColor() }"
          >
            {{ tech }}
          </span>
          <span
            v-if="variant === 'featured' && techStackCount > 3"
            class="project-card__tag project-card__tag--more"
          >
            +{{ techStackCount - 3 }}
          </span>
        </div>

        <!-- 项目名称 -->
        <h3 class="project-card__title">{{ project?.title }}</h3>

        <!-- 描述 -->
        <p class="project-card__description">
          {{ project?.subtitle || project?.description }}
        </p>

        <!-- 操作按钮（仅 list 模式） -->
        <div v-if="variant === 'list'" class="project-card__actions">
          <button
            class="project-card__btn project-card__btn--primary"
            @click.stop="handleCardClick"
            aria-label="查看详情"
          >
            查看详情
            <Icon icon="mdi:arrow-right" class="project-card__btn-icon" />
          </button>
          <button
            v-if="project?.live_url"
            class="project-card__btn project-card__btn--secondary"
            @click.stop="openLiveUrl"
            aria-label="访问线上地址"
          >
            <Icon icon="mdi:link" class="project-card__btn-icon" />
            线上地址
          </button>
          <button
            v-if="project?.repo_url"
            class="project-card__btn project-card__btn--secondary"
            @click.stop="openRepoUrl"
            aria-label="访问仓库地址"
          >
            <Icon icon="mdi:github" class="project-card__btn-icon" />
            仓库地址
          </button>
        </div>
      </div>
    </div>
  </Component>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { Icon } from '@iconify/vue'
import { getTagColor, getTagTextColor, getTagBackgroundColor, projectBrands } from '../../config/techStackColors'
import { resolveFilePath, getLocalFallback } from '../../utils/resolvePath'
import { useProjectBrand } from '../../composables/useProjectBrand'
import ParticleBorder from './ParticleBorder.vue'
import ProjectPlaceholder from './ProjectPlaceholder.vue'

const props = defineProps({
  project: {
    type: Object,
    required: true
  },
  variant: {
    type: String,
    default: 'list',
    validator: (v) => ['list', 'featured'].includes(v)
  },
  borderEffect: {
    type: String,
    default: 'none',
    validator: (v) => ['fade-glow', 'particle', 'nebula', 'none'].includes(v)
  }
})

const router = useRouter()

// 项目 ID 响应式引用，用于 composable
const projectId = computed(() => props.project?.id)

// 使用 composable 获取品牌相关样式
const { brandName, gradientStyle, cardContentStyle } = useProjectBrand(projectId)

// 封面图路径转换（支持后端 → public 目录 → 占位符 三级降级）
const coverFallbackUrl = ref(null)
const coverError = ref(false)
const resolvedCoverUrl = computed(() => {
  if (coverError.value) return null
  if (coverFallbackUrl.value) return coverFallbackUrl.value
  return resolveFilePath(props.project?.cover_url)
})

const handleCoverError = () => {
  const rawPath = props.project?.cover_url
  if (rawPath) {
    coverFallbackUrl.value = getLocalFallback(rawPath)
  } else {
    coverError.value = true
  }
}

// public 目录降级也失败 → 最终降级到 ProjectPlaceholder 占位符
const handleFallbackError = () => {
  coverError.value = true
  coverFallbackUrl.value = null
}

// 项目切换时重置错误状态，允许新项目的封面图重新尝试加载
watch(() => props.project?.id, () => {
  coverError.value = false
  coverFallbackUrl.value = null
})

// 品牌名称（来自 composable）

// 技术栈数组
const techStack = computed(() => {
  return props.project?.tech_stack || []
})

// 技术栈数量
const techStackCount = computed(() => techStack.value.length)

// 显示的技术栈（featured 模式只显示前 3 个）
const displayedTechStack = computed(() => {
  if (props.variant === 'featured') {
    return techStack.value.slice(0, 3)
  }
  return techStack.value
})

// ParticleBorder 组件的颜色（从项目品牌渐变色中提取或使用默认强调色）
const particleBorderColor = computed(() => {
  const brand = projectBrands[props.project?.id]
  if (brand?.gradient) {
    // 从 gradient 中提取第一个颜色值
    const match = brand.gradient.match(/#[a-fA-F0-9]{6}/)
    return match ? match[0] : '#e94560'
  }
  return '#e94560'
})

// 动态组件：根据 borderEffect 选择包装器
const wrapperComponent = computed(() => {
  return props.borderEffect === 'particle' ? ParticleBorder : 'div'
})

// 包装器 props
const wrapperProps = computed(() => {
  if (props.borderEffect === 'particle') {
    return {
      color: particleBorderColor.value,
      borderWidth: 6,
      class: 'project-card-wrapper'
    }
  }
  return {}
})

// 卡片 CSS 类
const cardClasses = computed(() => {
  const classes = {
    'project-card--featured': props.variant === 'featured',
    'project-card--list': props.variant === 'list'
  }
  // 非 particle 模式下添加边框特效类
  if (props.borderEffect !== 'particle' && props.borderEffect !== 'none') {
    classes[`border--${props.borderEffect}`] = true
  }
  return classes
})

// 点击卡片跳转到详情页
const handleCardClick = () => {
  if (props.project?.id) {
    router.push(`/projects/${props.project.id}`)
  }
}

// 打开线上地址
const openLiveUrl = () => {
  if (props.project?.live_url) {
    window.open(props.project.live_url, '_blank')
  }
}

// 打开仓库地址
const openRepoUrl = () => {
  if (props.project?.repo_url) {
    window.open(props.project.repo_url, '_blank')
  }
}
</script>

<style scoped>
/* ============================================================
   ProjectCard — Base Styles
   ============================================================ */

.project-card {
  background: var(--color-surface, #1a1a2e);
  border-radius: var(--radius-md, 12px);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
  border: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
  display: flex;
  flex-direction: column;
  height: 100%;
}

.project-card:hover,
.project-card:focus {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg, 0 10px 40px rgba(0, 0, 0, 0.3));
  border-color: var(--color-accent, #e94560);
  outline: none;
}

.project-card:active {
  transform: translateY(-2px) scale(0.98);
}

.project-card:focus-visible {
  outline: 2px solid var(--color-accent, #e94560);
  outline-offset: 2px;
}

/* ============================================================
   Cover Area
   ============================================================ */

.project-card__cover {
  width: 100%;
  overflow: hidden;
  position: relative;
}

.project-card--featured .project-card__cover {
  aspect-ratio: 16 / 10;
}

.project-card--list .project-card__cover {
  aspect-ratio: 16 / 9;
}

.project-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;
}

.project-card:hover .project-card__image {
  transform: scale(1.05);
}

/* ============================================================
   Content Area
   ============================================================ */

.project-card__content {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  flex: 1;
}

/* Tech stack tags */
.project-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.project-card__tag {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  transition: transform 0.2s ease;
  white-space: nowrap;
}

.project-card__tag:hover {
  transform: scale(1.05);
}

.project-card__tag--more {
  background: rgba(255, 255, 255, 0.1);
  color: var(--color-text-primary, #e6e6e6);
}

/* Project title */
.project-card__title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text-primary, #ffffff);
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
}

/* Description */
.project-card__description {
  font-size: 0.875rem;
  color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
  margin: 0 0 1rem 0;
  line-height: 1.6;
  flex: 1;
}

/* 不限制描述文字行数，完整展示内容 */

/* Action buttons */
.project-card__actions {
  display: flex;
  flex-wrap: nowrap;
  gap: 0.5rem;
  margin-top: auto;
}

.project-card__btn {
  padding: 0.5rem 1rem;
  border-radius: var(--radius-sm, 8px);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  white-space: nowrap;
}

.project-card__btn--primary {
  background: var(--color-accent, #e94560);
  color: #ffffff;
}

.project-card__btn--primary:hover {
  background: var(--color-accent-hover);
  transform: translateY(-2px);
}

.project-card__btn--secondary {
  background: rgba(255, 255, 255, 0.1);
  color: var(--color-text-primary, #ffffff);
  border: 1px solid var(--color-border, rgba(255, 255, 255, 0.2));
}

.project-card__btn--secondary:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}

.project-card__btn-icon {
  font-size: 1rem;
  width: 1em;
  height: 1em;
  vertical-align: middle;
}

/* ============================================================
   Responsive Design
   ============================================================ */

@media (max-width: 768px) {
  .project-card__content {
    padding: 1rem;
  }

  .project-card__title {
    font-size: 1rem;
  }

  .project-card__description {
    font-size: 0.8125rem;
  }

  .project-card__btn {
    padding: 0.4rem 0.8rem;
    font-size: 0.8125rem;
  }
}

@media (max-width: 480px) {
  .project-card__actions {
    flex-direction: column;
  }

  .project-card__btn {
    width: 100%;
    justify-content: center;
  }
}

/* ============================================================
   Accessibility: Reduced Motion
   ============================================================ */

@media (prefers-reduced-motion: reduce) {
  .project-card,
  .project-card__image,
  .project-card__tag,
  .project-card__btn {
    transition: none;
    animation: none;
  }
}

/* ============================================================
   ParticleBorder Wrapper
   ============================================================ */

.project-card-wrapper {
  display: block;
  height: 100%;
}

.project-card-wrapper .project-card {
  border: none;
}

.project-card-wrapper .project-card:hover,
.project-card-wrapper .project-card:focus {
  border-color: transparent;
}

.project-card-wrapper .project-card:focus-visible {
  outline: 2px solid var(--color-accent, #e94560);
  outline-offset: 4px;
}

/* Border effects */
.project-card.border--fade-glow,
.project-card.border--nebula {
  border: none;
}

.project-card.border--fade-glow:hover,
.project-card.border--fade-glow:focus,
.project-card.border--nebula:hover,
.project-card.border--nebula:focus {
  border-color: transparent;
}
</style>
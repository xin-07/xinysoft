<template>
  <div
    class="project-card"
    :class="{
      'project-card--featured': variant === 'featured',
      'project-card--list': variant === 'list'
    }"
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
        v-if="project?.cover_url"
        :src="project.cover_url"
        :alt="project.title || '项目封面'"
        class="project-card__image"
        loading="lazy"
      />
      <div
        v-else
        class="project-card__placeholder"
        :style="gradientStyle"
      >
        <span class="project-card__letter">{{ brandName }}</span>
      </div>
    </div>

    <!-- 内容区域 -->
    <div class="project-card__content" :style="cardContentStyle">
      <!-- 技术栈标签 -->
      <div class="project-card__tags">
        <span
          v-for="tech in displayedTechStack"
          :key="tech"
          class="project-card__tag"
          :style="{ backgroundColor: getTagBackgroundColor(tech), color: getTagColor(tech) }"
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
          <span class="project-card__btn-icon">→</span>
        </button>
        <button
          v-if="project?.live_url"
          class="project-card__btn project-card__btn--secondary"
          @click.stop="openLiveUrl"
          aria-label="访问线上地址"
        >
          <span class="project-card__btn-icon">🔗</span>
          线上地址
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { getTagColor, getTagBackgroundColor, projectBrands } from '../../config/techStackColors'

const props = defineProps({
  project: {
    type: Object,
    required: true
  },
  variant: {
    type: String,
    default: 'list',
    validator: (v) => ['list', 'featured'].includes(v)
  }
})

const router = useRouter()

// 根据项目 id 返回品牌名称
const brandName = computed(() => {
  return projectBrands[props.project?.id]?.name || ''
})

// 根据项目 id 计算渐变色
const gradientStyle = computed(() => {
  const brand = projectBrands[props.project?.id]
  return {
    background: brand?.gradient || projectBrands[1].gradient
  }
})

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

// 卡片背景色与封面渐变呼应（末端色以极低透明度延展到内容区顶部）
const cardContentStyle = computed(() => {
  const brand = projectBrands[props.project?.id]
  return { background: brand?.tint || projectBrands[1].tint }
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
</script>

<style scoped>
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

.project-card:focus-visible {
  outline: 2px solid var(--color-accent, #e94560);
  outline-offset: 2px;
}

/* 封面区域 */
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

.project-card__placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 120px;
  background-size: 250% 250%;
  animation: gradientShift 6s ease-in-out infinite alternate;
}

@keyframes gradientShift {
  0%   { background-position: 0% 0%; }
  50%  { background-position: 100% 100%; }
  100% { background-position: 0% 100%; }
}

.project-card__letter {
  font-size: 1.75rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  user-select: none;
  letter-spacing: 0.1em;
  transition: transform 0.3s ease;
}

.project-card:hover .project-card__letter {
  transform: scale(1.1);
}

/* 内容区域 */
.project-card__content {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  flex: 1;
}

/* 技术栈标签 */
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
  color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
}

/* 项目名称 */
.project-card__title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text-primary, #ffffff);
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
}

/* 描述 */
.project-card__description {
  font-size: 0.875rem;
  color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
  margin: 0 0 1rem 0;
  line-height: 1.6;
  flex: 1;
}

.project-card--featured .project-card__description {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-card--list .project-card__description {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* 操作按钮 */
.project-card__actions {
  display: flex;
  gap: 0.75rem;
  margin-top: auto;
}

.project-card__btn {
  padding: 0.5rem 1rem;
  border-radius: var(--radius-sm, 8px);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
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
}

/* 响应式设计 */
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

  .project-card__letter {
    font-size: 1.5rem;
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
</style>
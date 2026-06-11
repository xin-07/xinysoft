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
          <!-- Layer 3: Bottom dark gradient fade -->
          <div class="placeholder-fade" aria-hidden="true"></div>

          <!-- Layer 5: Floating geometric decorations -->
          <div class="placeholder-decor placeholder-decor--circle" aria-hidden="true"></div>
          <div class="placeholder-decor placeholder-decor--ring" aria-hidden="true"></div>
          <div class="placeholder-decor placeholder-decor--dot" aria-hidden="true"></div>

          <!-- Layer 6: Brand name -->
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
        </div>
      </div>
    </div>
  </Component>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { Icon } from '@iconify/vue'
import { getTagColor, getTagTextColor, getTagBackgroundColor, projectBrands } from '../../config/techStackColors'
import { useProjectBrand } from '../../composables/useProjectBrand'
import ParticleBorder from './ParticleBorder.vue'

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
   Placeholder — 6-Layer Visual Effects
   ============================================================ */

/* Layer 1: Brand gradient background */
.project-card__placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 120px;
  position: relative;
  overflow: hidden;

  /* Brand gradient via CSS variable injected by composable */
  background: var(--card-brand-gradient, linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%));
  background-size: 250% 250%;
  animation: gradientShift 6s ease-in-out infinite alternate;
}

/* Layer 2: Geometric grid texture (disabled) */
/* Removed per design preference */

/* Layer 4: Diagonal light sweep (::after) */
.project-card__placeholder::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    105deg,
    transparent 35%,
    rgba(255, 255, 255, 0.12) 42%,
    rgba(255, 255, 255, 0.35) 50%,
    rgba(255, 255, 255, 0.12) 58%,
    transparent 65%
  );
  animation: lightSweep 4s ease-in-out infinite;
  pointer-events: none;
  z-index: 3;
}

.project-card:hover .project-card__placeholder::after {
  animation-duration: 2s;
  background: linear-gradient(
    105deg,
    transparent 35%,
    rgba(255, 255, 255, 0.2) 42%,
    rgba(255, 255, 255, 0.5) 50%,
    rgba(255, 255, 255, 0.2) 58%,
    transparent 65%
  );
}

/* Layer 3: Bottom dark gradient fade */
.placeholder-fade {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 35%;
  background: linear-gradient(
    to top,
    var(--color-surface, #0f3460) 0%,
    rgba(15, 52, 96, 0.25) 50%,
    transparent 100%
  );
  pointer-events: none;
  z-index: 2;
}

/* Layer 5: Floating geometric decorations */
.placeholder-decor {
  position: absolute;
  pointer-events: none;
  z-index: 4;
  opacity: 0.7;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.project-card:hover .placeholder-decor {
  opacity: 1;
}

/* Large circle — top right */
.placeholder-decor--circle {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.06);
  border: 2px solid rgba(0, 0, 0, 0.08);
  top: -28px;
  right: -18px;
  animation: floatCircle 7s ease-in-out infinite alternate;
}

/* Ring — bottom left */
.placeholder-decor--ring {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: 3px solid rgba(0, 0, 0, 0.12);
  bottom: 18px;
  left: 14px;
  animation: floatRing 5.5s ease-in-out infinite alternate-reverse;
}

/* Small dot — middle right */
.placeholder-decor--dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.15);
  top: 38%;
  right: 22%;
  animation: floatDot 3.5s ease-in-out infinite alternate;
  box-shadow: 0 0 16px 4px rgba(0, 0, 0, 0.1);
}

/* Layer 6: First letter */
.project-card__letter {
  position: relative;
  z-index: 5;
  font-size: 2rem;
  font-weight: 700;
  color: rgba(0, 0, 0, 0.35);
  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.6),
    0 2px 8px rgba(0, 0, 0, 0.15);
  user-select: none;
  letter-spacing: 0.1em;
  transition: transform 0.3s ease, text-shadow 0.3s ease;
}

/* Letter glow behind */
.project-card__letter::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 90px;
  height: 90px;
  transform: translate(-50%, -50%);
  background: radial-gradient(
    circle,
    rgba(0, 0, 0, 0.06) 0%,
    transparent 70%
  );
  pointer-events: none;
  z-index: -1;
  transition: width 0.3s ease, height 0.3s ease;
}

.project-card:hover .project-card__letter {
  transform: scale(1.2);
  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.8),
    0 4px 16px rgba(0, 0, 0, 0.2);
}

.project-card:hover .project-card__letter::after {
  width: 120px;
  height: 120px;
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

.project-card--featured .project-card__description {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-card--list .project-card__description {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Action buttons */
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
  transition: background-color 0.2s ease, transform 0.2s ease;
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
  width: 1em;
  height: 1em;
  vertical-align: middle;
}

/* ============================================================
   Animations
   ============================================================ */

@keyframes floatCircle {
  0%   { transform: translate(0, 0) scale(1); }
  100% { transform: translate(-6px, 8px) scale(1.08); }
}

@keyframes floatRing {
  0%   { transform: translate(0, 0) rotate(0deg); }
  100% { transform: translate(5px, -7px) rotate(45deg); }
}

@keyframes floatDot {
  0%   { transform: translate(0, 0) scale(1); opacity: 0.6; }
  100% { transform: translate(-3px, -5px) scale(1.3); opacity: 1; }
}

@keyframes gradientShift {
  0%   { background-position: 0% 0%; }
  50%  { background-position: 100% 100%; }
  100% { background-position: 0% 100%; }
}

@keyframes lightSweep {
  0%   { transform: translateX(-100%) rotate(15deg); }
  100% { transform: translateX(100%) rotate(15deg); }
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

  .project-card__placeholder {
    animation: none;
  }

  .project-card__placeholder::after {
    animation: none;
    display: none;
  }

  .placeholder-decor {
    animation: none;
    transition: none;
  }

  .project-card__letter,
  .project-card__letter::after {
    transition: none;
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
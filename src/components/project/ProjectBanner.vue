<template>
  <div class="project-banner">
    <!-- 有封面图时显示图片 -->
    <img
      v-if="project?.cover_url"
      :src="project.cover_url"
      :alt="project.title || '项目封面'"
      class="banner-image"
      loading="lazy"
    />
    <!-- 无封面图时显示 6 层占位效果（与卡片封面一致） -->
    <div
      v-else
      class="banner-placeholder"
      :style="gradientStyle"
    >
      <!-- Layer 3: Bottom dark gradient fade -->
      <div class="banner-fade" aria-hidden="true"></div>

      <!-- Layer 5: Floating geometric decorations -->
      <div class="banner-decor banner-decor--circle" aria-hidden="true"></div>
      <div class="banner-decor banner-decor--ring" aria-hidden="true"></div>
      <div class="banner-decor banner-decor--dot" aria-hidden="true"></div>

      <!-- Layer 6: Brand name -->
      <span class="banner-brand">{{ brandName }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useProjectBrand } from '../../composables/useProjectBrand'

const props = defineProps({
  project: {
    type: Object,
    required: true
  }
})

// 项目 ID 响应式引用，用于 composable
const projectId = computed(() => props.project?.id)

// 使用 composable 获取品牌相关样式
const { brandName, gradientStyle } = useProjectBrand(projectId)
</script>

<style scoped>
/* ============================================================
   ProjectBanner — Base
   ============================================================ */

.project-banner {
  width: 100%;
  border-radius: var(--radius-lg);
  overflow: hidden;
  aspect-ratio: 16 / 9;
}

.banner-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* ============================================================
   Placeholder — 6-Layer Visual Effects (matches ProjectCard)
   ============================================================ */

/* Layer 1: Brand gradient background */
.banner-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  position: relative;
  overflow: hidden;

  background: var(--card-brand-gradient, linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%));
  background-size: 250% 250%;
  animation: gradientShift 6s ease-in-out infinite alternate;
}

/* Layer 2: Geometric grid texture (disabled) */
/* Removed per design preference */

/* Layer 4: Diagonal light sweep (::after) */
.banner-placeholder::after {
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
  animation: lightSweep 5s ease-in-out infinite;
  pointer-events: none;
  z-index: 3;
}

/* Layer 3: Bottom dark gradient fade */
.banner-fade {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 55%;
  background: linear-gradient(
    to top,
    var(--color-surface, #0f3460) 0%,
    rgba(15, 52, 96, 0.4) 40%,
    transparent 100%
  );
  pointer-events: none;
  z-index: 2;
}

/* Layer 5: Floating geometric decorations */
.banner-decor {
  position: absolute;
  pointer-events: none;
  z-index: 4;
  opacity: 0.6;
}

/* Large circle — top right */
.banner-decor--circle {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.06);
  border: 2px solid rgba(0, 0, 0, 0.08);
  top: -36px;
  right: -24px;
  animation: floatCircle 7s ease-in-out infinite alternate;
}

/* Ring — bottom left */
.banner-decor--ring {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  border: 3px solid rgba(0, 0, 0, 0.12);
  bottom: 24px;
  left: 20px;
  animation: floatRing 5.5s ease-in-out infinite alternate-reverse;
}

/* Small dot — middle right */
.banner-decor--dot {
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.15);
  top: 38%;
  right: 22%;
  animation: floatDot 3.5s ease-in-out infinite alternate;
  box-shadow: 0 0 18px 5px rgba(0, 0, 0, 0.1);
}

/* Layer 6: Brand name */
.banner-brand {
  position: relative;
  z-index: 5;
  font-size: 3.5rem;
  font-weight: 700;
  color: rgba(0, 0, 0, 0.35);
  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.6),
    0 2px 8px rgba(0, 0, 0, 0.15);
  user-select: none;
  transition: transform 0.3s ease, text-shadow 0.3s ease;
}

/* Brand name glow behind */
.banner-brand::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 120px;
  height: 120px;
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

.banner-placeholder:hover .banner-brand {
  transform: scale(1.08);
  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.8),
    0 4px 16px rgba(0, 0, 0, 0.2);
}

.banner-placeholder:hover .banner-brand::after {
  width: 150px;
  height: 150px;
}

/* ============================================================
   Animations
   ============================================================ */

@keyframes gradientShift {
  0%   { background-position: 0% 0%; }
  50%  { background-position: 100% 100%; }
  100% { background-position: 0% 100%; }
}

@keyframes lightSweep {
  0%   { transform: translateX(-100%) rotate(15deg); }
  100% { transform: translateX(100%) rotate(15deg); }
}

@keyframes floatCircle {
  0%   { transform: translate(0, 0) scale(1); }
  100% { transform: translate(-8px, 10px) scale(1.08); }
}

@keyframes floatRing {
  0%   { transform: translate(0, 0) rotate(0deg); }
  100% { transform: translate(6px, -9px) rotate(45deg); }
}

@keyframes floatDot {
  0%   { transform: translate(0, 0) scale(1); opacity: 0.6; }
  100% { transform: translate(-4px, -6px) scale(1.3); opacity: 1; }
}

/* ============================================================
   Responsive Design
   ============================================================ */

@media (max-width: 768px) {
  .project-banner {
    aspect-ratio: 4 / 3;
  }

  .banner-brand {
    font-size: 2rem;
  }

  .banner-decor--circle {
    width: 100px;
    height: 100px;
  }

  .banner-decor--ring {
    width: 52px;
    height: 52px;
  }
}

@media (max-width: 480px) {
  .banner-brand {
    font-size: 1.5rem;
  }
}

/* ============================================================
   Accessibility: Reduced Motion
   ============================================================ */

@media (prefers-reduced-motion: reduce) {
  .banner-placeholder {
    animation: none;
    background-size: 100% 100%;
  }

  .banner-placeholder::after {
    animation: none;
    display: none;
  }

  .banner-decor {
    animation: none;
  }

  .banner-brand,
  .banner-brand::after {
    transition: none;
  }

  .banner-placeholder:hover .banner-brand {
    transform: none;
  }
}
</style>
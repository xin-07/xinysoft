<template>
  <div v-if="resolvedScreenshots?.length" class="project-screenshots">
    <h2 class="screenshots-title">项目截图</h2>

    <div class="screenshots-grid">
      <div
        v-for="(src, index) in displayScreenshots"
        :key="index"
        class="screenshot-item"
        @click="openLightbox(index)"
      >
        <!-- 骨架占位（图片加载前显示） -->
        <div
          v-if="!loadedImages.has(index) && !imageErrors.has(index)"
          class="screenshot-skeleton skeleton-shimmer"
        ></div>
        <!-- 图片（加载完成后显示） -->
        <img
          v-show="loadedImages.has(index)"
          :src="src"
          :alt="projectTitle ? `${projectTitle} 截图 ${index + 1}` : `截图 ${index + 1}`"
          @load="onImageLoad(index)"
          @error="onImageError(index)"
        />
        <!-- 加载失败占位 -->
        <div v-if="imageErrors.has(index)" class="screenshot-error">
          <Icon icon="mdi:image-broken" />
        </div>
      </div>
    </div>

    <!-- 灯箱 -->
    <Teleport to="body">
      <div
        v-if="lightboxIndex !== null"
        class="lightbox"
        @click="closeLightbox"
        tabindex="-1"
        ref="lightboxRef"
      >
        <button
          v-if="displayScreenshots.length > 1"
          class="lightbox-nav lightbox-prev"
          @click.stop="prevImage"
          aria-label="上一张"
        >&#8249;</button>

        <img
          :src="displayScreenshots[lightboxIndex]"
          :alt="`${projectTitle || '项目'} 截图 ${lightboxIndex + 1}`"
          class="lightbox-image"
          @click.stop
        />

        <button
          v-if="displayScreenshots.length > 1"
          class="lightbox-nav lightbox-next"
          @click.stop="nextImage"
          aria-label="下一张"
        >&#8250;</button>

        <button
          class="lightbox-close"
          @click="closeLightbox"
          aria-label="关闭"
        >&#10005;</button>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, nextTick, onMounted, onUnmounted } from 'vue'
import { Icon } from '@iconify/vue'
import { resolveFilePath, getLocalFallback } from '../../utils/resolvePath'

const props = defineProps({
  screenshots: {
    type: Array,
    required: true
  },
  projectTitle: {
    type: String,
    default: ''
  }
})

const resolvedScreenshots = computed(() => {
  return props.screenshots.map(s => resolveFilePath(s))
})

// 每张截图的 public 目录降级 URL（按索引记录）
const screenshotFallbacks = ref({})

// 实际显示的 URL（优先使用降级 URL）
const displayScreenshots = computed(() => {
  return resolvedScreenshots.value.map((url, index) => {
    return screenshotFallbacks.value[index] || url
  })
})

const lightboxIndex = ref(null)
const loadedImages = ref(new Set())
const imageErrors = ref(new Set())
const lightboxRef = ref(null)

function openLightbox(index) {
  lightboxIndex.value = index
  nextTick(() => {
    lightboxRef.value?.focus()
  })
}

function closeLightbox() {
  lightboxIndex.value = null
}

function prevImage() {
  const len = props.screenshots.length
  lightboxIndex.value = (lightboxIndex.value - 1 + len) % len
}

function nextImage() {
  const len = props.screenshots.length
  lightboxIndex.value = (lightboxIndex.value + 1) % len
}

function onImageLoad(index) {
  const next = new Set(loadedImages.value)
  next.add(index)
  loadedImages.value = next
}

function onImageError(index) {
  const rawPath = props.screenshots[index]
  // 还没尝试过降级 → 先尝试 public 目录
  if (rawPath && !screenshotFallbacks.value[index]) {
    screenshotFallbacks.value = { ...screenshotFallbacks.value, [index]: getLocalFallback(rawPath) }
    return
  }
  // 降级也失败了 → 显示破碎图标占位符
  const next = new Set(imageErrors.value)
  next.add(index)
  imageErrors.value = next
}

function handleKeydown(e) {
  if (lightboxIndex.value === null) return

  switch (e.key) {
    case 'ArrowLeft':
      e.preventDefault()
      prevImage()
      break
    case 'ArrowRight':
      e.preventDefault()
      nextImage()
      break
    case 'Escape':
      e.preventDefault()
      closeLightbox()
      break
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
/* ============================================================
   ProjectScreenshots — 容器
   ============================================================ */

.project-screenshots {
  margin-top: 2rem;
}

.screenshots-title {
  font-size: 1.5rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin-bottom: 1.25rem;
}

/* ============================================================
   缩略图网格
   ============================================================ */

.screenshots-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.screenshot-item {
  position: relative;
  aspect-ratio: 16 / 9;
  border-radius: var(--radius-md);
  overflow: hidden;
  cursor: pointer;
  transition: transform var(--transition-base);
}

.screenshot-item:hover {
  transform: scale(1.02);
}

.screenshot-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}

/* ============================================================
   骨架占位
   ============================================================ */

.screenshot-skeleton {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.05) 25%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0.05) 75%
  );
}

/* ============================================================
   加载失败占位
   ============================================================ */

.screenshot-error {
  position: absolute;
  inset: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.05);
  color: var(--color-text-secondary);
  font-size: 2rem;
}

/* ============================================================
   灯箱
   ============================================================ */

.lightbox {
  position: fixed;
  inset: 0;
  z-index: 1000;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

.lightbox-image {
  max-width: 90vw;
  max-height: 85vh;
  object-fit: contain;
}

/* 切换按钮 */
.lightbox-nav {
  position: fixed;
  top: 50%;
  transform: translateY(-50%);
  background: rgba(0, 0, 0, 0.5);
  color: #fff;
  border: none;
  font-size: 3rem;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  cursor: pointer;
  z-index: 1001;
  transition: background var(--transition-fast);
  line-height: 1;
}

.lightbox-nav:hover {
  background: rgba(0, 0, 0, 0.8);
}

.lightbox-prev {
  left: 1rem;
}

.lightbox-next {
  right: 1rem;
}

/* 关闭按钮 */
.lightbox-close {
  position: fixed;
  top: 1rem;
  right: 1rem;
  background: rgba(0, 0, 0, 0.5);
  color: #fff;
  border: none;
  font-size: 1.5rem;
  width: 44px;
  height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  cursor: pointer;
  z-index: 1001;
  transition: background var(--transition-fast);
}

.lightbox-close:hover {
  background: rgba(0, 0, 0, 0.8);
}

/* ============================================================
   响应式设计
   ============================================================ */

@media (max-width: 768px) {
  .screenshots-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .lightbox-nav {
    font-size: 2.5rem;
    width: 44px;
    height: 44px;
  }
}

@media (max-width: 480px) {
  .screenshots-grid {
    grid-template-columns: 1fr;
  }

  .lightbox-image {
    max-width: 95vw;
  }
}

/* ============================================================
   无障碍：减少动画偏好
   ============================================================ */

@media (prefers-reduced-motion: reduce) {
  .screenshot-item {
    transition: none;
  }

  .lightbox-nav,
  .lightbox-close {
    transition: none;
  }
}
</style>
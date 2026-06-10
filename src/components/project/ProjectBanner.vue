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
    <!-- 无封面图时显示渐变背景 + 项目名称首字母 -->
    <div
      v-else
      class="banner-placeholder"
      :style="gradientStyle"
    >
      <span class="banner-brand">{{ brandName }}</span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  project: {
    type: Object,
    required: true
  }
})

// 根据项目 id 返回品牌名称
const brandName = computed(() => {
  const id = props.project?.id
  const names = {
    1: '鲜途智送',
    2: '昕悦读',
    3: 'xinysoft'
  }
  return names[id] || ''
})

// 根据项目 id 计算渐变色（与 ProjectCard 保持一致）
const gradientStyle = computed(() => {
  const id = props.project?.id
  const gradients = {
    1: 'linear-gradient(135deg, #e94560 0%, #ff6b81 100%)',  // 鲜途智送 — 粉红→浅粉
    2: 'linear-gradient(135deg, #2b5876 0%, #4e4376 100%)',  // 昕悦读 — 深海蓝→暮光紫
    3: 'linear-gradient(135deg, #303d7a 0%, #6b4794 100%)'   // xinysoft — 靛蓝→紫罗兰
  }
  return {
    background: gradients[id] || gradients[1]
  }
})
</script>

<style scoped>
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

.banner-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  background-size: 250% 250%;
  animation: bannerGradientShift 6s ease-in-out infinite alternate;
}

@keyframes bannerGradientShift {
  0%   { background-position: 0% 0%; }
  50%  { background-position: 100% 100%; }
  100% { background-position: 0% 100%; }
}

.banner-brand {
  font-size: 4rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  user-select: none;
  transition: transform 0.3s ease;
}

.banner-placeholder:hover .banner-brand {
  transform: scale(1.05);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .project-banner {
    aspect-ratio: 4 / 3;
  }

  .banner-brand {
    font-size: 3rem;
  }
}

@media (max-width: 480px) {
  .banner-brand {
    font-size: 2.5rem;
  }
}
</style>
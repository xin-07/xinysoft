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
      <span class="banner-letter">{{ firstLetter }}</span>
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

// 获取项目名称首字母
const firstLetter = computed(() => {
  const title = props.project?.title || ''
  return title.charAt(0).toUpperCase()
})

// 根据项目 id 计算渐变色
const gradientStyle = computed(() => {
  const id = props.project?.id
  const gradients = {
    1: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', // 蓝紫渐变
    2: 'linear-gradient(135deg, #11998e 0%, #38ef7d 100%)', // 青绿渐变
    3: 'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)'  // 橙红渐变
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
}

.banner-letter {
  font-size: 4rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  user-select: none;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .project-banner {
    aspect-ratio: 4 / 3;
  }

  .banner-letter {
    font-size: 3rem;
  }
}

@media (max-width: 480px) {
  .banner-letter {
    font-size: 2.5rem;
  }
}
</style>
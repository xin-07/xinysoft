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
    <ProjectPlaceholder
      v-else
      :brand-name="brandName"
      :gradient-style="gradientStyle"
      variant="banner"
    />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useProjectBrand } from '../../composables/useProjectBrand'
import ProjectPlaceholder from './ProjectPlaceholder.vue'

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
   Responsive Design
   ============================================================ */

@media (max-width: 768px) {
  .project-banner {
    aspect-ratio: 4 / 3;
  }
}

</style>
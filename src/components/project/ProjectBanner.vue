<template>
  <div class="project-banner">
    <!-- 有封面图时显示图片 -->
    <img
      v-if="resolvedCoverUrl"
      :src="resolvedCoverUrl"
      :alt="project.title || '项目封面'"
      class="banner-image"
      loading="lazy"
      @error="coverFallbackUrl ? handleFallbackError() : handleCoverError()"
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
import { computed, ref } from 'vue'
import { useProjectBrand } from '../../composables/useProjectBrand'
import { resolveFilePath, getLocalFallback } from '../../utils/resolvePath'
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
import { computed } from 'vue'
import { projectBrands } from '../config/techStackColors'

/**
 * 项目品牌信息 composable
 * 封装项目品牌名称、渐变样式、卡片内容样式的计算逻辑
 * @param {import('vue').Ref<number>} projectId - 项目 ID 的响应式引用
 */
export function useProjectBrand(projectId) {
  const brandName = computed(() => {
    return projectBrands[projectId.value]?.name || ''
  })

  const gradientStyle = computed(() => {
    const brand = projectBrands[projectId.value]
    if (brand) {
      return { '--card-brand-gradient': brand.gradient }
    }
    // 无品牌配置时的默认渐变
    return { '--card-brand-gradient': 'linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%)' }
  })

  const cardContentStyle = computed(() => {
    const brand = projectBrands[projectId.value]
    return { background: brand?.tint || 'transparent' }
  })

  return {
    brandName,
    gradientStyle,
    cardContentStyle
  }
}
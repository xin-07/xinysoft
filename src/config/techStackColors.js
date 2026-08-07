export const techStackColors = {
  'Vue3': '#42b883',
  'Vue 3': '#4FC08D',
  'Vue': '#4FC08D',
  'Vite': '#646CFF',
  'FastAPI': '#009688',
  'Flask': '#888888',
  'MySQL': '#4479A1',
  'Spring Boot': '#6DB33F',
  'MyBatis': '#C71A1A',
  'HarmonyOS': '#007DFE',
  'ArkTS': '#007DFE',
  'ArkUI': '#007DFE',
  'Three.js': '#888888',
  'ECharts': '#AA344D',
  '天地图 API': '#F56C6C',
  'Redis': '#DC382D',
  'JWT': '#FF6B6B',
  'PyMySQL': '#4479A1',
  'Vue Router': '#4FC08D',
  '蚂蚁群+粒子群混合算法': '#9C27B0',
}

export const getTagColor = (tech) => {
  return techStackColors[tech] || '#e94560'
}

/**
 * 返回技术栈标签的文字颜色
 * WCAG AA 优化方案：使用白色文字确保在彩色背景上的可读性
 */
export const getTagTextColor = () => {
  return '#FFFFFF'
}

/**
 * 返回技术栈标签的背景色（原色 + 60% 透明度）
 * 与白色文字搭配使用，确保 WCAG AA 对比度标准 (≥ 4.5:1)
 */
export const getTagBackgroundColor = (tech) => {
  return `color-mix(in srgb, ${getTagColor(tech)} 60%, transparent)`
}

/**
 * 项目品牌信息配置
 * 与 API 返回的 project.id 对应，ProjectCard 和 ProjectBanner 共享同一份数据
 * 新增项目时只需在这里添加一条记录
 */
export const projectBrands = {
  1: {
    name: '鲜途智送',
    gradient: 'linear-gradient(135deg, #ff6b8a 0%, #f9a8d4 100%)',
    tint: 'linear-gradient(180deg, rgba(249, 168, 212, 0.06) 0%, transparent 40%)'
  },
  2: {
    name: '昕悦读',
    gradient: 'linear-gradient(135deg, #60a5fa 0%, #22d3ee 100%)',
    tint: 'linear-gradient(180deg, rgba(34, 211, 238, 0.06) 0%, transparent 40%)'
  },
  3: {
    name: 'xinysoft',
    gradient: 'linear-gradient(135deg, #fbbf24 0%, #f87171 100%)',
    tint: 'linear-gradient(180deg, rgba(248, 113, 113, 0.06) 0%, transparent 40%)'
  },
  4: {
    name: 'Jack要加油',
    gradient: 'linear-gradient(135deg, #a855f7 0%, #6366f1 100%)',
    tint: 'transparent'
  }
}
export const techStackColors = {
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
 * 返回技术栈标签的浅色背景色（原色 + 12.5% 透明度）
 * 与 getTagColor 搭配使用，形成浅底+彩色文字风格
 */
export const getTagBackgroundColor = (tech) => {
  return `${getTagColor(tech)}20`
}

/**
 * 项目品牌信息配置
 * 与 API 返回的 project.id 对应，ProjectCard 和 ProjectBanner 共享同一份数据
 * 新增项目时只需在这里添加一条记录
 */
export const projectBrands = {
  1: {
    name: '鲜途智送',
    gradient: 'linear-gradient(135deg, #e94560 0%, #ff6b81 100%)',
    tint: 'linear-gradient(180deg, rgba(255, 107, 129, 0.06) 0%, transparent 40%)'
  },
  2: {
    name: '昕悦读',
    gradient: 'linear-gradient(135deg, #2b5876 0%, #4e4376 100%)',
    tint: 'linear-gradient(180deg, rgba(78, 67, 118, 0.06) 0%, transparent 40%)'
  },
  3: {
    name: 'xinysoft',
    gradient: 'linear-gradient(135deg, #303d7a 0%, #6b4794 100%)',
    tint: 'linear-gradient(180deg, rgba(107, 71, 148, 0.06) 0%, transparent 40%)'
  }
}
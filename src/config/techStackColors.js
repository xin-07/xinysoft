export const techStackColors = {
  'Vue 3': '#4FC08D',
  'Vue': '#4FC08D',
  'Vite': '#646CFF',
  'FastAPI': '#009688',
  'Flask': '#000000',
  'MySQL': '#4479A1',
  'Spring Boot': '#6DB33F',
  'MyBatis': '#C71A1A',
  'HarmonyOS': '#007DFE',
  'ArkTS': '#007DFE',
  'ArkUI': '#007DFE',
  'Three.js': '#000000',
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
export function resolveFilePath(path) {
  if (!path) return path
  if (path.startsWith('http://') || path.startsWith('https://')) return path
  if (path.startsWith('/api/')) return path
  return `/api/files/${encodeURIComponent(path)}`
}

/**
 * 从绝对路径中提取文件名，返回 public 目录下的相对路径作为降级方案
 * 例: D:\File\photos\落日.jpg → /落日.jpg
 *     D:/Project/web/xinysoft_Vite/public/鲜途智送-首页.png → /鲜途智送-首页.png
 */
export function getLocalFallback(path) {
  if (!path) return path
  const filename = path.replace(/[/\\]/g, '/').split('/').pop()
  return filename ? `/${filename}` : path
}

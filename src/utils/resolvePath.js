export function resolveFilePath(path) {
  if (!path) return path
  // 网络地址直接返回
  if (path.startsWith('http://') || path.startsWith('https://')) return path
  // 后端 API 路径直接返回（向后兼容）
  if (path.startsWith('/api/')) return path
  // 根相对路径（如 /鲜途智送-首页.png）→ 直接指向 public 目录静态文件
  if (path.startsWith('/')) return path
  // 绝对路径 → 通过后端代理访问（向后兼容旧数据格式）
  return `/api/files/${encodeURIComponent(path)}`
}

/**
 * 从路径中提取文件名，返回 public 目录下的相对路径作为降级方案
 * 支持绝对路径、URL 编码路径、/api/files/ 路径等多种格式
 *
 * 例: D:\File\photos\落日.jpg → /落日.jpg
 *     /api/files/D%3A/.../%E9%B2%9C%E9%80%94.png → /鲜途智送.png（自动解码）
 *     /鲜途智送-首页.png → /鲜途智送-首页.png（已是根相对路径，直接返回）
 */
export function getLocalFallback(path) {
  if (!path) return path
  // 已经是根相对路径（新后端格式），无需转换
  if (path.startsWith('/')) return path
  const filename = path.replace(/[/\\]/g, '/').split('/').pop()
  let decoded
  try { decoded = decodeURIComponent(filename || '') } catch { decoded = filename }
  return decoded ? `/${decoded}` : path
}

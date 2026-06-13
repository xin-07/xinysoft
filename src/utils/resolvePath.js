export function resolveFilePath(path) {
  if (!path) return path
  if (path.startsWith('http://') || path.startsWith('https://')) return path
  if (path.startsWith('/api/')) return path
  return `/api/files/${encodeURIComponent(path)}`
}

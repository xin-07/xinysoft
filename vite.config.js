import { defineConfig, loadEnv } from 'vite'
import vue from '@vitejs/plugin-vue'
import { fileURLToPath, URL } from 'node:url'
import http from 'node:http'

// 固定后备地址
const FALLBACK_API_TARGET = 'http://127.0.0.1:8000'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')
  const primaryTarget = env.VITE_API_TARGET

  return {
    plugins: [vue()],
    resolve: {
      alias: {
        '@': fileURLToPath(new URL('./src', import.meta.url))
      }
    },
    server: {
      // 方案一：自定义代理中间件，主后端不可达时自动切换后备地址
      configureServer(server) {
        const proxyRequest = (target, req, res) => {
          return new Promise((resolve, reject) => {
            const url = new URL(req.url, target)
            const proxyReq = http.request(
              url,
              {
                method: req.method,
                headers: req.headers
              },
              (proxyRes) => {
                res.writeHead(proxyRes.statusCode, proxyRes.headers)
                proxyRes.pipe(res)
                resolve()
              }
            )
            proxyReq.on('error', reject)
            // 有请求体时 pipe 过去
            if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(req.method)) {
              req.pipe(proxyReq)
            } else {
              proxyReq.end()
            }
          })
        }

        server.middlewares.use('/api', async (req, res, next) => {
          try {
            await proxyRequest(primaryTarget, req, res)
          } catch (err) {
            console.warn(`[Proxy] 主后端 ${primaryTarget} 不可达: ${err.message}`)
            console.warn(`[Proxy] 尝试后备地址 ${FALLBACK_API_TARGET}`)
            try {
              await proxyRequest(FALLBACK_API_TARGET, req, res)
            } catch (fallbackErr) {
              console.error(`[Proxy] 后备地址也失败: ${fallbackErr.message}`)
              res.writeHead(502, { 'Content-Type': 'application/json' })
              res.end(JSON.stringify({ error: '后端服务不可用' }))
            }
          }
        })
      }
    }
  }
})
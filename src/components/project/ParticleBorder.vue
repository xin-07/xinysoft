<template>
  <div class="particle-border" ref="containerRef">
    <!-- Canvas 层 -->
    <canvas ref="canvasRef" class="particle-border__canvas"></canvas>

    <!-- 内容插槽 -->
    <div class="particle-border__content">
      <slot></slot>
    </div>

    <!-- 降级边框（prefers-reduced-motion 或无 Canvas 支持 或 低端设备降级） -->
    <div
      v-if="isReducedMotion || !supportsCanvas || isLowPerformance"
      class="particle-border__fallback"
      aria-hidden="true"
    ></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue'

const props = defineProps({
  // 粒子颜色（默认从 CSS 变量 --color-accent 读取）
  color: {
    type: String,
    default: ''
  },
  // 边框宽度（像素）
  borderWidth: {
    type: Number,
    default: 3
  },
  // 粒子大小范围
  particleSize: {
    type: Object,
    default: () => ({ min: 5, max: 12 })
  },
  // 粒子速度范围
  particleSpeed: {
    type: Object,
    default: () => ({ min: 0.5, max: 2 })
  },
  // 粒子生命周期（毫秒）
  particleLifetime: {
    type: Number,
    default: 3000
  },
  // 发光强度
  glowIntensity: {
    type: Number,
    default: 1.0
  },
  // 是否启用动画
  enabled: {
    type: Boolean,
    default: true
  }
})

// 计算颜色：优先使用 props.color，否则从 CSS 变量读取
const computedColor = computed(() => {
  if (props.color) return props.color
  // 从 CSS 变量读取强调色
  return getComputedStyle(document.documentElement).getPropertyValue('--color-accent').trim() || '#e94560'
})

// Refs
const containerRef = ref(null)
const canvasRef = ref(null)

// 状态
const isVisible = ref(false)
const isReducedMotion = ref(false)
const supportsCanvas = ref(true)
const isMobile = ref(false)
const isLowPerformance = ref(false) // 低端设备降级标记

// 缓存 canvas 尺寸，避免每帧调用 getBoundingClientRect
const cachedRect = ref({ width: 0, height: 0 })

// 粒子数量（移动端降级）
const maxParticles = computed(() => (isMobile.value ? 60 : 120))

// 粒子数组
let particles = []
let animationId = null
let lastTime = 0
let intersectionObserver = null
let prefersReducedMotionQuery = null
let spawnAccumulator = 0
const spawnInterval = 60 // ms
let resizeDebounceTimer = null

// 帧率监控变量
let frameCount = 0
let fpsLastTime = 0
let currentFPS = 60
const FPS_SAMPLE_SIZE = 60 // 采样帧数
const FPS_THRESHOLD = 30 // 帧率阈值
const fpsHistory = []

// 防抖函数
const debounce = (fn, delay) => {
  return (...args) => {
    if (resizeDebounceTimer) {
      clearTimeout(resizeDebounceTimer)
    }
    resizeDebounceTimer = setTimeout(() => {
      fn.apply(this, args)
      resizeDebounceTimer = null
    }, delay)
  }
}

// 检测移动设备
const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768 || 'ontouchstart' in window
}

// 检测 prefers-reduced-motion
const checkReducedMotion = () => {
  isReducedMotion.value = window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

// 检测 Canvas 支持
const checkCanvasSupport = () => {
  try {
    const testCanvas = document.createElement('canvas')
    supportsCanvas.value = !!(testCanvas.getContext && testCanvas.getContext('2d'))
  } catch {
    supportsCanvas.value = false
  }
}

// 粒子类
class Particle {
  constructor(borderWidth, props, color) {
    this.borderWidth = borderWidth
    this.props = props
    this.color = color
    this.x = 0
    this.y = 0
    this.edge = 0
    this.direction = 1
    this.speed = 0
    this.size = 0
    this.lifetime = 0
    this.age = 0
    this.opacity = 0
    this.fadeIn = true
  }

  reset(cachedRect) {
    const { borderWidth, props } = this
    const width = cachedRect.width
    const height = cachedRect.height

    // 随机选择边（0: 上, 1: 右, 2: 下, 3: 左）
    this.edge = Math.floor(Math.random() * 4)

    // 根据边设置初始位置
    switch (this.edge) {
      case 0: // 上边
        this.x = Math.random() * width
        this.y = borderWidth / 2
        break
      case 1: // 右边
        this.x = width - borderWidth / 2
        this.y = Math.random() * height
        break
      case 2: // 下边
        this.x = Math.random() * width
        this.y = height - borderWidth / 2
        break
      case 3: // 左边
        this.x = borderWidth / 2
        this.y = Math.random() * height
        break
    }

    // 随机方向（顺时针或逆时针）
    this.direction = Math.random() > 0.5 ? 1 : -1

    // 随机速度
    this.speed =
      props.particleSpeed.min + Math.random() * (props.particleSpeed.max - props.particleSpeed.min)

    // 随机大小
    this.size =
      props.particleSize.min + Math.random() * (props.particleSize.max - props.particleSize.min)

    // 生命周期
    this.lifetime = props.particleLifetime
    this.age = 0

    // 初始透明度
    this.opacity = 0
    this.fadeIn = true
  }

  update(deltaTime, cachedRect) {
    const { borderWidth } = this
    const width = cachedRect.width
    const height = cachedRect.height

    // 更新年龄
    this.age += deltaTime

    // 淡入淡出
    const fadeInDuration = this.lifetime * 0.2
    const fadeOutStart = this.lifetime * 0.6

    if (this.age < fadeInDuration) {
      // 淡入
      this.opacity = (this.age / fadeInDuration) * this.props.glowIntensity
    } else if (this.age > fadeOutStart) {
      // 淡出
      const fadeOutDuration = this.lifetime - fadeOutStart
      this.opacity =
        ((this.lifetime - this.age) / fadeOutDuration) * this.props.glowIntensity
    } else {
      // 完全可见
      this.opacity = this.props.glowIntensity
    }

    // 沿边缘移动
    const moveAmount = this.speed * (deltaTime / 16)

    switch (this.edge) {
      case 0: // 上边
        this.x += moveAmount * this.direction
        if (this.x > width - borderWidth / 2) {
          this.edge = 1
          this.x = width - borderWidth / 2
        } else if (this.x < borderWidth / 2) {
          this.edge = 3
          this.x = borderWidth / 2
        }
        break
      case 1: // 右边
        this.y += moveAmount * this.direction
        if (this.y > height - borderWidth / 2) {
          this.edge = 2
          this.y = height - borderWidth / 2
        } else if (this.y < borderWidth / 2) {
          this.edge = 0
          this.y = borderWidth / 2
        }
        break
      case 2: // 下边
        this.x -= moveAmount * this.direction
        if (this.x < borderWidth / 2) {
          this.edge = 3
          this.x = borderWidth / 2
        } else if (this.x > width - borderWidth / 2) {
          this.edge = 1
          this.x = width - borderWidth / 2
        }
        break
      case 3: // 左边
        this.y -= moveAmount * this.direction
        if (this.y < borderWidth / 2) {
          this.edge = 0
          this.y = borderWidth / 2
        } else if (this.y > height - borderWidth / 2) {
          this.edge = 2
          this.y = height - borderWidth / 2
        }
        break
    }

    // 检查是否过期
    return this.age < this.lifetime
  }

  draw(ctx) {
    if (this.opacity <= 0) return

    const { x, y, size, opacity, color } = this

    // 创建径向渐变
    const gradient = ctx.createRadialGradient(x, y, 0, x, y, size * 2)

    // 解析颜色
    const r = parseInt(color.slice(1, 3), 16)
    const g = parseInt(color.slice(3, 5), 16)
    const b = parseInt(color.slice(5, 7), 16)

    gradient.addColorStop(0, `rgba(${r}, ${g}, ${b}, ${opacity})`)
    gradient.addColorStop(0.5, `rgba(${r}, ${g}, ${b}, ${opacity * 0.5})`)
    gradient.addColorStop(1, `rgba(${r}, ${g}, ${b}, 0)`)

    ctx.fillStyle = gradient
    ctx.beginPath()
    ctx.arc(x, y, size * 2, 0, Math.PI * 2)
    ctx.fill()
  }
}

// 设置 Canvas 尺寸
const setupCanvas = () => {
  const canvas = canvasRef.value
  const container = containerRef.value
  if (!canvas || !container) return

  const rect = container.getBoundingClientRect()
  const dpr = window.devicePixelRatio || 1

  canvas.width = rect.width * dpr
  canvas.height = rect.height * dpr
  canvas.style.width = `${rect.width}px`
  canvas.style.height = `${rect.height}px`

  // 初始化缓存的 canvas 尺寸
  cachedRect.value = { width: rect.width, height: rect.height }

  const ctx = canvas.getContext('2d')
  if (ctx) {
    ctx.scale(dpr, dpr)
  }
}

// 动画循环
const animate = (currentTime) => {
  if (!isVisible.value || isReducedMotion.value || !supportsCanvas.value || !props.enabled || isLowPerformance.value) {
    animationId = null
    return
  }

  const canvas = canvasRef.value
  const ctx = canvas?.getContext('2d')
  if (!canvas || !ctx) {
    animationId = null
    return
  }

  // 使用缓存的尺寸，避免每帧调用 getBoundingClientRect
  const rect = cachedRect.value
  if (rect.width === 0 || rect.height === 0) {
    animationId = null
    return
  }

  // 计算时间差
  const deltaTime = lastTime ? currentTime - lastTime : 16
  lastTime = currentTime

  // 帧率监控
  frameCount++
  if (fpsLastTime === 0) {
    fpsLastTime = currentTime
  }

  // 每秒计算一次帧率
  if (currentTime - fpsLastTime >= 1000) {
    currentFPS = Math.round((frameCount * 1000) / (currentTime - fpsLastTime))
    fpsHistory.push(currentFPS)

    // 保持历史记录在合理范围
    if (fpsHistory.length > FPS_SAMPLE_SIZE) {
      fpsHistory.shift()
    }

    // 计算平均帧率
    const avgFPS = fpsHistory.reduce((sum, fps) => sum + fps, 0) / fpsHistory.length

    // 如果平均帧率低于阈值，触发降级
    if (avgFPS < FPS_THRESHOLD && fpsHistory.length >= 10) {
      console.warn(`[ParticleBorder] 性能降级：平均帧率 ${avgFPS.toFixed(1)} FPS 低于阈值 ${FPS_THRESHOLD} FPS`)
      isLowPerformance.value = true
      stopAnimation()
      return
    }

    // 重置计数器
    frameCount = 0
    fpsLastTime = currentTime
  }

  // 清空画布
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  // 设置混合模式
  ctx.globalCompositeOperation = 'lighter'

  // 更新和绘制粒子
  particles = particles.filter((particle) => {
    const alive = particle.update(deltaTime, rect)
    if (alive) {
      particle.draw(ctx)
    }
    return alive
  })

  // 粒子生成节流：每 spawnInterval 毫秒生成一次新粒子
  spawnAccumulator += deltaTime
  if (spawnAccumulator >= spawnInterval) {
    spawnAccumulator = 0
    if (particles.length < maxParticles.value) {
      const newParticle = new Particle(props.borderWidth, props, computedColor.value)
      newParticle.reset(rect)
      particles.push(newParticle)
    }
  }

  // 继续动画
  animationId = requestAnimationFrame(animate)
}

// 开始动画
const startAnimation = () => {
  if (animationId) return
  lastTime = 0
  // 重置帧率监控变量
  frameCount = 0
  fpsLastTime = 0
  fpsHistory.length = 0
  animationId = requestAnimationFrame(animate)
}

// 停止动画
const stopAnimation = () => {
  if (animationId) {
    cancelAnimationFrame(animationId)
    animationId = null
  }
}

// 设置 IntersectionObserver
const setupIntersectionObserver = () => {
  if (!containerRef.value) return

  intersectionObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        isVisible.value = entry.isIntersecting
        if (entry.isIntersecting && props.enabled && !isReducedMotion.value && !isLowPerformance.value) {
          startAnimation()
        } else {
          stopAnimation()
        }
      })
    },
    {
      threshold: 0.1,
      rootMargin: '50px'
    }
  )

  intersectionObserver.observe(containerRef.value)
}

// 清理 IntersectionObserver
const cleanupIntersectionObserver = () => {
  if (intersectionObserver) {
    intersectionObserver.disconnect()
    intersectionObserver = null
  }
}

// 处理窗口大小变化
const handleResize = () => {
  checkMobile()
  setupCanvas()
  // 更新缓存的 canvas 尺寸
  const canvas = canvasRef.value
  if (canvas) {
    const rect = canvas.getBoundingClientRect()
    cachedRect.value = { width: rect.width, height: rect.height }
  }
  // 重置粒子并重启/停止动画
  particles = []
  lastTime = 0
  spawnAccumulator = 0
  if (isVisible.value && props.enabled && !isReducedMotion.value && !isLowPerformance.value) {
    startAnimation()
  } else {
    stopAnimation()
  }
}

// 防抖版本的 resize 处理（150ms 延迟）
const debouncedHandleResize = debounce(handleResize, 150)

// 监听 enabled 变化
watch(
  () => props.enabled,
  (newVal) => {
    if (newVal && isVisible.value && !isReducedMotion.value && !isLowPerformance.value) {
      startAnimation()
    } else {
      stopAnimation()
    }
  }
)

// 监听 prefers-reduced-motion 变化
watch(isReducedMotion, (newVal) => {
  if (newVal) {
    stopAnimation()
    particles = []
  } else if (isVisible.value && props.enabled && !isLowPerformance.value) {
    startAnimation()
  }
})

// 监听低端设备降级状态变化
watch(isLowPerformance, (newVal) => {
  if (newVal) {
    stopAnimation()
    particles = []
    console.warn('[ParticleBorder] 已降级到虚线边框模式')
  }
})

// 生命周期
onMounted(() => {
  checkCanvasSupport()
  checkReducedMotion()
  checkMobile()

  if (supportsCanvas.value && !isReducedMotion.value && !isLowPerformance.value) {
    setupCanvas()
    setupIntersectionObserver()
    window.addEventListener('resize', debouncedHandleResize)

    // 监听 prefers-reduced-motion 变化
    prefersReducedMotionQuery = window.matchMedia('(prefers-reduced-motion: reduce)')
    prefersReducedMotionQuery.addEventListener('change', checkReducedMotion)
  }
})

onUnmounted(() => {
  stopAnimation()
  cleanupIntersectionObserver()
  window.removeEventListener('resize', debouncedHandleResize)

  // 清理防抖计时器
  if (resizeDebounceTimer) {
    clearTimeout(resizeDebounceTimer)
    resizeDebounceTimer = null
  }

  // 移除 mediaQuery 监听器
  if (prefersReducedMotionQuery) {
    prefersReducedMotionQuery.removeEventListener('change', checkReducedMotion)
    prefersReducedMotionQuery = null
  }

  // 清理帧率监控变量
  fpsHistory.length = 0
  frameCount = 0
  fpsLastTime = 0

  particles = []
})
</script>

<style scoped>
.particle-border {
  position: relative;
  border-radius: var(--radius-md, 12px);
  overflow: hidden;
}

.particle-border__canvas {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 1;
}

.particle-border__content {
  position: relative;
  z-index: 2;
  width: 100%;
  height: 100%;
}

.particle-border__fallback {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  pointer-events: none;
  z-index: 0;
  border: 2px dashed var(--color-border, rgba(255, 255, 255, 0.2));
  opacity: 0.5;
}

/* 响应式调整 */
@media (max-width: 768px) {
  .particle-border__fallback {
    border-width: 1px;
  }
}

/* 无障碍：减少动画偏好支持 */
@media (prefers-reduced-motion: reduce) {
  .particle-border__canvas {
    display: none;
  }
}
</style>
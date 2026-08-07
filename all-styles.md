# xinysoft 项目样式体系文档

> 生成时间：2026-06-11  
> 覆盖 `src/` 下全部 15 个文件的样式代码（从 `<style>` 块中完整提取，包含所有注释）

---

## 1. `src/style.css` — 全局样式与 CSS 变量

```css
/* 全局样式和 CSS 变量 */

/* Geist 字体 (使用 Outfit 作为 Google Fonts 替代方案) */
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&display=swap');

/* 默认暗色主题 */
:root,
:root[data-theme="dark"] {
  /* 主色板 */
  --color-bg-primary: #1a1a2e;      /* 深蓝黑底色 */
  --color-bg-secondary: #16213e;    /* 稍浅的二级背景 */
  --color-surface: #0f3460;         /* 卡片/区域表面色 */
  --color-accent: #e94560;          /* 强调色（如按钮、高亮） */
  --color-accent-light: rgba(233, 69, 96, 0.1); /* 标签背景 */
  --color-accent-hover: #d13a52;                /* 强调色悬停态 */

  /* 文本色 */
  --color-text-primary: #e6e6e6;    /* 主要文字 */
  --color-text-secondary: #a6a6a6;  /* 次要/描述文字 */
  --color-text-on-accent: #ffffff;  /* 强调色上的文字 */

  /* 导航栏背景色 */
  --color-navbar-bg: rgba(26, 26, 46, 0.95);
  --color-navbar-bg-solid: rgba(26, 26, 46, 0.98);
  --color-navbar-border: rgba(255,255,255,0.1);

  /* 通用边框色 */
  --color-border: rgba(255, 255, 255, 0.1);

  /* 字体栈 */
  --font-sans: 'Outfit', system-ui, sans-serif;
  --font-mono: 'Fira Code', 'Consolas', 'Monaco', 'Andale Mono', 'Ubuntu Mono', monospace;

  /* 响应式断点 */
  --breakpoint-tablet: 1200px;
  --breakpoint-mobile: 768px;
  --breakpoint-xl: 1440px;
  --breakpoint-2xl: 1920px;

  /* 间距系统 */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  --spacing-2xl: 3rem;
  --spacing-3xl: 4rem;
  --spacing-4xl: 5rem;
  --spacing-5xl: 6rem;

  /* 圆角 */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --radius-full: 9999px;

  /* 阴影 */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.1);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.15);
  --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.2);
  --shadow-xl: 0 16px 48px rgba(0, 0, 0, 0.25);

  /* 过渡 */
  --transition-fast: 0.15s ease;
  --transition-base: 0.3s ease;
  --transition-slow: 0.5s ease;
}

/* 亮色主题 */
:root[data-theme="light"] {
  /* 主色板 */
  --color-bg-primary: #f8f9fa;
  --color-bg-secondary: #ffffff;
  --color-surface: #e9ecef;

  /* 文本色 */
  --color-text-primary: #212529;
  --color-text-secondary: #6c757d;

  /* 强调色 */
  --color-accent: #e94560;
  --color-accent-light: rgba(233, 69, 96, 0.15);
  --color-accent-hover: #c2304a;                /* 强调色悬停态（亮色稍深） */

  /* 导航栏背景色 */
  --color-navbar-bg: rgba(248, 249, 250, 0.95);
  --color-navbar-bg-solid: rgba(255, 255, 255, 0.98);
  --color-navbar-border: rgba(0,0,0,0.1);

  /* 通用边框色 */
  --color-border: rgba(0, 0, 0, 0.1);

  /* 阴影（亮色主题使用更柔和的阴影） */
  --shadow-sm: 0 2px 8px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 16px rgba(0, 0, 0, 0.08);
  --shadow-lg: 0 8px 32px rgba(0, 0, 0, 0.12);
  --shadow-xl: 0 16px 48px rgba(0, 0, 0, 0.15);

  /* 字体栈 */
  --font-sans: 'Outfit', system-ui, sans-serif;
  --font-mono: 'Fira Code', 'Consolas', 'Monaco', 'Andale Mono', 'Ubuntu Mono', monospace;

  /* 响应式断点 */
  --breakpoint-tablet: 1200px;
  --breakpoint-mobile: 768px;
  --breakpoint-xl: 1440px;
  --breakpoint-2xl: 1920px;

  /* 间距系统 */
  --spacing-xs: 0.25rem;
  --spacing-sm: 0.5rem;
  --spacing-md: 1rem;
  --spacing-lg: 1.5rem;
  --spacing-xl: 2rem;
  --spacing-2xl: 3rem;
  --spacing-3xl: 4rem;
  --spacing-4xl: 5rem;
  --spacing-5xl: 6rem;

  /* 圆角 */
  --radius-sm: 8px;
  --radius-md: 12px;
  --radius-lg: 16px;
  --radius-xl: 24px;
  --radius-full: 9999px;

  /* 过渡 */
  --transition-fast: 0.15s ease;
  --transition-base: 0.3s ease;
  --transition-slow: 0.5s ease;
}

/* 全局重置 */
*,
*::before,
*::after {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}


html {
  font-size: 16px;
  scroll-behavior: smooth;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  margin: 0;
  font-family: var(--font-sans);
  font-size: 1rem;
  line-height: 1.6;
  color: var(--color-text-primary);
  background: var(--color-bg-primary);
  overflow-x: hidden;
}

/* 标题样式 */
h1, h2, h3, h4, h5, h6 {
  margin: 0;
  font-weight: 600;
  line-height: 1.2;
  color: var(--color-text-primary);
}

h1 {
  font-size: 3.5rem;
}

h2 {
  font-size: 2.5rem;
}

h3 {
  font-size: 1.75rem;
}

h4 {
  font-size: 1.25rem;
}

h5 {
  font-size: 1rem;
}

h6 {
  font-size: 0.875rem;
}

/* 段落样式 */
p {
  margin: 0;
  line-height: 1.6;
  color: var(--color-text-secondary);
}

/* 链接样式 */
a {
  color: var(--color-accent);
  text-decoration: none;
  transition: color var(--transition-base);
}

a:hover {
  color: var(--color-text-primary);
}

/* 链接焦点样式 */
a:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* :focus 样式回退（兼容不支持 :focus-visible 的浏览器） */
a:focus {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* 按钮样式 */
button {
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
  color: inherit;
  background: none;
  border: none;
  cursor: pointer;
  outline: none;
}

button:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* :focus 样式回退（兼容不支持 :focus-visible 的浏览器） */
button:focus {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* 输入框样式 */
input,
textarea,
select {
  font-family: inherit;
  font-size: inherit;
  line-height: inherit;
  color: var(--color-text-primary);
  background: var(--color-surface);
  border: 1px solid rgba(233, 69, 96, 0.2);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  outline: none;
  transition: border-color var(--transition-base), box-shadow var(--transition-base);
}

input:focus,
textarea:focus,
select:focus {
  border-color: var(--color-accent);
  box-shadow: 0 0 0 3px rgba(233, 69, 96, 0.1);
}

/* 图片样式 */
img {
  max-width: 100%;
  height: auto;
  display: block;
}

/* 列表样式 */
ul,
ol {
  list-style: none;
  margin: 0;
  padding: 0;
}

/* 滚动条样式 */
::-webkit-scrollbar {
  width: 8px;
  height: 8px;
}

::-webkit-scrollbar-track {
  background: var(--color-bg-secondary);
}

::-webkit-scrollbar-thumb {
  background: var(--color-surface);
  border-radius: var(--radius-full);
}

::-webkit-scrollbar-thumb:hover {
  background: var(--color-accent);
}

/* 选择文本样式 */
::selection {
  background: rgba(233, 69, 96, 0.3);
  color: var(--color-text-primary);
}

/* 响应式字体大小 */
@media (max-width: 1200px) {
  html {
    font-size: 15px;
  }

  h1 {
    font-size: 3rem;
  }

  h2 {
    font-size: 2.25rem;
  }

  h3 {
    font-size: 1.5rem;
  }
}

@media (max-width: 768px) {
  html {
    font-size: 14px;
  }

  h1 {
    font-size: 2.5rem;
  }

  h2 {
    font-size: 2rem;
  }

  h3 {
    font-size: 1.25rem;
  }
}

@media (max-width: 480px) {
  html {
    font-size: 13px;
  }

  h1 {
    font-size: 2rem;
  }

  h2 {
    font-size: 1.75rem;
  }

  h3 {
    font-size: 1.125rem;
  }
}

/* 超大屏幕断点 */
@media (min-width: 1440px) {
  html {
    font-size: 16px;
  }

  /* 超大屏幕容器适配 */
  .projects-container,
  .hero-container,
  .footer-content,
  .navbar-content,
  .featured-projects-container {
    max-width: 1400px;
  }

  /* 超大屏幕网格适配 - 4列 */
  .projects-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (min-width: 1920px) {
  html {
    font-size: 17px;
  }

  /* 超宽屏容器适配 */
  .projects-container,
  .hero-container,
  .footer-content,
  .navbar-content,
  .featured-projects-container {
    max-width: 1600px;
  }

  /* 超宽屏网格适配 - 保持4列 */
  .projects-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

/* 动画工具类 */
.fade-in {
  animation: fadeIn 0.6s ease-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

.slide-up {
  animation: slideUp 0.6s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.slide-down {
  animation: slideDown 0.6s ease-out;
}

@keyframes slideDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 辅助类 */
.text-center {
  text-align: center;
}

.text-left {
  text-align: left;
}

.text-right {
  text-align: right;
}

.visually-hidden {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

/* 禁用状态 */
.disabled {
  opacity: 0.5;
  cursor: not-allowed;
  pointer-events: none;
}

/* 加载状态 */
.loading {
  position: relative;
  overflow: hidden;
}

.loading::after {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.1) 50%,
    transparent 100%
  );
  animation: loading 1.5s ease-in-out infinite;
}

@keyframes loading {
  0% {
    transform: translateX(-100%);
  }
  100% {
    transform: translateX(100%);
  }
}

/* 首次加载防闪烁 */
.disable-transition *,
.disable-transition *::before,
.disable-transition *::after {
  transition: none !important;
}

/* ===== 骨架屏（Skeleton）工具类 ===== */
/* 用法：在骨架屏元素的 style 中加入 background-image 覆盖具体渐变色，然后加上 .skeleton-shimmer 类即可 */
@keyframes skeleton-shimmer {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

.skeleton-shimmer {
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s ease-in-out infinite;
}

.skeleton-block {
  background: linear-gradient(
    90deg,
    rgba(255, 255, 255, 0.05) 25%,
    rgba(255, 255, 255, 0.1) 50%,
    rgba(255, 255, 255, 0.05) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s ease-in-out infinite;
  border-radius: var(--radius-sm);
}

/* ===== 边框特效模块 ===== */
@import './styles/border-effects.css';
```

---

## 2. `src/styles/border-effects.css` — 边框特效系统

```css
/* 边框特效样式模块 */

/**
 * 浏览器兼容性说明：
 * - 目标浏览器：Chrome、Edge、Firefox、Safari 最新版本
 * - 效果2 (fade-glow)：需要支持 CSS mask 和 linear-gradient
 * - 效果4 (nebula)：需要支持 conic-gradient 和 CSS animation
 * - 对于不支持这些特性的浏览器，会自动降级为简单边框
 * - 所有效果都支持 prefers-reduced-motion 媒体查询
 */

/* ===== 浏览器兼容性回退 ===== */
/* 对于不支持 mask、conic-gradient 的浏览器，提供简单边框回退 */
@supports not (mask: linear-gradient(#fff 0 0)) {
  .border--fade-glow {
    border: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
  }
}

@supports not (background: conic-gradient(from 0deg, red, blue)) {
  .border--nebula {
    border: 2px solid var(--color-border, rgba(255, 255, 255, 0.1));
    box-shadow: 0 0 20px rgba(233, 69, 96, 0.3);
  }
}

/* ===== CSS 变量定义 ===== */
:root {
  /* 边框特效基础变量 */
  --border-width: 6px;
  --nebula-duration: 10s;

  /* 发光颜色 */
  --border-glow-color: rgba(255, 255, 255, 0.3);
  --border-glow-color-hover: rgba(255, 255, 255, 0.5);

  /* 星云颜色序列 - 高对比度、高饱和度，确保与暗色背景有明显区分 */
  --nebula-color-1: #e94560;  /* 玫红色 - 亮 */
  --nebula-color-2: #9b59b6;  /* 紫色 - 亮 */
  --nebula-color-3: #3498db;  /* 蓝色 - 亮 */
  --nebula-color-4: #e74c3c;  /* 红橙色 - 亮 */
  --nebula-color-5: #f39c12;  /* 金橙色 - 亮 */
}

/* 亮色主题调整 */
:root[data-theme="light"] {
  --border-glow-color: rgba(0, 0, 0, 0.12);
  /* 星云颜色序列 - 高饱和度，确保与亮色背景有明显对比 */
  --nebula-color-1: #e94560;  /* 玫红色 - 高饱和 */
  --nebula-color-2: #9b59b6;  /* 紫色 - 高饱和 */
  --nebula-color-3: #3498db;  /* 蓝色 - 高饱和 */
  --nebula-color-4: #e74c3c;  /* 红橙色 - 高饱和 */
  --nebula-color-5: #f39c12;  /* 金橙色 - 高饱和 */
}

/* ===== 效果2：淡出至透明 + 轻微发光 ===== */
/* 类名：border--fade-glow */
.border--fade-glow {
  position: relative;
  border: none;
  border-radius: var(--radius-md);
  background: var(--color-surface);
  overflow: hidden;
}

/* 伪元素 ::before 创建模糊的渐变背景，使用径向渐变 mask 实现从边框向内淡出 */
.border--fade-glow::before {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: inherit;
  padding: var(--border-width);
  background: linear-gradient(
    135deg,
    var(--border-glow-color) 0%,
    transparent 50%,
    var(--border-glow-color) 100%
  );
  -webkit-mask:
    linear-gradient(#fff 0 0) content-box,
    radial-gradient(
      ellipse 100% 100% at center,
      transparent calc(100% - var(--border-width) * 1.5),
      #fff 100%
    );
  mask:
    linear-gradient(#fff 0 0) content-box,
    radial-gradient(
      ellipse 100% 100% at center,
      transparent calc(100% - var(--border-width) * 1.5),
      #fff 100%
    );
  -webkit-mask-composite: xor;
  mask-composite: exclude;
  opacity: 0.6;
  filter: blur(12px);
  transition: opacity var(--transition-base), filter var(--transition-base);
  pointer-events: none;
}

/* 确保内容在伪元素之上 */
.border--fade-glow > * {
  position: relative;
  z-index: 1;
}

/* hover 时增强发光效果 */
.border--fade-glow:hover::before,
.border--fade-glow:focus-within::before {
  background: linear-gradient(
    135deg,
    var(--border-glow-color-hover) 0%,
    transparent 50%,
    var(--border-glow-color-hover) 100%
  );
  opacity: 1;
  filter: blur(16px);
}

/* focus 状态支持 */
.border--fade-glow:focus {
  outline: none;
}

.border--fade-glow:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* ===== 效果4：星云流光边框 ===== */
/* 类名：border--nebula */
.border--nebula {
  position: relative;
  border: none;
  border-radius: var(--radius-md);
  background: var(--color-surface);
  overflow: hidden;
  isolation: isolate;
}

/* 使用 conic-gradient 创建锥形渐变 */
.border--nebula::before {
  content: '';
  position: absolute;
  inset: calc(var(--border-width) * -1);
  border-radius: inherit;
  background: conic-gradient(
    from 0deg,
    var(--nebula-color-1),
    var(--nebula-color-2),
    var(--nebula-color-3),
    var(--nebula-color-4),
    var(--nebula-color-5),
    var(--nebula-color-1)
  );
  animation: nebula-rotate var(--nebula-duration) linear infinite;
  filter: blur(16px) saturate(1.5);
  opacity: 0.7;
  pointer-events: none;
  z-index: 0;
}

/* 伪元素 ::after 覆盖内层 */
.border--nebula::after {
  content: '';
  position: absolute;
  inset: var(--border-width);
  border-radius: calc(var(--radius-md) - var(--border-width));
  background: conic-gradient(
    from 0deg,
    var(--nebula-color-1),
    var(--nebula-color-2),
    var(--nebula-color-3),
    var(--nebula-color-4),
    var(--nebula-color-5),
    var(--nebula-color-1)
  );
  filter: blur(20px) saturate(1.8);
  opacity: 0.5;
  pointer-events: none;
  z-index: 1;
}

/* 确保内容在伪元素之上 */
.border--nebula > * {
  position: relative;
  z-index: 2;
}

/* 星云旋转动画 */
@keyframes nebula-rotate {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

/* hover 时增强效果 */
.border--nebula:hover::before,
.border--nebula:focus-within::before {
  opacity: 1;
  filter: blur(20px) saturate(2);
}

/* focus 状态支持 */
.border--nebula:focus {
  outline: none;
}

.border--nebula:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* ===== 无障碍：减少动画偏好支持 ===== */
@media (prefers-reduced-motion: reduce) {
  .border--fade-glow::before,
  .border--nebula::before {
    animation: none;
    transition: none;
  }

  .border--nebula::before {
    transform: rotate(0deg);
  }
}

/* ===== 渐变动画 - 全局定义 ===== */
@keyframes gradientShift {
  0%   { background-position: 0% 0%; }
  50%  { background-position: 100% 100%; }
  100% { background-position: 0% 100%; }
}
```

---

## 3. `src/App.vue` — 根组件

```css
#app {
  width: 100%;
  min-height: 100vh;
}

/* 页面切换过渡动画 */
.page-enter-active,
.page-leave-active {
  transition: opacity 0.25s ease, transform 0.25s ease;
}

.page-enter-from {
  opacity: 0;
  transform: translateY(12px);
}

.page-leave-to {
  opacity: 0;
  transform: translateY(-12px);
}
```

---

## 4. `src/components/Navbar.vue` — 导航栏

```css
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: var(--color-navbar-bg);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid transparent;
  transition: all 0.3s ease;
}

.navbar-scrolled {
  border-bottom-color: var(--color-navbar-border);
  box-shadow: var(--shadow-md);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  height: 70px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--color-text-primary);
  text-decoration: none;
  letter-spacing: -0.5px;
  transition: color 0.3s ease;
}

.logo:hover {
  color: var(--color-accent);
}

.nav-links {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: var(--color-text-secondary);
  text-decoration: none;
  font-size: 0.95rem;
  font-weight: 500;
  position: relative;
  transition: color 0.3s ease;
}

.nav-link::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 0;
  height: 2px;
  background: var(--color-accent);
  transition: width 0.3s ease;
}

.nav-link:hover,
.nav-link.active {
  color: var(--color-text-primary);
}

.nav-link.active::after,
.nav-link:hover::after {
  width: 100%;
}

/* PC端主题切换按钮 */
.theme-toggle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-full);
  background: transparent;
  border: 1px solid var(--color-accent-light);
  cursor: pointer;
  transition: all 0.3s ease;
}

.theme-toggle:hover {
  background: var(--color-accent-light);
  border-color: var(--color-accent);
}

.theme-toggle:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

.theme-icon {
  font-size: 1.2rem;
  display: inline-block;
  transition: transform 0.3s ease;
}

.theme-toggle:hover .theme-icon {
  transform: rotate(15deg);
}

.hamburger {
  display: none;
  flex-direction: column;
  gap: 5px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 10px;
  z-index: 1001;
}

.hamburger span {
  display: block;
  width: 25px;
  height: 2px;
  background: var(--color-text-primary);
  transition: all 0.3s ease;
}

.hamburger.active span:nth-child(1) {
  transform: rotate(45deg) translate(5px, 5px);
}

.hamburger.active span:nth-child(2) {
  opacity: 0;
}

.hamburger.active span:nth-child(3) {
  transform: rotate(-45deg) translate(5px, -5px);
}

.mobile-menu {
  display: none;
  position: absolute;
  top: 70px;
  left: 0;
  right: 0;
  background: var(--color-navbar-bg-solid);
  backdrop-filter: blur(10px);
  border-top: 1px solid var(--color-navbar-border);
  padding: 1rem 0;
  transform: translateY(-100%);
  opacity: 0;
  transition: all 0.3s ease;
}

.mobile-menu.open {
  transform: translateY(0);
  opacity: 1;
}

.mobile-nav-link {
  display: block;
  padding: 1rem 2rem;
  color: var(--color-text-secondary);
  text-decoration: none;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.mobile-nav-link:hover {
  color: var(--color-accent);
  background: var(--color-accent-light);
}

/* 移动端主题切换按钮 */
.mobile-theme-toggle {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  width: 100%;
  padding: 1rem 2rem;
  color: var(--color-text-secondary);
  font-size: 1rem;
  text-align: left;
  transition: all 0.3s ease;
}

.mobile-theme-toggle:hover {
  color: var(--color-accent);
  background: var(--color-accent-light);
}

.mobile-theme-toggle .theme-icon {
  font-size: 1.2rem;
}

.mobile-theme-toggle .theme-text {
  flex: 1;
}

@media (max-width: 768px) {
  .nav-links {
    display: none;
  }

  .hamburger {
    display: flex;
  }

  .mobile-menu {
    display: block;
  }

  .navbar-container {
    padding: 0 1.5rem;
  }
}
```

---

## 5. `src/components/Hero.vue` — 首页英雄区

```css
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6rem 2rem 4rem;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(circle at 20% 50%, rgba(233, 69, 96, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 50%, rgba(15, 52, 96, 0.3) 0%, transparent 50%);
  pointer-events: none;
}

.hero-container {
  max-width: 1200px;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 4rem;
  align-items: center;
  position: relative;
  z-index: 1;
}

.hero-content {
  animation: fadeInLeft 0.8s ease-out;
}

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.hero-text {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.name-title-wrapper {
  margin-bottom: 0.5rem;
}

.name {
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1.2;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 0.5rem;
}

.name-text {
  color: var(--color-text-primary);
  background: linear-gradient(135deg, var(--color-accent), #ff6b9d);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.title-divider {
  color: var(--color-text-secondary);
  font-weight: 300;
}

.title {
  font-size: 1.5rem;
  font-weight: 400;
  color: var(--color-text-secondary);
}

.bio {
  font-size: 1.125rem;
  line-height: 1.8;
  color: var(--color-text-secondary);
  max-width: 600px;
  margin: 0;
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.tech-tag {
  display: inline-block;
  padding: 0.5rem 1.25rem;
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 500;
  border: 1px solid;
  transition: background-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
  animation: fadeInUp 0.6s ease-out backwards;
  cursor: pointer;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.tech-tag:hover {
  background: color-mix(in srgb, var(--tag-color) 30%, transparent);
  transform: scale(1.05);
  box-shadow: 0 4px 15px color-mix(in srgb, var(--tag-color) 40%, transparent);
}

/* 焦点样式 */
.tech-tag:focus-visible {
  outline: 2px solid var(--tag-color);
  outline-offset: 2px;
}

.tech-tag:focus {
  outline: 2px solid var(--tag-color);
  outline-offset: 2px;
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  background: var(--color-accent);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
  box-shadow: 0 4px 15px rgba(233, 69, 96, 0.3);
  width: fit-content;
}

.cta-button:hover {
  background: #d63a52;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(233, 69, 96, 0.4);
}

.cta-button:active {
  transform: translateY(0);
}

/* 焦点样式 */
.cta-button:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

.cta-button:focus {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

.social-links {
  display: flex;
  gap: 1.5rem;
  margin-top: 0.5rem;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: rgba(15, 52, 96, 0.3);
  border: 1px solid rgba(233, 69, 96, 0.2);
  border-radius: 12px;
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: background-color 0.3s ease, border-color 0.3s ease, color 0.3s ease, transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.social-link:hover {
  background: rgba(233, 69, 96, 0.1);
  border-color: var(--color-accent);
  color: var(--color-accent);
  transform: translateY(-3px);
  box-shadow: 0 4px 15px rgba(233, 69, 96, 0.3);
}

/* 焦点样式 */
.social-link:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

.social-link:focus {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

.social-link.wechat:hover,
.social-link.wechat:focus-visible,
.social-link.wechat:focus {
  background: rgba(7, 193, 96, 0.1);
  border-color: #07c160;
  color: #07c160;
  box-shadow: 0 4px 15px rgba(7, 193, 96, 0.3);
}

.social-link.qq:hover,
.social-link.qq:focus-visible,
.social-link.qq:focus {
  background: rgba(18, 183, 245, 0.1);
  border-color: #12b7f5;
  color: #12b7f5;
  box-shadow: 0 4px 15px rgba(18, 183, 245, 0.3);
}

.hero-avatar {
  animation: fadeInRight 0.8s ease-out;
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.avatar-wrapper {
  position: relative;
  width: 320px;
  height: 320px;
}

.avatar-image,
.avatar-placeholder,
.avatar-skeleton {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-image {
  border: 4px solid var(--color-accent);
  box-shadow:
    0 0 0 8px rgba(233, 69, 96, 0.1),
    0 20px 60px rgba(0, 0, 0, 0.5);
}

.avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-accent), #ff6b9d);
  color: white;
  font-size: 8rem;
  font-weight: 700;
  border: 4px solid rgba(233, 69, 96, 0.3);
  box-shadow:
    0 0 0 8px rgba(233, 69, 96, 0.1),
    0 20px 60px rgba(0, 0, 0, 0.5);
}

.avatar-skeleton {
  background: linear-gradient(
    90deg,
    rgba(15, 52, 96, 0.3) 25%,
    rgba(15, 52, 96, 0.5) 50%,
    rgba(15, 52, 96, 0.3) 75%
  );
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s ease-in-out infinite;
  border: 4px solid rgba(233, 69, 96, 0.2);
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: 3rem;
  }

  .hero-avatar {
    order: -1;
    display: flex;
    justify-content: center;
  }

  .avatar-wrapper {
    width: 280px;
    height: 280px;
  }
}

@media (max-width: 768px) {
  .hero {
    padding: 5rem 1.5rem 3rem;
  }

  .name {
    font-size: 2.5rem;
    flex-direction: column;
    gap: 0.25rem;
  }

  .title {
    font-size: 1.125rem;
  }

  .bio {
    font-size: 1rem;
  }

  .avatar-wrapper {
    width: 220px;
    height: 220px;
  }

  .cta-button {
    width: 100%;
    justify-content: center;
  }

  .social-links {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .name {
    font-size: 2rem;
  }

  .title {
    font-size: 1rem;
  }

  .tech-tags {
    gap: 0.5rem;
  }

  .tech-tag {
    padding: 0.4rem 1rem;
    font-size: 0.85rem;
  }

  .avatar-wrapper {
    width: 180px;
    height: 180px;
  }

  .avatar-placeholder {
    font-size: 6rem;
  }
}

/* 无障碍：减少动画偏好 */
@media (prefers-reduced-motion: reduce) {
  .hero-content {
    animation: none;
  }

  .hero-avatar {
    animation: none;
  }

  .tech-tag {
    animation: none;
  }
}
```

---

## 6. `src/components/ContactModal.vue` — 联系方式弹窗

```css
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
  padding: 1rem;
  outline: none;
}

.modal-content {
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  border: 1px solid rgba(233, 69, 96, 0.2);
  box-shadow: var(--shadow-xl);
  max-width: 500px;
  width: 100%;
  position: relative;
  overflow: hidden;
}

.modal-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.5rem;
  border-bottom: 1px solid rgba(233, 69, 96, 0.1);
}

.modal-header h3 {
  margin: 0;
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary);
}

.close-btn {
  background: none;
  border: none;
  color: var(--color-text-secondary);
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 8px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  color: var(--color-accent);
  background: rgba(233, 69, 96, 0.1);
}

.modal-body {
  padding: 1rem;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  margin-bottom: 0.5rem;
  background: var(--color-surface);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.contact-item:last-child {
  margin-bottom: 0;
}

.contact-item:hover {
  background: rgba(233, 69, 96, 0.1);
  border-color: rgba(233, 69, 96, 0.3);
  transform: translateX(5px);
}

.contact-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  flex-shrink: 0;
}

.wechat-icon {
  background: linear-gradient(135deg, #07c160, #00a854);
  color: white;
}

.qq-icon {
  background: linear-gradient(135deg, #12b7f5, #0099ff);
  color: white;
}

.email-icon {
  background: linear-gradient(135deg, var(--color-accent), #ff6b9d);
  color: white;
}

.contact-info {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.contact-label {
  font-size: 0.85rem;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.contact-value {
  color: var(--color-text-primary);
  font-size: 0.95rem;
  word-break: break-all;
}

.copy-icon {
  color: var(--color-text-secondary);
  opacity: 0;
  transition: opacity 0.3s ease;
  flex-shrink: 0;
}

.contact-item:hover .copy-icon {
  opacity: 1;
}

.copy-toast {
  position: absolute;
  bottom: 1.5rem;
  left: 50%;
  transform: translateX(-50%);
  background: var(--color-accent);
  color: white;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  font-size: 0.9rem;
  animation: slideUp 0.3s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateX(-50%) translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

/* Modal transitions */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-active .modal-content,
.modal-leave-active .modal-content {
  transition: transform 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.9) translateY(-20px);
}
```

---

## 7. `src/components/Footer.vue` — 页脚

```css
.footer {
  width: 100%;
  background: var(--color-bg-secondary);
  border-top: 1px solid var(--color-navbar-border);
  padding: var(--spacing-xl) var(--spacing-lg);
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.footer-main {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-bottom: var(--spacing-lg);
  border-bottom: 1px solid var(--color-navbar-border);
}

.footer-brand {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-xs);
}

.brand-name {
  font-size: 1.25rem;
  font-weight: 600;
  color: var(--color-text-primary);
  letter-spacing: 0.5px;
}

.brand-desc {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

.footer-links {
  display: flex;
  gap: var(--spacing-md);
}

.footer-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  color: var(--color-text-secondary);
  background: var(--color-surface);
  transition: all var(--transition-base);
}

.footer-link:hover {
  color: var(--color-accent);
  background: var(--color-accent-light);
  transform: translateY(-2px);
}

.footer-bottom {
  padding-top: var(--spacing-lg);
  text-align: center;
}

.copyright {
  font-size: 0.875rem;
  color: var(--color-text-secondary);
}

/* 响应式设计 */
@media (max-width: 768px) {
  .footer {
    padding: var(--spacing-lg) var(--spacing-md);
  }

  .footer-main {
    flex-direction: column;
    gap: var(--spacing-lg);
    text-align: center;
  }

  .footer-brand {
    align-items: center;
  }

  /* 移动端触控区域优化 - WCAG触控目标尺寸建议 */
  .footer-link {
    width: 44px;
    height: 44px;
  }
}
```

---

## 8. `src/components/home/FeaturedProjects.vue` — 精选项目

```css
.featured-projects {
  padding: 4rem 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.featured-projects__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.featured-projects__title {
  font-size: 1.75rem;
  font-weight: 600;
  color: var(--color-text-primary, #ffffff);
  margin: 0;
}

.featured-projects__link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-accent, #e94560);
  text-decoration: none;
  font-size: 0.9375rem;
  font-weight: 500;
  transition: all 0.2s ease;
}

.featured-projects__link:hover {
  gap: 0.75rem;
}

/* 焦点样式 */
.featured-projects__link:focus-visible {
  outline: 2px solid var(--color-accent, #e94560);
  outline-offset: 2px;
}

.featured-projects__link:focus {
  outline: 2px solid var(--color-accent, #e94560);
  outline-offset: 2px;
}

.featured-projects__link-icon {
  transition: transform 0.2s ease;
}

.featured-projects__link:hover .featured-projects__link-icon {
  transform: translateX(4px);
}

.featured-projects__grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1.5rem;
}

/* 卡片入场动画 */
.featured-projects__grid > * {
  animation: featuredCardEntrance 0.4s ease-out both;
  animation-delay: calc(var(--card-index, 0) * 0.1s + 0.05s);
}

@keyframes featuredCardEntrance {
  from {
    opacity: 0;
    transform: translateY(24px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* 骨架屏样式 */
.featured-projects__skeleton-link {
  width: 80px;
  height: 20px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.1) 25%, rgba(255, 255, 255, 0.2) 50%, rgba(255, 255, 255, 0.1) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
  border-radius: 4px;
}

.featured-projects__skeleton-card {
  background: var(--color-surface, #1a1a2e);
  border-radius: var(--radius-md, 12px);
  overflow: hidden;
  border: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
}

.featured-projects__skeleton-cover {
  aspect-ratio: 16 / 10;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
}

.featured-projects__skeleton-content {
  padding: 1.25rem;
}

.featured-projects__skeleton-tags {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.featured-projects__skeleton-tag {
  width: 60px;
  height: 24px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
  border-radius: 9999px;
}

.featured-projects__skeleton-title {
  width: 70%;
  height: 24px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
  border-radius: 4px;
  margin-bottom: 0.75rem;
}

.featured-projects__skeleton-text {
  width: 100%;
  height: 14px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
  border-radius: 4px;
  margin-bottom: 0.5rem;
}

.featured-projects__skeleton-text--short {
  width: 60%;
}

/* 响应式设计 */
@media (max-width: 1199px) {
  .featured-projects__grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 767px) {
  .featured-projects {
    padding: 3rem 1.5rem;
  }

  .featured-projects__title {
    font-size: 1.5rem;
  }

  .featured-projects__grid {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .featured-projects__skeleton-content {
    padding: 1rem;
  }
}
```

---

## 9. `src/views/ProjectsView.vue` — 项目作品集页面

```css
.projects-view {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bg-primary);
}

.projects-main {
  flex: 1;
  padding-top: 70px; /* Navbar 高度 */
}

.projects-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 3rem 2rem;
  width: 100%;
}

/* 页面标题 */
.projects-header {
  text-align: center;
  margin-bottom: 3rem;
}

.projects-title {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin: 0 0 0.75rem 0;
}

.projects-subtitle {
  font-size: 1.125rem;
  color: var(--color-text-secondary);
  margin: 0;
}

/* 项目网格 */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2rem;
}

/* 卡片入场动画 */
.projects-grid > * {
  animation: cardEntrance 0.4s ease-out both;
  animation-delay: calc(var(--card-index, 0) * 0.1s + 0.05s);
}

@keyframes cardEntrance {
  from {
    opacity: 0;
    transform: translateY(24px) scale(0.98);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* 骨架屏 */
.skeleton-card {
  background: var(--color-surface);
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid var(--color-border);
}

.skeleton-cover {
  aspect-ratio: 16 / 10;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
}

.skeleton-content {
  padding: 1.25rem;
}

.skeleton-tags {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.skeleton-tag {
  width: 60px;
  height: 24px;
  border-radius: 9999px;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
}

.skeleton-title {
  width: 80%;
  height: 24px;
  border-radius: 4px;
  margin-bottom: 0.75rem;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
}

.skeleton-text {
  width: 100%;
  height: 16px;
  border-radius: 4px;
  margin-bottom: 0.5rem;
  background: linear-gradient(90deg, rgba(255, 255, 255, 0.05) 25%, rgba(255, 255, 255, 0.1) 50%, rgba(255, 255, 255, 0.05) 75%);
  background-size: 200% 100%;
  animation: skeleton-shimmer 1.5s infinite;
}

.skeleton-text--short {
  width: 60%;
}

/* 错误状态 */
.projects-error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.error-message {
  font-size: 1.125rem;
  color: var(--color-text-secondary);
  margin: 0 0 1.5rem 0;
}

.retry-btn {
  padding: 0.75rem 2rem;
  font-size: 1rem;
  font-weight: 500;
  color: #ffffff;
  background: var(--color-accent);
  border: none;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
}

.retry-btn:hover {
  background: var(--color-accent-hover);
  transform: translateY(-2px);
}

/* 焦点样式 */
.retry-btn:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

.retry-btn:focus {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* 空状态 */
.projects-empty {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
}

.empty-message {
  font-size: 1.125rem;
  color: var(--color-text-secondary);
  margin: 0;
}

/* 响应式布局 */
@media (max-width: 1199px) {
  .projects-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .projects-container {
    padding: 2rem 1.5rem;
  }

  .projects-title {
    font-size: 2rem;
  }

  .projects-subtitle {
    font-size: 1rem;
  }

  .projects-header {
    margin-bottom: 2rem;
  }
}

/* 600px断点 - 保持两列布局 */
@media (min-width: 600px) and (max-width: 768px) {
  .projects-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 1.5rem;
  }
}

/* 600px以下 - 单列布局 */
@media (max-width: 599px) {
  .projects-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
}
```

---

## 10. `src/components/project/ProjectCard.vue` — 项目卡片（核心组件）

```css
/* ============================================================
   ProjectCard — Base Styles
   ============================================================ */

.project-card {
  background: var(--color-surface, #1a1a2e);
  border-radius: var(--radius-md, 12px);
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease, border-color 0.3s ease;
  border: 1px solid var(--color-border, rgba(255, 255, 255, 0.1));
  display: flex;
  flex-direction: column;
  height: 100%;
}

.project-card:hover,
.project-card:focus {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg, 0 10px 40px rgba(0, 0, 0, 0.3));
  border-color: var(--color-accent, #e94560);
  outline: none;
}

.project-card:active {
  transform: translateY(-2px) scale(0.98);
}

.project-card:focus-visible {
  outline: 2px solid var(--color-accent, #e94560);
  outline-offset: 2px;
}

/* ============================================================
   Cover Area
   ============================================================ */

.project-card__cover {
  width: 100%;
  overflow: hidden;
  position: relative;
}

.project-card--featured .project-card__cover {
  aspect-ratio: 16 / 10;
}

.project-card--list .project-card__cover {
  aspect-ratio: 16 / 9;
}

.project-card__image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
  transition: transform 0.3s ease;
}

.project-card:hover .project-card__image {
  transform: scale(1.05);
}

/* ============================================================
   Placeholder — 6-Layer Visual Effects
   ============================================================ */

/* Layer 1: Brand gradient background */
.project-card__placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 120px;
  position: relative;
  overflow: hidden;

  /* Brand gradient via CSS variable injected by composable */
  background: var(--card-brand-gradient, linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%));
  background-size: 250% 250%;
  animation: gradientShift 6s ease-in-out infinite alternate;
}

/* Layer 2: Geometric grid texture (::before) */
.project-card__placeholder::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px);
  background-size: 32px 32px;
  /* Texture fades from top to bottom */
  -webkit-mask-image: linear-gradient(180deg, rgba(0, 0, 0, 0.5) 0%, transparent 85%);
  mask-image: linear-gradient(180deg, rgba(0, 0, 0, 0.5) 0%, transparent 85%);
  pointer-events: none;
  z-index: 1;
  transition: opacity 0.3s ease;
}

.project-card:hover .project-card__placeholder::before {
  /* Boost brightness via filter since opacity maxes at 1 */
  filter: brightness(1.4);
}

/* Layer 4: Diagonal light sweep (::after) */
.project-card__placeholder::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    105deg,
    transparent 38%,
    rgba(255, 255, 255, 0.05) 43%,
    rgba(255, 255, 255, 0.12) 50%,
    rgba(255, 255, 255, 0.05) 57%,
    transparent 62%
  );
  animation: lightSweep 5s ease-in-out infinite;
  pointer-events: none;
  z-index: 3;
}

.project-card:hover .project-card__placeholder::after {
  animation-duration: 2.5s;
  background: linear-gradient(
    105deg,
    transparent 38%,
    rgba(255, 255, 255, 0.08) 43%,
    rgba(255, 255, 255, 0.18) 50%,
    rgba(255, 255, 255, 0.08) 57%,
    transparent 62%
  );
}

/* Layer 3: Bottom dark gradient fade */
.placeholder-fade {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 55%;
  background: linear-gradient(
    to top,
    var(--color-surface, #0f3460) 0%,
    rgba(15, 52, 96, 0.4) 40%,
    transparent 100%
  );
  pointer-events: none;
  z-index: 2;
}

/* Layer 5: Floating geometric decorations */
.placeholder-decor {
  position: absolute;
  pointer-events: none;
  z-index: 4;
  opacity: 0.6;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.project-card:hover .placeholder-decor {
  opacity: 0.85;
}

/* Large circle — top right */
.placeholder-decor--circle {
  width: 110px;
  height: 110px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  top: -28px;
  right: -18px;
  animation: floatCircle 7s ease-in-out infinite alternate;
}

/* Ring — bottom left */
.placeholder-decor--ring {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.07);
  bottom: 18px;
  left: 14px;
  animation: floatRing 5.5s ease-in-out infinite alternate-reverse;
}

/* Small dot — middle right */
.placeholder-decor--dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.18);
  top: 38%;
  right: 22%;
  animation: floatDot 3.5s ease-in-out infinite alternate;
  box-shadow: 0 0 12px 2px rgba(255, 255, 255, 0.06);
}

/* Layer 6: First letter */
.project-card__letter {
  position: relative;
  z-index: 5;
  font-size: 1.75rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.25);
  user-select: none;
  letter-spacing: 0.1em;
  transition: transform 0.3s ease, text-shadow 0.3s ease;
}

/* Letter glow behind */
.project-card__letter::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 80px;
  height: 80px;
  transform: translate(-50%, -50%);
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.08) 0%,
    transparent 70%
  );
  pointer-events: none;
  z-index: -1;
  transition: width 0.3s ease, height 0.3s ease;
}

.project-card:hover .project-card__letter {
  transform: scale(1.15);
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.project-card:hover .project-card__letter::after {
  width: 100px;
  height: 100px;
}

/* ============================================================
   Content Area
   ============================================================ */

.project-card__content {
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  flex: 1;
}

/* Tech stack tags */
.project-card__tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.project-card__tag {
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 500;
  transition: transform 0.2s ease;
  white-space: nowrap;
}

.project-card__tag:hover {
  transform: scale(1.05);
}

.project-card__tag--more {
  background: rgba(255, 255, 255, 0.1);
  color: var(--color-text-primary, #e6e6e6);
}

/* Project title */
.project-card__title {
  font-size: 1.125rem;
  font-weight: 600;
  color: var(--color-text-primary, #ffffff);
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
}

/* Description */
.project-card__description {
  font-size: 0.875rem;
  color: var(--color-text-secondary, rgba(255, 255, 255, 0.7));
  margin: 0 0 1rem 0;
  line-height: 1.6;
  flex: 1;
}

.project-card--featured .project-card__description {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.project-card--list .project-card__description {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* Action buttons */
.project-card__actions {
  display: flex;
  gap: 0.75rem;
  margin-top: auto;
}

.project-card__btn {
  padding: 0.5rem 1rem;
  border-radius: var(--radius-sm, 8px);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: background-color 0.2s ease, transform 0.2s ease;
  border: none;
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
}

.project-card__btn--primary {
  background: var(--color-accent, #e94560);
  color: #ffffff;
}

.project-card__btn--primary:hover {
  background: var(--color-accent-hover);
  transform: translateY(-2px);
}

.project-card__btn--secondary {
  background: rgba(255, 255, 255, 0.1);
  color: var(--color-text-primary, #ffffff);
  border: 1px solid var(--color-border, rgba(255, 255, 255, 0.2));
}

.project-card__btn--secondary:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: translateY(-2px);
}

.project-card__btn-icon {
  font-size: 1rem;
  width: 1em;
  height: 1em;
  vertical-align: middle;
}

/* ============================================================
   Animations
   ============================================================ */

@keyframes floatCircle {
  0%   { transform: translate(0, 0) scale(1); }
  100% { transform: translate(-6px, 8px) scale(1.08); }
}

@keyframes floatRing {
  0%   { transform: translate(0, 0) rotate(0deg); }
  100% { transform: translate(5px, -7px) rotate(45deg); }
}

@keyframes floatDot {
  0%   { transform: translate(0, 0) scale(1); opacity: 0.6; }
  100% { transform: translate(-3px, -5px) scale(1.3); opacity: 1; }
}

@keyframes gradientShift {
  0%   { background-position: 0% 0%; }
  50%  { background-position: 100% 100%; }
  100% { background-position: 0% 100%; }
}

@keyframes lightSweep {
  0%   { transform: translateX(-100%) rotate(15deg); }
  100% { transform: translateX(100%) rotate(15deg); }
}

/* ============================================================
   Responsive Design
   ============================================================ */

@media (max-width: 768px) {
  .project-card__content {
    padding: 1rem;
  }

  .project-card__title {
    font-size: 1rem;
  }

  .project-card__description {
    font-size: 0.8125rem;
  }

  .project-card__btn {
    padding: 0.4rem 0.8rem;
    font-size: 0.8125rem;
  }

  .project-card__letter {
    font-size: 1.5rem;
  }
}

@media (max-width: 480px) {
  .project-card__actions {
    flex-direction: column;
  }

  .project-card__btn {
    width: 100%;
    justify-content: center;
  }
}

/* ============================================================
   Accessibility: Reduced Motion
   ============================================================ */

@media (prefers-reduced-motion: reduce) {
  .project-card,
  .project-card__image,
  .project-card__tag,
  .project-card__btn {
    transition: none;
    animation: none;
  }

  .project-card__placeholder {
    animation: none;
  }

  .project-card__placeholder::after {
    animation: none;
    display: none;
  }

  .placeholder-decor {
    animation: none;
    transition: none;
  }

  .project-card__placeholder::before {
    transition: none;
  }

  .project-card__letter,
  .project-card__letter::after {
    transition: none;
  }
}

/* ============================================================
   ParticleBorder Wrapper
   ============================================================ */

.project-card-wrapper {
  display: block;
  height: 100%;
}

.project-card-wrapper .project-card {
  border: none;
}

.project-card-wrapper .project-card:hover,
.project-card-wrapper .project-card:focus {
  border-color: transparent;
}

.project-card-wrapper .project-card:focus-visible {
  outline: 2px solid var(--color-accent, #e94560);
  outline-offset: 4px;
}

/* Border effects */
.project-card.border--fade-glow,
.project-card.border--nebula {
  border: none;
}

.project-card.border--fade-glow:hover,
.project-card.border--fade-glow:focus,
.project-card.border--nebula:hover,
.project-card.border--nebula:focus {
  border-color: transparent;
}
```

---

## 11. `src/components/project/ProjectBanner.vue` — 项目 Banner

```css
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
   Placeholder — 6-Layer Visual Effects (matches ProjectCard)
   ============================================================ */

/* Layer 1: Brand gradient background */
.banner-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 200px;
  position: relative;
  overflow: hidden;

  background: var(--card-brand-gradient, linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%));
  background-size: 250% 250%;
  animation: gradientShift 6s ease-in-out infinite alternate;
}

/* Layer 2: Geometric grid texture (::before) */
.banner-placeholder::before {
  content: '';
  position: absolute;
  inset: 0;
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.04) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 255, 255, 0.04) 1px, transparent 1px);
  background-size: 48px 48px;
  -webkit-mask-image: linear-gradient(180deg, rgba(0, 0, 0, 0.5) 0%, transparent 85%);
  mask-image: linear-gradient(180deg, rgba(0, 0, 0, 0.5) 0%, transparent 85%);
  pointer-events: none;
  z-index: 1;
}

/* Layer 4: Diagonal light sweep (::after) */
.banner-placeholder::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    105deg,
    transparent 38%,
    rgba(255, 255, 255, 0.05) 43%,
    rgba(255, 255, 255, 0.12) 50%,
    rgba(255, 255, 255, 0.05) 57%,
    transparent 62%
  );
  animation: lightSweep 5s ease-in-out infinite;
  pointer-events: none;
  z-index: 3;
}

/* Layer 3: Bottom dark gradient fade */
.banner-fade {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 55%;
  background: linear-gradient(
    to top,
    var(--color-surface, #0f3460) 0%,
    rgba(15, 52, 96, 0.4) 40%,
    transparent 100%
  );
  pointer-events: none;
  z-index: 2;
}

/* Layer 5: Floating geometric decorations */
.banner-decor {
  position: absolute;
  pointer-events: none;
  z-index: 4;
  opacity: 0.6;
}

/* Large circle — top right */
.banner-decor--circle {
  width: 140px;
  height: 140px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  top: -36px;
  right: -24px;
  animation: floatCircle 7s ease-in-out infinite alternate;
}

/* Ring — bottom left */
.banner-decor--ring {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  border: 2px solid rgba(255, 255, 255, 0.07);
  bottom: 24px;
  left: 20px;
  animation: floatRing 5.5s ease-in-out infinite alternate-reverse;
}

/* Small dot — middle right */
.banner-decor--dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.18);
  top: 38%;
  right: 22%;
  animation: floatDot 3.5s ease-in-out infinite alternate;
  box-shadow: 0 0 14px 3px rgba(255, 255, 255, 0.06);
}

/* Layer 6: Brand name */
.banner-brand {
  position: relative;
  z-index: 5;
  font-size: 3.5rem;
  font-weight: 700;
  color: rgba(255, 255, 255, 0.9);
  text-shadow: 0 2px 12px rgba(0, 0, 0, 0.25);
  user-select: none;
  transition: transform 0.3s ease, text-shadow 0.3s ease;
}

/* Brand name glow behind */
.banner-brand::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 120px;
  height: 120px;
  transform: translate(-50%, -50%);
  background: radial-gradient(
    circle,
    rgba(255, 255, 255, 0.08) 0%,
    transparent 70%
  );
  pointer-events: none;
  z-index: -1;
  transition: width 0.3s ease, height 0.3s ease;
}

.banner-placeholder:hover .banner-brand {
  transform: scale(1.08);
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.banner-placeholder:hover .banner-brand::after {
  width: 150px;
  height: 150px;
}

/* ============================================================
   Animations
   ============================================================ */

@keyframes gradientShift {
  0%   { background-position: 0% 0%; }
  50%  { background-position: 100% 100%; }
  100% { background-position: 0% 100%; }
}

@keyframes lightSweep {
  0%   { transform: translateX(-100%) rotate(15deg); }
  100% { transform: translateX(100%) rotate(15deg); }
}

@keyframes floatCircle {
  0%   { transform: translate(0, 0) scale(1); }
  100% { transform: translate(-8px, 10px) scale(1.08); }
}

@keyframes floatRing {
  0%   { transform: translate(0, 0) rotate(0deg); }
  100% { transform: translate(6px, -9px) rotate(45deg); }
}

@keyframes floatDot {
  0%   { transform: translate(0, 0) scale(1); opacity: 0.6; }
  100% { transform: translate(-4px, -6px) scale(1.3); opacity: 1; }
}

/* ============================================================
   Responsive Design
   ============================================================ */

@media (max-width: 768px) {
  .project-banner {
    aspect-ratio: 4 / 3;
  }

  .banner-brand {
    font-size: 2rem;
  }

  .banner-decor--circle {
    width: 100px;
    height: 100px;
  }

  .banner-decor--ring {
    width: 52px;
    height: 52px;
  }
}

@media (max-width: 480px) {
  .banner-brand {
    font-size: 1.5rem;
  }
}

/* ============================================================
   Accessibility: Reduced Motion
   ============================================================ */

@media (prefers-reduced-motion: reduce) {
  .banner-placeholder {
    animation: none;
    background-size: 100% 100%;
  }

  .banner-placeholder::after {
    animation: none;
    display: none;
  }

  .banner-decor {
    animation: none;
  }

  .banner-brand,
  .banner-brand::after {
    transition: none;
  }

  .banner-placeholder:hover .banner-brand {
    transform: none;
  }
}
```

---

## 12. `src/components/project/ParticleBorder.vue` — Canvas 粒子边框

```css
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
```

---

## 13. `src/views/Home.vue` — 首页

```css
.home {
  min-height: 100vh;
  background: var(--color-bg-primary);
}
```

---

## 14. `src/views/ProjectDetail.vue` — 项目详情页

```css
.project-detail {
  max-width: 900px;
  margin: 0 auto;
  padding: 2rem 1.5rem;
}

/* 骨架屏样式 */
.loading-skeleton {
  animation: pulse 1.5s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.skeleton-back {
  width: 120px;
  height: 24px;
  background: var(--color-surface);
  border-radius: var(--radius-sm);
  margin-bottom: 2rem;
}

.skeleton-banner {
  width: 100%;
  aspect-ratio: 16 / 9;
  background: var(--color-surface);
  border-radius: var(--radius-lg);
  margin-bottom: 2rem;
}

.skeleton-content {
  padding: 0 1rem;
}

.skeleton-title {
  width: 60%;
  height: 36px;
  background: var(--color-surface);
  border-radius: var(--radius-sm);
  margin-bottom: 1rem;
}

.skeleton-subtitle {
  width: 40%;
  height: 20px;
  background: var(--color-surface);
  border-radius: var(--radius-sm);
  margin-bottom: 1.5rem;
}

.skeleton-tags {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.skeleton-tag {
  width: 80px;
  height: 28px;
  background: var(--color-surface);
  border-radius: var(--radius-sm);
}

.skeleton-description {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.skeleton-line {
  width: 100%;
  height: 16px;
  background: var(--color-surface);
  border-radius: var(--radius-sm);
}

.skeleton-line:last-child {
  width: 70%;
}

/* 404 状态 */
.not-found,
.error-state {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  text-align: center;
}

.not-found-content h2,
.error-content h2 {
  font-size: 1.5rem;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
}

.not-found-content p,
.error-content p {
  color: var(--color-text-secondary);
  margin-bottom: 1.5rem;
}

.back-to-list,
.retry-btn {
  display: inline-block;
  padding: 0.75rem 1.5rem;
  background: var(--color-accent);
  color: white;
  text-decoration: none;
  border-radius: var(--radius-sm);
  font-weight: 500;
  transition: all 0.3s ease;
  border: none;
  cursor: pointer;
}

.back-to-list:hover,
.retry-btn:hover {
  background: var(--color-accent-hover);
  transform: translateY(-2px);
}

/* 返回按钮 */
.back-link {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-text-secondary);
  text-decoration: none;
  font-size: 0.95rem;
  margin-bottom: 2rem;
  transition: color 0.3s ease;
}

.back-link:hover {
  color: var(--color-accent);
}

.back-link .arrow {
  transition: transform 0.3s ease;
}

.back-link:hover .arrow {
  transform: translateX(-4px);
}

/* 项目信息 */
.project-info {
  margin-top: 2rem;
}

.project-title {
  font-size: 2.25rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
  line-height: 1.3;
}

.project-subtitle {
  font-size: 1.125rem;
  color: var(--color-text-secondary);
  margin-bottom: 1.5rem;
}

/* 技术栈标签 */
.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 2rem;
}

.tech-tag {
  display: inline-block;
  padding: 0.375rem 0.875rem;
  border-radius: 999px;
  font-size: 0.875rem;
  font-weight: 500;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  cursor: default;
  backdrop-filter: blur(2px);
}

.tech-tag:hover {
  transform: scale(1.05);
}

/* 项目描述 */
.project-description {
  margin-bottom: 2rem;
  line-height: 1.8;
  color: var(--color-text-primary);
}

.project-description p {
  margin-bottom: 1rem;
}

.project-description p:last-child {
  margin-bottom: 0;
}

/* 线上地址按钮 */
.live-url-btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  background: var(--color-accent);
  color: white;
  text-decoration: none;
  border-radius: var(--radius-sm);
  font-weight: 500;
  transition: all 0.3s ease;
}

.live-url-btn:hover {
  background: var(--color-accent-hover);
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(233, 69, 96, 0.3);
}

.live-url-btn svg {
  flex-shrink: 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .project-detail {
    padding: 1.5rem 1rem;
  }

  .project-title {
    font-size: 1.75rem;
  }

  .project-subtitle {
    font-size: 1rem;
  }

  .tech-tags {
    gap: 0.375rem;
  }

  .tech-tag {
    font-size: 0.8125rem;
    padding: 0.3rem 0.75rem;
  }
}

@media (max-width: 480px) {
  .project-title {
    font-size: 1.5rem;
  }
}
```

---

## 15. `src/views/NotFound.vue` — 404 页面

```css
.not-found-page {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  background: var(--color-bg-primary);
}

.not-found-main {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6rem 2rem 4rem;
}

.not-found-content {
  text-align: center;
  max-width: 480px;
}

.not-found-code {
  font-size: 6rem;
  font-weight: 800;
  background: linear-gradient(135deg, var(--color-accent), #ff6b9d);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  line-height: 1;
  margin-bottom: 1rem;
}

.not-found-title {
  font-size: 1.75rem;
  color: var(--color-text-primary);
  margin-bottom: 0.75rem;
}

.not-found-message {
  font-size: 1.125rem;
  color: var(--color-text-secondary);
  margin-bottom: 2rem;
}

.not-found-btn {
  display: inline-block;
  padding: 0.75rem 2rem;
  background: var(--color-accent);
  color: #ffffff;
  text-decoration: none;
  border-radius: var(--radius-sm);
  font-weight: 500;
  transition: all 0.3s ease;
}

.not-found-btn:hover {
  background: var(--color-accent-hover);
  transform: translateY(-2px);
}
```

---

## 16. 样式优化变更（2026-06-11 更新）

> 基于视觉优化建议，提升卡片渐变色明度并降低叠层压暗效果。

### 16.1 `src/config/techStackColors.js` — 项目品牌渐变色提亮

```javascript
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
  }
}
```

色值变化对比：

| 项目 | 旧渐变 | 新渐变 | 变化 |
|---|---|---|---|
| 鲜途智送 | `#e94560 → #f472b6` | `#ff6b8a → #f9a8d4` | 红偏粉，整体更明艳 |
| 昕悦读 | `#3b82f6 → #06b6d4` | `#60a5fa → #22d3ee` | 蓝更亮，青更透 |
| xinysoft | `#f59e0b → #ef4444` | `#fbbf24 → #f87171` | 金更亮，红更柔和 |

### 16.2 `src/components/project/ProjectCard.vue` — 底部过渡层压暗优化

```css
/* Layer 3: Bottom dark gradient fade */
.placeholder-fade {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 35%;                     /* 原 55% → 35%，减少覆盖面积 */
  background: linear-gradient(
    to top,
    var(--color-surface, #0f3460) 0%,
    rgba(15, 52, 96, 0.25) 50%,    /* 原 0.4 → 0.25，降低不透明度 */
    transparent 100%
  );
  pointer-events: none;
  z-index: 2;
}
```

### 16.3 `src/components/project/ProjectCard.vue` — 网格纹理透明度降低

```css
/* Layer 2: Geometric grid texture (::before) */
.project-card__placeholder::before {
  /* ... */
  background-image:
    linear-gradient(rgba(255, 255, 255, 0.025) 1px, transparent 1px),  /* 原 0.04 → 0.025 */
    linear-gradient(90deg, rgba(255, 255, 255, 0.025) 1px, transparent 1px);
  /* ... */
}
```

### 16.4 `src/composables/useProjectBrand.js` — 内容区品牌 tint 色彩过渡

内容区 `.project-card__content` 已通过 `cardContentStyle` 计算属性自动注入 `brand.tint` 渐变背景，与封面占位符的品牌色形成呼应：

```javascript
const cardContentStyle = computed(() => {
  const brand = projectBrands[projectId.value]
  return { background: brand?.tint || projectBrands[1].tint }
})
```

模板中通过 `:style="cardContentStyle"` 自动应用。

---

## 17. 样式优化变更 — 装饰层深色化（2026-06-11 更新）

> 问题：渐变提亮后，白色半透明的叠层效果（网格纹理、光线扫过、浮动装饰）对比度不足，动画不可见。
> 方案：将叠层颜色策略从"白色半透明"改为"深色半透明"，同时增强动画幅度和节奏。网格纹理已移除。

### 17.1 `src/components/project/ProjectCard.vue` — 卡片封面装饰优化

```css
/* Layer 2: Geometric grid texture (disabled) */
/* Removed per design preference */

/* Layer 4: Diagonal light sweep (::after) */
.project-card__placeholder::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    105deg,
    transparent 35%,                          /* 原 38% → 35%，光带加宽 */
    rgba(255, 255, 255, 0.12) 42%,           /* 原 0.05 → 0.12 */
    rgba(255, 255, 255, 0.35) 50%,           /* 原 0.12 → 0.35 */
    rgba(255, 255, 255, 0.12) 58%,
    transparent 65%                           /* 原 62% → 65% */
  );
  animation: lightSweep 4s ease-in-out infinite;  /* 原 5s → 4s */
  pointer-events: none;
  z-index: 3;
}

.project-card:hover .project-card__placeholder::after {
  animation-duration: 2s;                     /* 原 2.5s → 2s */
  background: linear-gradient(
    105deg,
    transparent 35%,
    rgba(255, 255, 255, 0.2) 42%,            /* 原 0.08 → 0.2 */
    rgba(255, 255, 255, 0.5) 50%,             /* 原 0.18 → 0.5 */
    rgba(255, 255, 255, 0.2) 58%,
    transparent 65%
  );
}

/* Layer 5: Floating geometric decorations */
.placeholder-decor {
  opacity: 0.7;                               /* 原 0.6 → 0.7 */
}

.project-card:hover .placeholder-decor {
  opacity: 1;                                 /* 原 0.85 → 1 */
}

/* Large circle — top right */
.placeholder-decor--circle {
  background: rgba(0, 0, 0, 0.06);           /* 原 rgba(255,255,255,0.05) → 深色 */
  border: 2px solid rgba(0, 0, 0, 0.08);     /* 新增描边 */
}

/* Ring — bottom left */
.placeholder-decor--ring {
  border: 3px solid rgba(0, 0, 0, 0.12);    /* 原 2px 白色 → 3px 深色 */
}

/* Small dot — middle right */
.placeholder-decor--dot {
  width: 12px;                                /* 原 8px → 12px */
  height: 12px;
  background: rgba(0, 0, 0, 0.15);           /* 原 rgba(255,255,255,0.18) → 深色 */
  box-shadow: 0 0 16px 4px rgba(0, 0, 0, 0.1); /* 原 白色阴影 → 深色阴影 */
}

/* Layer 6: First letter */
.project-card__letter {
  font-size: 2rem;                            /* 原 1.75rem → 2rem */
  color: rgba(0, 0, 0, 0.35);                /* 原 rgba(255,255,255,0.9) → 深色 */
  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.6),        /* 浅色描边增加立体感 */
    0 2px 8px rgba(0, 0, 0, 0.15);           /* 原 0 2px 12px rgba(0,0,0,0.25) */
}

.project-card__letter::after {
  width: 90px;                                /* 原 80px → 90px */
  height: 90px;
  background: radial-gradient(
    circle,
    rgba(0, 0, 0, 0.06) 0%,                  /* 原 rgba(255,255,255,0.08) → 深色 */
    transparent 70%
  );
}

.project-card:hover .project-card__letter {
  transform: scale(1.2);                      /* 原 1.15 → 1.2 */
  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.8),
    0 4px 16px rgba(0, 0, 0, 0.2);
}

.project-card:hover .project-card__letter::after {
  width: 120px;                               /* 原 100px → 120px */
  height: 120px;
}
```

### 17.2 `src/components/project/ProjectBanner.vue` — Banner 装饰同步优化

```css
/* Layer 2: Geometric grid texture (disabled) */
/* Removed per design preference */

/* Layer 4: Diagonal light sweep (::after) */
.banner-placeholder::after {
  background: linear-gradient(
    105deg,
    transparent 35%,
    rgba(255, 255, 255, 0.12) 42%,
    rgba(255, 255, 255, 0.35) 50%,           /* 原 0.12 → 0.35 */
    rgba(255, 255, 255, 0.12) 58%,
    transparent 65%
  );
}

/* Layer 5: Floating geometric decorations */
.banner-decor--circle {
  background: rgba(0, 0, 0, 0.06);           /* 原 白色 → 深色 */
  border: 2px solid rgba(0, 0, 0, 0.08);     /* 新增描边 */
}

.banner-decor--ring {
  border: 3px solid rgba(0, 0, 0, 0.12);    /* 原 2px 白色 → 3px 深色 */
}

.banner-decor--dot {
  width: 14px;                                /* 原 10px → 14px */
  height: 14px;
  background: rgba(0, 0, 0, 0.15);           /* 原 白色 → 深色 */
  box-shadow: 0 0 18px 5px rgba(0, 0, 0, 0.1);
}

/* Layer 6: Brand name */
.banner-brand {
  color: rgba(0, 0, 0, 0.35);                /* 原 rgba(255,255,255,0.9) → 深色 */
  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.6),        /* 浅色描边 */
    0 2px 8px rgba(0, 0, 0, 0.15);
}

.banner-brand::after {
  background: radial-gradient(
    circle,
    rgba(0, 0, 0, 0.06) 0%,                  /* 原 白色 → 深色 */
    transparent 70%
  );
}

.banner-placeholder:hover .banner-brand {
  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.8),
    0 4px 16px rgba(0, 0, 0, 0.2);
}
```

### 优化前后效果对比

| 效果层 | 优化前（亮色上白） | 优化后（亮色上暗） |
|---|---|---|
| 网格纹理 | 不可见 | 已移除 |
| 光线扫过 | 勉强可见 | 明亮的光带扫过，悬停时更宽更亮 |
| 圆形装饰 | 不可见 | 淡暗色圆 + 描边轮廓 |
| 圆环装饰 | 不可见 | 加粗暗色圆环，旋转可见 |
| 光点装饰 | 勉强可见 | 更大的暗色光点，带扩散阴影 |
| 首字母/品牌名 | 偏淡 | 深色字母 + 浅色描边，悬停放大更明显 |

---
---
> **覆盖文件清单**（共 15 个源文件，全部完整提取）：
> `style.css` → `border-effects.css` → `App.vue` → `Navbar.vue` → `Hero.vue` → `ContactModal.vue` → `Footer.vue` → `FeaturedProjects.vue` → `ProjectsView.vue` → `ProjectCard.vue` → `ProjectBanner.vue` → `ParticleBorder.vue` → `Home.vue` → `ProjectDetail.vue` → `NotFound.vue`
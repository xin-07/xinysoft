<template>
  <nav class="navbar" :class="{ 'navbar-scrolled': isScrolled }">
    <div class="navbar-container">
      <a href="#" class="logo" @click.prevent="scrollToTop">
        xiny
      </a>

      <!-- PC端导航 -->
      <div class="nav-links">
        <a href="#hero" class="nav-link" :class="{ active: activeSection === 'hero' }">
          首页
        </a>
      </div>

      <!-- 移动端汉堡菜单 -->
      <button class="hamburger" @click="toggleMenu" :class="{ active: isMenuOpen }">
        <span></span>
        <span></span>
        <span></span>
      </button>
    </div>

    <!-- 移动端菜单 -->
    <div class="mobile-menu" :class="{ open: isMenuOpen }">
      <a href="#hero" class="mobile-nav-link" @click="closeMenu">
        首页
      </a>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const isScrolled = ref(false)
const isMenuOpen = ref(false)
const activeSection = ref('hero')

const handleScroll = () => {
  isScrolled.value = window.scrollY > 50

  // 检测当前区域
  const heroSection = document.getElementById('hero')
  if (heroSection) {
    const rect = heroSection.getBoundingClientRect()
    if (rect.top <= 100 && rect.bottom >= 100) {
      activeSection.value = 'hero'
    }
  }
}

const scrollToTop = () => {
  window.scrollTo({
    top: 0,
    behavior: 'smooth'
  })
  closeMenu()
}

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  handleScroll()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style scoped>
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  background: rgba(26, 26, 46, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid transparent;
  transition: all 0.3s ease;
}

.navbar-scrolled {
  border-bottom-color: rgba(233, 69, 96, 0.2);
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.3);
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
  background: rgba(26, 26, 46, 0.98);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(233, 69, 96, 0.2);
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
  background: rgba(233, 69, 96, 0.1);
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
</style>
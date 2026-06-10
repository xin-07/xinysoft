<template>
  <div class="not-found-page">
    <Navbar />
    <main class="not-found-main">
      <div class="not-found-content">
        <div class="not-found-code">404</div>
        <h1 class="not-found-title">页面未找到</h1>
        <p class="not-found-message">抱歉，您访问的页面不存在或已被移除。</p>
        <router-link to="/" class="not-found-btn">返回首页</router-link>
      </div>
    </main>
    <Footer />
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
import Footer from '../components/Footer.vue'
</script>

<style scoped>
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
</style>

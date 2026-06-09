<template>
  <div class="home">
    <Navbar />
    <Hero />
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
import Hero from '../components/Hero.vue'
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: var(--color-bg-primary);
}
</style>
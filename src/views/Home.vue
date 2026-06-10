<template>
  <div class="home">
    <Navbar />
    <Hero />
    <FeaturedProjects />
    <Footer />
  </div>
</template>

<script setup>
import Navbar from '../components/Navbar.vue'
import Hero from '../components/Hero.vue'
import FeaturedProjects from '../components/home/FeaturedProjects.vue'
import Footer from '../components/Footer.vue'
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: var(--color-bg-primary);
}
</style>
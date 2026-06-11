<template>
  <div
    class="project-placeholder"
    :class="`project-placeholder--${variant}`"
    :style="gradientStyle"
  >
    <!-- Layer 3: Bottom dark gradient fade -->
    <div class="placeholder-fade" aria-hidden="true"></div>

    <!-- Layer 5: Floating geometric decorations -->
    <div class="placeholder-decor placeholder-decor--circle" aria-hidden="true"></div>
    <div class="placeholder-decor placeholder-decor--ring" aria-hidden="true"></div>
    <div class="placeholder-decor placeholder-decor--dot" aria-hidden="true"></div>

    <!-- Layer 6: Brand name -->
    <span class="placeholder-brand">{{ brandName }}</span>
  </div>
</template>

<script setup>
defineProps({
  brandName: {
    type: String,
    default: ''
  },
  gradientStyle: {
    type: Object,
    default: () => ({})
  },
  variant: {
    type: String,
    default: 'card',
    validator: (v) => ['card', 'banner'].includes(v)
  }
})
</script>

<style scoped>
/* ============================================================
   Placeholder — 6-Layer Visual Effects (shared by Card & Banner)
   ============================================================ */

/* Layer 1: Brand gradient background */
.project-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;

  /* Brand gradient via CSS variable injected by composable */
  background: var(--card-brand-gradient, linear-gradient(135deg, #1a1a2e 0%, #0f3460 100%));
  background-size: 250% 250%;
  animation: gradientShift 6s ease-in-out infinite alternate;
}

/* Variant: Card */
.project-placeholder--card {
  min-height: 120px;
}

/* Variant: Banner */
.project-placeholder--banner {
  min-height: 200px;
}

/* Layer 2: Geometric grid texture (disabled) */
/* Removed per design preference */

/* Layer 4: Diagonal light sweep (::after) */
.project-placeholder::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: linear-gradient(
    105deg,
    transparent 35%,
    rgba(255, 255, 255, 0.12) 42%,
    rgba(255, 255, 255, 0.35) 50%,
    rgba(255, 255, 255, 0.12) 58%,
    transparent 65%
  );
  pointer-events: none;
  z-index: 3;
}

.project-placeholder--card::after {
  animation: lightSweep 4s ease-in-out infinite;
}

.project-placeholder--banner::after {
  animation: lightSweep 5s ease-in-out infinite;
}

/* Layer 3: Bottom dark gradient fade */
.placeholder-fade {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  background: linear-gradient(
    to top,
    var(--color-surface, #0f3460) 0%,
    rgba(15, 52, 96, 0.25) 50%,
    transparent 100%
  );
  pointer-events: none;
  z-index: 2;
}

.project-placeholder--card .placeholder-fade {
  height: 35%;
}

.project-placeholder--banner .placeholder-fade {
  height: 55%;
  background: linear-gradient(
    to top,
    var(--color-surface, #0f3460) 0%,
    rgba(15, 52, 96, 0.4) 40%,
    transparent 100%
  );
}

/* Layer 5: Floating geometric decorations */
.placeholder-decor {
  position: absolute;
  pointer-events: none;
  z-index: 4;
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.project-placeholder--card .placeholder-decor {
  opacity: 0.7;
}

.project-placeholder--banner .placeholder-decor {
  opacity: 0.6;
}

/* Large circle — top right */
.placeholder-decor--circle {
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.06);
  border: 2px solid rgba(0, 0, 0, 0.08);
}

.project-placeholder--card .placeholder-decor--circle {
  width: 110px;
  height: 110px;
  top: -28px;
  right: -18px;
  animation: floatCircle 7s ease-in-out infinite alternate;
}

.project-placeholder--banner .placeholder-decor--circle {
  width: 140px;
  height: 140px;
  top: -36px;
  right: -24px;
  animation: floatCircle 7s ease-in-out infinite alternate;
}

/* Ring — bottom left */
.placeholder-decor--ring {
  border-radius: 50%;
  border: 3px solid rgba(0, 0, 0, 0.12);
}

.project-placeholder--card .placeholder-decor--ring {
  width: 56px;
  height: 56px;
  bottom: 18px;
  left: 14px;
  animation: floatRing 5.5s ease-in-out infinite alternate-reverse;
}

.project-placeholder--banner .placeholder-decor--ring {
  width: 72px;
  height: 72px;
  bottom: 24px;
  left: 20px;
  animation: floatRing 5.5s ease-in-out infinite alternate-reverse;
}

/* Small dot — middle right */
.placeholder-decor--dot {
  border-radius: 50%;
  background: rgba(0, 0, 0, 0.15);
  top: 38%;
  right: 22%;
}

.project-placeholder--card .placeholder-decor--dot {
  width: 12px;
  height: 12px;
  animation: floatDot 3.5s ease-in-out infinite alternate;
  box-shadow: 0 0 16px 4px rgba(0, 0, 0, 0.1);
}

.project-placeholder--banner .placeholder-decor--dot {
  width: 14px;
  height: 14px;
  animation: floatDot 3.5s ease-in-out infinite alternate;
  box-shadow: 0 0 18px 5px rgba(0, 0, 0, 0.1);
}

/* Layer 6: Brand name */
.placeholder-brand {
  position: relative;
  z-index: 5;
  font-weight: 700;
  color: rgba(0, 0, 0, 0.35);
  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.6),
    0 2px 8px rgba(0, 0, 0, 0.15);
  user-select: none;
  letter-spacing: 0.1em;
  transition: transform 0.3s ease, text-shadow 0.3s ease;
}

.project-placeholder--card .placeholder-brand {
  font-size: 2rem;
}

.project-placeholder--banner .placeholder-brand {
  font-size: 3.5rem;
}

/* Brand name glow behind */
.placeholder-brand::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: radial-gradient(
    circle,
    rgba(0, 0, 0, 0.06) 0%,
    transparent 70%
  );
  pointer-events: none;
  z-index: -1;
  transition: width 0.3s ease, height 0.3s ease;
}

.project-placeholder--card .placeholder-brand::after {
  width: 90px;
  height: 90px;
}

.project-placeholder--banner .placeholder-brand::after {
  width: 120px;
  height: 120px;
}

/* ============================================================
   Hover Effects (card only)
   ============================================================ */

.project-placeholder--card:hover .placeholder-decor {
  opacity: 1;
}

.project-placeholder--card:hover .placeholder-brand {
  transform: scale(1.2);
  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.8),
    0 4px 16px rgba(0, 0, 0, 0.2);
}

.project-placeholder--card:hover .placeholder-brand::after {
  width: 120px;
  height: 120px;
}

.project-placeholder--card:hover::after {
  animation-duration: 2s;
  background: linear-gradient(
    105deg,
    transparent 35%,
    rgba(255, 255, 255, 0.2) 42%,
    rgba(255, 255, 255, 0.5) 50%,
    rgba(255, 255, 255, 0.2) 58%,
    transparent 65%
  );
}

/* Banner hover (subtle) */
.project-placeholder--banner:hover .placeholder-brand {
  transform: scale(1.08);
  text-shadow:
    0 1px 0 rgba(255, 255, 255, 0.8),
    0 4px 16px rgba(0, 0, 0, 0.2);
}

.project-placeholder--banner:hover .placeholder-brand::after {
  width: 150px;
  height: 150px;
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
  .project-placeholder--card .placeholder-brand {
    font-size: 1.5rem;
  }

  .project-placeholder--banner .placeholder-brand {
    font-size: 2rem;
  }

  .project-placeholder--banner .placeholder-decor--circle {
    width: 100px;
    height: 100px;
  }

  .project-placeholder--banner .placeholder-decor--ring {
    width: 52px;
    height: 52px;
  }
}

@media (max-width: 480px) {
  .project-placeholder--banner .placeholder-brand {
    font-size: 1.5rem;
  }
}

/* ============================================================
   Accessibility: Reduced Motion
   ============================================================ */

@media (prefers-reduced-motion: reduce) {
  .project-placeholder {
    animation: none;
    background-size: 100% 100%;
  }

  .project-placeholder::after {
    animation: none;
    display: none;
  }

  .placeholder-decor {
    animation: none;
    transition: none;
  }

  .placeholder-brand,
  .placeholder-brand::after {
    transition: none;
  }

  .project-placeholder--card:hover .placeholder-brand,
  .project-placeholder--banner:hover .placeholder-brand {
    transform: none;
  }
}
</style>
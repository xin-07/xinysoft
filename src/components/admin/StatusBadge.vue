<script setup>
defineProps({
  status: {
    type: String,
    required: true,
    validator: (v) => ['published', 'draft'].includes(v)
  }
})
</script>

<template>
  <span :class="['status-badge', `status-badge--${status}`]">
    {{ status === 'published' ? '已发布' : '草稿' }}
  </span>
</template>

<style scoped>
.status-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.375rem;
  font-size: 0.8125rem;
  font-weight: 500;
  padding: 0.25rem 0.625rem;
  border-radius: var(--radius-full);
  line-height: 1.4;
}

.status-badge::before {
  content: '';
  display: inline-block;
  width: 0.5rem;
  height: 0.5rem;
  border-radius: 50%;
  flex-shrink: 0;
}

.status-badge--published {
  background: rgba(34, 197, 94, 0.12);
  color: #22c55e;
}

.status-badge--published::before {
  background: #22c55e;
}

.status-badge--draft {
  background: rgba(245, 158, 11, 0.12);
  color: #f59e0b;
}

.status-badge--draft::before {
  background: #f59e0b;
}
</style>
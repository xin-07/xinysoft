<script setup>
import { useToast } from '../../composables/useToast'

const { toasts, remove } = useToast()
</script>

<template>
  <Teleport to="body">
    <div class="admin-toast-container">
      <TransitionGroup name="admin-toast">
        <div
          v-for="toast in toasts"
          :key="toast.id"
          :class="['admin-toast', `admin-toast--${toast.type}`]"
        >
          <span class="admin-toast__icon">
            <template v-if="toast.type === 'success'">&#x2713;</template>
            <template v-else-if="toast.type === 'error'">&#x2717;</template>
            <template v-else>&#x2139;</template>
          </span>
          <span class="admin-toast__message">{{ toast.message }}</span>
          <button class="admin-toast__close" @click="remove(toast.id)">&times;</button>
        </div>
      </TransitionGroup>
    </div>
  </Teleport>
</template>

<style scoped>
.admin-toast-container {
  position: fixed;
  top: var(--spacing-lg);
  right: var(--spacing-lg);
  z-index: 2000;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
  pointer-events: none;
}

.admin-toast {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-md) var(--spacing-lg);
  border-radius: var(--radius-md);
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  box-shadow: var(--shadow-md);
  min-width: 280px;
  max-width: 420px;
  pointer-events: auto;
}

.admin-toast--success {
  border-left: 3px solid #22c55e;
}

.admin-toast--error {
  border-left: 3px solid #ef4444;
}

.admin-toast--info {
  border-left: 3px solid #3b82f6;
}

.admin-toast__icon {
  flex-shrink: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
  border-radius: 50%;
  font-weight: 700;
}

.admin-toast--success .admin-toast__icon {
  color: #22c55e;
  background: rgba(34, 197, 94, 0.12);
}

.admin-toast--error .admin-toast__icon {
  color: #ef4444;
  background: rgba(239, 68, 68, 0.12);
}

.admin-toast--info .admin-toast__icon {
  color: #3b82f6;
  background: rgba(59, 130, 246, 0.12);
}

.admin-toast__message {
  flex: 1;
  font-size: 0.875rem;
  color: var(--color-text-primary);
}

.admin-toast__close {
  flex-shrink: 0;
  width: 24px;
  height: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  color: var(--color-text-secondary);
  font-size: 1.125rem;
  line-height: 1;
  transition: background var(--transition-fast), color var(--transition-fast);
}

.admin-toast__close:hover {
  background: rgba(255, 255, 255, 0.1);
  color: var(--color-text-primary);
}

/* TransitionGroup */
.admin-toast-enter-active {
  transition: all 0.3s ease;
}

.admin-toast-leave-active {
  transition: all 0.25s ease;
}

.admin-toast-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.admin-toast-leave-to {
  opacity: 0;
  transform: translateX(100%);
}
</style>
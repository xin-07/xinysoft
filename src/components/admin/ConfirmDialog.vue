<script setup>
import { onMounted, onUnmounted } from 'vue'

const props = defineProps({
  visible: { type: Boolean, default: false },
  title: { type: String, default: '确认操作' },
  message: { type: String, default: '' },
  confirmText: { type: String, default: '确认' },
  cancelText: { type: String, default: '取消' },
  type: { type: String, default: 'danger' }
})

const emit = defineEmits(['confirm', 'cancel', 'update:visible'])

function handleConfirm() { emit('confirm'); emit('update:visible', false) }
function handleCancel() { emit('cancel'); emit('update:visible', false) }
function onKeydown(e) { if (e.key === 'Escape' && props.visible) handleCancel() }

onMounted(() => document.addEventListener('keydown', onKeydown))
onUnmounted(() => document.removeEventListener('keydown', onKeydown))
</script>

<template>
  <Teleport to="body">
    <Transition name="confirm-dialog">
      <div v-if="visible" class="confirm-dialog__overlay" @click.self="handleCancel">
        <div class="confirm-dialog">
          <div :class="['confirm-dialog__icon', `confirm-dialog__icon--${type}`]">
            <span v-if="type === 'danger'">&#x26A0;</span>
            <span v-else>&#x2139;</span>
          </div>
          <h3 class="confirm-dialog__title">{{ title }}</h3>
          <p class="confirm-dialog__message">{{ message }}</p>
          <div class="confirm-dialog__actions">
            <button class="admin-btn admin-btn--secondary" @click="handleCancel">{{ cancelText }}</button>
            <button :class="['admin-btn', type === 'danger' ? 'admin-btn--danger' : 'admin-btn--primary']" @click="handleConfirm">{{ confirmText }}</button>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<style scoped>
.confirm-dialog__overlay {
  position: fixed;
  inset: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(4px);
}

.confirm-dialog {
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  padding: var(--spacing-xl);
  max-width: 420px;
  width: 90%;
  text-align: center;
  box-shadow: var(--shadow-xl);
}

.confirm-dialog__icon {
  width: 48px;
  height: 48px;
  margin: 0 auto var(--spacing-md);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
}

.confirm-dialog__icon--danger {
  background: rgba(233, 69, 96, 0.12);
  color: var(--color-accent);
}

.confirm-dialog__icon--warning {
  background: rgba(245, 158, 11, 0.12);
  color: #f59e0b;
}

.confirm-dialog__title {
  font-size: 1.125rem;
  margin-bottom: var(--spacing-sm);
}

.confirm-dialog__message {
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-lg);
  font-size: 0.875rem;
}

.confirm-dialog__actions {
  display: flex;
  gap: var(--spacing-sm);
  justify-content: center;
}

/* Transition */
.confirm-dialog-enter-active,
.confirm-dialog-leave-active {
  transition: opacity 0.25s ease;
}

.confirm-dialog-enter-active .confirm-dialog,
.confirm-dialog-leave-active .confirm-dialog {
  transition: transform 0.25s ease, opacity 0.25s ease;
}

.confirm-dialog-enter-from,
.confirm-dialog-leave-to {
  opacity: 0;
}

.confirm-dialog-enter-from .confirm-dialog {
  transform: scale(0.95);
  opacity: 0;
}

.confirm-dialog-leave-to .confirm-dialog {
  transform: scale(0.95);
  opacity: 0;
}
</style>
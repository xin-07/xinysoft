<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>联系邮箱</h3>
            <button class="close-btn" @click="closeModal">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <div
              v-for="(email, index) in emails"
              :key="index"
              class="email-item"
              @click="copyEmail(email)"
            >
              <svg class="email-icon" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
              </svg>
              <span class="email-text">{{ email }}</span>
              <svg class="copy-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
              </svg>
            </div>
          </div>
          <div v-if="copiedEmail" class="copy-toast">
            已复制到剪贴板
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script setup>
import { ref } from 'vue'

const props = defineProps({
  isOpen: {
    type: Boolean,
    default: false
  },
  emails: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close'])

const copiedEmail = ref(false)

const closeModal = () => {
  emit('close')
}

const copyEmail = async (email) => {
  try {
    await navigator.clipboard.writeText(email)
    copiedEmail.value = true
    setTimeout(() => {
      copiedEmail.value = false
    }, 2000)
  } catch (err) {
    console.error('Failed to copy:', err)
  }
}
</script>

<style scoped>
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
}

.modal-content {
  background: var(--color-bg-secondary);
  border-radius: 16px;
  border: 1px solid rgba(233, 69, 96, 0.2);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
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

.email-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  margin-bottom: 0.5rem;
  background: rgba(15, 52, 96, 0.3);
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid transparent;
}

.email-item:last-child {
  margin-bottom: 0;
}

.email-item:hover {
  background: rgba(233, 69, 96, 0.1);
  border-color: rgba(233, 69, 96, 0.3);
  transform: translateX(5px);
}

.email-icon {
  color: var(--color-accent);
  flex-shrink: 0;
}

.email-text {
  flex: 1;
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

.email-item:hover .copy-icon {
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
  transition: all 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .modal-content,
.modal-leave-to .modal-content {
  transform: scale(0.9) translateY(-20px);
}
</style>
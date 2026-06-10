<template>
  <Teleport to="body">
    <Transition name="modal">
      <div v-if="isOpen" class="modal-overlay" @click="closeModal">
        <div class="modal-content" @click.stop>
          <div class="modal-header">
            <h3>联系方式</h3>
            <button class="close-btn" @click="closeModal">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
              </svg>
            </button>
          </div>
          <div class="modal-body">
            <!-- 邮箱列表 -->
            <div v-for="(email, index) in emails" :key="index" class="contact-item" @click="copyContact(email, '邮箱')">
              <div class="contact-icon email-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                  <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                  <polyline points="22,6 12,13 2,6"></polyline>
                </svg>
              </div>
              <div class="contact-info">
                <span class="contact-label">{{ getEmailLabel(email) }}</span>
                <span class="contact-value">{{ email }}</span>
              </div>
              <svg class="copy-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
              </svg>
            </div>

            <!-- 微信 -->
            <div v-if="wechat" class="contact-item" @click="copyContact(wechat, '微信')">
              <div class="contact-icon wechat-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M9.5 4C5.36 4 2 6.69 2 10c0 1.87 1.1 3.55 2.82 4.66l-.71 2.14 2.48-1.24c.78.24 1.62.37 2.48.39-.14-.52-.22-1.06-.22-1.62C8.85 10.84 12.69 8 17.5 8c.28 0 .56.01.83.04C16.87 5.68 13.47 4 9.5 4zM7 8.5a1.25 1.25 0 1 1 0 2.5 1.25 1.25 0 0 1 0-2.5zm5 0a1.25 1.25 0 1 1 0 2.5 1.25 1.25 0 0 1 0-2.5z"/>
                  <path d="M22 13.83c0-2.76-2.69-5-6-5s-6 2.24-6 5c0 2.76 2.69 5 6 5 .7 0 1.38-.1 2.02-.3l1.98.99-.5-1.52C21.06 17.08 22 15.56 22 13.83zM14.25 13a1 1 0 1 1 0 2 1 1 0 0 1 0-2zm3.5 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
                </svg>
              </div>
              <div class="contact-info">
                <span class="contact-label">微信</span>
                <span class="contact-value">{{ wechat }}</span>
              </div>
              <svg class="copy-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
              </svg>
            </div>

            <!-- QQ -->
            <div v-if="qq" class="contact-item" @click="copyContact(qq, 'QQ')">
              <div class="contact-icon qq-icon">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C8.13 2 5 5.13 5 9v1.23c-1.09 1.2-2 3.05-2 5.1v.34c0 1.1.6 1.67 1.3 1.67.23 0 .48-.07.73-.2.22 1.27 1.2 2.32 2.3 2.87-.4.2-.7.62-.7 1.13 0 .7.72 1.27 1.6 1.27.68 0 2.37-.43 3.77-1.53.5.08 1.01.13 1.53.13.52 0 1.03-.05 1.53-.13 1.4 1.1 3.09 1.53 3.77 1.53.88 0 1.6-.57 1.6-1.27 0-.51-.3-.93-.7-1.13 1.1-.55 2.07-1.6 2.3-2.87.25.13.5.2.73.2.7 0 1.3-.57 1.3-1.67v-.34c0-2.05-.91-3.9-2-5.1V9c0-3.87-3.13-7-7-7zm-2.75 4.5a1.25 1.25 0 1 1 0 2.5 1.25 1.25 0 0 1 0-2.5zm5.5 0a1.25 1.25 0 1 1 0 2.5 1.25 1.25 0 0 1 0-2.5z"/>
                </svg>
              </div>
              <div class="contact-info">
                <span class="contact-label">QQ</span>
                <span class="contact-value">{{ qq }}</span>
              </div>
              <svg class="copy-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
              </svg>
            </div>
          </div>
          <div v-if="copiedText" class="copy-toast">
            {{ copiedText }} 已复制到剪贴板
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
  wechat: {
    type: String,
    default: ''
  },
  qq: {
    type: String,
    default: ''
  },
  emails: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close'])

const copiedText = ref('')

const getEmailLabel = (email) => {
  const domain = email.split('@')[1]?.toLowerCase()
  const labelMap = {
    'qq.com': 'QQ邮箱',
    '163.com': '网易邮箱',
    '126.com': '网易邮箱',
    'gmail.com': 'Gmail',
    'outlook.com': 'Outlook邮箱',
    'hotmail.com': 'Hotmail邮箱',
    'foxmail.com': 'Foxmail邮箱',
    'sina.com': '新浪邮箱',
    'sohu.com': '搜狐邮箱',
    'yahoo.com': 'Yahoo邮箱',
    'aliyun.com': '阿里邮箱',
    'icloud.com': 'iCloud邮箱'
  }
  return labelMap[domain] || '邮箱'
}

const closeModal = () => {
  emit('close')
}

const copyContact = async (text, label) => {
  try {
    await navigator.clipboard.writeText(text)
    copiedText.value = label
    setTimeout(() => {
      copiedText.value = ''
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
  border-radius: 12px;
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
  border-radius: 12px;
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
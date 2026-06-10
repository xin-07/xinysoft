<template>
  <section id="hero" class="hero">
    <div class="hero-container">
      <!-- 左侧内容区 -->
      <div class="hero-content">
        <div class="hero-text">
          <!-- 姓名 + 头衔 -->
          <div class="name-title-wrapper">
            <h1 class="name">
              <span class="name-text">{{ profile.name || 'xiny' }}</span>
              <span class="title-divider">·</span>
              <span class="title">{{ profile.title || '全栈开发工程师 · AI Agent 探索者' }}</span>
            </h1>
          </div>

          <!-- 个人简介 -->
          <p class="bio">
            {{ profile.bio || '暂无简介' }}
          </p>

          <!-- 技术标签组 -->
          <div class="tech-tags">
            <span
              v-for="(tag, index) in (profile.tech_tags || defaultTags)"
              :key="index"
              class="tech-tag"
              :style="{ animationDelay: `${index * 0.1}s` }"
              @click="handleTagClick(tag)"
            >
              {{ tag }}
            </span>
          </div>

          <!-- CTA 按钮 -->
          <button class="cta-button" @click="showContactModal = true">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
              <polyline points="22,6 12,13 2,6"></polyline>
            </svg>
            联系我
          </button>

          <!-- 社交图标 -->
          <div class="social-links">
            <a
              v-if="profile.github"
              :href="profile.github"
              target="_blank"
              rel="noopener noreferrer"
              class="social-link"
              title="GitHub"
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
            </a>
            <a
              v-if="profile.gitee"
              :href="profile.gitee"
              target="_blank"
              rel="noopener noreferrer"
              class="social-link"
              title="Gitee"
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M11.984 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.016 0zm6.09 5.333c.328 0 .593.266.592.593v1.482a.594.594 0 0 1-.593.592H9.777c-.982 0-1.778.796-1.778 1.778v5.63c0 .327.266.592.593.592h5.63c.327 0 .593-.265.593-.593v-1.481a.593.593 0 0 0-.593-.593h-3.556a.593.593 0 0 1-.593-.593V9.778c0-.327.266-.593.593-.593h5.926c.327 0 .593.266.593.593v6.815a2.37 2.37 0 0 1-2.37 2.37H6.519a.593.593 0 0 1-.593-.593V9.778a4.444 4.444 0 0 1 4.444-4.445h7.704z"/>
              </svg>
            </a>
            <button
              class="social-link"
              @click="showContactModal = true"
              title="邮箱"
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z"></path>
                <polyline points="22,6 12,13 2,6"></polyline>
              </svg>
            </button>
            <button
              v-if="profile.wechat"
              class="social-link wechat"
              @click="showContactModal = true"
              title="微信"
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M9.5 4C5.36 4 2 6.69 2 10c0 1.87 1.1 3.55 2.82 4.66l-.71 2.14 2.48-1.24c.78.24 1.62.37 2.48.39-.14-.52-.22-1.06-.22-1.62C8.85 10.84 12.69 8 17.5 8c.28 0 .56.01.83.04C16.87 5.68 13.47 4 9.5 4zM7 8.5a1.25 1.25 0 1 1 0 2.5 1.25 1.25 0 0 1 0-2.5zm5 0a1.25 1.25 0 1 1 0 2.5 1.25 1.25 0 0 1 0-2.5z"/>
                <path d="M22 13.83c0-2.76-2.69-5-6-5s-6 2.24-6 5c0 2.76 2.69 5 6 5 .7 0 1.38-.1 2.02-.3l1.98.99-.5-1.52C21.06 17.08 22 15.56 22 13.83zM14.25 13a1 1 0 1 1 0 2 1 1 0 0 1 0-2zm3.5 0a1 1 0 1 1 0 2 1 1 0 0 1 0-2z"/>
              </svg>
            </button>
            <button
              v-if="profile.qq"
              class="social-link qq"
              @click="showContactModal = true"
              title="QQ"
            >
              <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 2C8.13 2 5 5.13 5 9v1.23c-1.09 1.2-2 3.05-2 5.1v.34c0 1.1.6 1.67 1.3 1.67.23 0 .48-.07.73-.2.22 1.27 1.2 2.32 2.3 2.87-.4.2-.7.62-.7 1.13 0 .7.72 1.27 1.6 1.27.68 0 2.37-.43 3.77-1.53.5.08 1.01.13 1.53.13.52 0 1.03-.05 1.53-.13 1.4 1.1 3.09 1.53 3.77 1.53.88 0 1.6-.57 1.6-1.27 0-.51-.3-.93-.7-1.13 1.1-.55 2.07-1.6 2.3-2.87.25.13.5.2.73.2.7 0 1.3-.57 1.3-1.67v-.34c0-2.05-.91-3.9-2-5.1V9c0-3.87-3.13-7-7-7zm-2.75 4.5a1.25 1.25 0 1 1 0 2.5 1.25 1.25 0 0 1 0-2.5zm5.5 0a1.25 1.25 0 1 1 0 2.5 1.25 1.25 0 0 1 0-2.5z"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- 右侧头像区 -->
      <div class="hero-avatar">
        <div class="avatar-wrapper">
          <div v-if="loading" class="avatar-skeleton"></div>
          <img
            v-else-if="avatarUrl"
            :src="avatarUrl"
            :alt="profile.name || 'xiny'"
            class="avatar-image"
            @error="handleAvatarError"
          />
          <div v-else class="avatar-placeholder">
            {{ profile.name ? profile.name[0].toUpperCase() : 'X' }}
          </div>
        </div>
      </div>
    </div>

    <!-- 联系方式弹窗 -->
    <ContactModal
      :is-open="showContactModal"
      :wechat="profile.wechat || defaultWechat"
      :qq="profile.qq || defaultQQ"
      :emails="profile.email || defaultEmails"
      @close="showContactModal = false"
    />
  </section>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { profileAPI } from '../api'
import ContactModal from './ContactModal.vue'

const profile = ref({})
const loading = ref(true)
const showContactModal = ref(false)
const avatarError = ref(false)

const defaultTags = ['Vue3', 'FastAPI', 'MySQL', 'OpenClaw', 'HarmonyOS', 'ECharts']
const tagUrls = {
  'Vue3': 'https://cn.vuejs.org/',
  'FastAPI': 'https://fastapi.tiangolo.com/zh/',
  'MySQL': 'https://www.mysql.com/',
  'OpenClaw': 'https://openclaw.ai/',
  'HarmonyOS': 'https://developer.huawei.com/consumer/cn/harmonyos/',
  'ECharts': 'https://echarts.apache.org/zh/index.html'
}
const defaultEmails = ['12074835619@qq.com', 'xin_y0607@outlook.com', 'xiny0607.23@gmail.com', '13886527881@163.com']
const defaultWechat = 'Yyk-293342'
const defaultQQ = '12074835619'

const handleTagClick = (tag) => {
  const url = tagUrls[tag]
  if (url) {
    window.open(url, '_blank', 'noopener,noreferrer')
  }
}

const avatarUrl = computed(() => {
  // 如果头像加载失败或没有头像URL，使用默认头像
  if (avatarError.value || !profile.value.avatar_url) {
    return '/落日.jpg'
  }

  const url = profile.value.avatar_url

  // 如果是网络URL，直接返回
  if (url.startsWith('http://') || url.startsWith('https://')) {
    return url
  }

  // 如果是后端返回的相对路径（以 /api/avatar 开头），拼接 base URL
  if (url.startsWith('/api/avatar')) {
    return `http://127.0.0.1:8000${url}`
  }

  // 其他情况使用默认头像
  return '/落日.jpg'
})

const handleAvatarError = () => {
  avatarError.value = true
}

const fetchProfile = async () => {
  try {
    loading.value = true
    const data = await profileAPI.getProfile()
    profile.value = data
  } catch (error) {
    console.error('Failed to fetch profile:', error)
    // 使用默认数据
    profile.value = {
      name: 'xiny',
      title: '全栈开发工程师 · AI Agent 探索者',
      bio: '持续追踪 Vue3 与 AI Agent 前沿技术，通过实践快速掌握。具备跨专业协作能力，坚持每周技术复盘。',
      tech_tags: defaultTags,
      github: 'https://github.com/xin-07',
      gitee: 'https://gitee.com/xin-keep-going',
      wechat: defaultWechat,
      qq: defaultQQ,
      email: defaultEmails
    }
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchProfile()
})
</script>

<style scoped>
.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 6rem 2rem 4rem;
  position: relative;
  overflow: hidden;
}

.hero::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(circle at 20% 50%, rgba(233, 69, 96, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 50%, rgba(15, 52, 96, 0.3) 0%, transparent 50%);
  pointer-events: none;
}

.hero-container {
  max-width: 1200px;
  width: 100%;
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 4rem;
  align-items: center;
  position: relative;
  z-index: 1;
}

.hero-content {
  animation: fadeInLeft 0.8s ease-out;
}

@keyframes fadeInLeft {
  from {
    opacity: 0;
    transform: translateX(-30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.hero-text {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.name-title-wrapper {
  margin-bottom: 0.5rem;
}

.name {
  font-size: 3.5rem;
  font-weight: 700;
  line-height: 1.2;
  margin: 0;
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: 0.5rem;
}

.name-text {
  color: var(--color-text-primary);
  background: linear-gradient(135deg, var(--color-accent), #ff6b9d);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.title-divider {
  color: var(--color-text-secondary);
  font-weight: 300;
}

.title {
  font-size: 1.5rem;
  font-weight: 400;
  color: var(--color-text-secondary);
}

.bio {
  font-size: 1.125rem;
  line-height: 1.8;
  color: var(--color-text-secondary);
  max-width: 600px;
  margin: 0;
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.tech-tag {
  display: inline-block;
  padding: 0.5rem 1.25rem;
  background: rgba(233, 69, 96, 0.1);
  color: var(--color-accent);
  border-radius: 50px;
  font-size: 0.9rem;
  font-weight: 500;
  border: 1px solid rgba(233, 69, 96, 0.2);
  transition: all 0.3s ease;
  animation: fadeInUp 0.6s ease-out backwards;
  cursor: pointer;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.tech-tag:hover {
  background: rgba(233, 69, 96, 0.2);
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(233, 69, 96, 0.3);
}

.cta-button {
  display: inline-flex;
  align-items: center;
  gap: 0.75rem;
  padding: 1rem 2rem;
  background: var(--color-accent);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(233, 69, 96, 0.3);
  width: fit-content;
}

.cta-button:hover {
  background: #d63a52;
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(233, 69, 96, 0.4);
}

.cta-button:active {
  transform: translateY(0);
}

.social-links {
  display: flex;
  gap: 1.5rem;
  margin-top: 0.5rem;
}

.social-link {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 48px;
  height: 48px;
  background: rgba(15, 52, 96, 0.3);
  border: 1px solid rgba(233, 69, 96, 0.2);
  border-radius: 12px;
  color: var(--color-text-secondary);
  text-decoration: none;
  transition: all 0.3s ease;
  cursor: pointer;
}

.social-link:hover {
  background: rgba(233, 69, 96, 0.1);
  border-color: var(--color-accent);
  color: var(--color-accent);
  transform: translateY(-3px);
  box-shadow: 0 4px 15px rgba(233, 69, 96, 0.3);
}

.social-link.wechat:hover {
  background: rgba(7, 193, 96, 0.1);
  border-color: #07c160;
  color: #07c160;
  box-shadow: 0 4px 15px rgba(7, 193, 96, 0.3);
}

.social-link.qq:hover {
  background: rgba(18, 183, 245, 0.1);
  border-color: #12b7f5;
  color: #12b7f5;
  box-shadow: 0 4px 15px rgba(18, 183, 245, 0.3);
}

.hero-avatar {
  animation: fadeInRight 0.8s ease-out;
}

@keyframes fadeInRight {
  from {
    opacity: 0;
    transform: translateX(30px);
  }
  to {
    opacity: 1;
    transform: translateX(0);
  }
}

.avatar-wrapper {
  position: relative;
  width: 320px;
  height: 320px;
}

.avatar-image,
.avatar-placeholder,
.avatar-skeleton {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.avatar-image {
  border: 4px solid var(--color-accent);
  box-shadow:
    0 0 0 8px rgba(233, 69, 96, 0.1),
    0 20px 60px rgba(0, 0, 0, 0.5);
}

.avatar-placeholder {
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--color-accent), #ff6b9d);
  color: white;
  font-size: 8rem;
  font-weight: 700;
  border: 4px solid rgba(233, 69, 96, 0.3);
  box-shadow:
    0 0 0 8px rgba(233, 69, 96, 0.1),
    0 20px 60px rgba(0, 0, 0, 0.5);
}

.avatar-skeleton {
  background: linear-gradient(
    90deg,
    rgba(15, 52, 96, 0.3) 25%,
    rgba(15, 52, 96, 0.5) 50%,
    rgba(15, 52, 96, 0.3) 75%
  );
  background-size: 200% 100%;
  animation: skeleton 1.5s ease-in-out infinite;
  border: 4px solid rgba(233, 69, 96, 0.2);
}

@keyframes skeleton {
  0% {
    background-position: 200% 0;
  }
  100% {
    background-position: -200% 0;
  }
}

/* 响应式设计 */
@media (max-width: 1200px) {
  .hero-container {
    grid-template-columns: 1fr;
    gap: 3rem;
  }

  .hero-avatar {
    order: -1;
    display: flex;
    justify-content: center;
  }

  .avatar-wrapper {
    width: 280px;
    height: 280px;
  }
}

@media (max-width: 768px) {
  .hero {
    padding: 5rem 1.5rem 3rem;
  }

  .name {
    font-size: 2.5rem;
    flex-direction: column;
    gap: 0.25rem;
  }

  .title {
    font-size: 1.125rem;
  }

  .bio {
    font-size: 1rem;
  }

  .avatar-wrapper {
    width: 220px;
    height: 220px;
  }

  .cta-button {
    width: 100%;
    justify-content: center;
  }

  .social-links {
    justify-content: center;
  }
}

@media (max-width: 480px) {
  .name {
    font-size: 2rem;
  }

  .title {
    font-size: 1rem;
  }

  .tech-tags {
    gap: 0.5rem;
  }

  .tech-tag {
    padding: 0.4rem 1rem;
    font-size: 0.85rem;
  }

  .avatar-wrapper {
    width: 180px;
    height: 180px;
  }

  .avatar-placeholder {
    font-size: 6rem;
  }
}
</style>
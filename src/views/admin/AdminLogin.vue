<script setup>
import { ref, inject } from 'vue'
import { useRouter, useRoute } from 'vue-router'

const router = useRouter()
const route = useRoute()

// 从 provide 获取 adminAuth（main.js 中注入）
const adminAuth = inject('adminAuth', null)

const username = ref('')
const password = ref('')
const loading = ref(false)
const errorMsg = ref('')

async function handleLogin() {
  errorMsg.value = ''
  if (!username.value || !password.value) {
    errorMsg.value = '请输入用户名和密码'
    return
  }

  loading.value = true
  try {
    await adminAuth.login(username.value, password.value)
    const redirect = route.query.redirect || '/admin'
    router.push(redirect)
  } catch (err) {
    const status = err.response?.status
    if (status === 401) {
      errorMsg.value = '用户名或密码错误'
    } else if (status === 429) {
      errorMsg.value = '操作过于频繁，请稍后再试'
    } else {
      errorMsg.value = err.response?.data?.message || '网络错误，请稍后重试'
    }
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="login-page">
    <div class="login-card">
      <div class="login-card__logo">
        <h1 class="login-card__title">管理后台</h1>
        <p class="login-card__subtitle">xinysoft 作品集管理</p>
      </div>

      <div v-if="errorMsg" class="login-card__error">
        <span>&#x26A0;</span>
        <span>{{ errorMsg }}</span>
      </div>

      <form class="login-card__form" @submit.prevent="handleLogin">
        <div class="admin-form-group">
          <label class="admin-form-group__label" for="login-username">用户名</label>
          <input
            id="login-username"
            v-model="username"
            type="text"
            class="admin-input"
            placeholder="请输入管理员用户名"
            autocomplete="username"
            :disabled="loading"
          />
        </div>

        <div class="admin-form-group">
          <label class="admin-form-group__label" for="login-password">密码</label>
          <input
            id="login-password"
            v-model="password"
            type="password"
            class="admin-input"
            placeholder="请输入密码"
            autocomplete="current-password"
            :disabled="loading"
          />
        </div>

        <button
          type="submit"
          class="admin-btn admin-btn--primary login-card__submit"
          :class="{ 'admin-btn--loading': loading }"
          :disabled="loading"
        >
          登 录
        </button>
      </form>
    </div>
  </div>
</template>
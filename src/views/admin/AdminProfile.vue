<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { adminAPI } from '../../api/admin'
import { useToast } from '../../composables/useToast'
import { getTagBackgroundColor } from '../../config/techStackColors'
import FileUploader from '../../components/admin/FileUploader.vue'

const router = useRouter()
const toast = useToast()

// 初始数据快照，用于检测未保存更改
const originalData = ref(null)

const form = ref({
  name: '',
  avatar_url: '',
  title: '',
  bio: '',
  tech_tags: [],
  github: '',
  gitee: '',
  wechat: '',
  qq: '',
  email: []
})

const tagInput = ref('')
const emailInput = ref('')

const loading = ref(false)
const saving = ref(false)

// 技术标签操作（直接操作 form.value.tech_tags）
function addTechTag() {
  const val = tagInput.value.trim()
  if (!val || form.value.tech_tags.includes(val)) { tagInput.value = ''; return }
  form.value.tech_tags.push(val)
  tagInput.value = ''
}
function removeTechTag(index) { form.value.tech_tags.splice(index, 1) }
function onTechKeydown(e) {
  if (e.key === 'Enter') { e.preventDefault(); addTechTag() }
}

// 邮箱操作（直接操作 form.value.email）
function addEmail() {
  const val = emailInput.value.trim()
  // 简单邮箱格式校验
  if (!val || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val)) {
    toast.error('请输入有效的邮箱地址')
    return
  }
  if (form.value.email.includes(val)) { emailInput.value = ''; return }
  form.value.email.push(val)
  emailInput.value = ''
}
function removeEmail(index) { form.value.email.splice(index, 1) }
function onEmailKeydown(e) {
  if (e.key === 'Enter') { e.preventDefault(); addEmail() }
}

// 检测是否有未保存的更改
function hasUnsavedChanges() {
  if (!originalData.value) return false
  const current = form.value
  return (
    current.name !== originalData.value.name ||
    current.avatar_url !== originalData.value.avatar_url ||
    current.title !== originalData.value.title ||
    current.bio !== originalData.value.bio ||
    JSON.stringify(current.tech_tags) !== JSON.stringify(originalData.value.tech_tags) ||
    current.github !== originalData.value.github ||
    current.gitee !== originalData.value.gitee ||
    current.wechat !== originalData.value.wechat ||
    current.qq !== originalData.value.qq ||
    JSON.stringify(current.email) !== JSON.stringify(originalData.value.email)
  )
}

// 加载个人资料
async function loadProfile() {
  loading.value = true
  try {
    const res = await adminAPI.getProfile()
    const data = res.data
    form.value = {
      name: data.name || '',
      avatar_url: data.avatar_url || '',
      title: data.title || '',
      bio: data.bio || '',
      tech_tags: data.tech_tags || [],
      github: data.github || '',
      gitee: data.gitee || '',
      wechat: data.wechat || '',
      qq: data.qq || '',
      email: data.email || []
    }
    // 记录初始快照
    originalData.value = { ...form.value }
  } catch (err) {
    toast.error('加载个人资料失败')
  } finally {
    loading.value = false
  }
}

// 表单校验
function validateForm() {
  // 必填项检查
  if (!form.value.name.trim()) {
    toast.error('姓名为必填项')
    return false
  }
  // URL 格式校验（非空时）
  if (form.value.github && !isValidUrl(form.value.github)) {
    toast.error('GitHub 地址格式不正确')
    return false
  }
  if (form.value.gitee && !isValidUrl(form.value.gitee)) {
    toast.error('Gitee 地址格式不正确')
    return false
  }
  return true
}

function isValidUrl(str) {
  try {
    new URL(str)
    return true
  } catch {
    return false
  }
}

// 保存
async function handleSave() {
  if (!validateForm()) return

  saving.value = true
  try {
    await adminAPI.updateProfile(form.value)
    // 更新初始快照，标记为已保存
    originalData.value = { ...form.value }
    toast.success('个人资料更新成功')
  } catch (err) {
    let msg
    if (!err.response) {
      msg = '网络连接失败，请检查网络后重试'
    } else {
      msg = err.response.data?.message || '保存失败，请重试'
    }
    toast.error(msg)
  } finally {
    saving.value = false
  }
}

function handleCancel() {
  if (hasUnsavedChanges()) {
    if (!confirm('当前有未保存的更改，确定要离开吗？')) return
  }
  router.push({ name: 'AdminDashboard' })
}

onMounted(() => {
  loadProfile()
})
</script>

<template>
  <div class="admin-form">
    <h1 class="admin-text-page-title">个人资料</h1>

    <div v-if="loading" class="admin-skeleton-group" style="margin-top:24px;">
      <!-- 基本信息区骨架 -->
      <div class="admin-skeleton admin-skeleton--title" style="width:40%"></div>
      <div class="admin-skeleton admin-skeleton--text"></div>
      <div class="admin-skeleton admin-skeleton--text-short"></div>
      <div class="admin-skeleton admin-skeleton--text-short"></div>
      <div class="admin-skeleton admin-skeleton--text" style="height:80px;"></div>
      <div class="admin-skeleton admin-skeleton--text"></div>
      <!-- 社交链接区骨架 -->
      <div class="admin-skeleton admin-skeleton--title" style="width:40%; margin-top:16px;"></div>
      <div class="admin-skeleton admin-skeleton--text-short"></div>
      <div class="admin-skeleton admin-skeleton--text-short"></div>
      <div class="admin-skeleton admin-skeleton--text-short"></div>
      <div class="admin-skeleton admin-skeleton--text-short"></div>
      <div class="admin-skeleton admin-skeleton--text"></div>
    </div>

    <template v-else>
      <!-- 基本信息 -->
      <div class="admin-form__section">
        <h2 class="admin-form__section-title">基本信息</h2>

        <div class="admin-form-group">
          <label class="admin-form-group__label">头像</label>
          <FileUploader v-model="form.avatar_url" :multiple="false" />
        </div>

        <div class="admin-form-group">
          <label class="admin-form-group__label admin-form-group__label--required" for="prof-name">姓名</label>
          <input id="prof-name" v-model="form.name" type="text" class="admin-input" placeholder="请输入姓名" />
        </div>

        <div class="admin-form-group">
          <label class="admin-form-group__label" for="prof-title">头衔</label>
          <input id="prof-title" v-model="form.title" type="text" class="admin-input" placeholder="如：全栈开发工程师" />
        </div>

        <div class="admin-form-group">
          <label class="admin-form-group__label" for="prof-bio">个人简介</label>
          <textarea id="prof-bio" v-model="form.bio" class="admin-textarea" placeholder="请输入个人简介"></textarea>
        </div>

        <div class="admin-form-group">
          <label class="admin-form-group__label">技术标签</label>
          <div class="tag-input">
            <span
              v-for="(tag, index) in form.tech_tags"
              :key="index"
              class="tag-input__tag"
              :style="{ backgroundColor: getTagBackgroundColor(tag), color: '#FFFFFF' }"
            >
              {{ tag }}
              <span class="tag-remove" @click="removeTechTag(index)">&times;</span>
            </span>
            <input
              v-model="tagInput"
              type="text"
              class="tag-input__input"
              placeholder="输入后按回车添加"
              @keydown="onTechKeydown"
            />
          </div>
        </div>
      </div>

      <!-- 社交链接 -->
      <div class="admin-form__section">
        <h2 class="admin-form__section-title">社交链接</h2>

        <div class="admin-form-group">
          <label class="admin-form-group__label" for="prof-github">GitHub</label>
          <input id="prof-github" v-model="form.github" type="url" class="admin-input" placeholder="https://github.com/..." />
        </div>

        <div class="admin-form-group">
          <label class="admin-form-group__label" for="prof-gitee">Gitee</label>
          <input id="prof-gitee" v-model="form.gitee" type="url" class="admin-input" placeholder="https://gitee.com/..." />
        </div>

        <div class="admin-form-group">
          <label class="admin-form-group__label" for="prof-wechat">微信</label>
          <input id="prof-wechat" v-model="form.wechat" type="text" class="admin-input" placeholder="微信号" />
        </div>

        <div class="admin-form-group">
          <label class="admin-form-group__label" for="prof-qq">QQ</label>
          <input id="prof-qq" v-model="form.qq" type="text" class="admin-input" placeholder="QQ号" />
        </div>

        <div class="admin-form-group">
          <label class="admin-form-group__label">邮箱</label>
          <div class="tag-input">
            <span
              v-for="(email, index) in form.email"
              :key="index"
              class="tag-input__tag"
              :style="{ backgroundColor: getTagBackgroundColor(email), color: '#FFFFFF' }"
            >
              {{ email }}
              <span class="tag-remove" @click="removeEmail(index)">&times;</span>
            </span>
            <input
              v-model="emailInput"
              type="email"
              class="tag-input__input"
              placeholder="输入邮箱后按回车添加"
              @keydown="onEmailKeydown"
            />
          </div>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="admin-form__actions">
        <button type="button" class="admin-btn admin-btn--secondary" @click="handleCancel">取消</button>
        <button
          type="button"
          class="admin-btn admin-btn--primary"
          :class="{ 'admin-btn--loading': saving }"
          :disabled="saving"
          @click="handleSave"
        >
          保存更改
        </button>
      </div>
    </template>
  </div>
</template>

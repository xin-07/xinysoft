<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { adminAPI } from '../../api/admin'
import { getTagBackgroundColor } from '../../config/techStackColors'
import ConfirmDialog from './ConfirmDialog.vue'
import FileUploader from './FileUploader.vue'
import { useToast } from '../../composables/useToast'

const router = useRouter()
const route = useRoute()
const toast = useToast()

// 区分新增/编辑模式
const projectId = computed(() => route.params.id ? Number(route.params.id) : null)
const isEdit = computed(() => !!projectId.value)

// 表单数据
const form = ref({
  title: '',
  subtitle: '',
  description: '',
  tech_stack: [],
  cover_url: '',
  screenshots: [],
  live_url: '',
  repo_url: '',
  is_featured: false,
  sort_order: 0
})

// 技术栈标签输入
const tagInput = ref('')
const techTags = ref([])

// 错误状态
const errors = ref({})
const saving = ref(false)
const loading = ref(false)
const formDirty = ref(false)

// 取消确认弹窗
const showCancelConfirm = ref(false)

// 标记表单已修改
function markDirty() {
  formDirty.value = true
}

// 加载编辑数据
async function loadProject() {
  if (!isEdit.value) return
  loading.value = true
  try {
    const res = await adminAPI.getProject(projectId.value)
    const data = res.data
    form.value = {
      title: data.title || '',
      subtitle: data.subtitle || '',
      description: data.description || '',
      tech_stack: data.tech_stack || [],
      cover_url: data.cover_url || '',
      screenshots: data.screenshots || [],
      live_url: data.live_url || '',
      repo_url: data.repo_url || '',
      is_featured: !!data.is_featured,
      sort_order: data.sort_order || 0
    }
    techTags.value = data.tech_stack || []
  } catch (err) {
    toast.error('加载项目数据失败')
  } finally {
    loading.value = false
  }
}

// 技术栈标签操作
function addTag() {
  const val = tagInput.value.trim()
  if (!val) return
  if (techTags.value.includes(val)) {
    tagInput.value = ''
    return
  }
  techTags.value.push(val)
  tagInput.value = ''
  markDirty()
}

function removeTag(index) {
  techTags.value.splice(index, 1)
  markDirty()
}

function handleTagKeydown(e) {
  if (e.key === 'Enter') {
    e.preventDefault()
    addTag()
  }
}

// 获取标签颜色
function tagBgColor(tag) {
  return getTagBackgroundColor(tag)
}

function tagTextColor() {
  return '#FFFFFF'
}

// 表单校验
function validate() {
  const errs = {}
  if (!form.value.title || !form.value.title.trim()) {
    errs.title = '标题不能为空'
  } else if (form.value.title.length > 100) {
    errs.title = '标题不能超过100个字符'
  }
  if (form.value.description && form.value.description.length > 5000) {
    errs.description = '描述不能超过5000个字符'
  }
  errors.value = errs
  return Object.keys(errs).length === 0
}

// 提交表单
async function handleSubmit() {
  if (!validate()) return
  saving.value = true
  try {
    const payload = {
      ...form.value,
      tech_stack: techTags.value
    }
    if (isEdit.value) {
      await adminAPI.updateProject(projectId.value, payload)
      toast.success('项目更新成功')
    } else {
      await adminAPI.createProject(payload)
      toast.success('项目创建成功')
    }
    router.push({ name: 'AdminProjects' })
  } catch (err) {
    const msg = err.response?.data?.message || '保存失败，请重试'
    toast.error(msg)
  } finally {
    saving.value = false
  }
}

// 取消
function handleCancel() {
  if (formDirty.value) {
    showCancelConfirm.value = true
  } else {
    router.push({ name: 'AdminProjects' })
  }
}

function confirmCancel() {
  showCancelConfirm.value = false
  router.push({ name: 'AdminProjects' })
}

onMounted(() => {
  loadProject()
})
</script>

<template>
  <div class="admin-form">
    <h1 class="admin-text-page-title">{{ isEdit ? '编辑项目' : '新增项目' }}</h1>

    <!-- 加载态 -->
    <div v-if="loading" class="admin-skeleton-group">
      <div class="admin-skeleton admin-skeleton--title"></div>
      <div class="admin-skeleton admin-skeleton--text"></div>
      <div class="admin-skeleton admin-skeleton--text-short"></div>
    </div>

    <template v-else>
      <!-- 基础信息 -->
      <div class="admin-form__section">
        <h2 class="admin-form__section-title">基础信息</h2>

        <div class="admin-form-group">
          <label class="admin-form-group__label admin-form-group__label--required" for="proj-title">项目标题</label>
          <input
            id="proj-title"
            v-model="form.title"
            type="text"
            class="admin-input"
            :class="{ 'admin-input--error': errors.title }"
            placeholder="请输入项目标题"
            maxlength="100"
            @input="markDirty"
          />
          <p v-if="errors.title" class="admin-form-group__error">{{ errors.title }}</p>
        </div>

        <div class="admin-form-group">
          <label class="admin-form-group__label" for="proj-subtitle">副标题</label>
          <input
            id="proj-subtitle"
            v-model="form.subtitle"
            type="text"
            class="admin-input"
            placeholder="请输入项目副标题"
            @input="markDirty"
          />
        </div>

        <div class="admin-form-group">
          <label class="admin-form-group__label" for="proj-desc">项目描述</label>
          <textarea
            id="proj-desc"
            v-model="form.description"
            class="admin-textarea"
            placeholder="请输入项目描述"
            maxlength="5000"
            @input="markDirty"
          ></textarea>
          <p class="admin-form-group__hint">{{ form.description.length }}/5000</p>
        </div>

        <div class="admin-form-group">
          <label class="admin-form-group__label">技术栈</label>
          <div class="tag-input">
            <span
              v-for="(tag, index) in techTags"
              :key="index"
              class="tag-input__tag"
              :style="{ backgroundColor: tagBgColor(tag), color: tagTextColor() }"
            >
              {{ tag }}
              <span class="tag-input__tag-remove" @click="removeTag(index)">&times;</span>
            </span>
            <input
              v-model="tagInput"
              type="text"
              class="tag-input__input"
              placeholder="输入后按回车添加"
              @keydown="handleTagKeydown"
            />
          </div>
        </div>
      </div>

      <!-- 媒体资源 -->
      <div class="admin-form__section">
        <h2 class="admin-form__section-title">媒体资源</h2>

        <div class="admin-form-group">
          <label class="admin-form-group__label">封面图片</label>
          <FileUploader v-model="form.cover_url" :multiple="false" @update:model-value="markDirty" />
        </div>

        <div class="admin-form-group">
          <label class="admin-form-group__label">截图列表</label>
          <FileUploader v-model="form.screenshots" :multiple="true" @update:model-value="markDirty" />
        </div>
      </div>

      <!-- 链接与设置 -->
      <div class="admin-form__section">
        <h2 class="admin-form__section-title">链接与设置</h2>

        <div class="admin-form-group">
          <label class="admin-form-group__label" for="proj-live">线上地址</label>
          <input
            id="proj-live"
            v-model="form.live_url"
            type="url"
            class="admin-input"
            placeholder="https://example.com"
            @input="markDirty"
          />
        </div>

        <div class="admin-form-group">
          <label class="admin-form-group__label" for="proj-repo">仓库地址</label>
          <input
            id="proj-repo"
            v-model="form.repo_url"
            type="url"
            class="admin-input"
            placeholder="https://github.com/..."
            @input="markDirty"
          />
        </div>

        <div class="admin-form-group">
          <label class="admin-form-group__label">精选项目</label>
          <label class="admin-toggle">
            <input
              v-model="form.is_featured"
              type="checkbox"
              class="admin-toggle__input"
              @change="markDirty"
            />
            <span class="admin-toggle__track"></span>
            <span>在首页精选区展示</span>
          </label>
        </div>

        <div class="admin-form-group">
          <label class="admin-form-group__label" for="proj-sort">排序权重</label>
          <input
            id="proj-sort"
            v-model.number="form.sort_order"
            type="number"
            class="admin-input"
            style="max-width:160px"
            @input="markDirty"
          />
          <p class="admin-form-group__hint">数值越大越靠前</p>
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="admin-form__actions">
        <button type="button" class="admin-btn admin-btn--secondary" @click="handleCancel">
          取消
        </button>
        <button
          type="button"
          class="admin-btn admin-btn--primary"
          :class="{ 'admin-btn--loading': saving }"
          :disabled="saving"
          @click="handleSubmit"
        >
          {{ isEdit ? '保存更改' : '创建项目' }}
        </button>
      </div>
    </template>

    <!-- 取消确认弹窗 -->
    <ConfirmDialog
      v-model:visible="showCancelConfirm"
      title="放弃更改？"
      message="未保存的更改将丢失，确定要离开吗？"
      confirm-text="确定离开"
      cancel-text="继续编辑"
      type="warning"
      @confirm="confirmCancel"
    />
  </div>
</template>
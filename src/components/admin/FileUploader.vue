<script setup>
import { ref, computed } from 'vue'
import { adminAPI } from '../../api/admin'
import { useToast } from '../../composables/useToast'

const props = defineProps({
  modelValue: { type: [String, Array], default: '' },
  multiple: { type: Boolean, default: false },
  accept: { type: String, default: 'image/jpeg,image/png,image/webp' },
  maxSize: { type: Number, default: 5 * 1024 * 1024 } // 5MB
})

const emit = defineEmits(['update:modelValue'])
const toast = useToast()

const uploading = ref(false)
const dragOver = ref(false)
const urlInputMode = ref(false)
const urlInput = ref('')

// 触发文件选择
const fileInput = ref(null)
function triggerFileInput() {
  fileInput.value?.click()
}

// 处理文件上传
async function handleFileSelect(e) {
  const files = e.target.files
  if (!files || files.length === 0) return
  await uploadFiles(Array.from(files))
  // 重置 input 以允许重复选择同一文件
  e.target.value = ''
}

async function uploadFiles(files) {
  const results = []
  uploading.value = true
  try {
    for (const file of files) {
      // 校验类型
      if (!props.accept.split(',').some(t => file.type.match(t.trim()))) {
        toast.error(`不支持的文件格式，仅允许 JPG、PNG、WebP`)
        continue
      }
      // 校验大小
      if (file.size > props.maxSize) {
        toast.error(`文件大小不能超过 ${Math.round(props.maxSize / 1024 / 1024)}MB`)
        continue
      }
      try {
        const res = await adminAPI.uploadFile(file)
        if (res.data?.url) {
          results.push(res.data.url)
        }
      } catch (err) {
        console.error('Upload failed:', err)
      }
    }

    if (props.multiple) {
      const current = Array.isArray(props.modelValue) ? [...props.modelValue] : []
      emit('update:modelValue', [...current, ...results])
    } else if (results.length > 0) {
      emit('update:modelValue', results[0])
    }
  } finally {
    uploading.value = false
  }
}

// 拖拽处理
function onDragOver(e) {
  e.preventDefault()
  dragOver.value = true
}
function onDragLeave() {
  dragOver.value = false
}
function onDrop(e) {
  e.preventDefault()
  dragOver.value = false
  const files = e.dataTransfer?.files
  if (files && files.length > 0) {
    uploadFiles(Array.from(files))
  }
}

// URL 输入模式
function addUrl() {
  const url = urlInput.value.trim()
  if (!url) return
  if (props.multiple) {
    const current = Array.isArray(props.modelValue) ? [...props.modelValue] : []
    emit('update:modelValue', [...current, url])
  } else {
    emit('update:modelValue', url)
  }
  urlInput.value = ''
}

// 移除已上传/已输入的文件
function removeItem(index) {
  if (props.multiple && Array.isArray(props.modelValue)) {
    const updated = [...props.modelValue]
    updated.splice(index, 1)
    emit('update:modelValue', updated)
  } else {
    emit('update:modelValue', '')
  }
}

// 预览列表（computed，避免模板中重复调用）
const previewList = computed(() => {
  if (props.multiple) {
    return Array.isArray(props.modelValue) ? props.modelValue : []
  }
  return props.modelValue ? [props.modelValue] : []
})
</script>

<template>
  <div class="file-uploader">
    <!-- 拖拽上传区域 -->
    <div
      class="file-uploader__dropzone"
      :class="{ 'file-uploader__dropzone--active': dragOver }"
      @click="triggerFileInput"
      @dragover="onDragOver"
      @dragleave="onDragLeave"
      @drop="onDrop"
    >
      <span class="file-uploader__dropzone-icon">
        <!-- 上传中：加载动画 -->
        <svg v-if="uploading" class="file-uploader__icon-spin" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 12a9 9 0 1 1-6.219-8.56"/>
        </svg>
        <!-- 默认：上传图标 -->
        <svg v-else viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="17 8 12 3 7 8"/>
          <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
      </span>
      <span class="file-uploader__dropzone-text">
        {{ uploading ? '上传中...' : '拖拽文件到此处或点击上传' }}
      </span>
      <span class="file-uploader__dropzone-hint">
        支持 JPG、PNG、WebP，最大 5MB
      </span>
      <input
        ref="fileInput"
        type="file"
        :accept="accept"
        :multiple="multiple"
        class="visually-hidden"
        @change="handleFileSelect"
      />
    </div>

    <!-- URL 手动输入 -->
    <div class="file-uploader__url-input">
      <input
        v-model="urlInput"
        type="text"
        class="admin-input"
        placeholder="或手动输入图片 URL"
        @keyup.enter="addUrl"
      />
      <button type="button" class="admin-btn admin-btn--secondary admin-btn--sm" @click="addUrl">添加</button>
    </div>

    <!-- 预览列表 -->
    <div v-if="previewList.length > 0" class="file-uploader__preview-list">
      <div
        v-for="(url, index) in previewList"
        :key="index"
        class="file-uploader__preview-item"
      >
        <img :src="url" class="file-uploader__preview-image" alt="预览" />
        <button class="file-uploader__preview-remove" @click="removeItem(index)">&times;</button>
      </div>
    </div>
  </div>
</template>
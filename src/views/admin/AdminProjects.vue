<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { adminAPI } from '../../api/admin'
import { getTagBackgroundColor } from '../../config/techStackColors'
import StatusBadge from '../../components/admin/StatusBadge.vue'
import ConfirmDialog from '../../components/admin/ConfirmDialog.vue'
import { useToast } from '../../composables/useToast'

const router = useRouter()
const toast = useToast()

// 数据
const projects = ref([])
const loading = ref(true)
const error = ref(false)
const pagination = ref({ total: 0, page: 1, pageSize: 10 })

// 删除确认
const deleteTarget = ref(null)
const showDeleteConfirm = ref(false)

// 状态切换中的项目 ID 集合
const togglingIds = ref(new Set())

// 加载项目列表
async function loadProjects() {
  loading.value = true
  error.value = false
  try {
    const res = await adminAPI.getProjects(pagination.value.page, pagination.value.pageSize)
    const data = res.data
    projects.value = data.items || []
    pagination.value.total = data.total || 0
    pagination.value.page = data.page || 1
    pagination.value.pageSize = data.page_size || 10
  } catch (err) {
    error.value = true
    projects.value = []
  } finally {
    loading.value = false
  }
}

// 分页
function changePage(page) {
  pagination.value.page = page
  loadProjects()
}

function changePageSize(e) {
  pagination.value.pageSize = Number(e.target.value)
  pagination.value.page = 1
  loadProjects()
}

const totalPages = computed(() => Math.ceil(pagination.value.total / pagination.value.pageSize) || 1)

// 技术栈缩略
function getTechStackDisplay(techStack) {
  if (!techStack || techStack.length === 0) return []
  const max = 3
  if (techStack.length <= max) return techStack.map(t => ({ label: t, isMore: false }))
  const shown = techStack.slice(0, max).map(t => ({ label: t, isMore: false }))
  shown.push({ label: `+${techStack.length - max}`, isMore: true })
  return shown
}

function tagBgColor(tag) {
  return getTagBackgroundColor(tag)
}

// 状态切换
async function toggleStatus(project) {
  const newStatus = project.status === 'published' ? 'draft' : 'published'
  togglingIds.value.add(project.id)
  try {
    await adminAPI.toggleStatus(project.id, newStatus)
    project.status = newStatus
    toast.success(newStatus === 'published' ? '已发布' : '已转为草稿')
  } catch (err) {
    toast.error('状态切换失败')
  } finally {
    togglingIds.value.delete(project.id)
  }
}

// 删除
function confirmDelete(project) {
  deleteTarget.value = project
  showDeleteConfirm.value = true
}

async function handleDelete() {
  if (!deleteTarget.value) return
  try {
    await adminAPI.deleteProject(deleteTarget.value.id)
    toast.success('项目已删除')
    showDeleteConfirm.value = false
    deleteTarget.value = null
    loadProjects()
  } catch (err) {
    toast.error('删除失败')
  }
}

// 编辑
function editProject(project) {
  router.push({ name: 'AdminProjectEdit', params: { id: project.id } })
}

// 新增
function goCreate() {
  router.push({ name: 'AdminProjectNew' })
}

// 格式化日期
function formatDate(dateStr) {
  if (!dateStr) return '-'
  const d = new Date(dateStr)
  return d.toLocaleDateString('zh-CN', { year: 'numeric', month: '2-digit', day: '2-digit' })
}

// 生成可视页码列表
const visiblePages = computed(() => {
  const total = totalPages.value
  const current = pagination.value.page
  const pages = []
  const maxVisible = 5
  let start = Math.max(1, current - Math.floor(maxVisible / 2))
  let end = Math.min(total, start + maxVisible - 1)
  if (end - start + 1 < maxVisible) {
    start = Math.max(1, end - maxVisible + 1)
  }
  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

onMounted(() => {
  loadProjects()
})
</script>

<template>
  <div>
    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 24px;">
      <h1 class="admin-text-page-title" style="margin-bottom: 0;">项目管理</h1>
      <button class="admin-btn admin-btn--primary" @click="goCreate">
        &#x2795; 新增项目
      </button>
    </div>

    <!-- 加载态：骨架屏 -->
    <div v-if="loading" class="admin-skeleton-table">
      <div v-for="i in 5" :key="i" class="admin-skeleton admin-skeleton--table-row"></div>
    </div>

    <!-- 错误态 -->
    <div v-else-if="error" class="admin-empty">
      <div class="admin-empty__icon">&#x26A0;</div>
      <h3 class="admin-empty__title">加载失败</h3>
      <p class="admin-empty__description">获取项目列表时发生错误，请检查网络后重试。</p>
      <button class="admin-btn admin-btn--secondary" @click="loadProjects">重试</button>
    </div>

    <!-- 空状态 -->
    <div v-else-if="projects.length === 0" class="admin-empty">
      <div class="admin-empty__icon">&#x1F4C1;</div>
      <h3 class="admin-empty__title">还没有项目</h3>
      <p class="admin-empty__description">点击右上角"新增项目"按钮创建第一个作品集项目。</p>
      <button class="admin-btn admin-btn--primary" @click="goCreate">新增项目</button>
    </div>

    <!-- 表格 -->
    <template v-else>
      <div class="admin-table-wrapper">
        <table class="admin-table">
          <thead>
            <tr>
              <th class="admin-table__cell--center" style="width:60px;">#</th>
              <th>标题</th>
              <th>技术栈</th>
              <th class="admin-table__cell--center" style="width:100px;">状态</th>
              <th class="admin-table__cell--center" style="width:80px;">权重</th>
              <th style="width:150px;">创建时间</th>
              <th class="admin-table__cell--center" style="width:200px;">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(project, index) in projects" :key="project.id">
              <td class="admin-table__cell--center">{{ (pagination.page - 1) * pagination.pageSize + index + 1 }}</td>
              <td>
                <span style="font-weight: 500;">{{ project.title }}</span>
              </td>
              <td>
                <div style="display: flex; flex-wrap: wrap; gap: 4px;">
                  <span
                    v-for="(t, ti) in getTechStackDisplay(project.tech_stack)"
                    :key="ti"
                    :style="t.isMore ? { background: 'var(--admin-skeleton-base)', color: 'var(--color-text-secondary)' } : { backgroundColor: tagBgColor(t.label), color: '#FFFFFF' }"
                    style="display: inline-block; padding: 2px 8px; border-radius: var(--radius-full); font-size: 0.75rem; font-weight: 500;"
                  >
                    {{ t.label }}
                  </span>
                </div>
              </td>
              <td class="admin-table__cell--center">
                <div style="display: flex; align-items: center; justify-content: center; gap: 8px;">
                  <!-- Toggle 开关 -->
                  <label class="admin-toggle" style="margin: 0;">
                    <input
                      type="checkbox"
                      class="admin-toggle__input"
                      :checked="project.status === 'published'"
                      :disabled="togglingIds.has(project.id)"
                      @change="toggleStatus(project)"
                    />
                    <span class="admin-toggle__track"></span>
                  </label>
                  <StatusBadge :status="project.status" />
                </div>
              </td>
              <td class="admin-table__cell--center admin-text-mono">{{ project.sort_order }}</td>
              <td class="admin-text-caption">{{ formatDate(project.created_at) }}</td>
              <td class="admin-table__cell--center">
                <div class="admin-table__cell--actions">
                  <button class="admin-btn admin-btn--text admin-btn--sm" @click="editProject(project)">编辑</button>
                  <button class="admin-btn admin-btn--text admin-btn--sm" style="color: var(--admin-status-error);" @click="confirmDelete(project)">删除</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- 分页 -->
      <div class="admin-pagination">
        <div class="admin-pagination__info">
          共 {{ pagination.total }} 条，第 {{ pagination.page }} / {{ totalPages }} 页
        </div>
        <div class="admin-pagination__pages">
          <button
            class="admin-pagination__btn admin-pagination__btn--arrow"
            :disabled="pagination.page <= 1"
            @click="changePage(pagination.page - 1)"
            aria-label="上一页"
          >&#x2039;</button>
          <button
            v-for="p in visiblePages"
            :key="p"
            class="admin-pagination__btn"
            :class="{ 'admin-pagination__btn--active': p === pagination.page }"
            @click="changePage(p)"
          >{{ p }}</button>
          <button
            class="admin-pagination__btn admin-pagination__btn--arrow"
            :disabled="pagination.page >= totalPages"
            @click="changePage(pagination.page + 1)"
            aria-label="下一页"
          >&#x203A;</button>
        </div>
        <select class="admin-pagination__size-select" :value="pagination.pageSize" @change="changePageSize">
          <option value="10">10条/页</option>
          <option value="20">20条/页</option>
          <option value="50">50条/页</option>
        </select>
      </div>
    </template>

    <!-- 删除确认弹窗 -->
    <ConfirmDialog
      v-model:visible="showDeleteConfirm"
      :title="'确认删除'"
      :message="deleteTarget ? `确定要删除项目「${deleteTarget.title}」吗？此操作不可撤销。` : ''"
      confirm-text="删除"
      cancel-text="取消"
      type="danger"
      @confirm="handleDelete"
    />
  </div>
</template>
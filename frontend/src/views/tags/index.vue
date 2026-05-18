<template>
  <div class="tags-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>标签管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增标签
          </el-button>
        </div>
      </template>

      <el-table v-loading="loading" :data="tagList" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="标签名称" width="200">
          <template #default="{ row }">
            <el-tag
              :style="{
                backgroundColor: row.color + '20',
                color: row.color,
                borderColor: row.color
              }"
            >
              {{ row.name }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="颜色" width="150">
          <template #default="{ row }">
            <div class="color-display">
              <div class="color-preview" :style="{ backgroundColor: row.color }"></div>
              <span>{{ row.color || '#409eff' }}</span>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" size="small" link @click="handleEdit(row)">
              编辑
            </el-button>
            <el-button type="danger" size="small" link @click="handleDelete(row)">
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑标签' : '新增标签'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="标签名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入标签名称" />
        </el-form-item>
        <el-form-item label="标签颜色" prop="color">
          <el-color-picker v-model="form.color" show-alpha />
        </el-form-item>
      </el-form>
      <template #footer>
        <div class="dialog-footer">
          <el-button @click="dialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleSubmit" :loading="submitLoading">
            确定
          </el-button>
        </div>
      </template>
    </el-dialog>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { ElMessage, ElMessageBox, type FormInstance, type FormRules } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { tagApi } from '@/api/tag'
import type { Tag, TagCreate, TagUpdate } from '@/types/machine'

const loading = ref(false)
const submitLoading = ref(false)
const dialogVisible = ref(false)
const formRef = ref<FormInstance>()
const tagList = ref<Tag[]>([])
const isEdit = ref(false)

const form = reactive<TagCreate & { id?: number }>({
  name: '',
  color: '#409eff'
})

const rules: FormRules = {
  name: [{ required: true, message: '请输入标签名称', trigger: 'blur' }]
}

const loadTags = async () => {
  loading.value = true
  try {
    tagList.value = await tagApi.getTags()
  } catch (error) {
    ElMessage.error('加载标签列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  form.name = ''
  form.color = '#409eff'
  delete form.id
  dialogVisible.value = true
}

const handleEdit = (row: Tag) => {
  isEdit.value = true
  form.id = row.id
  form.name = row.name
  form.color = row.color || '#409eff'
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      if (isEdit.value && form.id) {
        await tagApi.updateTag(form.id, form as TagUpdate)
        ElMessage.success('更新成功')
      } else {
        await tagApi.createTag(form)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      loadTags()
    } catch (error) {
      ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
    } finally {
      submitLoading.value = false
    }
  })
}

const handleDelete = async (row: Tag) => {
  try {
    await ElMessageBox.confirm(`确定要删除标签"${row.name}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await tagApi.deleteTag(row.id)
    ElMessage.success('删除成功')
    loadTags()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

loadTags()
</script>

<style scoped lang="scss">
.tags-page {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .color-display {
    display: flex;
    align-items: center;
    gap: 10px;

    .color-preview {
      width: 30px;
      height: 30px;
      border-radius: 4px;
      border: 1px solid #dcdfe6;
    }
  }

  .dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
  }
}
</style>

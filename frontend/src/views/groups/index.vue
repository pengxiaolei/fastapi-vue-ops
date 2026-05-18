<template>
  <div class="groups-page">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>分组管理</span>
          <el-button type="primary" @click="handleAdd">
            <el-icon><Plus /></el-icon>
            新增分组
          </el-button>
        </div>
      </template>

      <el-table v-loading="loading" :data="groupList" style="width: 100%">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="分组名称" width="200">
          <template #default="{ row }">
            <el-tag type="info">{{ row.name }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="description" label="描述" min-width="200" />
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
      :title="isEdit ? '编辑分组' : '新增分组'"
      width="500px"
    >
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-width="80px"
      >
        <el-form-item label="分组名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入分组名称" />
        </el-form-item>
        <el-form-item label="描述" prop="description">
          <el-input
            v-model="form.description"
            type="textarea"
            :rows="3"
            placeholder="请输入分组描述（可选）"
          />
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
import { groupApi } from '@/api/group'
import type { Group, GroupCreate, GroupUpdate } from '@/types/machine'

const loading = ref(false)
const submitLoading = ref(false)
const dialogVisible = ref(false)
const formRef = ref<FormInstance>()
const groupList = ref<Group[]>([])
const isEdit = ref(false)

const form = reactive<GroupCreate & { id?: number }>({
  name: '',
  description: ''
})

const rules: FormRules = {
  name: [{ required: true, message: '请输入分组名称', trigger: 'blur' }]
}

const loadGroups = async () => {
  loading.value = true
  try {
    groupList.value = await groupApi.getGroups()
  } catch (error) {
    ElMessage.error('加载分组列表失败')
  } finally {
    loading.value = false
  }
}

const handleAdd = () => {
  isEdit.value = false
  form.name = ''
  form.description = ''
  delete form.id
  dialogVisible.value = true
}

const handleEdit = (row: Group) => {
  isEdit.value = true
  form.id = row.id
  form.name = row.name
  form.description = row.description || ''
  dialogVisible.value = true
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      if (isEdit.value && form.id) {
        await groupApi.updateGroup(form.id, form as GroupUpdate)
        ElMessage.success('更新成功')
      } else {
        await groupApi.createGroup(form)
        ElMessage.success('创建成功')
      }
      dialogVisible.value = false
      loadGroups()
    } catch (error) {
      ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
    } finally {
      submitLoading.value = false
    }
  })
}

const handleDelete = async (row: Group) => {
  try {
    await ElMessageBox.confirm(`确定要删除分组"${row.name}"吗？`, '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await groupApi.deleteGroup(row.id)
    ElMessage.success('删除成功')
    loadGroups()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

const formatDate = (dateStr: string) => {
  return new Date(dateStr).toLocaleString('zh-CN')
}

loadGroups()
</script>

<style scoped lang="scss">
.groups-page {
  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
  }

  .dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 10px;
  }
}
</style>

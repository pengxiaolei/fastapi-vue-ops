<template>
  <el-dialog
    v-model="visibleDialog"
    :title="isEdit ? '编辑机器' : '新增机器'"
    width="600px"
    @close="handleClose"
  >
    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
    >
      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="机器名称" prop="name">
            <el-input v-model="form.name" placeholder="请输入机器名称" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="所属环境" prop="environment">
            <el-select v-model="form.environment" placeholder="请选择环境" style="width: 100%">
              <el-option label="开发" value="dev" />
              <el-option label="测试" value="test" />
              <el-option label="生产" value="prod" />
            </el-select>
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="16">
          <el-form-item label="主机地址" prop="hostname">
            <el-input v-model="form.hostname" placeholder="请输入IP地址或域名" />
          </el-form-item>
        </el-col>
        <el-col :span="8">
          <el-form-item label="端口" prop="port">
            <el-input-number v-model="form.port" :min="1" :max="65535" style="width: 100%" />
          </el-form-item>
        </el-col>
      </el-row>

      <el-row :gutter="20">
        <el-col :span="12">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="form.username" placeholder="请输入SSH用户名" />
          </el-form-item>
        </el-col>
        <el-col :span="12">
          <el-form-item label="认证方式" prop="auth_type">
            <el-radio-group v-model="form.auth_type">
              <el-radio label="password">密码</el-radio>
              <el-radio label="key">密钥</el-radio>
            </el-radio-group>
          </el-form-item>
        </el-col>
      </el-row>

      <el-form-item
        v-if="form.auth_type === 'password'"
        label="密码"
        prop="password"
      >
        <el-input
          v-model="form.password"
          type="password"
          placeholder="请输入SSH密码"
          show-password
        />
      </el-form-item>

      <el-form-item
        v-if="form.auth_type === 'key'"
        label="私钥内容"
        prop="private_key"
      >
        <el-input
          v-model="form.private_key"
          type="textarea"
          :rows="6"
          placeholder="请粘贴私钥内容"
        />
      </el-form-item>

      <el-form-item label="操作系统" prop="os_type">
        <el-input v-model="form.os_type" placeholder="请输入操作系统类型（可选）" />
      </el-form-item>

      <el-form-item label="描述" prop="description">
        <el-input
          v-model="form.description"
          type="textarea"
          :rows="3"
          placeholder="请输入机器描述（可选）"
        />
      </el-form-item>
    </el-form>

    <template #footer>
      <div class="dialog-footer">
        <el-button @click="testConnection" :loading="testLoading">
          测试连接
        </el-button>
        <el-button @click="handleClose">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">
          确定
        </el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage, type FormInstance, type FormRules } from 'element-plus'
import { machineApi } from '@/api/machine'
import type { Machine, MachineCreate, MachineUpdate, AuthType } from '@/types/machine'

interface Props {
  visible: boolean
  machine?: Machine | null
}

const props = defineProps<Props>()
const emit = defineEmits<{
  (e: 'update:visible', value: boolean): void
  (e: 'success'): void
}>()

const formRef = ref<FormInstance>()
const submitLoading = ref(false)
const testLoading = ref(false)

const visibleDialog = computed({
  get: () => props.visible,
  set: (val) => emit('update:visible', val)
})

const isEdit = computed(() => !!props.machine)

const form = reactive<MachineCreate & { id?: number }>({
  name: '',
  hostname: '',
  port: 22,
  username: '',
  auth_type: 'password' as AuthType,
  password: '',
  private_key: '',
  os_type: '',
  environment: '',
  description: ''
})

const rules: FormRules = {
  name: [{ required: true, message: '请输入机器名称', trigger: 'blur' }],
  hostname: [{ required: true, message: '请输入主机地址', trigger: 'blur' }],
  port: [{ required: true, message: '请输入端口', trigger: 'blur' }],
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  auth_type: [{ required: true, message: '请选择认证方式', trigger: 'change' }],
  password: [
    {
      required: () => form.auth_type === 'password',
      message: '请输入密码',
      trigger: 'blur'
    }
  ],
  private_key: [
    {
      required: () => form.auth_type === 'key',
      message: '请输入私钥内容',
      trigger: 'blur'
    }
  ]
}

watch(
  () => props.machine,
  (machine) => {
    if (machine) {
      Object.assign(form, {
        id: machine.id,
        name: machine.name,
        hostname: machine.hostname,
        port: machine.port,
        username: machine.username,
        auth_type: machine.auth_type,
        password: '',
        private_key: '',
        os_type: machine.os_type || '',
        environment: machine.environment || '',
        description: machine.description || ''
      })
    } else {
      resetForm()
    }
  },
  { immediate: true }
)

const resetForm = () => {
  Object.assign(form, {
    name: '',
    hostname: '',
    port: 22,
    username: '',
    auth_type: 'password' as AuthType,
    password: '',
    private_key: '',
    os_type: '',
    environment: '',
    description: ''
  })
  formRef.value?.resetFields()
}

const testConnection = async () => {
  if (!form.hostname || !form.username) {
    ElMessage.warning('请先填写主机地址和用户名')
    return
  }
  if (form.auth_type === 'password' && !form.password) {
    ElMessage.warning('请先填写密码')
    return
  }
  if (form.auth_type === 'key' && !form.private_key) {
    ElMessage.warning('请先填写私钥内容')
    return
  }

  testLoading.value = true
  try {
    const res = await machineApi.testConnection({
      hostname: form.hostname,
      port: form.port,
      username: form.username,
      auth_type: form.auth_type,
      password: form.password,
      private_key: form.private_key
    })
    if (res.success) {
      ElMessage.success(`连接成功！操作系统: ${res.os_type || '未知'}`)
    } else {
      ElMessage.error(`连接失败: ${res.message}`)
    }
  } catch (error) {
    ElMessage.error('连接测试失败')
  } finally {
    testLoading.value = false
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitLoading.value = true
    try {
      if (isEdit.value && form.id) {
        const updateData: MachineUpdate = { ...form }
        if (!form.password) delete updateData.password
        if (!form.private_key) delete updateData.private_key
        await machineApi.updateMachine(form.id, updateData)
        ElMessage.success('更新成功')
      } else {
        await machineApi.createMachine(form)
        ElMessage.success('创建成功')
      }
      emit('success')
    } catch (error) {
      ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
    } finally {
      submitLoading.value = false
    }
  })
}

const handleClose = () => {
  visibleDialog.value = false
}
</script>

<style scoped lang="scss">
.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>

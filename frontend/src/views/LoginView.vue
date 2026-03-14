<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { login, register } from "../api/auth";
import { useUserStore } from "../stores/user";

const router = useRouter();
const userStore = useUserStore();

const isRegister = ref(false);
const loading = ref(false);
const form = ref({
  username: "",
  email: "",
  password: "",
});

async function handleSubmit() {
  loading.value = true;
  try {
    if (isRegister.value) {
      const res = await register(form.value);
      userStore.setToken(res.data.token);
      ElMessage.success("注册成功");
    } else {
      const res = await login({
        username: form.value.username,
        password: form.value.password,
      });
      userStore.setToken(res.data.token);
      if (res.data.user) {
        userStore.setUserInfo(res.data.user);
      }
      ElMessage.success("登录成功");
    }
    router.push("/");
  } catch {
    /* 错误已在拦截器中处理 */
  } finally {
    loading.value = false;
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100">
    <el-card class="w-420px" shadow="always">
      <template #header>
        <div class="text-center">
          <h2 class="text-2xl font-bold text-gray-800 m-0">NL2SQL 查询平台</h2>
          <p class="text-gray-500 mt-2">{{ isRegister ? "创建账号" : "登录" }}</p>
        </div>
      </template>

      <el-form @submit.prevent="handleSubmit" label-position="top">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>

        <el-form-item v-if="isRegister" label="邮箱">
          <el-input v-model="form.email" type="email" placeholder="请输入邮箱" />
        </el-form-item>

        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" show-password />
        </el-form-item>

        <el-button type="primary" native-type="submit" :loading="loading" class="w-full" size="large">
          {{ isRegister ? "注册" : "登录" }}
        </el-button>

        <div class="text-center mt-4">
          <el-link type="primary" @click="isRegister = !isRegister">
            {{ isRegister ? "已有账号？去登录" : "没有账号？去注册" }}
          </el-link>
        </div>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
/**
 * 登录/注册页面。
 * 包含用户名、密码（注册时额外有邮箱）表单校验。
 */
import { ref, watch } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";
import { login, register } from "../api/auth";
import { getMe } from "../api/auth";
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
const errors = ref<Record<string, string>>({});

watch(isRegister, () => {
  form.value = { username: "", email: "", password: "" };
  errors.value = {};
});

function validate(): boolean {
  const e: Record<string, string> = {};
  const { username, email, password } = form.value;

  if (!username.trim()) {
    e.username = "请输入用户名";
  } else if (username.trim().length < 3) {
    e.username = "用户名至少 3 个字符";
  } else if (username.trim().length > 64) {
    e.username = "用户名最多 64 个字符";
  }

  if (isRegister.value) {
    if (!email.trim()) {
      e.email = "请输入邮箱";
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())) {
      e.email = "邮箱格式不正确";
    }
  }

  if (!password) {
    e.password = "请输入密码";
  } else if (password.length < 6) {
    e.password = "密码至少 6 个字符";
  } else if (password.length > 128) {
    e.password = "密码最多 128 个字符";
  }

  errors.value = e;
  return Object.keys(e).length === 0;
}

async function handleSubmit() {
  if (!validate()) return;

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

    try {
      const meRes = await getMe();
      if (meRes.data) {
        userStore.setUserInfo(meRes.data);
      }
    } catch {
      /* 非关键：用户信息获取失败不阻塞跳转 */
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
  <div class="login-page">
    <div class="login-bg">
      <div class="blob blob-1" />
      <div class="blob blob-2" />
      <div class="blob blob-3" />
    </div>

    <div class="login-wrapper">
      <div class="login-card glass">
        <div class="login-header">
          <div class="logo-icon">
            <svg width="40" height="40" viewBox="0 0 40 40" fill="none">
              <rect width="40" height="40" rx="10" fill="url(#g1)" />
              <path d="M12 20h16M20 14v12M14 16l6 4-6 4M26 16l-6 4 6 4" stroke="#fff" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.9"/>
              <defs><linearGradient id="g1" x1="0" y1="0" x2="40" y2="40"><stop stop-color="#6366f1"/><stop offset="1" stop-color="#06b6d4"/></linearGradient></defs>
            </svg>
          </div>
          <h1 class="login-title">NL2SQL</h1>
          <p class="login-subtitle">{{ isRegister ? "创建你的账号" : "自然语言驱动的智能查询" }}</p>
        </div>

        <el-form @submit.prevent="handleSubmit" class="login-form">
          <div class="form-field" :class="{ 'has-error': errors.username }">
            <label>用户名</label>
            <el-input
              v-model="form.username"
              placeholder="请输入用户名（至少 3 个字符）"
              size="large"
            />
            <span v-if="errors.username" class="field-error">{{ errors.username }}</span>
          </div>

          <Transition name="fade-up">
            <div v-if="isRegister" class="form-field" :class="{ 'has-error': errors.email }">
              <label>邮箱</label>
              <el-input
                v-model="form.email"
                type="email"
                placeholder="请输入邮箱"
                size="large"
              />
              <span v-if="errors.email" class="field-error">{{ errors.email }}</span>
            </div>
          </Transition>

          <div class="form-field" :class="{ 'has-error': errors.password }">
            <label>密码</label>
            <el-input
              v-model="form.password"
              type="password"
              placeholder="请输入密码（至少 6 个字符）"
              size="large"
              show-password
            />
            <span v-if="errors.password" class="field-error">{{ errors.password }}</span>
          </div>

          <el-button
            type="primary"
            native-type="submit"
            :loading="loading"
            size="large"
            class="submit-btn"
          >
            {{ isRegister ? "注册" : "登录" }}
          </el-button>

          <div class="switch-mode" @click="isRegister = !isRegister">
            {{ isRegister ? "已有账号？返回登录" : "没有账号？立即注册" }}
          </div>
        </el-form>
      </div>
    </div>
  </div>
</template>


<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
}

.login-bg {
  position: absolute;
  inset: 0;
  overflow: hidden;
}

.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.5;
  animation: float 8s ease-in-out infinite;
}

.blob-1 {
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, #6366f1 0%, transparent 70%);
  top: -100px;
  right: -100px;
  animation-delay: 0s;
}

.blob-2 {
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, #06b6d4 0%, transparent 70%);
  bottom: -80px;
  left: -60px;
  animation-delay: -3s;
}

.blob-3 {
  width: 300px;
  height: 300px;
  background: radial-gradient(circle, #8b5cf6 0%, transparent 70%);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: -5s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  33% { transform: translate(30px, -30px) scale(1.05); }
  66% { transform: translate(-20px, 20px) scale(0.95); }
}

.login-wrapper {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 420px;
  padding: 24px;
  animation: card-in 0.7s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes card-in {
  from {
    opacity: 0;
    transform: translateY(40px) scale(0.96);
  }
}

.login-card {
  border-radius: var(--radius-lg);
  padding: 40px 36px;
  background: rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 24px 48px rgba(0, 0, 0, 0.3);
}

.login-header {
  text-align: center;
  margin-bottom: 32px;
}

.logo-icon {
  margin-bottom: 16px;
  display: inline-block;
  animation: logo-bounce 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) 0.3s both;
}

@keyframes logo-bounce {
  from { opacity: 0; transform: scale(0.5) rotate(-10deg); }
}

.login-title {
  font-size: 28px;
  font-weight: 700;
  color: #fff;
  margin: 0 0 8px;
  letter-spacing: 2px;
}

.login-subtitle {
  color: rgba(255, 255, 255, 0.55);
  margin: 0;
  font-size: 14px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-field label {
  display: block;
  font-size: 13px;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 6px;
}

.form-field :deep(.el-input__wrapper) {
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 10px;
  box-shadow: none;
  transition: all 0.3s ease;
}

.form-field :deep(.el-input__wrapper:hover) {
  border-color: rgba(99, 102, 241, 0.4);
}

.form-field :deep(.el-input__wrapper.is-focus) {
  border-color: #6366f1;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.15);
}

.form-field :deep(.el-input__inner) {
  color: #fff;
}

.form-field :deep(.el-input__inner::placeholder) {
  color: rgba(255, 255, 255, 0.3);
}

.form-field :deep(.el-input__prefix .el-icon) {
  color: rgba(255, 255, 255, 0.4);
}

.submit-btn {
  margin-top: 8px;
  height: 48px;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  letter-spacing: 1px;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  border: none;
  transition: all 0.3s ease;
}

.submit-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 24px rgba(99, 102, 241, 0.35);
}

.switch-mode {
  text-align: center;
  color: rgba(255, 255, 255, 0.5);
  font-size: 13px;
  cursor: pointer;
  transition: color 0.2s;
  user-select: none;
}

.switch-mode:hover {
  color: #818cf8;
}

.field-error {
  font-size: 12px;
  color: #f87171;
  margin-top: 4px;
  display: block;
}

.has-error :deep(.el-input__wrapper) {
  border-color: rgba(248, 113, 113, 0.5);
}
</style>

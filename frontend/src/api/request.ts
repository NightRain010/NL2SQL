import axios from "axios";
import { ElMessage } from "element-plus";
import { useUserStore } from "../stores/user";
import router from "../router";

const request = axios.create({
  baseURL: "/api",
  timeout: 30000,
});

request.interceptors.request.use((config) => {
  const userStore = useUserStore();
  if (userStore.token) {
    config.headers.Authorization = `Bearer ${userStore.token}`;
  }
  return config;
});

request.interceptors.response.use(
  (response) => {
    const data = response.data;
    if (data.code && data.code !== 200) {
      ElMessage.error(data.message || "请求失败");
      return Promise.reject(new Error(data.message));
    }
    return data;
  },
  (error) => {
    const status = error.response?.status;
    if (status === 401) {
      const userStore = useUserStore();
      userStore.logout();
      ElMessage.error("登录已过期，请重新登录");
      router.push({ name: "Login" });
    } else if (status === 403) {
      ElMessage.error("没有权限执行此操作");
    } else if (status && status >= 500) {
      ElMessage.error("服务器错误，请稍后重试");
    } else {
      ElMessage.error(error.response?.data?.detail || "网络错误");
    }
    return Promise.reject(error);
  }
);

export default request;

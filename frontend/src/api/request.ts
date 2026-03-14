import axios from "axios";
import { ElMessage } from "element-plus";
import { useUserStore } from "../stores/user";

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
    if (error.response?.status === 401) {
      const userStore = useUserStore();
      userStore.logout();
      ElMessage.error("登录已过期，请重新登录");
      window.location.href = "/login";
    } else {
      ElMessage.error(error.response?.data?.detail || "网络错误");
    }
    return Promise.reject(error);
  }
);

export default request;

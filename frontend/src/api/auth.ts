import request from "./request";
import type { ApiResponse } from "../types";

/** 用户注册 */
export function register(data: {
  username: string;
  email: string;
  password: string;
}) {
  return request.post<unknown, ApiResponse>("/auth/register", data);
}

/** 用户登录 */
export function login(data: { username: string; password: string }) {
  return request.post<unknown, ApiResponse>("/auth/login", data);
}

/** 获取当前用户信息 */
export function getMe() {
  return request.get<unknown, ApiResponse>("/auth/me");
}

import request from "./request";
import type { ApiResponse } from "../types";

/** 获取所有业务表列表 */
export function getTableList() {
  return request.get<unknown, ApiResponse>("/schema/tables");
}

/** 获取指定表的详细结构 */
export function getTableDetail(tableName: string) {
  return request.get<unknown, ApiResponse>(`/schema/tables/${tableName}`);
}

/** 刷新元数据缓存 */
export function refreshMetadata() {
  return request.post<unknown, ApiResponse>("/schema/refresh");
}

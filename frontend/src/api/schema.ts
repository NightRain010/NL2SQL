import request from "./request";
import type { ApiResponse, TableDetail } from "../types";

/** 获取所有业务表列表。 */
export function getTableList() {
  return request.get<unknown, ApiResponse<{ tables: { name: string; comment?: string; column_count: number }[] }>>("/schema/tables");
}

/** 获取指定表的详细结构。 */
export function getTableDetail(tableName: string) {
  return request.get<unknown, ApiResponse<TableDetail>>(`/schema/tables/${tableName}`);
}

/** 刷新元数据缓存。 */
export function refreshMetadata() {
  return request.post<unknown, ApiResponse<{ refreshed_tables: number; total_columns: number }>>("/schema/refresh");
}

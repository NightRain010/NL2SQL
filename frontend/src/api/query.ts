import request from "./request";
import type { ApiResponse } from "../types";

/** 提交自然语言查询 */
export function askQuestion(question: string) {
  return request.post<unknown, ApiResponse>("/query/ask", { question });
}

/** 获取查询历史 */
export function getHistory(params: {
  page?: number;
  size?: number;
  status?: string;
}) {
  return request.get<unknown, ApiResponse>("/query/history", { params });
}

/** 获取查询详情 */
export function getQueryDetail(queryId: number) {
  return request.get<unknown, ApiResponse>(`/query/${queryId}`);
}

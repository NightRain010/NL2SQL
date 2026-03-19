import request from "./request";
import type { ApiResponse, AskResponse, PaginatedResponse, QueryHistoryItem } from "../types";

/** 提交自然语言查询。 */
export function askQuestion(question: string) {
  return request.post<unknown, ApiResponse<AskResponse>>("/query/ask", { question });
}

/** 获取查询历史（分页）。 */
export function getHistory(params: {
  page?: number;
  size?: number;
  status?: string;
}) {
  return request.get<unknown, ApiResponse<PaginatedResponse<QueryHistoryItem>>>("/query/history", { params });
}

/** 获取单条查询详情。 */
export function getQueryDetail(queryId: number) {
  return request.get<unknown, ApiResponse<AskResponse>>(`/query/${queryId}`);
}

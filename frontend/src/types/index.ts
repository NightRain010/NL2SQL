/** 用户信息 */
export interface UserInfo {
  id: number;
  username: string;
  email: string;
  is_active: boolean;
  created_at?: string;
}

/** 登录响应 */
export interface AuthResponse {
  token: string;
  expires_in: number;
  user: UserInfo;
}

/** 统一 API 响应 */
export interface ApiResponse<T = unknown> {
  code: number;
  message: string;
  data: T;
}

/** 表格列定义 */
export interface ColumnDef {
  key: string;
  label: string;
  align: "left" | "center" | "right";
  sortable: boolean;
}

/** 表格数据 */
export interface TableData {
  columns: ColumnDef[];
  rows: Record<string, unknown>[];
  total_count: number;
}

/** 图表建议 */
export interface ChartSuggestion {
  chart_type: "bar" | "line" | "pie" | "table_only";
  x_field: string;
  y_field: string;
  title: string;
}

/** 查询响应 */
export interface AskResponse {
  query_id: number;
  nl_input: string;
  generated_sql?: string;
  explanation?: string;
  result?: TableData;
  summary?: string;
  chart_suggestion?: ChartSuggestion;
  status: string;
  execution_ms?: number;
  error_message?: string;
}

/** 查询历史项 */
export interface QueryHistoryItem {
  id: number;
  nl_input: string;
  intent_type?: string;
  status: string;
  created_at?: string;
  execution_ms?: number;
}

/** 分页响应 */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  size: number;
}

/** 表摘要 */
export interface TableSummary {
  name: string;
  comment?: string;
  column_count: number;
}

/** 列详情 */
export interface ColumnDetail {
  name: string;
  type: string;
  comment?: string;
  is_primary: boolean;
  is_nullable: boolean;
  is_foreign_key?: boolean;
  references?: string;
}

/** 表详情 */
export interface TableDetail {
  table_name: string;
  columns: ColumnDetail[];
  row_count?: number;
}

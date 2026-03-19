import { describe, it, expect } from "vitest";
import type {
  UserInfo,
  ApiResponse,
  AskResponse,
  QueryHistoryItem,
  TableData,
  ColumnDef,
  ChartSuggestion,
  TableSummary,
  ColumnDetail,
} from "../types";

describe("TypeScript 类型定义", () => {
  it("UserInfo 结构应正确", () => {
    const user: UserInfo = {
      id: 1,
      username: "admin",
      email: "admin@test.com",
      is_active: true,
    };
    expect(user.id).toBe(1);
    expect(user.username).toBe("admin");
  });

  it("ApiResponse 泛型应正确约束 data 类型", () => {
    const resp: ApiResponse<{ name: string }> = {
      code: 200,
      message: "success",
      data: { name: "test" },
    };
    expect(resp.code).toBe(200);
    expect(resp.data.name).toBe("test");
  });

  it("AskResponse 应包含所有必要字段", () => {
    const result: AskResponse = {
      query_id: 1,
      nl_input: "测试查询",
      status: "success",
      generated_sql: "SELECT 1",
      execution_ms: 50,
    };
    expect(result.query_id).toBe(1);
    expect(result.status).toBe("success");
  });

  it("TableData 应正确包含列定义和行数据", () => {
    const col: ColumnDef = { key: "name", label: "姓名", align: "left", sortable: true };
    const data: TableData = {
      columns: [col],
      rows: [{ name: "张三" }],
      total_count: 1,
    };
    expect(data.columns[0].key).toBe("name");
    expect(data.total_count).toBe(1);
  });

  it("ChartSuggestion 应正确定义图表配置", () => {
    const chart: ChartSuggestion = {
      chart_type: "bar",
      x_field: "name",
      y_field: "score",
      title: "分数分布",
    };
    expect(chart.chart_type).toBe("bar");
  });

  it("QueryHistoryItem 应包含查询记录信息", () => {
    const item: QueryHistoryItem = {
      id: 1,
      nl_input: "查询平均分",
      status: "success",
      intent_type: "aggregate",
      created_at: "2025-01-01T00:00:00",
      execution_ms: 120,
    };
    expect(item.intent_type).toBe("aggregate");
  });

  it("ColumnDetail 应描述表字段", () => {
    const col: ColumnDetail = {
      name: "id",
      type: "INT",
      is_primary: true,
      is_nullable: false,
      comment: "主键",
    };
    expect(col.is_primary).toBe(true);
  });

  it("TableSummary 应包含表名和字段数", () => {
    const t: TableSummary = { name: "students", column_count: 7, comment: "学生表" };
    expect(t.name).toBe("students");
    expect(t.column_count).toBe(7);
  });
});

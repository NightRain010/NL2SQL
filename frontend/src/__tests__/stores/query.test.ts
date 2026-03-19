import { describe, it, expect, beforeEach } from "vitest";
import { setActivePinia, createPinia } from "pinia";
import { useQueryStore } from "../../stores/query";
import type { AskResponse, QueryHistoryItem } from "../../types";

describe("useQueryStore", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it("初始状态应为空", () => {
    const store = useQueryStore();
    expect(store.loading).toBe(false);
    expect(store.currentResult).toBeNull();
    expect(store.historyList).toEqual([]);
    expect(store.historyTotal).toBe(0);
  });

  it("setLoading 应正确切换加载状态", () => {
    const store = useQueryStore();
    store.setLoading(true);
    expect(store.loading).toBe(true);
    store.setLoading(false);
    expect(store.loading).toBe(false);
  });

  it("setResult 和 clearResult 应正确管理查询结果", () => {
    const store = useQueryStore();
    const mockResult: AskResponse = {
      query_id: 1,
      nl_input: "测试查询",
      generated_sql: "SELECT 1",
      status: "success",
      execution_ms: 10,
    };
    store.setResult(mockResult);
    expect(store.currentResult).toEqual(mockResult);
    expect(store.currentResult?.query_id).toBe(1);

    store.clearResult();
    expect(store.currentResult).toBeNull();
  });

  it("setHistory 应正确设置历史列表和总数", () => {
    const store = useQueryStore();
    const items: QueryHistoryItem[] = [
      { id: 1, nl_input: "查询1", status: "success", created_at: "2025-01-01" },
      { id: 2, nl_input: "查询2", status: "failed", created_at: "2025-01-02" },
    ];
    store.setHistory(items, 100);
    expect(store.historyList).toHaveLength(2);
    expect(store.historyTotal).toBe(100);
    expect(store.historyList[0].nl_input).toBe("查询1");
  });
});

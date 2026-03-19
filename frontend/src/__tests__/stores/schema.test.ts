import { describe, it, expect, beforeEach } from "vitest";
import { setActivePinia, createPinia } from "pinia";
import { useSchemaStore } from "../../stores/schema";
import type { TableSummary, TableDetail } from "../../types";

describe("useSchemaStore", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
  });

  it("初始状态应为空", () => {
    const store = useSchemaStore();
    expect(store.tables).toEqual([]);
    expect(store.currentTable).toBeNull();
    expect(store.loading).toBe(false);
  });

  it("setTables 应正确设置表列表", () => {
    const store = useSchemaStore();
    const tables: TableSummary[] = [
      { name: "students", column_count: 7 },
      { name: "scores", column_count: 5 },
    ];
    store.setTables(tables);
    expect(store.tables).toHaveLength(2);
    expect(store.tables[0].name).toBe("students");
  });

  it("setCurrentTable 应正确设置当前表详情", () => {
    const store = useSchemaStore();
    const detail: TableDetail = {
      table_name: "students",
      columns: [
        { name: "id", type: "INT", is_primary: true, is_nullable: false },
        { name: "name", type: "VARCHAR(64)", comment: "姓名", is_primary: false, is_nullable: false },
      ],
    };
    store.setCurrentTable(detail);
    expect(store.currentTable?.table_name).toBe("students");
    expect(store.currentTable?.columns).toHaveLength(2);

    store.setCurrentTable(null);
    expect(store.currentTable).toBeNull();
  });

  it("setLoading 应正确切换", () => {
    const store = useSchemaStore();
    store.setLoading(true);
    expect(store.loading).toBe(true);
  });
});

import { defineStore } from "pinia";
import { ref } from "vue";
import type { TableSummary, TableDetail } from "../types";

export const useSchemaStore = defineStore("schema", () => {
  const tables = ref<TableSummary[]>([]);
  const currentTable = ref<TableDetail | null>(null);
  const loading = ref(false);

  function setTables(list: TableSummary[]) {
    tables.value = list;
  }

  function setCurrentTable(detail: TableDetail | null) {
    currentTable.value = detail;
  }

  function setLoading(val: boolean) {
    loading.value = val;
  }

  return { tables, currentTable, loading, setTables, setCurrentTable, setLoading };
});

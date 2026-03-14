import { defineStore } from "pinia";
import { ref } from "vue";
import type { AskResponse, QueryHistoryItem } from "../types";

export const useQueryStore = defineStore("query", () => {
  const loading = ref(false);
  const currentResult = ref<AskResponse | null>(null);
  const historyList = ref<QueryHistoryItem[]>([]);
  const historyTotal = ref(0);

  function setLoading(val: boolean) {
    loading.value = val;
  }

  function setResult(result: AskResponse) {
    currentResult.value = result;
  }

  function clearResult() {
    currentResult.value = null;
  }

  function setHistory(items: QueryHistoryItem[], total: number) {
    historyList.value = items;
    historyTotal.value = total;
  }

  return {
    loading,
    currentResult,
    historyList,
    historyTotal,
    setLoading,
    setResult,
    clearResult,
    setHistory,
  };
});

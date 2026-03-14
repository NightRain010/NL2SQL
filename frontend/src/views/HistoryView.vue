<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useQueryStore } from "../stores/query";
import { getHistory } from "../api/query";

const router = useRouter();
const queryStore = useQueryStore();
const page = ref(1);
const size = ref(20);

async function fetchHistory() {
  try {
    const res = await getHistory({ page: page.value, size: size.value });
    queryStore.setHistory(res.data.items, res.data.total);
  } catch {
    /* 错误已在拦截器中处理 */
  }
}

function handlePageChange(newPage: number) {
  page.value = newPage;
  fetchHistory();
}

function statusType(status: string) {
  const map: Record<string, string> = {
    success: "success",
    failed: "danger",
    rejected: "warning",
    pending: "info",
  };
  return map[status] || "info";
}

onMounted(fetchHistory);
</script>

<template>
  <div class="min-h-screen">
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="page-container flex items-center gap-4 py-4">
        <el-button @click="router.push('/')" text>← 返回查询</el-button>
        <h1 class="text-xl font-bold text-gray-800 m-0">查询历史</h1>
      </div>
    </header>

    <main class="page-container">
      <el-table :data="queryStore.historyList" stripe>
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="nl_input" label="查询内容" min-width="200" />
        <el-table-column prop="intent_type" label="意图" width="120" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="statusType(row.status)" size="small">{{ row.status }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="execution_ms" label="耗时(ms)" width="100" />
        <el-table-column prop="created_at" label="时间" width="180" />
      </el-table>

      <div class="flex justify-center mt-4">
        <el-pagination
          :current-page="page"
          :page-size="size"
          :total="queryStore.historyTotal"
          layout="prev, pager, next"
          @current-change="handlePageChange"
        />
      </div>
    </main>
  </div>
</template>

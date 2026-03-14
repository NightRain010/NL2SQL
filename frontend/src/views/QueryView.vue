<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useQueryStore } from "../stores/query";
import { useUserStore } from "../stores/user";
import { askQuestion } from "../api/query";
import QueryInput from "../components/QueryInput.vue";
import SqlDisplay from "../components/SqlDisplay.vue";
import ResultTable from "../components/ResultTable.vue";
import LoadingState from "../components/LoadingState.vue";

const router = useRouter();
const queryStore = useQueryStore();
const userStore = useUserStore();

async function handleAsk(question: string) {
  queryStore.setLoading(true);
  queryStore.clearResult();
  try {
    const res = await askQuestion(question);
    queryStore.setResult(res.data);
  } catch {
    /* 错误已在拦截器中处理 */
  } finally {
    queryStore.setLoading(false);
  }
}

function handleLogout() {
  userStore.logout();
  router.push("/login");
}
</script>

<template>
  <div class="min-h-screen">
    <header class="bg-white shadow-sm border-b border-gray-200">
      <div class="page-container flex items-center justify-between py-4">
        <h1 class="text-xl font-bold text-gray-800 m-0">NL2SQL 查询平台</h1>
        <div class="flex items-center gap-4">
          <el-button text @click="router.push('/history')">查询历史</el-button>
          <el-button text @click="router.push('/schema')">数据结构</el-button>
          <el-button text type="danger" @click="handleLogout">退出</el-button>
        </div>
      </div>
    </header>

    <main class="page-container">
      <QueryInput @submit="handleAsk" :loading="queryStore.loading" />

      <LoadingState v-if="queryStore.loading" />

      <template v-if="queryStore.currentResult && !queryStore.loading">
        <SqlDisplay
          v-if="queryStore.currentResult.generated_sql"
          :sql="queryStore.currentResult.generated_sql"
          :status="queryStore.currentResult.status"
        />

        <el-alert
          v-if="queryStore.currentResult.summary"
          :title="queryStore.currentResult.summary"
          type="success"
          :closable="false"
          class="mt-4"
        />

        <el-alert
          v-if="queryStore.currentResult.error_message"
          :title="queryStore.currentResult.error_message"
          type="error"
          :closable="false"
          class="mt-4"
        />

        <ResultTable
          v-if="queryStore.currentResult.result"
          :data="queryStore.currentResult.result"
          class="mt-4"
        />

        <div v-if="queryStore.currentResult.execution_ms" class="text-gray-400 text-sm mt-2">
          查询耗时: {{ queryStore.currentResult.execution_ms }}ms
        </div>
      </template>
    </main>
  </div>
</template>

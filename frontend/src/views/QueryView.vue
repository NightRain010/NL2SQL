<script setup lang="ts">
/**
 * 查询主页面。
 * 接收用户自然语言输入，调用后端 API 展示 SQL、结果表格、摘要和图表。
 */
import { useRouter } from "vue-router";
import { useQueryStore } from "../stores/query";
import { useUserStore } from "../stores/user";
import { askQuestion } from "../api/query";
import QueryInput from "../components/QueryInput.vue";
import SqlDisplay from "../components/SqlDisplay.vue";
import ResultTable from "../components/ResultTable.vue";
import ChartDisplay from "../components/ChartDisplay.vue";
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
  <div class="query-page">
    <header class="top-bar glass">
      <div class="top-bar-inner">
        <div class="brand">
          <div class="brand-dot" />
          <span class="brand-name">NL2SQL</span>
        </div>
        <nav class="nav-links">
          <button class="nav-btn" @click="router.push('/history')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12,6 12,12 16,14"/></svg>
            查询历史
          </button>
          <button class="nav-btn" @click="router.push('/schema')">
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>
            数据结构
          </button>
          <button class="nav-btn logout" @click="handleLogout">退出</button>
        </nav>
      </div>
    </header>

    <main class="query-main">
      <div class="hero-section" v-if="!queryStore.currentResult && !queryStore.loading">
        <h1 class="hero-title">用自然语言查询数据</h1>
        <p class="hero-desc">输入你的问题，AI 自动转换为 SQL 并返回结果</p>
      </div>

      <QueryInput @submit="handleAsk" :loading="queryStore.loading" />

      <Transition name="fade-up">
        <LoadingState v-if="queryStore.loading" />
      </Transition>

      <Transition name="fade-up">
        <div v-if="queryStore.currentResult && !queryStore.loading" class="result-area">
          <SqlDisplay
            v-if="queryStore.currentResult.generated_sql"
            :sql="queryStore.currentResult.generated_sql"
            :status="queryStore.currentResult.status"
          />

          <div v-if="queryStore.currentResult.summary" class="summary-card">
            <div class="summary-icon">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2"><path d="M22 11.08V12a10 10 0 11-5.93-9.14"/><polyline points="22 4 12 14.01 9 11.01"/></svg>
            </div>
            <p>{{ queryStore.currentResult.summary }}</p>
          </div>

          <div v-if="queryStore.currentResult.error_message" class="error-card">
            <p>{{ queryStore.currentResult.error_message }}</p>
          </div>

          <ResultTable
            v-if="queryStore.currentResult.result"
            :data="queryStore.currentResult.result"
          />

          <ChartDisplay
            v-if="queryStore.currentResult.chart_suggestion && queryStore.currentResult.result"
            :suggestion="queryStore.currentResult.chart_suggestion"
            :table-data="queryStore.currentResult.result"
          />

          <div v-if="queryStore.currentResult.execution_ms" class="exec-time">
            查询耗时 {{ queryStore.currentResult.execution_ms }}ms
          </div>
        </div>
      </Transition>
    </main>
  </div>
</template>

<style scoped>
.query-page {
  min-height: 100vh;
  background: var(--bg-page);
}

.top-bar {
  position: sticky;
  top: 0;
  z-index: 100;
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(16px);
}

.top-bar-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 24px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.brand {
  display: flex;
  align-items: center;
  gap: 10px;
}

.brand-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: linear-gradient(135deg, #6366f1, #06b6d4);
}

.brand-name {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: 1px;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 4px;
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: none;
  background: none;
  color: var(--text-secondary);
  font-size: 14px;
  cursor: pointer;
  border-radius: 8px;
  transition: all 0.2s;
}

.nav-btn:hover {
  background: rgba(99, 102, 241, 0.08);
  color: var(--primary);
}

.nav-btn.logout {
  color: #ef4444;
}

.nav-btn.logout:hover {
  background: rgba(239, 68, 68, 0.08);
}

.query-main {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 24px 80px;
}

.hero-section {
  text-align: center;
  padding: 60px 0 20px;
  animation: card-in 0.7s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes card-in {
  from { opacity: 0; transform: translateY(30px); }
}

.hero-title {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
  margin: 0 0 12px;
  background: linear-gradient(135deg, #1e293b, #6366f1);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-desc {
  color: var(--text-secondary);
  font-size: 16px;
  margin: 0;
}

.result-area {
  display: flex;
  flex-direction: column;
  gap: 16px;
  margin-top: 24px;
}

.summary-card {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 16px 20px;
  background: linear-gradient(135deg, #ecfdf5, #f0fdf4);
  border: 1px solid #bbf7d0;
  border-radius: var(--radius);
}

.summary-card p {
  margin: 0;
  color: #166534;
  font-size: 14px;
  line-height: 1.6;
}

.summary-icon {
  flex-shrink: 0;
  margin-top: 2px;
}

.error-card {
  padding: 16px 20px;
  background: linear-gradient(135deg, #fef2f2, #fff1f2);
  border: 1px solid #fecaca;
  border-radius: var(--radius);
}

.error-card p {
  margin: 0;
  color: #991b1b;
  font-size: 14px;
}

.exec-time {
  text-align: right;
  color: var(--text-secondary);
  font-size: 12px;
  opacity: 0.7;
}
</style>

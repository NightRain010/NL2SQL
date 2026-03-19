<script setup lang="ts">
/**
 * 查询历史列表页面。
 * 展示当前用户的所有查询记录，支持分页浏览。
 */
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { useQueryStore } from "../stores/query";
import { getHistory } from "../api/query";

const router = useRouter();
const queryStore = useQueryStore();
const page = ref(1);
const size = ref(20);
const loading = ref(false);

async function fetchHistory() {
  loading.value = true;
  try {
    const res = await getHistory({ page: page.value, size: size.value });
    queryStore.setHistory(res.data.items, res.data.total);
  } catch {
    /* 错误已在拦截器中处理 */
  } finally {
    loading.value = false;
  }
}

function handlePageChange(newPage: number) {
  page.value = newPage;
  fetchHistory();
  window.scrollTo({ top: 0, behavior: "smooth" });
}

/** 状态显示配置映射。 */
function statusConfig(status: string) {
  const map: Record<string, { color: string; bg: string; label: string }> = {
    success: { color: "#10b981", bg: "rgba(16,185,129,0.1)", label: "成功" },
    failed: { color: "#ef4444", bg: "rgba(239,68,68,0.1)", label: "失败" },
    rejected: { color: "#f59e0b", bg: "rgba(245,158,11,0.1)", label: "拒绝" },
    pending: { color: "#6366f1", bg: "rgba(99,102,241,0.1)", label: "处理中" },
  };
  return map[status] || map.pending;
}

onMounted(fetchHistory);
</script>

<template>
  <div class="history-page">
    <header class="page-header glass">
      <div class="header-inner">
        <button class="back-btn" @click="router.push('/')">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12,19 5,12 12,5"/></svg>
        </button>
        <h1>查询历史</h1>
      </div>
    </header>

    <main class="page-container">
      <div v-if="loading" class="loading-center">
        <el-icon class="is-loading" :size="32"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/></svg></el-icon>
      </div>

      <div v-else-if="queryStore.historyList.length === 0" class="empty-state">
        <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#cbd5e1" stroke-width="1.2"><circle cx="12" cy="12" r="10"/><polyline points="12,6 12,12 16,14"/></svg>
        <p>还没有查询记录</p>
        <button class="go-query-btn" @click="router.push('/')">去提问</button>
      </div>

      <div v-else class="history-list">
        <div
          v-for="(item, idx) in queryStore.historyList"
          :key="item.id"
          class="history-card card-hover"
          :style="{ animationDelay: `${idx * 60}ms` }"
        >
          <div class="card-left">
            <div
              class="status-dot"
              :style="{ background: statusConfig(item.status).color }"
            />
          </div>
          <div class="card-body">
            <div class="card-question">{{ item.nl_input }}</div>
            <div class="card-meta">
              <span
                class="status-tag"
                :style="{
                  color: statusConfig(item.status).color,
                  background: statusConfig(item.status).bg,
                }"
              >
                {{ statusConfig(item.status).label }}
              </span>
              <span v-if="item.intent_type" class="intent-tag">{{ item.intent_type }}</span>
              <span v-if="item.execution_ms" class="time-info">{{ item.execution_ms }}ms</span>
              <span class="date-info">{{ item.created_at }}</span>
            </div>
          </div>
        </div>
      </div>

      <div v-if="queryStore.historyTotal > size" class="pagination-area">
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

<style scoped>
.history-page {
  min-height: 100vh;
  background: var(--bg-page);
}

.page-header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: rgba(255, 255, 255, 0.8);
  backdrop-filter: blur(16px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.05);
}

.header-inner {
  max-width: 1100px;
  margin: 0 auto;
  padding: 0 24px;
  height: 60px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.header-inner h1 {
  font-size: 18px;
  font-weight: 600;
  margin: 0;
}

.back-btn {
  width: 36px;
  height: 36px;
  border-radius: 10px;
  border: none;
  background: #f1f5f9;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--text-secondary);
  transition: all 0.2s;
}

.back-btn:hover {
  background: #e2e8f0;
  color: var(--text-primary);
}

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 16px;
  padding: 80px 0;
}

.empty-state p {
  color: var(--text-secondary);
  font-size: 16px;
  margin: 0;
}

.go-query-btn {
  padding: 10px 28px;
  border-radius: 10px;
  border: none;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  color: #fff;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.go-query-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(99, 102, 241, 0.35);
}

.history-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.history-card {
  display: flex;
  gap: 16px;
  padding: 20px;
  background: var(--bg-card);
  border-radius: var(--radius);
  box-shadow: var(--shadow-sm);
  cursor: default;
  animation: slide-in 0.4s ease both;
}

@keyframes slide-in {
  from { opacity: 0; transform: translateX(-16px); }
}

.card-left {
  padding-top: 4px;
}

.status-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.card-body {
  flex: 1;
  min-width: 0;
}

.card-question {
  font-size: 15px;
  font-weight: 500;
  color: var(--text-primary);
  margin-bottom: 10px;
  line-height: 1.5;
}

.card-meta {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
}

.status-tag {
  font-size: 12px;
  font-weight: 500;
  padding: 2px 10px;
  border-radius: 20px;
}

.intent-tag {
  font-size: 12px;
  color: var(--primary);
  background: rgba(99, 102, 241, 0.08);
  padding: 2px 10px;
  border-radius: 20px;
}

.time-info,
.date-info {
  font-size: 12px;
  color: var(--text-secondary);
}

.pagination-area {
  display: flex;
  justify-content: center;
  margin-top: 24px;
}

.loading-center {
  display: flex;
  justify-content: center;
  padding: 60px 0;
  color: var(--primary);
}
</style>

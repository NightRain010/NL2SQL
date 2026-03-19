<script setup lang="ts">
/**
 * 数据库结构浏览页面。
 * 左侧展示表树、右侧展示选中表的字段详情，支持元数据刷新。
 */
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useSchemaStore } from "../stores/schema";
import { getTableList, getTableDetail, refreshMetadata } from "../api/schema";
import SchemaTree from "../components/SchemaTree.vue";
import { ElMessage } from "element-plus";

const router = useRouter();
const schemaStore = useSchemaStore();

async function fetchTables() {
  schemaStore.setLoading(true);
  try {
    const res = await getTableList();
    schemaStore.setTables(res.data.tables);
  } catch {
    /* 错误已在拦截器中处理 */
  } finally {
    schemaStore.setLoading(false);
  }
}

async function handleSelectTable(tableName: string) {
  try {
    const res = await getTableDetail(tableName);
    schemaStore.setCurrentTable(res.data);
  } catch {
    /* 错误已在拦截器中处理 */
  }
}

async function handleRefresh() {
  try {
    await refreshMetadata();
    ElMessage.success("元数据已刷新");
    await fetchTables();
  } catch {
    /* 错误已在拦截器中处理 */
  }
}

onMounted(fetchTables);
</script>

<template>
  <div class="schema-page">
    <header class="page-header glass">
      <div class="header-inner">
        <button class="back-btn" @click="router.push('/')">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="19" y1="12" x2="5" y2="12"/><polyline points="12,19 5,12 12,5"/></svg>
        </button>
        <h1>数据库结构</h1>
        <button class="refresh-btn" @click="handleRefresh">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="23,4 23,10 17,10"/><path d="M20.49 15a9 9 0 11-2.12-9.36L23 10"/></svg>
          刷新元数据
        </button>
      </div>
    </header>

    <main class="schema-content">
      <aside class="sidebar-area">
        <SchemaTree
          :tables="schemaStore.tables"
          :loading="schemaStore.loading"
          :selected-table="schemaStore.currentTable?.table_name"
          @select="handleSelectTable"
        />
      </aside>

      <section class="detail-area">
        <Transition name="fade-up" mode="out-in">
          <div v-if="schemaStore.currentTable" :key="schemaStore.currentTable.table_name" class="detail-card">
            <div class="detail-header">
              <div class="detail-icon">
                <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
              </div>
              <div>
                <h2>{{ schemaStore.currentTable.table_name }}</h2>
                <p>{{ schemaStore.currentTable.columns.length }} 个字段</p>
              </div>
            </div>

            <div class="columns-list">
              <div
                v-for="(col, idx) in schemaStore.currentTable.columns"
                :key="col.name"
                class="column-row"
                :style="{ animationDelay: `${idx * 40}ms` }"
              >
                <div class="col-name">
                  <span v-if="col.is_primary" class="pk-badge">PK</span>
                  {{ col.name }}
                </div>
                <div class="col-type">{{ col.type }}</div>
                <div class="col-nullable">{{ col.is_nullable ? "NULL" : "NOT NULL" }}</div>
                <div class="col-comment">{{ col.comment || "-" }}</div>
              </div>
            </div>
          </div>

          <div v-else class="empty-detail">
            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" stroke="#e2e8f0" stroke-width="1"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
            <p>请从左侧选择一张表查看结构</p>
          </div>
        </Transition>
      </section>
    </main>
  </div>
</template>

<style scoped>
.schema-page {
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
  flex: 1;
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

.refresh-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: #fff;
  color: var(--text-secondary);
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
}

.refresh-btn:hover {
  border-color: var(--primary);
  color: var(--primary);
}

.schema-content {
  max-width: 1100px;
  margin: 0 auto;
  padding: 32px 24px;
  display: grid;
  grid-template-columns: 280px 1fr;
  gap: 24px;
  align-items: start;
}

.detail-card {
  background: var(--bg-card);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.detail-header {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 24px;
  background: linear-gradient(135deg, #4f46e5, #6366f1);
}

.detail-icon {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.15);
  display: flex;
  align-items: center;
  justify-content: center;
}

.detail-header h2 {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  color: #fff;
}

.detail-header p {
  margin: 4px 0 0;
  font-size: 13px;
  color: rgba(255, 255, 255, 0.7);
}

.columns-list {
  padding: 8px 0;
}

.column-row {
  display: grid;
  grid-template-columns: 1.5fr 1fr 0.8fr 2fr;
  gap: 12px;
  padding: 14px 24px;
  font-size: 13px;
  border-bottom: 1px solid #f8fafc;
  animation: row-in 0.3s ease both;
}

@keyframes row-in {
  from { opacity: 0; transform: translateX(-8px); }
}

.column-row:last-child {
  border-bottom: none;
}

.column-row:hover {
  background: #f8fafc;
}

.col-name {
  font-weight: 500;
  color: var(--text-primary);
  display: flex;
  align-items: center;
  gap: 6px;
}

.pk-badge {
  font-size: 10px;
  font-weight: 700;
  padding: 1px 6px;
  border-radius: 4px;
  background: #fef3c7;
  color: #d97706;
}

.col-type {
  color: var(--primary);
  font-family: "JetBrains Mono", "Consolas", monospace;
  font-size: 12px;
}

.col-nullable {
  color: var(--text-secondary);
  font-size: 12px;
}

.col-comment {
  color: var(--text-secondary);
}

.empty-detail {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 100px 0;
  gap: 16px;
}

.empty-detail p {
  color: var(--text-secondary);
  margin: 0;
  font-size: 15px;
}

@media (max-width: 768px) {
  .schema-content {
    grid-template-columns: 1fr;
  }
}
</style>

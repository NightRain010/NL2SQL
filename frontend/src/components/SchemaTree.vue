<script setup lang="ts">
/**
 * 数据库表树形列表组件。
 * 展示所有业务表，支持点击选中高亮。
 */
import type { TableSummary } from "../types";

defineProps<{
  /** 表摘要列表。 */
  tables: TableSummary[];
  /** 是否正在加载。 */
  loading: boolean;
  /** 当前选中的表名，用于高亮。 */
  selectedTable?: string;
}>();

const emit = defineEmits<{
  /** 用户点击某张表时触发。 */
  select: [tableName: string];
}>();
</script>

<template>
  <div class="schema-sidebar">
    <div class="sidebar-title">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>
      <span>数据库表</span>
    </div>

    <div v-if="loading" class="loading-skeleton">
      <div v-for="i in 5" :key="i" class="skeleton-item" />
    </div>

    <div v-else-if="tables.length === 0" class="empty-hint">
      暂无表数据
    </div>

    <div v-else class="table-list">
      <div
        v-for="table in tables"
        :key="table.name"
        class="table-item card-hover"
        :class="{ active: selectedTable === table.name }"
        @click="emit('select', table.name)"
      >
        <div class="table-icon">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2"/><line x1="3" y1="9" x2="21" y2="9"/><line x1="9" y1="21" x2="9" y2="9"/></svg>
        </div>
        <div class="table-info">
          <div class="table-name">{{ table.name }}</div>
          <div class="table-meta">{{ table.column_count }} 个字段</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.schema-sidebar {
  background: var(--bg-card);
  border-radius: var(--radius);
  padding: 20px;
  box-shadow: var(--shadow-sm);
}

.sidebar-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px solid #f1f5f9;
}

.loading-skeleton {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.skeleton-item {
  height: 48px;
  background: linear-gradient(90deg, #f1f5f9 25%, #e2e8f0 50%, #f1f5f9 75%);
  background-size: 200% 100%;
  border-radius: 8px;
  animation: shimmer 1.5s infinite;
}

@keyframes shimmer {
  to { background-position: -200% 0; }
}

.table-list {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.table-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.table-item:hover {
  background: rgba(99, 102, 241, 0.06);
}

.table-item.active {
  background: rgba(99, 102, 241, 0.12);
  border-left: 3px solid var(--primary);
  padding-left: 9px;
}

.table-item.active .table-name {
  color: var(--primary);
  font-weight: 600;
}

.table-icon {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 8px;
  background: linear-gradient(135deg, #eef2ff, #e0e7ff);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--primary);
}

.table-name {
  font-weight: 500;
  font-size: 14px;
  color: var(--text-primary);
}

.table-meta {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 2px;
}

.empty-hint {
  text-align: center;
  color: var(--text-secondary);
  padding: 32px 0;
  font-size: 14px;
}
</style>

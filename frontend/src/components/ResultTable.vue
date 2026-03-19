<script setup lang="ts">
/**
 * 查询结果表格组件。
 * 展示结构化的查询结果，支持前端分页和列排序。
 */
import { ref, computed } from "vue";
import type { TableData } from "../types";

const props = defineProps<{
  /** 表格数据，包含列定义、行数据和总数。 */
  data: TableData;
}>();

const pageSize = ref(20);
const currentPage = ref(1);

const pagedRows = computed(() => {
  const start = (currentPage.value - 1) * pageSize.value;
  return props.data.rows.slice(start, start + pageSize.value);
});

const showPagination = computed(() => props.data.rows.length > pageSize.value);

function handlePageChange(page: number) {
  currentPage.value = page;
}
</script>

<template>
  <div class="result-card">
    <div class="result-header">
      <span class="result-label">查询结果</span>
      <span class="result-count">{{ data.total_count }} 条记录</span>
    </div>
    <div class="table-wrap">
      <el-table :data="pagedRows" stripe max-height="420" size="small" :header-cell-style="{ background: '#f8fafc', color: '#475569', fontWeight: 600 }">
        <el-table-column
          v-for="col in data.columns"
          :key="col.key"
          :prop="col.key"
          :label="col.label"
          :align="col.align"
          :sortable="col.sortable"
          min-width="120"
        />
        <template #empty>
          <div class="empty-state">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="#cbd5e1" stroke-width="1.5"><path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
            <p>暂无数据</p>
          </div>
        </template>
      </el-table>
    </div>
    <div v-if="showPagination" class="table-pagination">
      <el-pagination
        :current-page="currentPage"
        :page-size="pageSize"
        :total="data.rows.length"
        layout="prev, pager, next"
        small
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<style scoped>
.result-card {
  background: var(--bg-card);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  animation: fade-in-up 0.5s ease 0.1s both;
}

@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(12px); }
}

.result-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid #f1f5f9;
}

.result-label {
  font-weight: 600;
  font-size: 15px;
  color: var(--text-primary);
}

.result-count {
  font-size: 13px;
  color: var(--text-secondary);
  background: #f1f5f9;
  padding: 3px 10px;
  border-radius: 20px;
}

.table-wrap {
  padding: 0 4px 4px;
}

.empty-state {
  padding: 40px 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
}

.empty-state p {
  color: #94a3b8;
  margin: 0;
  font-size: 14px;
}

.table-pagination {
  display: flex;
  justify-content: center;
  padding: 12px 0;
}
</style>

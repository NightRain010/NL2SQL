<script setup lang="ts">
/**
 * SQL 展示组件。
 * 以代码块样式展示生成的 SQL 语句，并显示执行状态。
 */

const props = defineProps<{
  /** 生成的 SQL 语句文本。 */
  sql: string;
  /** 执行状态：success / failed / rejected / pending。 */
  status: string;
}>();

const statusLabelMap: Record<string, string> = {
  success: "成功",
  failed: "失败",
  rejected: "拒绝",
  pending: "处理中",
};
</script>

<template>
  <div class="sql-card">
    <div class="sql-header">
      <div class="sql-label">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="16,18 22,12 16,6"/><polyline points="8,6 2,12 8,18"/></svg>
        <span>生成的 SQL</span>
      </div>
      <span class="status-badge" :class="status">{{ statusLabelMap[status] || status }}</span>
    </div>
    <pre class="sql-block"><code>{{ sql }}</code></pre>
  </div>
</template>

<style scoped>
.sql-card {
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  animation: fade-in-up 0.4s ease both;
}

@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(12px); }
}

.sql-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 20px;
  background: #1e1b4b;
  border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}

.sql-label {
  display: flex;
  align-items: center;
  gap: 8px;
  color: rgba(255, 255, 255, 0.7);
  font-size: 13px;
  font-weight: 500;
}

.status-badge {
  font-size: 11px;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 20px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.status-badge.success {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.status-badge.failed,
.status-badge.rejected {
  background: rgba(239, 68, 68, 0.15);
  color: #f87171;
}

.status-badge.pending {
  background: rgba(251, 191, 36, 0.15);
  color: #fbbf24;
}

pre.sql-block {
  margin: 0;
  padding: 20px 24px;
  background: linear-gradient(180deg, #0f0a2e 0%, #0f172a 100%);
  font-family: "JetBrains Mono", "Fira Code", "Consolas", monospace;
  font-size: 13.5px;
  line-height: 1.7;
  color: #a5f3fc;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-all;
}
</style>

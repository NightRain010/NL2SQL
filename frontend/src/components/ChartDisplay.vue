<script setup lang="ts">
/**
 * 简易图表展示组件。
 * 根据后端返回的 ChartSuggestion 渲染柱状图/折线图/饼图的 CSS 可视化。
 * 不依赖第三方图表库，使用纯 CSS 实现轻量级数据可视化。
 */
import { computed } from "vue";
import type { ChartSuggestion, TableData } from "../types";

const props = defineProps<{
  /** 图表建议配置。 */
  suggestion: ChartSuggestion;
  /** 表格数据源。 */
  tableData: TableData;
}>();

interface DataPoint {
  label: string;
  value: number;
}

const chartData = computed<DataPoint[]>(() => {
  const { x_field, y_field } = props.suggestion;
  return props.tableData.rows
    .slice(0, 20)
    .map((row) => ({
      label: String(row[x_field] ?? ""),
      value: Number(row[y_field] ?? 0),
    }))
    .filter((d) => !isNaN(d.value));
});

const maxValue = computed(() =>
  Math.max(...chartData.value.map((d) => d.value), 1)
);

const chartTypeLabel = computed(() => {
  const map: Record<string, string> = {
    bar: "柱状图",
    line: "折线图",
    pie: "饼图",
  };
  return map[props.suggestion.chart_type] || "图表";
});

const barColors = [
  "#6366f1", "#06b6d4", "#8b5cf6", "#10b981", "#f59e0b",
  "#ef4444", "#ec4899", "#14b8a6", "#f97316", "#3b82f6",
];
</script>

<template>
  <div v-if="chartData.length >= 2" class="chart-card">
    <div class="chart-header">
      <span class="chart-label">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <rect x="3" y="12" width="4" height="9" rx="1" />
          <rect x="10" y="7" width="4" height="14" rx="1" />
          <rect x="17" y="3" width="4" height="18" rx="1" />
        </svg>
        <span>{{ suggestion.title || chartTypeLabel }}</span>
      </span>
      <span class="chart-type-badge">{{ chartTypeLabel }}</span>
    </div>

    <div class="chart-body">
      <div class="bar-chart">
        <div
          v-for="(item, idx) in chartData"
          :key="idx"
          class="bar-group"
        >
          <div class="bar-label" :title="item.label">{{ item.label }}</div>
          <div class="bar-track">
            <div
              class="bar-fill"
              :style="{
                width: `${(item.value / maxValue) * 100}%`,
                background: barColors[idx % barColors.length],
                animationDelay: `${idx * 60}ms`,
              }"
            />
          </div>
          <div class="bar-value">{{ item.value }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.chart-card {
  background: var(--bg-card);
  border-radius: var(--radius);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  animation: fade-in-up 0.5s ease 0.15s both;
}

@keyframes fade-in-up {
  from { opacity: 0; transform: translateY(12px); }
}

.chart-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  border-bottom: 1px solid #f1f5f9;
}

.chart-label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
}

.chart-type-badge {
  font-size: 11px;
  font-weight: 500;
  padding: 2px 10px;
  border-radius: 20px;
  background: rgba(99, 102, 241, 0.08);
  color: var(--primary);
}

.chart-body {
  padding: 20px;
}

.bar-chart {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.bar-group {
  display: grid;
  grid-template-columns: 100px 1fr 60px;
  align-items: center;
  gap: 12px;
}

.bar-label {
  font-size: 13px;
  color: var(--text-secondary);
  text-align: right;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.bar-track {
  height: 24px;
  background: #f1f5f9;
  border-radius: 6px;
  overflow: hidden;
}

.bar-fill {
  height: 100%;
  border-radius: 6px;
  min-width: 4px;
  animation: bar-grow 0.6s cubic-bezier(0.16, 1, 0.3, 1) both;
}

@keyframes bar-grow {
  from { width: 0 !important; }
}

.bar-value {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  text-align: left;
}
</style>

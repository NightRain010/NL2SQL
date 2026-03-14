<script setup lang="ts">
import type { TableData } from "../types";

defineProps<{
  data: TableData;
}>();
</script>

<template>
  <el-card shadow="never">
    <template #header>
      <span class="font-bold text-gray-700">查询结果 ({{ data.total_count }} 条)</span>
    </template>
    <el-table :data="data.rows" stripe border max-height="480" size="small">
      <el-table-column
        v-for="col in data.columns"
        :key="col.key"
        :prop="col.key"
        :label="col.label"
        :align="col.align"
        :sortable="col.sortable"
        min-width="120"
      />
    </el-table>
  </el-card>
</template>

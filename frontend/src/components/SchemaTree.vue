<script setup lang="ts">
import type { TableSummary } from "../types";

defineProps<{
  tables: TableSummary[];
  loading: boolean;
}>();

const emit = defineEmits<{
  select: [tableName: string];
}>();
</script>

<template>
  <el-card shadow="never">
    <template #header>
      <span class="font-bold">数据库表</span>
    </template>
    <el-skeleton :loading="loading" :rows="6" animated>
      <template #default>
        <div
          v-for="table in tables"
          :key="table.name"
          class="py-2 px-3 cursor-pointer rounded hover:bg-blue-50 transition-colors"
          @click="emit('select', table.name)"
        >
          <div class="font-medium text-gray-800">{{ table.name }}</div>
          <div class="text-xs text-gray-400">{{ table.column_count }} 个字段</div>
        </div>
        <el-empty v-if="tables.length === 0" description="暂无表数据" :image-size="64" />
      </template>
    </el-skeleton>
  </el-card>
</template>

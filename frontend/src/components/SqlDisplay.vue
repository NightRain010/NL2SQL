<script setup lang="ts">
defineProps<{
  sql: string;
  status: string;
}>();
</script>

<template>
  <el-card class="mt-4" shadow="never">
    <template #header>
      <div class="flex items-center justify-between">
        <span class="font-bold text-gray-700">生成的 SQL</span>
        <el-tag :type="status === 'success' ? 'success' : 'warning'" size="small">
          {{ status }}
        </el-tag>
      </div>
    </template>
    <pre class="bg-gray-900 text-green-400 p-4 rounded-lg overflow-x-auto text-sm leading-relaxed m-0"><code>{{ sql }}</code></pre>
  </el-card>
</template>

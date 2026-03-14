<template>
  <div class="flex flex-col items-center justify-center py-12">
    <el-icon class="is-loading text-4xl text-blue-500 mb-4">
      <svg viewBox="0 0 1024 1024" xmlns="http://www.w3.org/2000/svg">
        <path
          d="M512 64a32 32 0 0 1 32 32v192a32 32 0 0 1-64 0V96a32 32 0 0 1 32-32z"
          fill="currentColor"
        />
        <path
          d="M512 736a32 32 0 0 1 32 32v192a32 32 0 0 1-64 0V768a32 32 0 0 1 32-32z"
          fill="currentColor"
          opacity="0.3"
        />
      </svg>
    </el-icon>
    <p class="text-gray-500">正在分析问题并生成查询...</p>
  </div>
</template>

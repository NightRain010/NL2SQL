<script setup lang="ts">
import { RouterView } from "vue-router";
</script>

<template>
  <el-config-provider>
    <div class="min-h-screen bg-gray-50">
      <RouterView />
    </div>
  </el-config-provider>
</template>

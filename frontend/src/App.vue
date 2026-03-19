<script setup lang="ts">
import { RouterView } from "vue-router";
</script>

<template>
  <el-config-provider>
    <RouterView v-slot="{ Component }">
      <Transition name="page" mode="out-in">
        <component :is="Component" />
      </Transition>
    </RouterView>
  </el-config-provider>
</template>

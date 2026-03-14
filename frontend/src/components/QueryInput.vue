<script setup lang="ts">
import { ref } from "vue";

const props = defineProps<{
  loading: boolean;
}>();

const emit = defineEmits<{
  submit: [question: string];
}>();

const question = ref("");

function handleSubmit() {
  const trimmed = question.value.trim();
  if (trimmed.length < 2) return;
  emit("submit", trimmed);
}
</script>

<template>
  <el-card class="mt-6" shadow="hover">
    <div class="flex gap-3">
      <el-input
        v-model="question"
        placeholder="用自然语言描述你想查询的数据，例如：查一下张三的数学成绩"
        size="large"
        clearable
        @keyup.enter="handleSubmit"
      />
      <el-button
        type="primary"
        size="large"
        :loading="props.loading"
        @click="handleSubmit"
        :disabled="question.trim().length < 2"
      >
        查询
      </el-button>
    </div>
  </el-card>
</template>

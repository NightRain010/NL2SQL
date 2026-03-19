<script setup lang="ts">
/**
 * 查询输入框组件。
 * 提供带搜索图标的输入框和提交按钮，支持 Enter 提交和 loading 状态。
 */
import { ref } from "vue";

const props = defineProps<{
  /** 是否正在加载（禁用提交按钮）。 */
  loading: boolean;
}>();

const emit = defineEmits<{
  /** 用户提交查询时触发。 */
  submit: [question: string];
}>();

const question = ref("");
const isFocused = ref(false);

function handleSubmit() {
  const trimmed = question.value.trim();
  if (trimmed.length < 2) return;
  emit("submit", trimmed);
}
</script>

<template>
  <div class="input-wrapper" :class="{ focused: isFocused }">
    <div class="input-icon">
      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65" y2="16.65"/></svg>
    </div>
    <input
      v-model="question"
      type="text"
      placeholder="用自然语言描述你想查询的数据，例如：全班数学平均分是多少"
      @focus="isFocused = true"
      @blur="isFocused = false"
      @keyup.enter="handleSubmit"
    />
    <button
      class="ask-btn"
      :class="{ disabled: question.trim().length < 2 }"
      :disabled="question.trim().length < 2 || props.loading"
      @click="handleSubmit"
    >
      <template v-if="props.loading">
        <span class="btn-spinner" />
      </template>
      <template v-else>
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.5" stroke-linecap="round"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12,5 19,12 12,19"/></svg>
      </template>
    </button>
  </div>
</template>

<style scoped>
.input-wrapper {
  display: flex;
  align-items: center;
  gap: 12px;
  background: var(--bg-card);
  border: 2px solid transparent;
  border-radius: 16px;
  padding: 6px 8px 6px 20px;
  box-shadow: var(--shadow-md);
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}

.input-wrapper.focused {
  border-color: var(--primary);
  box-shadow: 0 0 0 4px rgba(99, 102, 241, 0.1), var(--shadow-md);
  transform: translateY(-2px);
}

.input-icon {
  flex-shrink: 0;
  color: var(--text-secondary);
  opacity: 0.5;
  transition: opacity 0.2s;
}

.focused .input-icon {
  opacity: 1;
  color: var(--primary);
}

input {
  flex: 1;
  border: none;
  outline: none;
  background: none;
  font-size: 15px;
  color: var(--text-primary);
  padding: 12px 0;
  min-width: 0;
}

input::placeholder {
  color: #94a3b8;
}

.ask-btn {
  flex-shrink: 0;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  border: none;
  background: linear-gradient(135deg, #6366f1, #4f46e5);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.ask-btn:hover:not(.disabled) {
  transform: scale(1.05);
  box-shadow: 0 4px 16px rgba(99, 102, 241, 0.4);
}

.ask-btn.disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.btn-spinner {
  width: 20px;
  height: 20px;
  border: 2.5px solid rgba(255, 255, 255, 0.3);
  border-top-color: #fff;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}
</style>

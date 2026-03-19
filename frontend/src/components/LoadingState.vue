<script setup lang="ts">
/**
 * 加载状态组件。
 * 在查询处理期间展示动画指示器和提示文字。
 */
</script>

<template>
  <div class="loading-state">
    <div class="loading-visual">
      <div class="orbit">
        <div class="dot dot-1" />
        <div class="dot dot-2" />
        <div class="dot dot-3" />
      </div>
    </div>
    <p class="loading-text">正在分析问题并生成查询<span class="dots" /></p>
  </div>
</template>

<style scoped>
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 48px 0;
  animation: fade-in 0.4s ease;
}

@keyframes fade-in {
  from { opacity: 0; }
}

.loading-visual {
  width: 56px;
  height: 56px;
  position: relative;
  margin-bottom: 20px;
}

.orbit {
  width: 100%;
  height: 100%;
  position: relative;
  animation: spin-slow 3s linear infinite;
}

@keyframes spin-slow {
  to { transform: rotate(360deg); }
}

.dot {
  position: absolute;
  width: 12px;
  height: 12px;
  border-radius: 50%;
}

.dot-1 {
  background: #6366f1;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  animation: pulse 1.5s ease-in-out infinite;
}

.dot-2 {
  background: #06b6d4;
  bottom: 4px;
  left: 4px;
  animation: pulse 1.5s ease-in-out 0.3s infinite;
}

.dot-3 {
  background: #8b5cf6;
  bottom: 4px;
  right: 4px;
  animation: pulse 1.5s ease-in-out 0.6s infinite;
}

@keyframes pulse {
  0%, 100% { transform: scale(1); opacity: 1; }
  50% { transform: scale(0.6); opacity: 0.4; }
}

.loading-text {
  color: var(--text-secondary);
  font-size: 14px;
  margin: 0;
}

.dots::after {
  content: '';
  animation: typing 1.5s steps(3) infinite;
}

@keyframes typing {
  0% { content: ''; }
  25% { content: '.'; }
  50% { content: '..'; }
  75% { content: '...'; }
}
</style>

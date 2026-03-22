<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import WorkspacePanel from '../components/WorkspacePanel.vue'
import { reviewApi } from '../api'
import type { Problem } from '../types'

const router = useRouter()

const problem = ref<Problem | null>(null)
const isLoadingProblem = ref(false)
const error = ref('')

onMounted(async () => {
  await loadRandomProblem()
})

async function loadRandomProblem() {
  try {
    isLoadingProblem.value = true
    error.value = ''
    const response = await reviewApi.getRandomProblem(problem.value?.id)
    problem.value = response.data || null
  } catch (e: any) {
    error.value = e.response?.status === 404 ? '暂无可复习的题目' : '加载题目失败'
    console.error('Failed to load random problem:', e)
  } finally {
    isLoadingProblem.value = false
  }
}
</script>

<template>
  <div class="relative">
    <!-- Floating refresh button -->
    <button
      :disabled="isLoadingProblem"
      class="floating-btn"
      title="换一题"
      @click="loadRandomProblem"
    >
      <svg
        :class="{ 'animate-spin': isLoadingProblem }"
        class="w-5 h-5"
        viewBox="0 0 24 24"
        fill="none"
        stroke="currentColor"
        stroke-width="2"
      >
        <path d="M23 4v6h-6"></path>
        <path d="M1 20v-6h6"></path>
        <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
      </svg>
    </button>

    <!-- Error toast -->
    <Transition name="slide-down">
      <div
        v-if="error"
        class="fixed top-20 left-1/2 -translate-x-1/2 z-1000 flex items-center gap-2.5 px-5 py-3 bg-(--error-soft) border border-red-500/30 rounded-[10px] text-(--error) text-sm font-medium shadow-(--shadow-lg)"
      >
        <svg
          class="w-4.5 h-4.5 shrink-0"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <circle cx="12" cy="12" r="10"></circle>
          <line x1="12" y1="8" x2="12" y2="12"></line>
          <line x1="12" y1="16" x2="12.01" y2="16"></line>
        </svg>
        <span>{{ error }}</span>
        <button
          class="bg-transparent border-none text-(--error) text-xl cursor-pointer px-1 leading-none"
          @click="error = ''"
        >
          ×
        </button>
      </div>
    </Transition>

    <!-- Loading state -->
    <div
      v-if="isLoadingProblem"
      class="flex flex-col items-center justify-center min-h-[calc(100vh-64px-48px)] text-(--text-muted)"
    >
      <div
        class="w-8 h-8 border-[3px] border-(--border) border-t-(--accent) rounded-full animate-spin mb-4"
      ></div>
      <p>加载题目中...</p>
    </div>

    <!-- Empty state -->
    <div
      v-else-if="!problem"
      class="flex flex-col items-center justify-center min-h-[calc(100vh-64px-48px)] text-center"
    >
      <div
        class="w-20 h-20 flex items-center justify-center bg-(--bg-card) border border-(--border) rounded-2xl mb-5"
      >
        <svg
          class="w-9 h-9 text-(--text-muted)"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="1.5"
        >
          <path d="M12 2L2 7l10 5 10-5-10-5z"></path>
          <path d="M2 17l10 5 10-5"></path>
          <path d="M2 12l10 5 10-5"></path>
        </svg>
      </div>
      <h3 class="text-lg font-semibold m-0 mb-2">暂无可复习的题目</h3>
      <p class="text-sm text-(--text-muted) m-0">请先添加题目开始练习</p>
      <button class="btn btn-primary mt-5" @click="router.push('/')">去添加题目</button>
    </div>

    <!-- Workspace -->
    <WorkspacePanel
      v-else
      ref="workspaceRef"
      :problem="problem"
      @change-problem="loadRandomProblem"
    />
  </div>
</template>

<style scoped>
/* Floating button */
.floating-btn {
  position: fixed;
  right: 24px;
  bottom: 24px;
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--accent);
  color: #fff;
  border: none;
  border-radius: 50%;
  cursor: pointer;
  box-shadow: var(--shadow-lg), var(--shadow-glow);
  z-index: 50;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.dark .floating-btn {
  color: #000;
}

.floating-btn:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: var(--shadow-lg), 0 0 40px var(--accent-glow);
}

.floating-btn:active:not(:disabled) {
  transform: scale(0.95);
}

.floating-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Transitions */
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from,
.slide-down-leave-to {
  opacity: 0;
  transform: translate(-50%, -20px);
}
</style>

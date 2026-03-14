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
    const response = await reviewApi.getRandomProblem()
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
    <!-- Header -->
    <header
      class="flex items-start justify-between mb-6 max-md:flex-col max-md:gap-4 max-md:items-stretch"
    >
      <div>
        <h1
          class="text-[28px] font-bold m-0 mb-1 bg-linear-to-br from-(--text-primary) to-(--accent) bg-clip-text text-transparent max-md:text-[22px]"
        >
          复习
        </h1>
        <p class="text-[15px] text-(--text-muted) m-0">随机练习，巩固所学</p>
      </div>
      <button
        :disabled="isLoadingProblem"
        class="btn btn-secondary min-w-30 whitespace-nowrap max-md:w-full"
        @click="loadRandomProblem"
      >
        <svg
          :class="{ 'animate-spin': isLoadingProblem }"
          class="w-4 h-4"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <path d="M23 4v6h-6"></path>
          <path d="M1 20v-6h6"></path>
          <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15"></path>
        </svg>
        换一题
      </button>
    </header>

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
      class="flex flex-col items-center justify-center py-20 px-5 text-(--text-muted)"
    >
      <div
        class="w-8 h-8 border-[3px] border-(--border) border-t-(--accent) rounded-full animate-spin mb-4"
      ></div>
      <p>加载题目中...</p>
    </div>

    <!-- Empty state -->
    <div
      v-else-if="!problem"
      class="flex flex-col items-center justify-center py-20 px-5 text-center"
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

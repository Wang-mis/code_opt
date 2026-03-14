<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import WorkspacePanel from '../components/WorkspacePanel.vue'
import { problemsApi } from '../api'
import type { Problem } from '../types'

const route = useRoute()
const router = useRouter()

// State
const problem = ref<Problem | null>(null)
const problems = ref<Problem[]>([])
const showProblemList = ref(false)
const showNewProblemForm = ref(false)
const isTransitioning = ref(false)
const error = ref('')

// Form state
const newProblemTitle = ref('')
const newProblemDescription = ref('')
const isCreating = ref(false)

// Load problems on mount
onMounted(async () => {
  await loadProblems()
  const problemId = route.params.id
  if (problemId) {
    await loadProblem(Number(problemId))
  }
})

// Watch route changes
watch(
  () => route.params.id,
  async newId => {
    if (newId) {
      await loadProblem(Number(newId))
    }
  }
)

async function loadProblems() {
  try {
    const response = await problemsApi.getAll()
    problems.value = response.data || []
  } catch (e: any) {
    console.error('Failed to load problems:', e)
  }
}

async function loadProblem(id: number) {
  try {
    const response = await problemsApi.get(id)
    problem.value = response.data || null
  } catch (e: any) {
    error.value = '加载题目失败'
    console.error('Failed to load problem:', e)
  }
}

async function createProblem() {
  if (!newProblemTitle.value || !newProblemDescription.value) {
    error.value = '请填写标题和描述'
    return
  }

  try {
    isCreating.value = true
    const response = await problemsApi.create({
      title: newProblemTitle.value,
      description: newProblemDescription.value,
    })
    problem.value = response.data || null
    problems.value.push(problem.value)
    showNewProblemForm.value = false
    newProblemTitle.value = ''
    newProblemDescription.value = ''
    router.push(`/problem/${problem.value?.id}`)
  } catch (e: any) {
    error.value = '创建题目失败'
    console.error('Failed to create problem:', e)
  } finally {
    isCreating.value = false
  }
}

function selectProblem(p: Problem) {
  problem.value = p
  showProblemList.value = false
  router.push(`/problem/${p.id}`)
}

function changeProblem() {
  problem.value = null
  router.push('/')
}

function formatDate(date: string) {
  return new Date(date).toLocaleDateString('zh-CN', {
    month: 'short',
    day: 'numeric',
  })
}

function goBack() {
  isTransitioning.value = true
  showProblemList.value = false
  showNewProblemForm.value = false
}

function onTransitionEnd() {
  isTransitioning.value = false
}
</script>

<template>
  <div class="relative">
    <!-- Workspace when problem is selected -->
    <WorkspacePanel v-if="problem" :problem="problem" @change-problem="changeProblem" />

    <!-- Welcome section - No problem selected -->
    <div v-else class="flex flex-col items-center justify-center min-h-[calc(100vh-140px)]">
      <!-- Welcome content -->
      <div
        v-if="!showProblemList && !showNewProblemForm && !isTransitioning"
        class="flex items-center justify-center p-5 w-full"
      >
        <div class="max-w-150 w-full text-center">
          <h1
            class="text-3xl font-bold mb-2 bg-linear-to-br from-(--text-primary) to-(--accent) bg-clip-text text-transparent"
          >
            开始练习
          </h1>
          <p class="text-base text-(--text-muted) mb-8">选择一个题目开始你的代码优化之旅</p>

          <div class="flex gap-4 justify-center max-md:flex-col">
            <button
              class="btn btn-primary min-w-40 py-3 px-6 max-md:w-full"
              @click="showProblemList = true"
            >
              <svg
                class="w-4 h-4"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
                <line x1="16" y1="13" x2="8" y2="13"></line>
                <line x1="16" y1="17" x2="8" y2="17"></line>
              </svg>
              选择题目
            </button>
            <button
              class="btn btn-secondary min-w-40 py-3 px-6 max-md:w-full"
              @click="showNewProblemForm = true"
            >
              <svg
                class="w-4 h-4"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <line x1="12" y1="5" x2="12" y2="19"></line>
                <line x1="5" y1="12" x2="19" y2="12"></line>
              </svg>
              创建新题目
            </button>
          </div>
        </div>
      </div>

      <!-- Problem list dropdown -->
      <Transition name="slide-up" @after-leave="onTransitionEnd">
        <div v-if="showProblemList" class="w-full max-w-170 px-5 max-md:px-4">
          <button
            class="flex items-center gap-1 bg-transparent border-none text-(--text-muted) text-sm font-medium cursor-pointer mb-4 p-0 hover:text-(--accent)"
            @click="goBack"
          >
            <svg
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
            返回
          </button>

          <div class="bg-(--bg-card) border border-(--border) rounded-xl overflow-hidden text-left">
            <div v-if="problems.length === 0" class="p-8 text-(--text-muted) text-center">
              暂无题目，请创建新题目
            </div>
            <div v-else class="max-h-100 overflow-y-auto">
              <button
                v-for="p in problems"
                :key="p.id"
                class="w-full flex items-center justify-between px-5 py-4 bg-transparent border-none border-b border-(--border) text-(--text-primary) cursor-pointer text-left last:border-b-0 hover:bg-(--bg-elevated)"
                @click="selectProblem(p)"
              >
                <div class="flex flex-col gap-1">
                  <span class="text-[15px] font-medium">{{ p.title }}</span>
                  <span class="text-xs text-(--text-muted)">{{ formatDate(p.createdAt) }}</span>
                </div>
                <svg
                  class="w-4.5 h-4.5 text-(--text-muted) shrink-0"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <polyline points="9 18 15 12 9 6"></polyline>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </Transition>

      <!-- New problem form -->
      <Transition name="slide-up" @after-leave="onTransitionEnd">
        <div v-if="showNewProblemForm" class="w-full max-w-170 px-5 max-md:px-4">
          <button
            class="flex items-center gap-1 bg-transparent border-none text-(--text-muted) text-sm font-medium cursor-pointer mb-4 p-0 hover:text-(--accent)"
            @click="goBack"
          >
            <svg
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <polyline points="15 18 9 12 15 6"></polyline>
            </svg>
            返回
          </button>

          <div class="bg-(--bg-card) border border-(--border) rounded-xl p-6 text-left">
            <h3 class="text-lg font-semibold mb-5">创建新题目</h3>

            <div class="mb-4">
              <label class="block text-[13px] font-medium text-(--text-secondary) mb-2"
                >题目标题</label
              >
              <input
                v-model="newProblemTitle"
                type="text"
                class="input"
                placeholder="输入题目标题..."
              />
            </div>

            <div class="mb-4">
              <label class="block text-[13px] font-medium text-(--text-secondary) mb-2">
                题目描述 <span class="font-normal text-(--text-muted)">支持 Markdown</span>
              </label>
              <textarea
                v-model="newProblemDescription"
                rows="8"
                class="input resize-y min-h-40"
                placeholder="描述题目要求..."
              ></textarea>
            </div>

            <div class="flex gap-3 mt-5">
              <button :disabled="isCreating" class="btn btn-primary" @click="createProblem">
                {{ isCreating ? '创建中...' : '创建题目' }}
              </button>
            </div>
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<style scoped>
/* Slide up transition */
.slide-up-enter-active {
  animation: slide-up-in 0.3s ease-out;
}

.slide-up-leave-active {
  animation: slide-up-in 0.2s ease-in reverse;
}

@keyframes slide-up-in {
  0% {
    opacity: 0;
    transform: translateY(20px);
  }

  100% {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>

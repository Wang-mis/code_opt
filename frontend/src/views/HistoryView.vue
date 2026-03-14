<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { submissionsApi } from '../api'
import MarkdownViewer from '../components/MarkdownViewer.vue'
import type { LearningSession, Submission } from '../types'

const sessions = ref<LearningSession[]>([])
const expandedSessions = ref<Set<string>>(new Set())
const expandedCodes = ref<Set<number>>(new Set())
const isLoading = ref(true)
const error = ref('')

onMounted(async () => {
  await loadSessions()
})

async function loadSessions() {
  try {
    isLoading.value = true
    const response = await submissionsApi.getAll()
    const allSubmissions = response.data || []

    const sessionMap = new Map<string, LearningSession>()
    for (const sub of allSubmissions) {
      const sessionId = sub.sessionId
      if (!sessionMap.has(sessionId)) {
        sessionMap.set(sessionId, {
          id: sessionId,
          problemId: sub.problemId,
          problem: sub.problem,
          startedAt: sub.createdAt,
          submissions: [],
        })
      }
      const session = sessionMap.get(sessionId)!
      session.submissions!.push(sub)
    }

    sessions.value = Array.from(sessionMap.values()).sort(
      (a, b) => new Date(b.startedAt).getTime() - new Date(a.startedAt).getTime()
    )
  } catch (e: unknown) {
    error.value = '加载历史记录失败'
    console.error('Failed to load sessions:', e)
  } finally {
    isLoading.value = false
  }
}

function toggleSession(sessionId: string) {
  if (expandedSessions.value.has(sessionId)) {
    expandedSessions.value.delete(sessionId)
  } else {
    expandedSessions.value.add(sessionId)
  }
}

function toggleCode(submissionId: number) {
  if (expandedCodes.value.has(submissionId)) {
    expandedCodes.value.delete(submissionId)
  } else {
    expandedCodes.value.add(submissionId)
  }
}

function formatDate(date: string) {
  if (!date) return ''
  const d = new Date(date)
  if (isNaN(d.getTime())) return ''
  return d.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
  })
}

function getStatusConfig(status: string) {
  switch (status) {
    case 'perfect':
      return { text: '完美', class: 'bg-(--success-soft) text-(--success)' }
    case 'has_issues':
      return { text: '需改进', class: 'bg-(--warning-soft) text-(--warning)' }
    default:
      return { text: '待评价', class: 'bg-(--bg-surface) text-(--text-muted)' }
  }
}

function getSortedSubmissions(submissions: Submission[] | undefined): Submission[] {
  if (!submissions) return []
  // Sort by iteration descending (highest iteration = newest first)
  return [...submissions].sort((a, b) => b.iteration - a.iteration)
}
</script>

<template>
  <div class="max-w-200 mx-auto">
    <!-- Header -->
    <header class="mb-8">
      <h1
        class="text-[28px] font-bold m-0 mb-1 bg-linear-to-br from-(--text-primary) to-(--accent) bg-clip-text text-transparent max-md:text-[22px]"
      >
        学习历史
      </h1>
      <p class="text-[15px] text-(--text-muted) m-0">回顾你的代码优化历程</p>
    </header>

    <!-- Error state -->
    <div
      v-if="error"
      class="flex items-center gap-2.5 px-5 py-4 bg-(--error-soft) border border-red-500/20 rounded-[10px] text-(--error)"
    >
      <svg class="w-5 h-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="8" x2="12" y2="12"></line>
        <line x1="12" y1="16" x2="12.01" y2="16"></line>
      </svg>
      {{ error }}
    </div>

    <!-- Loading state -->
    <div
      v-if="isLoading"
      class="flex flex-col items-center justify-center py-20 px-5 text-(--text-muted)"
    >
      <div
        class="w-8 h-8 border-[3px] border-(--border) border-t-(--accent) rounded-full animate-spin mb-4"
      ></div>
      <p>加载中...</p>
    </div>

    <!-- Empty state -->
    <div
      v-else-if="sessions.length === 0"
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
          <path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
        </svg>
      </div>
      <h3 class="text-lg font-semibold m-0 mb-2">暂无学习记录</h3>
      <p class="text-sm text-(--text-muted) m-0">提交代码后，记录将显示在这里</p>
    </div>

    <!-- Sessions list -->
    <div v-else class="flex flex-col gap-3">
      <div
        v-for="session in sessions"
        :key="session.id"
        class="bg-(--bg-card) border border-(--border) rounded-xl overflow-hidden hover:border-(--border-hover)"
        :class="{ 'border-(--accent)!': expandedSessions.has(session.id) }"
      >
        <!-- Session header -->
        <button
          class="w-full flex items-center justify-between px-5 py-4 bg-transparent border-none cursor-pointer text-left hover:bg-(--bg-elevated) max-md:py-3.5"
          @click="toggleSession(session.id)"
        >
          <div class="flex items-center gap-3.5">
            <div
              class="w-10 h-10 flex items-center justify-center bg-(--accent-soft) rounded-[10px] max-md:hidden"
            >
              <svg
                class="w-5 h-5 text-(--accent)"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path>
                <polyline points="14 2 14 8 20 8"></polyline>
              </svg>
            </div>
            <div class="flex flex-col gap-0.5">
              <span class="text-[15px] font-semibold text-(--text-primary)">{{
                session.problem?.title || `题目 #${session.problemId}`
              }}</span>
              <span class="text-[13px] text-(--text-muted)">{{
                formatDate(session.startedAt)
              }}</span>
            </div>
          </div>
          <div class="flex items-center gap-3">
            <span
              class="text-[13px] font-medium text-(--text-muted) px-2.5 py-1 bg-(--bg-surface) rounded-full"
              >{{ session.submissions?.length || 0 }} 次提交</span
            >
            <svg
              class="w-4.5 h-4.5 text-(--text-muted) transition-transform duration-200"
              :class="{ 'rotate-180': expandedSessions.has(session.id) }"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <polyline points="6 9 12 15 18 9"></polyline>
            </svg>
          </div>
        </button>

        <!-- Session details -->
        <Transition name="expand">
          <div v-if="expandedSessions.has(session.id)" class="border-t border-(--border)">
            <div
              v-for="submission in getSortedSubmissions(session.submissions)"
              :key="submission.id"
              class="p-5 border-b border-(--border) last:border-b-0 max-md:p-4"
            >
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-2.5">
                  <span class="text-[13px] font-medium text-(--text-muted)"
                    >第 {{ submission.iteration }} 次提交</span
                  >
                  <span
                    class="text-xs font-medium px-2 py-0.75 rounded-full"
                    :class="getStatusConfig(submission.status).class"
                  >
                    {{ getStatusConfig(submission.status).text }}
                  </span>
                </div>
                <span class="text-xs text-(--text-muted)">{{
                  formatDate(submission.createdAt)
                }}</span>
              </div>

              <!-- Code snippet -->
              <div class="bg-(--bg-surface) rounded-lg overflow-hidden mb-3">
                <pre
                  class="m-0 px-4 py-3 font-mono text-xs leading-relaxed overflow-x-auto text-(--text-primary)"
                ><code>{{ expandedCodes.has(submission.id) ? submission.code : submission.code.slice(0, 300) + (submission.code.length > 300 ? '...' : '') }}</code></pre>
                <button
                  v-if="submission.code.length > 300"
                  class="w-full px-4 py-2 text-xs text-(--accent) bg-transparent border-none border-t border-(--border) cursor-pointer hover:bg-(--bg-elevated)"
                  @click="toggleCode(submission.id)"
                >
                  {{ expandedCodes.has(submission.id) ? '收起代码' : '展开完整代码' }}
                </button>
              </div>

              <!-- Evaluation -->
              <div>
                <h4 class="text-[13px] font-semibold text-(--text-secondary) m-0 mb-2">评价</h4>
                <MarkdownViewer :content="submission.evaluation" />
              </div>
            </div>
          </div>
        </Transition>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Expand transition */
.expand-enter-active,
.expand-leave-active {
  transition: all 0.3s ease;
  overflow: hidden;
}

.expand-enter-from,
.expand-leave-to {
  opacity: 0;
  max-height: 0;
}

.expand-enter-to,
.expand-leave-from {
  max-height: 2000px;
}
</style>
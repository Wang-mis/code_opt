<script setup lang="ts">
import { ref, computed, watch } from 'vue'
import CodeEditor from '../components/CodeEditor.vue'
import MarkdownViewer from '../components/MarkdownViewer.vue'
import { useModelConfigStore } from '../stores/modelConfig'
import { useEditorStore } from '../stores/editor'
import { evaluateApi } from '../api'
import type { Problem, EvaluationResult, OptimalSolution } from '../types'
import { LANGUAGE_OPTIONS } from '../types'

const props = defineProps<{
  problem: Problem
}>()

const _emit = defineEmits<{
  'change-problem': []
}>()

const modelConfigStore = useModelConfigStore()
const editorStore = useEditorStore()

// State
const evaluationResult = ref<EvaluationResult | null>(null)
const optimalSolution = ref<OptimalSolution | null>(null)
const showOptimalSolution = ref(false)
const betterSolutionHint = ref('')
const showBetterHint = ref(false)
const isLoading = ref(false)
const error = ref('')

// Panel width state (percentage for problem panel, editor takes the rest)
const problemPanelWidth = ref(30)

// Computed
const isPerfectCode = computed(() => evaluationResult.value?.status === 'perfect')
const canShowBetterHint = computed(() => isPerfectCode.value && !showBetterHint.value)

// Watch problem changes to reset state
watch(
  () => props.problem,
  () => {
    evaluationResult.value = null
    optimalSolution.value = null
    showOptimalSolution.value = false
    betterSolutionHint.value = ''
    showBetterHint.value = false
    editorStore.reset()
  },
  { immediate: true }
)

async function submitCode() {
  if (!editorStore.code.trim()) {
    error.value = '请输入代码'
    return
  }

  if (!modelConfigStore.isConfigured()) {
    error.value = '请先配置模型'
    return
  }

  try {
    isLoading.value = true
    error.value = ''
    evaluationResult.value = null
    optimalSolution.value = null
    showOptimalSolution.value = false

    const sessionId = editorStore.currentSessionId || editorStore.generateSessionId()

    const response = await evaluateApi.submit({
      problemId: props.problem.id,
      code: editorStore.code,
      sessionId,
      modelConfig: modelConfigStore.config,
    })

    evaluationResult.value = response.data || null
  } catch (e: any) {
    error.value = e.response?.data?.detail || '提交失败'
    console.error('Failed to submit code:', e)
  } finally {
    isLoading.value = false
  }
}

async function showAnswer() {
  if (!modelConfigStore.isConfigured()) {
    error.value = '请先配置模型'
    return
  }

  try {
    isLoading.value = true
    error.value = ''

    const response = await evaluateApi.getOptimalSolution({
      problemId: props.problem.id,
      modelConfig: modelConfigStore.config,
    })

    optimalSolution.value = response.data || null
    showOptimalSolution.value = true
  } catch (e: any) {
    error.value = '获取答案失败'
    console.error('Failed to get optimal solution:', e)
  } finally {
    isLoading.value = false
  }
}

async function getBetterHint() {
  if (!editorStore.code) return

  if (!modelConfigStore.isConfigured()) {
    error.value = '请先配置模型'
    return
  }

  try {
    isLoading.value = true
    error.value = ''

    const response = await evaluateApi.getBetterSolutionHint({
      problemId: props.problem.id,
      code: editorStore.code,
      modelConfig: modelConfigStore.config,
    })

    betterSolutionHint.value = response.data?.hint || ''
    showBetterHint.value = true
  } catch (e: any) {
    error.value = '获取提示失败'
    console.error('Failed to get better hint:', e)
  } finally {
    isLoading.value = false
  }
}

function copyToClipboard(text: string) {
  navigator.clipboard.writeText(text)
}

function clearError() {
  error.value = ''
}

function startResize(e: MouseEvent) {
  e.preventDefault()

  function onMouseMove(e: MouseEvent) {
    const container = (e.target as HTMLElement).closest('.workspace-top')
    if (!container) return
    const containerRect = container.getBoundingClientRect()
    const newWidth = ((e.clientX - containerRect.left) / containerRect.width) * 100
    problemPanelWidth.value = Math.min(Math.max(newWidth, 30), 70)
  }

  function onMouseUp() {
    document.removeEventListener('mousemove', onMouseMove)
    document.removeEventListener('mouseup', onMouseUp)
  }

  document.addEventListener('mousemove', onMouseMove)
  document.addEventListener('mouseup', onMouseUp)
}

defineExpose({
  submitCode,
  showAnswer,
})
</script>

<template>
  <div class="flex flex-col">
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
          @click="clearError"
        >
          ×
        </button>
      </div>
    </Transition>

    <!-- Top row: Problem + Editor -->
    <div class="workspace-top flex h-[calc(100vh-64px-48px)] max-lg:flex-col">
      <!-- Left panel: Problem -->
      <section
        class="flex flex-col bg-(--bg-card) border border-(--border) border-r-0 rounded-l-xl overflow-hidden shrink-0 max-lg:w-full max-lg:rounded-xl max-lg:border-r max-lg:border-b-0"
        :style="{ width: problemPanelWidth + '%' }"
      >
        <header
          class="flex items-center justify-between px-5 py-4 border-b border-(--border) shrink-0"
        >
          <h2 class="text-base font-semibold m-0">{{ problem.title }}</h2>
          <button
            class="flex items-center gap-1 text-[13px] font-medium text-(--text-muted) bg-transparent border-none cursor-pointer hover:text-(--accent)"
            @click="$emit('change-problem')"
          >
            更换题目
            <svg
              class="w-3.5 h-3.5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <polyline points="9 18 15 12 9 6"></polyline>
            </svg>
          </button>
        </header>
        <div class="flex-1 p-5 overflow-y-auto">
          <MarkdownViewer :content="problem.description" />
        </div>
      </section>

      <!-- Resizer -->
      <div
        class="w-2 bg-(--border) cursor-col-resize flex items-center justify-center shrink-0 hover:bg-(--accent) max-lg:hidden"
        @mousedown="startResize"
      >
        <div
          class="w-1 h-10 bg-(--text-muted) rounded opacity-50 hover:bg-(--bg-deep) hover:opacity-100"
        ></div>
      </div>

      <!-- Right panel: Editor -->
      <section
        class="flex flex-col flex-1 bg-(--bg-card) border border-(--border) rounded-r-xl overflow-hidden max-lg:rounded-xl"
      >
        <header
          class="flex items-center justify-between px-5 py-4 border-b border-(--border) shrink-0"
        >
          <div class="flex items-center gap-3">
            <h2 class="text-base font-semibold m-0">代码</h2>
            <select
              v-model="editorStore.language"
              class="px-3 py-1.5 text-[13px] font-mono bg-(--bg-surface) border border-(--border) rounded-md text-(--text-primary) cursor-pointer"
            >
              <option v-for="lang in LANGUAGE_OPTIONS" :key="lang.value" :value="lang.value">
                {{ lang.label }}
              </option>
            </select>
          </div>
        </header>
        <div class="flex-1 min-h-0">
          <CodeEditor v-model="editorStore.code" :language="editorStore.language" />
        </div>
        <footer class="flex gap-3 px-5 py-4 border-t border-(--border) shrink-0 max-md:flex-col">
          <button
            :disabled="isLoading || !editorStore.code.trim()"
            class="btn btn-primary min-w-35 py-3 px-6 max-md:w-full"
            @click="submitCode"
          >
            <svg
              v-if="isLoading"
              class="spin w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <path d="M21 12a9 9 0 1 1-6.219-8.56"></path>
            </svg>
            <svg
              v-else
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <line x1="22" y1="2" x2="11" y2="13"></line>
              <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
            </svg>
            {{ isLoading ? '评价中...' : '提交评价' }}
          </button>
          <button
            :disabled="isLoading"
            class="btn btn-secondary min-w-35 py-3 px-6 max-md:w-full"
            @click="showAnswer"
          >
            <svg
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <circle cx="12" cy="12" r="10"></circle>
              <path d="M9.09 9a3 3 0 0 1 5.83 1c0 2-3 3-3 3"></path>
              <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>
            看答案
          </button>
        </footer>
      </section>
    </div>

    <!-- Bottom row: Result -->
    <section
      class="flex flex-col bg-(--bg-card) border border-(--border) rounded-xl overflow-hidden mt-5"
    >
      <header
        class="flex items-center justify-between px-5 py-4 border-b border-(--border) shrink-0"
      >
        <h2 class="text-base font-semibold m-0">评价结果</h2>
      </header>
      <div class="flex-1 p-5 overflow-y-auto flex flex-col">
        <!-- Evaluation result -->
        <div v-if="evaluationResult" class="flex-1">
          <div class="mb-4">
            <span
              :class="[
                'inline-flex items-center gap-1.5 px-3 py-1.5 text-[13px] font-medium rounded-full',
                evaluationResult.status === 'perfect'
                  ? 'bg-(--success-soft) text-(--success)'
                  : 'bg-(--warning-soft) text-(--warning)',
              ]"
            >
              <svg
                v-if="evaluationResult.status === 'perfect'"
                class="w-4 h-4"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22 4 12 14.01 9 11.01"></polyline>
              </svg>
              <svg
                v-else
                class="w-4 h-4"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <path
                  d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"
                ></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
              </svg>
              {{ evaluationResult.status === 'perfect' ? '代码完美' : '需要改进' }}
            </span>
          </div>
          <MarkdownViewer :content="evaluationResult.evaluation" />

          <!-- Better hint button -->
          <button
            v-if="canShowBetterHint"
            :disabled="isLoading"
            class="btn mt-4 bg-(--warning-soft) text-(--warning) border border-amber-500/20 hover:bg-amber-500/20"
            @click="getBetterHint"
          >
            <svg
              class="w-4 h-4"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <circle cx="12" cy="12" r="10"></circle>
              <line x1="12" y1="16" x2="12" y2="12"></line>
              <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>
            提示更好解法
          </button>

          <!-- Better hint result -->
          <Transition name="fade-slide">
            <div
              v-if="showBetterHint && betterSolutionHint"
              class="mt-4 p-4 bg-(--warning-soft) border border-amber-500/20 rounded-[10px]"
            >
              <div class="flex items-center gap-2 text-sm font-semibold text-(--warning) mb-3">
                <svg
                  class="w-4 h-4"
                  viewBox="0 0 24 24"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="2"
                >
                  <path d="M9 18l6-6-6-6"></path>
                </svg>
                <span>更好的解法</span>
              </div>
              <MarkdownViewer :content="betterSolutionHint" />
            </div>
          </Transition>
        </div>

        <!-- Optimal solution -->
        <div v-else-if="showOptimalSolution && optimalSolution" class="flex-1">
          <div class="mb-4">
            <span
              class="inline-flex items-center gap-1.5 px-3 py-1.5 text-[13px] font-medium rounded-full bg-(--accent-soft) text-(--accent)"
            >
              <svg
                class="w-4 h-4"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2"
              >
                <polygon
                  points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"
                ></polygon>
              </svg>
              最优解法
            </span>
          </div>

          <div class="grid grid-cols-2 gap-6 mt-4 max-lg:grid-cols-1">
            <div class="bg-(--bg-surface) rounded-[10px] overflow-hidden border border-(--border)">
              <div
                class="flex items-center justify-between px-4 py-2.5 bg-(--bg-elevated) border-b border-(--border) text-xs font-medium text-(--text-muted)"
              >
                <span>代码</span>
                <button
                  class="w-7 h-7 flex items-center justify-center bg-transparent border-none rounded-md text-(--text-muted) cursor-pointer hover:bg-(--bg-card) hover:text-(--text-primary)"
                  @click="copyToClipboard(optimalSolution.code)"
                >
                  <svg
                    class="w-3.5 h-3.5"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    stroke-width="2"
                  >
                    <rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect>
                    <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path>
                  </svg>
                </button>
              </div>
              <pre
                class="m-0 p-4 font-mono text-[13px] leading-relaxed overflow-x-auto text-(--text-primary) max-h-100"
              ><code>{{ optimalSolution.code }}</code></pre>
            </div>

            <div>
              <h4 class="text-sm font-semibold m-0 mb-3">解释</h4>
              <MarkdownViewer :content="optimalSolution.explanation" />
            </div>
          </div>
        </div>

        <!-- Empty state -->
        <div
          v-else
          class="flex-1 flex flex-col items-center justify-center text-center text-(--text-muted) p-10"
        >
          <div
            class="w-16 h-16 flex items-center justify-center bg-(--bg-surface) border border-(--border) rounded-2xl mb-4"
          >
            <svg
              class="w-7 h-7"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
            >
              <path
                d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
              ></path>
            </svg>
          </div>
          <p class="text-sm leading-relaxed m-0">提交代码后，评价结果将显示在这里</p>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }

  to {
    transform: rotate(360deg);
  }
}

/* Transitions */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.3s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

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

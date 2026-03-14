<script setup lang="ts">
import { useModelConfigStore } from '../stores/modelConfig'
import { PROVIDER_OPTIONS, type ModelProvider } from '../types'

const emit = defineEmits<{
  close: []
}>()

const store = useModelConfigStore()

function handleProviderChange(event: Event) {
  const target = event.target as HTMLSelectElement
  store.setProvider(target.value as ModelProvider)
}
</script>

<template>
  <div class="h-full flex flex-col">
    <!-- Header -->
    <div class="flex items-start justify-between p-6 border-b border-(--border)">
      <div>
        <h2 class="text-lg font-semibold text-(--text-primary) m-0 mb-1">模型配置</h2>
        <p class="text-[13px] text-(--text-muted) m-0">配置你的 AI 评价模型</p>
      </div>
      <button
        class="w-8 h-8 flex items-center justify-center bg-transparent border-none rounded-lg text-(--text-muted) cursor-pointer hover:bg-(--bg-elevated) hover:text-(--text-primary)"
        aria-label="关闭"
        @click="emit('close')"
      >
        <svg
          class="w-4.5 h-4.5"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <path d="M18 6L6 18M6 6l12 12"></path>
        </svg>
      </button>
    </div>

    <!-- Form -->
    <div class="flex-1 overflow-y-auto p-6">
      <!-- Provider -->
      <div class="mb-5">
        <label class="block text-[13px] font-medium text-(--text-secondary) mb-2">供应商</label>
        <select v-model="store.config.provider" class="input" @change="handleProviderChange">
          <option
            v-for="provider in PROVIDER_OPTIONS"
            :key="provider.value"
            :value="provider.value"
          >
            {{ provider.label }}
          </option>
        </select>
      </div>

      <!-- Model -->
      <div class="mb-5">
        <label class="block text-[13px] font-medium text-(--text-secondary) mb-2">模型名称</label>
        <input
          v-model="store.config.model"
          type="text"
          class="input"
          placeholder="gpt-4o, claude-sonnet-4-5..."
        />
      </div>

      <!-- API Key -->
      <div v-if="store.config.provider !== 'ollama'" class="mb-5">
        <label class="block text-[13px] font-medium text-(--text-secondary) mb-2">API Key</label>
        <input
          v-model="store.config.apiKey"
          type="password"
          class="input font-mono"
          placeholder="sk-..."
        />
      </div>

      <!-- Base URL -->
      <div class="mb-5">
        <label class="block text-[13px] font-medium text-(--text-secondary) mb-2">Base URL</label>
        <input
          v-model="store.config.baseUrl"
          type="text"
          class="input font-mono"
          placeholder="可选，自定义 API 端点"
        />
      </div>

      <!-- Status -->
      <div class="mt-8 pt-6 border-t border-(--border)">
        <div
          v-if="store.isConfigured()"
          class="flex items-center gap-2.5 px-4 py-3 rounded-[10px] text-sm font-medium bg-(--success-soft) text-(--success)"
        >
          <svg
            class="w-5 h-5"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
            <polyline points="22 4 12 14.01 9 11.01"></polyline>
          </svg>
          <span>模型已配置</span>
        </div>
        <div
          v-else
          class="flex items-center gap-2.5 px-4 py-3 rounded-[10px] text-sm font-medium bg-(--warning-soft) text-(--warning)"
        >
          <svg
            class="w-5 h-5"
            viewBox="0 0 24 24"
            fill="none"
            stroke="currentColor"
            stroke-width="2"
          >
            <circle cx="12" cy="12" r="10"></circle>
            <line x1="12" y1="8" x2="12" y2="12"></line>
            <line x1="12" y1="16" x2="12.01" y2="16"></line>
          </svg>
          <span>请配置 API Key</span>
        </div>
      </div>
    </div>

    <!-- Footer -->
    <div class="p-4 px-6 border-t border-(--border)">
      <p class="flex items-center gap-2 text-xs text-(--text-muted) m-0">
        <svg
          class="w-3.5 h-3.5"
          viewBox="0 0 24 24"
          fill="none"
          stroke="currentColor"
          stroke-width="2"
        >
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path>
        </svg>
        配置将安全存储在本地
      </p>
    </div>
  </div>
</template>

<style scoped>
/* 无额外样式 */
</style>

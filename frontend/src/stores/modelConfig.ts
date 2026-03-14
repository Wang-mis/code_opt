import { defineStore } from 'pinia'
import { ref, watch } from 'vue'
import type { ModelConfig, ModelProvider } from '../types'

const STORAGE_KEY = 'model_config'

const defaultConfig: ModelConfig = {
  provider: 'openai',
  model: 'gpt-4o',
  apiKey: '',
  baseUrl: '',
}

export const useModelConfigStore = defineStore('modelConfig', () => {
  // Load from localStorage
  const loadConfig = (): ModelConfig => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored) {
        return JSON.parse(stored)
      }
    } catch (e) {
      console.error('Failed to load model config:', e)
    }
    return { ...defaultConfig }
  }

  const config = ref<ModelConfig>(loadConfig())

  // Watch for changes and save to localStorage
  watch(
    config,
    newConfig => {
      try {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(newConfig))
      } catch (e) {
        console.error('Failed to save model config:', e)
      }
    },
    { deep: true }
  )

  function setConfig(newConfig: Partial<ModelConfig>) {
    config.value = { ...config.value, ...newConfig }
  }

  function setProvider(provider: ModelProvider) {
    config.value.provider = provider
    // Set default model for provider
    switch (provider) {
      case 'openai':
        config.value.model = 'gpt-4o'
        break
      case 'anthropic':
        config.value.model = 'claude-sonnet-4-5-20250929'
        break
      case 'deepseek':
        config.value.model = 'deepseek-chat'
        break
      case 'ollama':
        config.value.model = 'llama3.2'
        config.value.baseUrl = 'http://localhost:11434'
        break
      case 'google_vertexai':
        config.value.model = 'gemini-2.0-flash'
        break
      case 'mistralai':
        config.value.model = 'mistral-large-latest'
        break
      default:
        break
    }
  }

  function isConfigured(): boolean {
    return !!config.value.apiKey || config.value.provider === 'ollama'
  }

  return {
    config,
    setConfig,
    setProvider,
    isConfigured,
  }
})

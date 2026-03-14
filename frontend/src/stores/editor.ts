import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { ProgrammingLanguage } from '../types'

export const useEditorStore = defineStore('editor', () => {
  const language = ref<ProgrammingLanguage>('python')
  const code = ref('')
  const isSubmitting = ref(false)
  const currentSessionId = ref<string | null>(null)

  function setLanguage(lang: ProgrammingLanguage) {
    language.value = lang
  }

  function setCode(newCode: string) {
    code.value = newCode
  }

  function setSubmitting(value: boolean) {
    isSubmitting.value = value
  }

  function setSessionId(sessionId: string | null) {
    currentSessionId.value = sessionId
  }

  function generateSessionId(): string {
    const id = crypto.randomUUID()
    currentSessionId.value = id
    return id
  }

  function reset() {
    code.value = ''
    currentSessionId.value = null
  }

  return {
    language,
    code,
    isSubmitting,
    currentSessionId,
    setLanguage,
    setCode,
    setSubmitting,
    setSessionId,
    generateSessionId,
    reset,
  }
})

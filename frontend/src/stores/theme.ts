import { defineStore } from 'pinia'
import { ref, watch } from 'vue'

const STORAGE_KEY = 'theme_mode'

export type ThemeMode = 'light' | 'dark'

export const useThemeStore = defineStore('theme', () => {
  // Default to light mode
  const loadTheme = (): ThemeMode => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY)
      if (stored === 'light' || stored === 'dark') {
        return stored
      }
    } catch (e) {
      console.error('Failed to load theme:', e)
    }
    return 'light' // Default to light
  }

  const mode = ref<ThemeMode>(loadTheme())

  // Apply theme to document
  function applyTheme(theme: ThemeMode) {
    if (theme === 'dark') {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }

  // Watch for changes
  watch(
    mode,
    newMode => {
      localStorage.setItem(STORAGE_KEY, newMode)
      applyTheme(newMode)
    },
    { immediate: true }
  )

  function toggle() {
    mode.value = mode.value === 'light' ? 'dark' : 'light'
  }

  function setTheme(theme: ThemeMode) {
    mode.value = theme
  }

  return {
    mode,
    toggle,
    setTheme,
  }
})

<script setup lang="ts">
import { ref, onMounted, watch, shallowRef } from 'vue'
import { EditorState } from '@codemirror/state'
import {
  EditorView,
  keymap,
  lineNumbers,
  highlightActiveLineGutter,
  highlightSpecialChars,
  drawSelection,
  dropCursor,
  rectangularSelection,
  crosshairCursor,
  highlightActiveLine,
} from '@codemirror/view'
import { defaultKeymap, history, historyKeymap, indentWithTab } from '@codemirror/commands'
import {
  syntaxHighlighting,
  indentOnInput,
  bracketMatching,
  foldGutter,
  foldKeymap,
  defaultHighlightStyle,
} from '@codemirror/language'
import { javascript } from '@codemirror/lang-javascript'
import { python } from '@codemirror/lang-python'
import { java } from '@codemirror/lang-java'
import { cpp } from '@codemirror/lang-cpp'
import type { ProgrammingLanguage } from '../types'

const props = defineProps<{
  modelValue: string
  language: ProgrammingLanguage
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const editorContainer = ref<HTMLElement>()
const editorView = shallowRef<EditorView>()

// Custom dark theme
const darkTheme = EditorView.theme(
  {
    '&': {
      backgroundColor: 'var(--bg-surface)',
      color: 'var(--text-primary)',
      height: '100%',
    },
    '.cm-content': {
      caretColor: 'var(--accent)',
      fontFamily: "'JetBrains Mono', monospace",
      fontSize: '14px',
      lineHeight: '1.6',
    },
    '.cm-cursor': {
      borderLeftColor: 'var(--accent)',
    },
    '&.cm-focused .cm-selectionBackground, .cm-selectionBackground': {
      backgroundColor: 'var(--accent-soft)',
    },
    '.cm-activeLine': {
      backgroundColor: 'rgba(255, 255, 255, 0.03)',
    },
    '.cm-gutters': {
      backgroundColor: 'transparent',
      color: 'var(--text-muted)',
      border: 'none',
    },
    '.cm-activeLineGutter': {
      backgroundColor: 'var(--accent-soft)',
      color: 'var(--accent)',
    },
    '.cm-foldPlaceholder': {
      backgroundColor: 'var(--bg-elevated)',
      color: 'var(--text-muted)',
      border: '1px solid var(--border)',
    },
    '.cm-scroller': {
      overflow: 'auto',
    },
  },
  { dark: true }
)

function getLanguageExtension(lang: ProgrammingLanguage) {
  switch (lang) {
    case 'javascript':
    case 'typescript':
      return javascript({ typescript: lang === 'typescript' })
    case 'python':
      return python()
    case 'java':
      return java()
    case 'cpp':
    case 'c':
      return cpp()
    default:
      return []
  }
}

function createEditor() {
  if (!editorContainer.value) return

  if (editorView.value) {
    editorView.value.destroy()
  }

  const extensions = [
    lineNumbers(),
    highlightActiveLineGutter(),
    highlightSpecialChars(),
    history(),
    foldGutter(),
    drawSelection(),
    dropCursor(),
    EditorState.allowMultipleSelections.of(true),
    indentOnInput(),
    syntaxHighlighting(defaultHighlightStyle, { fallback: true }),
    bracketMatching(),
    rectangularSelection(),
    crosshairCursor(),
    highlightActiveLine(),
    keymap.of([...defaultKeymap, ...historyKeymap, ...foldKeymap, indentWithTab]),
    getLanguageExtension(props.language),
    darkTheme,
    EditorView.updateListener.of(update => {
      if (update.docChanged) {
        emit('update:modelValue', update.state.doc.toString())
      }
    }),
    EditorView.theme({
      '&': { height: '100%' },
      '.cm-scroller': { overflow: 'auto' },
    }),
  ]

  const state = EditorState.create({
    doc: props.modelValue,
    extensions,
  })

  editorView.value = new EditorView({
    state,
    parent: editorContainer.value,
  })
}

onMounted(() => {
  createEditor()
})

watch(
  () => props.language,
  () => {
    createEditor()
  }
)

watch(
  () => props.modelValue,
  newValue => {
    if (editorView.value && editorView.value.state.doc.toString() !== newValue) {
      editorView.value.dispatch({
        changes: {
          from: 0,
          to: editorView.value.state.doc.length,
          insert: newValue,
        },
      })
    }
  }
)
</script>

<template>
  <div
    ref="editorContainer"
    class="h-full overflow-hidden rounded-lg bg-(--bg-surface) [&_.cm-editor]:h-full [&_.cm-scroller]:overflow-auto"
  ></div>
</template>

<style scoped>
/* CodeMirror 需要特殊处理，保留最小必要样式 */
</style>

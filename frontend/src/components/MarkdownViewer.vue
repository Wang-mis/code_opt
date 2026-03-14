<script setup lang="ts">
import { computed } from 'vue'
import MarkdownIt from 'markdown-it'

const props = defineProps<{
  content: string
}>()

const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
})

const renderedContent = computed(() => {
  return md.render(props.content || '')
})
</script>

<template>
  <div class="markdown-body" v-html="renderedContent"></div>
</template>

<style>
.markdown-body {
  color: var(--text-secondary);
  line-height: 1.7;
  font-size: 14px;
}

.markdown-body > *:first-child {
  margin-top: 0;
}

.markdown-body > *:last-child {
  margin-bottom: 0;
}

.markdown-body h1,
.markdown-body h2,
.markdown-body h3,
.markdown-body h4 {
  color: var(--text-primary);
  margin-top: 1.5em;
  margin-bottom: 0.5em;
  font-weight: 600;
}

.markdown-body h1 {
  font-size: 1.4em;
}

.markdown-body h2 {
  font-size: 1.2em;
}

.markdown-body h3 {
  font-size: 1.1em;
}

.markdown-body h4 {
  font-size: 1em;
}

.markdown-body p {
  margin-bottom: 1em;
}

.markdown-body ul,
.markdown-body ol {
  padding-left: 1.5em;
  margin-bottom: 1em;
}

.markdown-body li {
  margin-bottom: 0.25em;
}

.markdown-body li > ul,
.markdown-body li > ol {
  margin-bottom: 0;
}

.markdown-body code {
  font-family: 'JetBrains Mono', monospace;
  background: var(--bg-surface);
  color: var(--accent);
  padding: 2px 6px;
  border-radius: 4px;
  font-size: 0.9em;
}

.markdown-body pre {
  background: var(--bg-surface);
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  margin-bottom: 1em;
}

.markdown-body pre code {
  background: transparent;
  padding: 0;
  color: var(--text-primary);
}

.markdown-body blockquote {
  border-left: 3px solid var(--accent);
  padding-left: 1em;
  margin: 1em 0;
  color: var(--text-muted);
  font-style: italic;
}

.markdown-body a {
  color: var(--accent);
  text-decoration: none;
  transition: opacity 0.2s ease;
}

.markdown-body a:hover {
  opacity: 0.8;
  text-decoration: underline;
}

.markdown-body table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 1em;
}

.markdown-body th,
.markdown-body td {
  padding: 10px 12px;
  border: 1px solid var(--border);
  text-align: left;
}

.markdown-body th {
  background: var(--bg-surface);
  font-weight: 600;
}

.markdown-body hr {
  border: none;
  border-top: 1px solid var(--border);
  margin: 1.5em 0;
}

.markdown-body img {
  max-width: 100%;
  border-radius: 8px;
}

.markdown-body strong {
  color: var(--text-primary);
  font-weight: 600;
}

.markdown-body em {
  font-style: italic;
}
</style>

# 算法代码优化助手 - 前端

一个现代化的算法代码优化练习平台前端应用，帮助用户通过 AI 评价迭代改进代码质量。

## 技术栈

- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全
- **Tailwind CSS v4** - 原子化 CSS 框架
- **Pinia** - 状态管理
- **Vue Router** - 路由管理
- **CodeMirror 6** - 代码编辑器
- **vue-markdown-it** - Markdown 渲染

## 项目结构

```
src/
├── api/                    # API 请求封装
│   └── index.ts
├── components/             # 可复用组件
│   ├── CodeEditor.vue      # CodeMirror 代码编辑器
│   ├── MarkdownViewer.vue  # Markdown 渲染组件
│   ├── ModelConfig.vue     # 模型配置侧边栏
│   └── WorkspacePanel.vue  # 工作区面板（题目+编辑器+结果）
├── stores/                 # Pinia 状态管理
│   ├── editor.ts           # 编辑器状态（代码、语言）
│   └── modelConfig.ts      # 模型配置状态
├── types/                  # TypeScript 类型定义
│   └── index.ts
├── views/                  # 页面视图
│   ├── HomeView.vue        # 主页（题目选择/创建）
│   ├── HistoryView.vue     # 历史记录页面
│   └── ReviewView.vue      # 复习页面
├── App.vue                 # 根组件
├── main.ts                 # 应用入口
└── style.css               # 全局样式和 CSS 变量
```

## 功能特性

### 1. 主页 (HomeView)
- 题目列表选择
- 创建新题目（支持 Markdown）
- 流畅的过渡动画

### 2. 工作区 (WorkspacePanel)
- 左侧：题目描述（Markdown 渲染）
- 中间：代码编辑器（支持多语言语法高亮）
- 右侧：评价结果展示
- 可调节面板宽度
- 提交评价 / 看答案 / 提示更好解法

### 3. 历史记录 (HistoryView)
- 按学习会话分组展示
- 展开查看每次提交详情
- 代码片段预览

### 4. 复习页面 (ReviewView)
- 随机抽取题目
- 换一题功能

### 5. 模型配置 (ModelConfig)
- 支持 OpenAI / Anthropic / DeepSeek / Ollama 等供应商
- API Key 安全存储在 localStorage
- 自定义 Base URL

## 开发命令

```bash
# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build

# 预览生产版本
npm run preview
```

## 主题定制

应用使用 CSS 自定义属性实现主题系统，所有变量定义在 `style.css` 中：

```css
:root {
  --bg-deep: #0a0a0f;
  --bg-card: #12121a;
  --bg-surface: #1a1a24;
  --accent: #6366f1;
  --text-primary: #f0f0f5;
  /* ... 更多变量 */
}
```

修改这些变量即可自定义主题颜色。

## Tailwind CSS v4 语法说明

本项目使用 Tailwind CSS v4，CSS 变量引用采用新语法：

```html
<!-- 旧语法（不推荐） -->
<!-- <div class="text-[var(--text-primary)] bg-[var(--bg-card)]"> -->

<!-- 新语法（推荐） -->
<div class="text-(--text-primary) bg-(--bg-card)">
```

## API 接口

前端通过 `/api` 模块与后端通信，主要接口：

- `problemsApi.getAll()` - 获取所有题目
- `problemsApi.create(data)` - 创建题目
- `evaluateApi.submit(data)` - 提交代码评价
- `evaluateApi.getOptimalSolution(data)` - 获取最优答案
- `evaluateApi.getBetterSolutionHint(data)` - 获取更好解法提示
- `submissionsApi.getAll()` - 获取提交历史
- `reviewApi.getRandomProblem()` - 获取随机复习题目

## 响应式设计

应用支持桌面端和移动端：

- 桌面端：三栏布局，可调节面板宽度
- 移动端：垂直堆叠布局，自适应宽度

断点使用 Tailwind CSS 的 `max-md:` 和 `max-lg:` 前缀。

## 浏览器支持

- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+
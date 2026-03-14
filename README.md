# 算法代码优化助手

一个基于 AI 的算法代码优化练习平台，帮助用户通过智能评价和迭代改进代码质量。

## 项目简介

算法代码优化助手是一个全栈 Web 应用，旨在帮助用户提升算法编程能力。用户可以：

- 创建和管理算法题目
- 编写代码并获得 AI 智能评价
- 查看最优解法，学习更好的实现思路
- 追踪学习历史，回顾进步过程
- 随机抽取题目进行复习

## 技术栈

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **TypeScript** - 类型安全
- **Tailwind CSS v4** - 原子化 CSS 框架
- **Pinia** - 状态管理
- **CodeMirror 6** - 代码编辑器

### 后端
- **FastAPI** - 高性能 Python Web 框架
- **SQLAlchemy** - 异步 ORM
- **LangChain** - LLM 集成框架
- **SQLite** - 轻量级数据库

### 支持的 LLM 供应商
- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- DeepSeek
- Ollama (本地模型)
- 其他兼容 OpenAI API 的服务

## 快速开始

### 环境要求
- Python 3.12+
- Node.js 18+

### 安装与运行

#### 1. 启动后端

```bash
cd backend

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -e .

# 启动开发服务器
uvicorn app.main:app --reload --port 8000
```

#### 2. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

#### 3. 访问应用

打开浏览器访问 http://localhost:5173

## 功能特性

### 📝 题目管理
- 创建自定义算法题目（支持 Markdown 格式）
- 题目列表展示与选择
- 题目描述实时渲染

### 💻 代码编辑
- 多语言支持（Python、JavaScript、TypeScript、Java、C/C++）
- 语法高亮
- 代码自动缩进
- 行号显示

### 🤖 AI 智能评价
- 代码质量评估
- 时间/空间复杂度分析
- 潜在问题指出
- 优化建议提供
- 最优解法展示
- 更好解法提示

### 📚 学习历史
- 按学习会话分组
- 提交记录追踪
- 代码迭代对比

### 🔄 复习模式
- 随机抽取题目
- 巩固学习成果

### ⚙️ 模型配置
- 支持多种 LLM 供应商
- 自定义 API Key
- 自定义 Base URL（兼容各服务商）

## 项目结构

```
code_opt/
├── backend/                 # 后端代码
│   ├── app/
│   │   ├── main.py         # FastAPI 应用入口
│   │   ├── database.py     # 数据库配置
│   │   ├── models.py       # SQLAlchemy 模型
│   │   ├── schemas.py      # Pydantic 模式
│   │   ├── routers/        # API 路由
│   │   └── services/       # 业务逻辑
│   └── pyproject.toml      # Python 依赖配置
│
├── frontend/                # 前端代码
│   ├── src/
│   │   ├── api/            # API 请求封装
│   │   ├── components/     # Vue 组件
│   │   ├── views/          # 页面视图
│   │   ├── stores/         # Pinia 状态管理
│   │   └── types/          # TypeScript 类型
│   └── package.json        # Node.js 依赖配置
│
└── scripts/                 # 辅助脚本
```

## 配置说明

### LLM 配置

在应用的模型配置面板中设置：

1. **供应商**：选择 LLM 服务商
2. **模型**：选择要使用的模型
3. **API Key**：输入你的 API 密钥
4. **Base URL**：可选，用于自定义 API 端点

#### 常见配置示例

| 供应商 | Base URL |
|--------|----------|
| OpenAI | https://api.openai.com/v1 |
| Anthropic | https://api.anthropic.com |
| DeepSeek | https://api.deepseek.com/v1 |
| Ollama | http://localhost:11434/v1 |

## 开发指南

### 前端开发

```bash
cd frontend

# 开发模式
npm run dev

# 构建生产版本
npm run build

# 代码检查
npm run lint

# 代码格式化
npm run format
```

### 后端开发

```bash
cd backend

# 启动开发服务器（热重载）
uvicorn app.main:app --reload --port 8000

# 数据库文件
# SQLite 数据库位于 backend/code_opt.db
```

## 许可证

MIT License
# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

算法代码优化助手 (Algorithm Code Optimization Assistant) - A web application that helps users improve their algorithm code through AI-powered evaluation and iterative refinement.

**Architecture:** Monorepo with Vue 3 frontend and FastAPI backend.

## Development Commands

### Backend (Python 3.12+)
```bash
cd backend

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -e .

# Run development server
uvicorn app.main:app --reload --port 8000
```

### Frontend (Node.js)
```bash
cd frontend

# Install dependencies
npm install

# Run development server (proxies API to backend:8000)
npm run dev

# Build for production
npm run build

# Lint and format
npm run lint
npm run lint:fix
npm run format
```

## Architecture

### Backend (`backend/app/`)
- **FastAPI** with async SQLAlchemy (aiosqlite)
- **LangChain** for LLM integration (supports OpenAI, Anthropic, DeepSeek, Ollama, etc.)
- Database: SQLite (`code_opt.db`)
- Key files:
  - `main.py` - FastAPI app with CORS, lifespan
  - `database.py` - Async session factory
  - `models.py` - SQLAlchemy models (Problem, Submission, LearningSession)
  - `schemas.py` - Pydantic request/response schemas
  - `services/llm_service.py` - LLM evaluation logic
  - `routers/` - API endpoints (problems, submissions, evaluate, review)

### Frontend (`frontend/src/`)
- **Vue 3** with Composition API (`<script setup>`)
- **Tailwind CSS v4** - Use new syntax: `text-(--var)` instead of `text-[var(--var)]`
- **Pinia** for state management
- **CodeMirror 6** for code editing
- Key directories:
  - `api/` - Axios wrapper with camelCase↔snake_case transformation
  - `components/` - Reusable Vue components
  - `views/` - Page-level components
  - `stores/` - Pinia stores

### API Communication
- Frontend uses camelCase, backend uses snake_case
- `frontend/src/api/index.ts` handles transformation
- Special case: `modelConfig` → `llm_config`
- Vite dev server proxies `/api` to `localhost:8000`

### Database Models
- **Problem**: Algorithm problem with title, description (Markdown)
- **Submission**: Code submission with evaluation result, linked to Problem and LearningSession
- **LearningSession**: Groups multiple submissions for a problem, tracks progress

## Important Patterns

### SQLAlchemy Async
Always use `selectinload()` for relationship access to avoid lazy loading errors:
```python
stmt = select(Submission).options(selectinload(Submission.problem))
```

### LLM Response Handling
LLM responses may be a string or list of content blocks. Always check type:
```python
content = response.content
if isinstance(content, list):
    text = "\n".join(block.get("text", "") for block in content if isinstance(block, dict))
```
import axios from 'axios'
import type {
  Problem,
  ProblemCreate,
  Submission,
  EvaluationResult,
  BetterSolutionHint,
  OptimalSolution,
  LearningSession,
  ModelConfig,
} from '../types'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Convert camelCase to snake_case for API requests
function toSnakeCase(str: string): string {
  return str.replace(/[A-Z]/g, letter => `_${letter.toLowerCase()}`)
}

// Convert snake_case to camelCase for API responses
function toCamelCase(str: string): string {
  return str.replace(/_([a-z])/g, (_, letter) => letter.toUpperCase())
}

function transformToSnakeCase(obj: Record<string, unknown>): Record<string, unknown> {
  const result: Record<string, unknown> = {}
  for (const [key, value] of Object.entries(obj)) {
    // Special case: modelConfig -> llm_config
    let snakeKey = key === 'modelConfig' ? 'llm_config' : toSnakeCase(key)
    if (value && typeof value === 'object' && !Array.isArray(value)) {
      result[snakeKey] = transformToSnakeCase(value as Record<string, unknown>)
    } else {
      result[snakeKey] = value
    }
  }
  return result
}

function transformToCamelCase<T>(obj: unknown): T {
  if (Array.isArray(obj)) {
    return obj.map(item => transformToCamelCase(item)) as T
  }
  if (obj && typeof obj === 'object') {
    const result: Record<string, unknown> = {}
    for (const [key, value] of Object.entries(obj as Record<string, unknown>)) {
      const camelKey = toCamelCase(key)
      result[camelKey] = transformToCamelCase(value)
    }
    return result as T
  }
  return obj as T
}

// Problems API
export const problemsApi = {
  getAll: () => api.get<Problem[]>('/problems'),

  get: (id: number) => api.get<Problem>(`/problems/${id}`),

  create: (data: ProblemCreate) => api.post<Problem>('/problems', data),

  update: (id: number, data: ProblemCreate) => api.put<Problem>(`/problems/${id}`, data),

  delete: (id: number) => api.delete(`/problems/${id}`),
}

// Submissions API
export const submissionsApi = {
  getAll: async () => {
    const response = await api.get<Submission[]>('/submissions')
    return { ...response, data: transformToCamelCase<Submission[]>(response.data) }
  },

  get: (id: number) => api.get<Submission>(`/submissions/${id}`),

  getSession: (sessionId: string) => api.get<LearningSession>(`/sessions/${sessionId}`),
}

// Evaluate API
export const evaluateApi = {
  submit: (data: {
    problemId: number
    code: string
    sessionId?: string
    modelConfig: ModelConfig
  }) => api.post<EvaluationResult>('/evaluate', transformToSnakeCase(data as Record<string, unknown>)),

  getBetterSolutionHint: (data: { problemId: number; code: string; modelConfig: ModelConfig }) =>
    api.post<BetterSolutionHint>('/evaluate/better-solution', transformToSnakeCase(data as Record<string, unknown>)),

  getOptimalSolution: (data: { problemId: number; modelConfig: ModelConfig }) =>
    api.post<OptimalSolution>('/evaluate/answer', transformToSnakeCase(data as Record<string, unknown>)),
}

// Review API
export const reviewApi = {
  getRandomProblem: (excludeId?: number) =>
    api.get<Problem>('/review/random', { params: excludeId ? { exclude_id: excludeId } : {} }),
}

export default api

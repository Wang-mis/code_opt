// Model configuration
export interface ModelConfig {
  provider: string
  model: string
  apiKey: string
  baseUrl?: string
}

// Problem
export interface Problem {
  id: number
  title: string
  description: string
  createdAt: string
  updatedAt: string
}

export interface ProblemCreate {
  title: string
  description: string
}

// Submission
export interface Submission {
  id: number
  problemId: number
  code: string
  evaluation: string
  status: 'pending' | 'perfect' | 'has_issues'
  iteration: number
  sessionId: string
  createdAt: string
  problem?: Problem
}

export interface SubmissionCreate {
  problemId: number
  code: string
  sessionId?: string
  modelConfig: ModelConfig
}

// Learning Session
export interface LearningSession {
  id: string
  problemId: number
  problem?: Problem
  startedAt: string
  completedAt?: string
  finalStatus?: 'completed' | 'viewed_answer'
  submissions?: Submission[]
}

// Evaluation result
export interface EvaluationResult {
  evaluation: string
  status: 'pending' | 'perfect' | 'has_issues'
  submissionId: number
}

// Better solution hint
export interface BetterSolutionHint {
  hint: string
}

// Optimal solution
export interface OptimalSolution {
  code: string
  explanation: string
}

// API Response
export interface ApiResponse<T> {
  data?: T
  error?: string
}

// Programming languages for code editor
export type ProgrammingLanguage =
  | 'javascript'
  | 'typescript'
  | 'python'
  | 'java'
  | 'cpp'
  | 'c'
  | 'go'
  | 'rust'

export const LANGUAGE_OPTIONS: { value: ProgrammingLanguage; label: string }[] = [
  { value: 'javascript', label: 'JavaScript' },
  { value: 'typescript', label: 'TypeScript' },
  { value: 'python', label: 'Python' },
  { value: 'java', label: 'Java' },
  { value: 'cpp', label: 'C++' },
  { value: 'c', label: 'C' },
  { value: 'go', label: 'Go' },
  { value: 'rust', label: 'Rust' },
]

// Model providers
export type ModelProvider =
  | 'openai'
  | 'anthropic'
  | 'deepseek'
  | 'ollama'
  | 'google_vertexai'
  | 'mistralai'
  | 'custom'

export const PROVIDER_OPTIONS: { value: ModelProvider; label: string }[] = [
  { value: 'openai', label: 'OpenAI' },
  { value: 'anthropic', label: 'Anthropic' },
  { value: 'deepseek', label: 'DeepSeek' },
  { value: 'ollama', label: 'Ollama (Local)' },
  { value: 'google_vertexai', label: 'Google Vertex AI' },
  { value: 'mistralai', label: 'Mistral AI' },
  { value: 'custom', label: 'Custom' },
]

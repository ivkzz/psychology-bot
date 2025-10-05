/**
 * Task types - типы для заданий и назначений
 */

export enum TaskDifficulty {
  EASY = 'EASY',
  MEDIUM = 'MEDIUM',
  HARD = 'HARD'
}

export enum AssignmentStatus {
  PENDING = 'PENDING',
  COMPLETED = 'COMPLETED'
}

export interface Task {
  id: string
  title: string
  description: string
  category: string
  difficulty: TaskDifficulty
  created_at: string
}

export interface Assignment {
  id: string
  user_id: string
  task_id: string
  assigned_date: string // ISO date (YYYY-MM-DD)
  completed_at: string | null
  status: AssignmentStatus
  answer_text: string | null
  created_at: string
  task: Task
}

export interface TaskCreate {
  title: string
  description: string
  category: string
  difficulty: TaskDifficulty
}

export interface TaskUpdate {
  title?: string
  description?: string
  category?: string
  difficulty?: TaskDifficulty
}

export interface AssignmentComplete {
  answer_text?: string
}

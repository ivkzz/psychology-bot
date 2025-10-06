/**
 * User types - типы для пользователей
 */

export enum UserRole {
  USER = 'user',
  ADMIN = 'admin'
}

export interface User {
  id: string
  name: string
  email: string | null
  telegram_id: number | null
  role: UserRole
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface UserProgress {
  total_tasks: number
  completed_tasks: number
  completion_rate: number // 0-100
  streak_days: number
}

export interface UserUpdate {
  name?: string
  email?: string
  telegram_id?: number
}

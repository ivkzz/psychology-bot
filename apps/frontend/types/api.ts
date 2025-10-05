/**
 * API types - общие типы для API
 */

export interface ApiError {
  detail: string
  status?: number
}

export interface PaginatedParams {
  skip?: number
  limit?: number
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  skip: number
  limit: number
}

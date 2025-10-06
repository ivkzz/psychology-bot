/**
 * Axios HTTP client с interceptors для автоматической обработки токенов
 */

import axios, { AxiosError, InternalAxiosRequestConfig } from 'axios'
import type { ApiError } from '@/types'

// Создаем axios instance
export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 секунд
})

// Request interceptor - добавляем токен к каждому запросу
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // Получаем токен из localStorage
    const token = typeof window !== 'undefined'
      ? localStorage.getItem('accessToken')
      : null

    // Добавляем токен в headers если он есть
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }

    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Флаг для предотвращения множественных refresh запросов
let isRefreshing = false
let failedQueue: Array<{
  resolve: (value?: unknown) => void
  reject: (reason?: unknown) => void
}> = []

const processQueue = (error: AxiosError<ApiError> | null, token: string | null = null) => {
  failedQueue.forEach((prom) => {
    if (error) {
      prom.reject(error)
    } else {
      prom.resolve(token)
    }
  })

  failedQueue = []
}

// Response interceptor - обрабатываем ошибки и автообновление токена
apiClient.interceptors.response.use(
  (response) => {
    // Успешный ответ - возвращаем как есть
    return response
  },
  async (error: AxiosError<ApiError>) => {
    const originalRequest = error.config as InternalAxiosRequestConfig & { _retry?: boolean }

    // Если ошибка 401 и это не запрос на refresh/login и не повторная попытка
    if (
      error.response?.status === 401 &&
      originalRequest &&
      !originalRequest.url?.includes('/auth/login') &&
      !originalRequest.url?.includes('/auth/refresh') &&
      !originalRequest._retry
    ) {
      if (isRefreshing) {
        // Если уже идет refresh, добавляем запрос в очередь
        return new Promise((resolve, reject) => {
          failedQueue.push({ resolve, reject })
        })
          .then((token) => {
            if (originalRequest.headers) {
              originalRequest.headers.Authorization = `Bearer ${token}`
            }
            return apiClient(originalRequest)
          })
          .catch((err) => {
            return Promise.reject(err)
          })
      }

      originalRequest._retry = true
      isRefreshing = true

      const refreshToken = typeof window !== 'undefined'
        ? localStorage.getItem('refreshToken')
        : null

      if (!refreshToken) {
        // Нет refresh token - редирект на login
        if (typeof window !== 'undefined') {
          localStorage.removeItem('accessToken')
          localStorage.removeItem('refreshToken')
          document.cookie = 'accessToken=; path=/; max-age=0'
          document.cookie = 'refreshToken=; path=/; max-age=0'
          window.location.href = '/login'
        }
        return Promise.reject(error)
      }

      try {
        // Запрос на обновление токена
        const response = await axios.post(
          `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/refresh`,
          { refresh_token: refreshToken }
        )

        const { access_token, refresh_token: new_refresh_token } = response.data

        // Сохраняем новые токены в localStorage и cookies
        if (typeof window !== 'undefined') {
          localStorage.setItem('accessToken', access_token)
          localStorage.setItem('refreshToken', new_refresh_token)
          document.cookie = `accessToken=${access_token}; path=/; max-age=${15 * 60}; SameSite=Lax`
          document.cookie = `refreshToken=${new_refresh_token}; path=/; max-age=${7 * 24 * 60 * 60}; SameSite=Lax`
        }

        // Обновляем токен в оригинальном запросе
        if (originalRequest.headers) {
          originalRequest.headers.Authorization = `Bearer ${access_token}`
        }

        // Обрабатываем очередь запросов
        processQueue(null, access_token)

        isRefreshing = false

        // Повторяем оригинальный запрос с новым токеном
        return apiClient(originalRequest)
      } catch (refreshError) {
        // Ошибка при обновлении токена
        processQueue(refreshError as AxiosError<ApiError>, null)
        isRefreshing = false

        // Редирект на login
        if (typeof window !== 'undefined') {
          localStorage.removeItem('accessToken')
          localStorage.removeItem('refreshToken')
          document.cookie = 'accessToken=; path=/; max-age=0'
          document.cookie = 'refreshToken=; path=/; max-age=0'
          window.location.href = '/login'
        }
        return Promise.reject(refreshError)
      }
    }

    // Для других ошибок - возвращаем как есть
    return Promise.reject(error)
  }
)

export default apiClient

/**
 * Auth Store - Zustand store только для auth токенов
 * User data хранится в TanStack Query!
 */

import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface AuthState {
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean

  // Actions
  setTokens: (accessToken: string, refreshToken: string) => void
  clearTokens: () => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      // State
      accessToken: null,
      refreshToken: null,
      isAuthenticated: false,

      // Actions
      setTokens: (accessToken, refreshToken) => {
        set({
          accessToken,
          refreshToken,
          isAuthenticated: true,
        })

        // Сохраняем в localStorage для axios interceptor
        if (typeof window !== 'undefined') {
          localStorage.setItem('accessToken', accessToken)
          localStorage.setItem('refreshToken', refreshToken)

          // Также сохраняем в cookies для middleware (15 мин для access, 7 дней для refresh)
          document.cookie = `accessToken=${accessToken}; path=/; max-age=${15 * 60}; SameSite=Lax`
          document.cookie = `refreshToken=${refreshToken}; path=/; max-age=${7 * 24 * 60 * 60}; SameSite=Lax`
        }
      },

      clearTokens: () => {
        set({
          accessToken: null,
          refreshToken: null,
          isAuthenticated: false,
        })

        // Удаляем из localStorage и cookies
        if (typeof window !== 'undefined') {
          localStorage.removeItem('accessToken')
          localStorage.removeItem('refreshToken')
          document.cookie = 'accessToken=; path=/; max-age=0'
          document.cookie = 'refreshToken=; path=/; max-age=0'
        }
      },

      logout: () => {
        set({
          accessToken: null,
          refreshToken: null,
          isAuthenticated: false,
        })

        // Удаляем из localStorage и cookies
        if (typeof window !== 'undefined') {
          localStorage.removeItem('accessToken')
          localStorage.removeItem('refreshToken')
          document.cookie = 'accessToken=; path=/; max-age=0'
          document.cookie = 'refreshToken=; path=/; max-age=0'
        }
      },
    }),
    {
      name: 'auth-storage', // Ключ в localStorage
      partialize: (state) => ({
        // Сохраняем только токены и isAuthenticated
        accessToken: state.accessToken,
        refreshToken: state.refreshToken,
        isAuthenticated: state.isAuthenticated,
      }),
    }
  )
)

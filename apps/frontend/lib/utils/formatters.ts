/**
 * Formatters - утилиты для форматирования данных
 */

import { format, parseISO } from 'date-fns'
import { ru } from 'date-fns/locale'

/**
 * Форматирование даты в читабельный формат
 */
export function formatDate(date: string | Date): string {
  const dateObj = typeof date === 'string' ? parseISO(date) : date
  return format(dateObj, 'd MMMM yyyy', { locale: ru })
}

/**
 * Форматирование даты и времени
 */
export function formatDateTime(date: string | Date): string {
  const dateObj = typeof date === 'string' ? parseISO(date) : date
  return format(dateObj, 'd MMMM yyyy, HH:mm', { locale: ru })
}

/**
 * Форматирование даты в короткий формат
 */
export function formatDateShort(date: string | Date): string {
  const dateObj = typeof date === 'string' ? parseISO(date) : date
  return format(dateObj, 'dd.MM.yyyy', { locale: ru })
}

/**
 * Форматирование процента выполнения
 */
export function formatProgress(completed: number, total: number): string {
  if (total === 0) return '0%'
  const percentage = Math.round((completed / total) * 100)
  return `${percentage}%`
}

/**
 * Форматирование серии дней
 */
export function formatStreak(days: number): string {
  if (days === 0) return 'Нет серии'
  if (days === 1) return '1 день'
  if (days >= 2 && days <= 4) return `${days} дня`
  return `${days} дней`
}

/**
 * Перевод сложности на русский
 */
export function formatDifficulty(difficulty: string): string {
  const difficultyMap: Record<string, string> = {
    easy: 'Лёгкое',
    medium: 'Среднее',
    hard: 'Сложное',
  }
  return difficultyMap[difficulty] || difficulty
}

/**
 * Перевод статуса на русский
 */
export function formatStatus(status: string): string {
  const statusMap: Record<string, string> = {
    pending: 'Ожидает',
    completed: 'Выполнено',
  }
  return statusMap[status] || status
}

/**
 * Получить цвет для сложности
 */
export function getDifficultyColor(
  difficulty: string
): 'default' | 'secondary' | 'destructive' {
  const colorMap: Record<
    string,
    'default' | 'secondary' | 'destructive'
  > = {
    easy: 'secondary',
    medium: 'default',
    hard: 'destructive',
  }
  return colorMap[difficulty] || 'default'
}

/**
 * Получить цвет для статуса
 */
export function getStatusColor(
  status: string
): 'default' | 'secondary' | 'outline' {
  const colorMap: Record<string, 'default' | 'secondary' | 'outline'> = {
    pending: 'outline',
    completed: 'default',
  }
  return colorMap[status] || 'default'
}

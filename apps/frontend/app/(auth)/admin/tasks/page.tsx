/**
 * Admin Tasks Page - управление шаблонами заданий
 */

'use client'

import { useState, useMemo } from 'react'
import { useTaskTemplates } from '@/lib/hooks/use-admin'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { Skeleton } from '@/components/ui/skeleton'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { TaskTemplateModal } from '@/components/admin/TaskTemplateModal'
import { DeleteTaskDialog } from '@/components/admin/DeleteTaskDialog'
import { FileText, Plus, Edit, Trash2, Filter } from 'lucide-react'
import { formatDate, formatDifficulty, getDifficultyColor } from '@/lib/utils/formatters'
import type { Task, TaskDifficulty } from '@/types'

export default function AdminTasksPage() {
  const [categoryFilter, setCategoryFilter] = useState<string>('all')
  const [difficultyFilter, setDifficultyFilter] = useState<string>('all')

  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false)
  const [editingTask, setEditingTask] = useState<Task | null>(null)
  const [deletingTask, setDeletingTask] = useState<Task | null>(null)

  const { data: templates, isLoading } = useTaskTemplates({ limit: 100 })

  // Получаем уникальные категории
  const categories = useMemo(() => {
    if (!templates) return []
    const uniqueCategories = Array.from(
      new Set(templates.map((t) => t.category))
    )
    return uniqueCategories.sort()
  }, [templates])

  // Фильтрация шаблонов
  const filteredTemplates = useMemo(() => {
    if (!templates) return []

    let filtered = templates

    // Фильтр по категории
    if (categoryFilter !== 'all') {
      filtered = filtered.filter((t) => t.category === categoryFilter)
    }

    // Фильтр по сложности
    if (difficultyFilter !== 'all') {
      filtered = filtered.filter((t) => t.difficulty === difficultyFilter)
    }

    return filtered
  }, [templates, categoryFilter, difficultyFilter])

  if (isLoading) {
    return (
      <div className="space-y-8">
        <Skeleton className="h-10 w-96" />
        <Skeleton className="h-64" />
      </div>
    )
  }

  return (
    <div className="space-y-8">
      {/* Заголовок */}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
            <FileText className="h-8 w-8" />
            Управление шаблонами
          </h1>
          <p className="text-muted-foreground mt-2">
            Создавайте и редактируйте шаблоны заданий для пользователей
          </p>
        </div>
        <Button onClick={() => setIsCreateModalOpen(true)}>
          <Plus className="mr-2 h-4 w-4" />
          Создать шаблон
        </Button>
      </div>

      {/* Фильтры */}
      <Card>
        <CardHeader>
          <div className="flex items-center gap-2">
            <Filter className="h-5 w-5" />
            <CardTitle>Фильтры</CardTitle>
          </div>
        </CardHeader>
        <CardContent>
          <div className="flex flex-col sm:flex-row gap-4">
            {/* Фильтр по категории */}
            <div className="flex-1">
              <Select
                value={categoryFilter}
                onValueChange={setCategoryFilter}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Все категории" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Все категории</SelectItem>
                  {categories.map((category) => (
                    <SelectItem key={category} value={category}>
                      {category}
                    </SelectItem>
                  ))}
                </SelectContent>
              </Select>
            </div>

            {/* Фильтр по сложности */}
            <div className="flex-1">
              <Select
                value={difficultyFilter}
                onValueChange={setDifficultyFilter}
              >
                <SelectTrigger>
                  <SelectValue placeholder="Вся сложность" />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="all">Вся сложность</SelectItem>
                  <SelectItem value="easy">Лёгкое</SelectItem>
                  <SelectItem value="medium">Среднее</SelectItem>
                  <SelectItem value="hard">Сложное</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Счетчик */}
            <div className="flex items-center text-sm text-muted-foreground">
              Найдено: {filteredTemplates.length}
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Список шаблонов */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {filteredTemplates.length > 0 ? (
          filteredTemplates.map((template) => (
            <Card key={template.id} className="flex flex-col">
              <CardHeader>
                <CardTitle className="text-lg line-clamp-2">
                  {template.title}
                </CardTitle>
                <CardDescription className="line-clamp-3">
                  {template.description}
                </CardDescription>
              </CardHeader>
              <CardContent className="flex-1 flex flex-col justify-between">
                <div className="space-y-3 mb-4">
                  {/* Badges */}
                  <div className="flex flex-wrap items-center gap-2">
                    <Badge variant="outline">{template.category}</Badge>
                    <Badge
                      variant={getDifficultyColor(
                        template.difficulty as TaskDifficulty
                      )}
                    >
                      {formatDifficulty(template.difficulty)}
                    </Badge>
                  </div>

                  {/* Дата создания */}
                  <p className="text-xs text-muted-foreground">
                    Создан: {formatDate(template.created_at)}
                  </p>
                </div>

                {/* Действия */}
                <div className="flex gap-2">
                  <Button
                    variant="outline"
                    size="sm"
                    className="flex-1"
                    onClick={() => setEditingTask(template)}
                  >
                    <Edit className="h-4 w-4 mr-1" />
                    Редактировать
                  </Button>
                  <Button
                    variant="outline"
                    size="sm"
                    className="text-destructive hover:text-destructive"
                    onClick={() => setDeletingTask(template)}
                  >
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>
          ))
        ) : (
          <div className="col-span-full">
            <Card>
              <CardContent className="flex flex-col items-center justify-center py-12">
                <FileText className="h-12 w-12 text-muted-foreground mb-4" />
                <p className="text-muted-foreground">
                  {categoryFilter !== 'all' || difficultyFilter !== 'all'
                    ? 'Шаблоны не найдены'
                    : 'Нет шаблонов заданий'}
                </p>
                {categoryFilter === 'all' && difficultyFilter === 'all' && (
                  <Button
                    className="mt-4"
                    onClick={() => setIsCreateModalOpen(true)}
                  >
                    <Plus className="mr-2 h-4 w-4" />
                    Создать первый шаблон
                  </Button>
                )}
              </CardContent>
            </Card>
          </div>
        )}
      </div>

      {/* Модальные окна */}
      <TaskTemplateModal
        open={isCreateModalOpen}
        onOpenChange={setIsCreateModalOpen}
      />

      <TaskTemplateModal
        open={!!editingTask}
        onOpenChange={(open) => !open && setEditingTask(null)}
        task={editingTask}
      />

      <DeleteTaskDialog
        open={!!deletingTask}
        onOpenChange={(open) => !open && setDeletingTask(null)}
        task={deletingTask}
      />
    </div>
  )
}

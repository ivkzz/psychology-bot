/**
 * TaskCard - карточка задания
 */

'use client'

import { useState } from 'react'
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { CheckSquare, Clock, Calendar } from 'lucide-react'
import {
  formatDate,
  formatDifficulty,
  formatStatus,
  getDifficultyColor,
  getStatusColor,
} from '@/lib/utils/formatters'
import type { Assignment } from '@/types'
import { CompleteTaskModal } from './CompleteTaskModal'

interface TaskCardProps {
  assignment: Assignment
  showCompleteButton?: boolean
}

export function TaskCard({ assignment, showCompleteButton = false }: TaskCardProps) {
  const [isModalOpen, setIsModalOpen] = useState(false)

  const isCompleted = assignment.status === 'completed'

  return (
    <>
      <Card className={isCompleted ? 'border-green-200 bg-green-50/50' : ''}>
        <CardHeader>
          <div className="flex items-start justify-between gap-4">
            <div className="flex-1">
              <CardTitle className="flex items-center gap-2">
                {isCompleted && <CheckSquare className="h-5 w-5 text-green-600" />}
                {assignment.task.title}
              </CardTitle>
              <CardDescription className="mt-2">
                {assignment.task.description}
              </CardDescription>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2 mt-4">
            <Badge variant="outline">{assignment.task.category}</Badge>
            <Badge variant={getDifficultyColor(assignment.task.difficulty)}>
              {formatDifficulty(assignment.task.difficulty)}
            </Badge>
            <Badge variant={getStatusColor(assignment.status)}>
              {formatStatus(assignment.status)}
            </Badge>
          </div>
        </CardHeader>

        <CardContent>
          <div className="flex items-center justify-between">
            <div className="flex flex-col gap-2 text-sm text-muted-foreground">
              <div className="flex items-center gap-2">
                <Calendar className="h-4 w-4" />
                <span>Назначено: {formatDate(assignment.assigned_date)}</span>
              </div>

              {isCompleted && assignment.completed_at && (
                <div className="flex items-center gap-2 text-green-600">
                  <Clock className="h-4 w-4" />
                  <span>Выполнено: {formatDate(assignment.completed_at)}</span>
                </div>
              )}

              {isCompleted && assignment.answer_text && (
                <div className="mt-2 p-3 bg-background rounded-md border">
                  <p className="text-sm font-medium mb-1">Ваш ответ:</p>
                  <p className="text-sm">{assignment.answer_text}</p>
                </div>
              )}
            </div>

            {showCompleteButton && !isCompleted && (
              <Button onClick={() => setIsModalOpen(true)}>
                Выполнить
              </Button>
            )}
          </div>
        </CardContent>
      </Card>

      {/* Модальное окно для выполнения задания */}
      <CompleteTaskModal
        assignment={assignment}
        open={isModalOpen}
        onOpenChange={setIsModalOpen}
      />
    </>
  )
}

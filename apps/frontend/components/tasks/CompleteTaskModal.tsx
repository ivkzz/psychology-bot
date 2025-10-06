/**
 * CompleteTaskModal - модальное окно для выполнения задания
 */

'use client'

import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import { z } from 'zod'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { Textarea } from '@/components/ui/textarea'
import { Label } from '@/components/ui/label'
import { useCompleteTask } from '@/lib/hooks/use-tasks'
import type { Assignment } from '@/types'

// Zod схема валидации
const completeTaskSchema = z.object({
  answer_text: z
    .string()
    .max(2000, 'Ответ не должен превышать 2000 символов')
    .optional(),
})

type CompleteTaskFormData = z.infer<typeof completeTaskSchema>

interface CompleteTaskModalProps {
  assignment: Assignment
  open: boolean
  onOpenChange: (open: boolean) => void
}

export function CompleteTaskModal({
  assignment,
  open,
  onOpenChange,
}: CompleteTaskModalProps) {
  const completeTaskMutation = useCompleteTask()

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
  } = useForm<CompleteTaskFormData>({
    resolver: zodResolver(completeTaskSchema),
  })

  const onSubmit = async (data: CompleteTaskFormData) => {
    try {
      await completeTaskMutation.mutateAsync({
        assignmentId: assignment.id,
        data,
      })

      // Закрываем модальное окно и сбрасываем форму
      onOpenChange(false)
      reset()
    } catch (error) {
      // Ошибка уже обработана в хуке через toast
      console.error('Error completing task:', error)
    }
  }

  // Сбрасываем форму при закрытии модального окна
  const handleOpenChange = (newOpen: boolean) => {
    if (!newOpen) {
      reset()
    }
    onOpenChange(newOpen)
  }

  return (
    <Dialog open={open} onOpenChange={handleOpenChange}>
      <DialogContent className="sm:max-w-[600px]">
        <DialogHeader>
          <DialogTitle>{assignment.task.title}</DialogTitle>
          <DialogDescription>{assignment.task.description}</DialogDescription>
        </DialogHeader>

        <form onSubmit={handleSubmit(onSubmit)} className="space-y-4">
          <div className="space-y-2">
            <Label htmlFor="answer_text">
              Ваш ответ (необязательно)
            </Label>
            <Textarea
              id="answer_text"
              placeholder="Опишите ваши мысли, чувства или результаты выполнения задания..."
              rows={6}
              {...register('answer_text')}
              disabled={completeTaskMutation.isPending}
            />
            {errors.answer_text && (
              <p className="text-sm text-red-500">
                {errors.answer_text.message}
              </p>
            )}
            <p className="text-sm text-muted-foreground">
              Это поможет вам отслеживать ваш прогресс и понимать эффективность
              упражнений
            </p>
          </div>

          <DialogFooter>
            <Button
              type="button"
              variant="outline"
              onClick={() => handleOpenChange(false)}
              disabled={completeTaskMutation.isPending}
            >
              Отмена
            </Button>
            <Button type="submit" disabled={completeTaskMutation.isPending}>
              {completeTaskMutation.isPending
                ? 'Сохранение...'
                : 'Выполнить задание'}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  )
}

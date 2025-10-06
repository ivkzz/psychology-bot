/**
 * DeleteTaskDialog - диалог подтверждения удаления шаблона задания
 */

'use client'

import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from '@/components/ui/alert-dialog'
import { useDeleteTemplate } from '@/lib/hooks/use-admin'
import type { Task } from '@/types'

interface DeleteTaskDialogProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  task: Task | null
}

export function DeleteTaskDialog({
  open,
  onOpenChange,
  task,
}: DeleteTaskDialogProps) {
  const deleteTemplate = useDeleteTemplate()

  const handleDelete = () => {
    if (!task) return

    deleteTemplate.mutate(task.id, {
      onSuccess: () => {
        onOpenChange(false)
      },
    })
  }

  if (!task) return null

  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Вы уверены?</AlertDialogTitle>
          <AlertDialogDescription>
            Вы собираетесь удалить шаблон задания{' '}
            <span className="font-semibold">&quot;{task.title}&quot;</span>.
            <br />
            <br />
            Это действие нельзя отменить. Шаблон будет удалён навсегда.
            <br />
            <br />
            <span className="text-yellow-600 dark:text-yellow-500">
              ⚠️ Внимание: Уже назначенные задания на основе этого шаблона не
              будут удалены, но новые задания назначать будет невозможно.
            </span>
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel disabled={deleteTemplate.isPending}>
            Отмена
          </AlertDialogCancel>
          <AlertDialogAction
            onClick={handleDelete}
            disabled={deleteTemplate.isPending}
            className="bg-destructive text-destructive-foreground hover:bg-destructive/90"
          >
            {deleteTemplate.isPending ? 'Удаление...' : 'Удалить'}
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  )
}

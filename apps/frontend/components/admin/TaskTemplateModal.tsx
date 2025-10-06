/**
 * TaskTemplateModal - модальное окно для создания/редактирования шаблона задания
 */

'use client'

import { useEffect } from 'react'
import { useForm } from 'react-hook-form'
import { zodResolver } from '@hookform/resolvers/zod'
import * as z from 'zod'
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog'
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form'
import { Input } from '@/components/ui/input'
import { Textarea } from '@/components/ui/textarea'
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { useCreateTemplate, useUpdateTemplate } from '@/lib/hooks/use-admin'
import { Task, TaskDifficulty } from '@/types'
import { formatDifficulty, getDifficultyColor } from '@/lib/utils/formatters'

const taskSchema = z.object({
  title: z
    .string()
    .min(1, 'Название обязательно')
    .max(200, 'Максимум 200 символов'),
  description: z.string().min(1, 'Описание обязательно'),
  category: z
    .string()
    .min(1, 'Категория обязательна')
    .max(50, 'Максимум 50 символов'),
  difficulty: z.nativeEnum(TaskDifficulty, {
    message: 'Выберите сложность',
  }),
})

type TaskFormData = z.infer<typeof taskSchema>

interface TaskTemplateModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  task?: Task | null
}

// Предустановленные категории
const CATEGORIES = [
  'Медитация',
  'Дыхательные практики',
  'Физическая активность',
  'Рефлексия',
  'Творчество',
  'Общение',
  'Саморазвитие',
  'Благодарность',
]

export function TaskTemplateModal({
  open,
  onOpenChange,
  task,
}: TaskTemplateModalProps) {
  const isEditing = !!task

  const createTemplate = useCreateTemplate()
  const updateTemplate = useUpdateTemplate()

  const form = useForm<TaskFormData>({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      title: '',
      description: '',
      category: '',
      difficulty: TaskDifficulty.EASY,
    },
  })

  // Заполняем форму при редактировании
  useEffect(() => {
    if (task && open) {
      form.reset({
        title: task.title,
        description: task.description,
        category: task.category,
        difficulty: task.difficulty,
      })
    } else if (!open) {
      form.reset()
    }
  }, [task, open, form])

  const onSubmit = (data: TaskFormData) => {
    if (isEditing && task) {
      updateTemplate.mutate(
        { taskId: task.id, data },
        {
          onSuccess: () => {
            onOpenChange(false)
            form.reset()
          },
        }
      )
    } else {
      createTemplate.mutate(data, {
        onSuccess: () => {
          onOpenChange(false)
          form.reset()
        },
      })
    }
  }

  const isPending = createTemplate.isPending || updateTemplate.isPending

  // Preview данных формы
  const formValues = form.watch()

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-3xl max-h-[90vh] overflow-y-auto">
        <DialogHeader>
          <DialogTitle>
            {isEditing ? 'Редактировать шаблон' : 'Создать шаблон задания'}
          </DialogTitle>
          <DialogDescription>
            {isEditing
              ? 'Измените информацию о шаблоне задания'
              : 'Создайте новый шаблон задания для пользователей'}
          </DialogDescription>
        </DialogHeader>

        <Form {...form}>
          <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
            {/* Название */}
            <FormField
              control={form.control}
              name="title"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Название задания</FormLabel>
                  <FormControl>
                    <Input
                      placeholder="Например: Утренняя медитация"
                      {...field}
                    />
                  </FormControl>
                  <FormDescription>
                    Краткое и понятное название (1-200 символов)
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            {/* Описание */}
            <FormField
              control={form.control}
              name="description"
              render={({ field }) => (
                <FormItem>
                  <FormLabel>Описание задания</FormLabel>
                  <FormControl>
                    <Textarea
                      placeholder="Опишите подробно, что нужно сделать..."
                      rows={5}
                      {...field}
                    />
                  </FormControl>
                  <FormDescription>
                    Подробная инструкция для выполнения задания
                  </FormDescription>
                  <FormMessage />
                </FormItem>
              )}
            />

            <div className="grid gap-4 md:grid-cols-2">
              {/* Категория */}
              <FormField
                control={form.control}
                name="category"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Категория</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      value={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Выберите категорию" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        {CATEGORIES.map((cat) => (
                          <SelectItem key={cat} value={cat}>
                            {cat}
                          </SelectItem>
                        ))}
                        <SelectItem value="custom">Другое (введите вручную)</SelectItem>
                      </SelectContent>
                    </Select>
                    {field.value === 'custom' && (
                      <Input
                        placeholder="Введите категорию"
                        value={field.value}
                        onChange={field.onChange}
                        className="mt-2"
                      />
                    )}
                    <FormMessage />
                  </FormItem>
                )}
              />

              {/* Сложность */}
              <FormField
                control={form.control}
                name="difficulty"
                render={({ field }) => (
                  <FormItem>
                    <FormLabel>Сложность</FormLabel>
                    <Select
                      onValueChange={field.onChange}
                      value={field.value}
                    >
                      <FormControl>
                        <SelectTrigger>
                          <SelectValue placeholder="Выберите сложность" />
                        </SelectTrigger>
                      </FormControl>
                      <SelectContent>
                        <SelectItem value={TaskDifficulty.EASY}>Лёгкое</SelectItem>
                        <SelectItem value={TaskDifficulty.MEDIUM}>Среднее</SelectItem>
                        <SelectItem value={TaskDifficulty.HARD}>Сложное</SelectItem>
                      </SelectContent>
                    </Select>
                    <FormMessage />
                  </FormItem>
                )}
              />
            </div>

            {/* Preview */}
            <div className="border rounded-lg p-4 bg-muted/50">
              <p className="text-sm font-medium mb-3">Предпросмотр карточки:</p>
              <div className="bg-background border rounded-lg p-4">
                <h3 className="font-semibold text-lg mb-2">
                  {formValues.title || 'Название задания'}
                </h3>
                <p className="text-sm text-muted-foreground mb-3">
                  {formValues.description || 'Описание задания'}
                </p>
                <div className="flex items-center gap-2">
                  {formValues.category && (
                    <Badge variant="outline">{formValues.category}</Badge>
                  )}
                  {formValues.difficulty && (
                    <Badge
                      variant={getDifficultyColor(
                        formValues.difficulty as TaskDifficulty
                      )}
                    >
                      {formatDifficulty(formValues.difficulty as TaskDifficulty)}
                    </Badge>
                  )}
                </div>
              </div>
            </div>

            <DialogFooter>
              <Button
                type="button"
                variant="outline"
                onClick={() => onOpenChange(false)}
                disabled={isPending}
              >
                Отмена
              </Button>
              <Button type="submit" disabled={isPending}>
                {isPending
                  ? 'Сохранение...'
                  : isEditing
                    ? 'Сохранить изменения'
                    : 'Создать шаблон'}
              </Button>
            </DialogFooter>
          </form>
        </Form>
      </DialogContent>
    </Dialog>
  )
}

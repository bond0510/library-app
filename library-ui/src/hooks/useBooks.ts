import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../services/api'
import type { Book } from '../types'

export const useBooks = (page: number, limit: number) => {
  const qc = useQueryClient()

    const list = useQuery({
        queryKey: ['books', page, limit],
        queryFn: async () => {
            const res = await api.get(`/books/paginated?skip=${(page - 1) * limit}&limit=${limit}`)
        
            const data = res.data

            return {
                items: data.data,
                total: data.meta.total,
                page,
                limit,
                hasNext: (page * limit) < data.meta.total
            }
        }
    })

    const add = useMutation({
        mutationFn: (data: Partial<Book>) => api.post('/books', data),
        onSuccess: () => qc.invalidateQueries({ queryKey: ['books'] })
    })

    const update = useMutation({
        mutationFn: (data: any) => api.put(`/books/${data.id}`, data),
        onSuccess: () => qc.invalidateQueries({ queryKey: ['books'] })
    })

    const remove = useMutation({
        mutationFn: (id: number) => api.delete(`/books/${id}`),
        onSuccess: () => qc.invalidateQueries({ queryKey: ['books'] })
    })

    return { list, add, update, remove }
}

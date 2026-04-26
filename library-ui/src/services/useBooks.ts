import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../services/api'

export const useBooks = (page: number, limit: number) => {
  const qc = useQueryClient()

  const list = useQuery({
    queryKey: ['books', page, limit],
    queryFn: async () => (await api.get(`/books?page=${page}&limit=${limit}`)).data
  })

  const add = useMutation({
    mutationFn: (data: any) => api.post('/books', data),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['books'] })
  })

  return { list, add }
}

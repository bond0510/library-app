import { useState, useEffect } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import toast from 'react-hot-toast'
import { api } from '../services/api'
import ErrorBanner from './errorBanner'

export default function Borrow() {
  const qc = useQueryClient()

  const [memberId, setMemberId] = useState<number>(0)
  const [bookId, setBookId] = useState<number>(0)
  const [errorMessage, setErrorMessage] = useState('')
  const [successMessage, setSuccessMessage] = useState('')
  const [page, setPage] = useState(1)
  const [limit] = useState(5)
  const [search, setSearch] = useState('')
  const [filters, setFilters] = useState({
    member: '',
    book: '',
    status: ''
  })

  // Members
  const members = useQuery({
    queryKey: ['members'],
    queryFn: async () => (await api.get('/members')).data
  })

  // Books
  const books = useQuery({
    queryKey: ['books'],
    queryFn: async () => (await api.get('/books')).data // adjust if paginated
  })

  // Borrows
  const borrows = useQuery({
    queryKey: ['borrows', page, search, filters],
    queryFn: async () => {
      const res = await api.get(
        `/borrows?skip=${(page - 1) * limit}&limit=${limit}` +
          `&search=${search}` +
          `&member=${filters.member}` +
          `&book=${filters.book}` +
          `&status=${filters.status}`
      )

      const data = res.data

      return {
        items: data.data,
        total: data.meta.total || 0,
        hasNext: page * limit < (data.meta.total || 0)
      }
    }
  })

  // HANDLE QUERY ERROR
  useEffect(() => {
    if (borrows.isError) {
      setErrorMessage(
        (borrows.error as any)?.response?.data?.detail ||
          'Failed to load borrow records'
      )
    }
  }, [borrows.isError])

  // Borrow
  const borrowBook = useMutation({
    mutationFn: () =>
      api.post('/borrows', {
        member_id: memberId,
        book_id: bookId
      }),
    onSuccess: () => {
      setSuccessMessage('Book borrowed successfully')
      qc.invalidateQueries({ queryKey: ['borrows'] })
      qc.invalidateQueries({ queryKey: ['books'] })
    },
    onError: (error: any) => {
      const msg =
        error?.response?.data?.message || 'Failed to borrow book'
      toast.error(msg)
      setErrorMessage(msg)
    }
  })

  // Return
  const returnBook = useMutation({
    mutationFn: (id: number) =>
      api.patch(`/borrows/${id}/return`),
    onSuccess: () => {
      setSuccessMessage('Book returned successfully')
      qc.invalidateQueries({ queryKey: ['borrows'] })
      qc.invalidateQueries({ queryKey: ['books'] })
    }
  })

  const handleBorrow = () => {
    if (!memberId || !bookId) {
      alert('Select member and book')
      return
    }
    borrowBook.mutate()
  }

  // 🔥 Helper functions (IMPORTANT FIX)
  const getMemberName = (id: number) =>
    members.data?.find((m: any) => m.id === id)?.name || id

  const getBookTitle = (id: number) =>
    books.data?.find((b: any) => b.id === id)?.title || id



  return (

    <div>
        <ErrorBanner
            message={errorMessage}
            variant="error"
            onClose={() => setErrorMessage('')}
            onRetry={() => borrows.refetch()}
        />

        <ErrorBanner
            message={successMessage}
            variant="success"
            onClose={() => setSuccessMessage('')}
        />
      <h2 className="text-xl mb-4">Borrow / Return Books</h2>

      {/* BORROW FORM */}
      <div className="flex gap-2 mb-4">
        <select
          onChange={(e) => setMemberId(Number(e.target.value))}
          className="border p-2"
        >
          <option value="">Select Member</option>
          {members.data?.map((m: any) => (
            <option key={m.id} value={m.id}>
              {m.name}
            </option>
          ))}
        </select>

        <select
          onChange={(e) => setBookId(Number(e.target.value))}
          className="border p-2"
        >
          <option value="">Select Book</option>
          {books.data?.map((b: any) => (
            <option key={b.id} value={b.id}>
              {b.title} ({b.available_copies})
            </option>
          ))}
        </select>

        <button
          onClick={handleBorrow}
          className="bg-blue-600 text-white px-4"
        >
          Borrow
        </button>
      </div>

      {/* BORROW TABLE */}
      <table className="w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2">ID</th>
            <th className="p-2">Member</th>
            <th className="p-2">Book</th>
            <th className="p-2">Issue Date</th>
            <th className="p-2">Due Date</th>
            <th className="p-2">Return Date</th>
            <th className="p-2">Status</th>
            <th className="p-2">Action</th>
          </tr>
        </thead>
        <tbody>
          {borrows.data?.items?.map((b: any) => (
            <tr key={b.id} className="border-t">
              <td className="p-2">{b.id}</td>

              {/* 🔥 FIXED MAPPING */}
              <td className="p-2">{getMemberName(b.member_id)}</td>
              <td className="p-2">{getBookTitle(b.book_id)}</td>

              <td className="p-2">{b.issued_at}</td>
              <td className="p-2">{b.due_date}</td>
              <td className="p-2">{b.returned_at || '-'}</td>

              <td className="p-2">
                {b.status === 'RETURNED' ? 'Returned' : 'Borrowed'}
              </td>

              <td className="p-2">
                {b.status !== 'RETURNED' && (
                  <button
                    onClick={() => returnBook.mutate(b.id)}
                    className="bg-green-600 text-white px-2"
                  >
                    Return
                  </button>
                )}
              </td>
            </tr>
          ))}
        </tbody>
         {borrows.data?.items.length === 0 && (
            <tr>
              <td colSpan={8} className="text-center p-4 text-gray-500">
                No results found
              </td>
            </tr>
          )}
      </table>
      {/* PAGINATION */}
      <div className="flex gap-2 mt-4">
        <button
          disabled={page === 1}
          onClick={() => setPage((p) => p - 1)}
          className="bg-gray-300 px-3 py-1"
        >
          Prev
        </button>

        <span>Page {page}</span>

        <button
          disabled={!borrows.data?.hasNext}
          onClick={() => setPage((p) => p + 1)}
          className="bg-gray-300 px-3 py-1"
        >
          Next
        </button>
      </div>
    </div>


  )
}
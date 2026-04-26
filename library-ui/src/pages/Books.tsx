import { useState } from 'react'
import { useBooks } from '../hooks/useBooks'

import ErrorBanner from './errorBanner'


export default function Books() {
  const [page, setPage] = useState(1)

  const [limit] = useState(5)

  const { list, add, update, remove } = useBooks(page, limit)

  const [isEdit, setIsEdit] = useState(false)

  const [form, setForm] = useState({
    title: '',
    author: '',
    isbn: '',
    total_copies: 0
  })
  const [errorMessage, setErrorMessage] = useState('')
  const [successMessage, setSuccessMessage] = useState('')

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setForm((prev) => ({
      ...prev,
      [name]: name === 'total_copies' ? Number(value) : value
    }))
  }

  const handleSubmit = () => {
    if (!form.title || !form.author || !form.isbn || form.total_copies <= 0) {
      alert('Fill all fields')
      return
    }

    if (isEdit) {
      update.mutate(form, {
        onSuccess: resetForm
        
      })
      setSuccessMessage('Book added successfully')
    } else {
      add.mutate(form, {
        onSuccess: resetForm
      })
      setSuccessMessage('Book edited successfully')
    }
    
  }

  const handleEdit = (book: any) => {
    setForm(book)
    setIsEdit(true)
    
  }

  const handleDelete = (id: number) => {
    if (confirm('Delete this book?')) {
      remove.mutate(id)
    }
    setSuccessMessage('Book deleted successfully')
  }

  const resetForm = () => {
    setForm({ id: 0, title: '', author: '', isbn: '', copies: 0 })
    setIsEdit(false)
  }

  return (
    <div>
        <ErrorBanner
            message={errorMessage}
            variant="error"
            onClose={() => setErrorMessage('')}
        />
        <ErrorBanner
            message={successMessage}
            variant="success"
            onClose={() => setSuccessMessage('')}
        />
      <h2 className="text-xl mb-4">Books</h2>

      <div className="grid grid-cols-4 gap-2 mb-4">
        <input
          name="title"
          value={form.title}
          onChange={handleChange}
          placeholder="Title"
          className="border p-2"
        />

        <input
          name="author"
          value={form.author}
          onChange={handleChange}
          placeholder="Author"
          className="border p-2"
        />

        <input
          name="isbn"
          value={form.isbn}
          onChange={handleChange}
          placeholder="ISBN"
          className="border p-2"
        />

        <input
          name="total_copies"
          type="number"
          value={form.total_copies}
          onChange={handleChange}
          placeholder="Copies"
          className="border p-2"
        />
      </div>

      <button
        onClick={handleSubmit}
        className="bg-blue-600 text-white px-4 py-2 mb-4"
      >
       {isEdit ? 'Update Book' : 'Add Book'}
      </button>

      {list.isLoading && <p>Loading...</p>}

      <table className="w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2">ID</th>
            <th className="p-2">Title</th>
            <th className="p-2">Author</th>
            <th className="p-2">ISBN</th>
            <th className="p-2">Total Copies</th>
            <th className="p-2">Available Copies</th>
            <th className="p-2">Actions</th>
          </tr>
        </thead>
        <tbody>
          {list.data?.items?.map((b: any) => (
            <tr key={b.id} className="border-t">
              <td className="p-2">{b.id}</td>
              <td className="p-2">{b.title}</td>
              <td className="p-2">{b.author}</td>
              <td className="p-2">{b.isbn}</td>
              <td className="p-2">{b.total_copies}</td>
              <td className="p-2">{b.available_copies}</td>
              <td className="p-2 flex gap-2">
                <button onClick={() => handleEdit(b)} className="bg-yellow-500 text-white px-2">Edit</button>
                <button onClick={() => handleDelete(b.id)} className="bg-red-600 text-white px-2">Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
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
          disabled={!list.data?.hasNext}
          onClick={() => setPage((p) => p + 1)}
          className="bg-gray-300 px-3 py-1"
        >
          Next
        </button>
      </div>
    </div>
  )
}
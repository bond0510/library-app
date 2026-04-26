import { useState } from 'react'
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query'
import { api } from '../services/api'
import type { Member } from '../types'
import ErrorBanner from './errorBanner'

export default function Members() {
  const qc = useQueryClient()

  const [form, setForm] = useState({
    name: '',
    email: '',
    phone: ''
  })
  const [errorMessage, setErrorMessage] = useState('')
  const [successMessage, setSuccessMessage] = useState('')

  const list = useQuery<Member[]>({
    queryKey: ['members'],
    queryFn: async () => (await api.get('/members')).data
  })

  const add = useMutation({
    mutationFn: (data: Partial<Member>) => api.post('/members', data),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['members'] })
      setForm({ name: '', email: '', phone: '' }) // reset form
      setSuccessMessage('Book returned successfully')
    },
    onError: (err: any) => {
        setErrorMessage(err?.response?.data?.message || 'Action failed')
    }
  })

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target
    setForm((prev) => ({ ...prev, [name]: value }))
  }

  const handleSubmit = () => {
    if (!form.name || !form.email || !form.phone) {
      alert('Fill all fields')
      return
    }
    add.mutate(form)
        
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
      <h2 className="text-xl mb-4">Members</h2>

      {/* FORM */}
      <div className="flex gap-2 mb-4">
        <input
          name="name"
          value={form.name}
          onChange={handleChange}
          placeholder="Name"
          className="border p-2"
        />

        <input
          name="email"
          value={form.email}
          onChange={handleChange}
          placeholder="Email"
          className="border p-2"
        />

        <input
          name="phone"
          value={form.phone}
          onChange={handleChange}
          placeholder="Phone"
          className="border p-2"
        />

        <button
          onClick={handleSubmit}
          className="bg-green-600 text-white px-4"
        >
          Add
        </button>
      </div>

      {/* TABLE */}
      <table className="w-full border">
        <thead>
          <tr className="bg-gray-100">
            <th className="p-2">ID</th>
            <th className="p-2">Name</th>
            <th className="p-2">Email</th>
            <th className="p-2">Phone</th>
          </tr>
        </thead>
        <tbody>
          {list.data?.map((m) => (
            <tr key={m.id} className="border-t">
              <td className="p-2">{m.id}</td>
              <td className="p-2">{m.name}</td>
              <td className="p-2">{m.email}</td>
              <td className="p-2">{m.phone}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
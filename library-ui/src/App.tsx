import { Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Layout from './layout/Layout'
import Dashboard from './pages/Dashboard'
import Books from './pages/Books'
import Members from './pages/Members'
import Borrow from './pages/Borrow'

export default function App() {
  return (
    <Layout>
      <Toaster position="top-right" />
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/books" element={<Books />} />
        <Route path="/members" element={<Members />} />
        <Route path="/borrows" element={<Borrow />} />
      </Routes>
    </Layout>
  )
}
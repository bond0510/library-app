import { Link } from 'react-router-dom'

export default function Sidebar() {
  return (
    <div className="w-64 bg-gray-900 text-white p-4">
      <h2 className="text-xl mb-6">Enterprise App</h2>
      <nav className="flex flex-col gap-3">
        <Link to="/">Dashboard</Link>
        <Link to="/books">Books</Link>
        <Link to="/members">Members</Link>
        <Link to="/borrows">Borrows</Link>
      </nav>
    </div>
  )
}
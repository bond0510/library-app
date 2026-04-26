export interface Book {
  id: number
  title: string
  author: string
  isbn: string
  total_copies: number
  available_copies: number
}

export interface BookApiResponse {
  data: Book[]
  meta: {
    total: number   
    skip: number
    limit: number
  }
}

export interface Member {
  id: number
  name: string
  email: string
  phone: string
  status: string
}
import { create } from 'zustand'

interface AppState {
  search: string
  setSearch: (s: string) => void
}

export const useStore = create<AppState>((set) => ({
  search: '',
  setSearch: (s) => set({ search: s })
}))
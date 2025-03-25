import { create } from "zustand";

type QueryStoreState = {
  url?: string
  login?: string 
}

type QueryStoreActions = {
  setUrl: (url: string) => void
  setLogin: (login: string) => void
}

export const useQueryStore = create<QueryStoreState & QueryStoreActions>()(
  (set) => ({
    url: undefined,
    login: undefined,
    setUrl: (url) => set(() => ({ url: url })),
    setLogin: (login) => set(() => ({ login: login }))
  })
)


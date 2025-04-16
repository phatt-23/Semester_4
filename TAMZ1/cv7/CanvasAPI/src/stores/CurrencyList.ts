import { create } from "zustand";

export type CurrencyCode = string

export type CurrencyListItem = {
  countryLabel: string
  currencyLabel: string
  unit: number 
  code: CurrencyCode // primary key
  rate: number
}

type CurrencyListState = {
  list: CurrencyListItem[]
  selected: CurrencyCode[]
}

type CurrencyListAction = {
  add: (i: CurrencyListItem) => void
  set: (i: CurrencyListItem[]) => void
  addSelected: (i: CurrencyCode) => void
  setSelected: (i: CurrencyCode[]) => void
  removeSelected: (i: CurrencyCode) => void
}

export const useCurrencyListStore = create<CurrencyListState & CurrencyListAction>()((set) => ({
  list: [],
  selected: [],
  add: (i) => set(state => ({ list: [...state.list, i] })),
  set: (l) => set(() => ({ list: l })),
  addSelected: (i) => set(state => ({ selected: [...state.selected, i] })),
  setSelected: (l) => set(() => ({ selected: l })),
  removeSelected: (i) => set(state => ({ selected: state.selected.filter(v => v != i) })) 
}))

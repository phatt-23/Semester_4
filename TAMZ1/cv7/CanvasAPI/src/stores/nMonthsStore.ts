import { create } from "zustand";
import { immer } from "zustand/middleware/immer";

type State = {
  nMonthsToView: number
}

type Action = {
  setNMonthsToView: (v: number) => void
}

export const useNMonthsStore = create<State & Action>()(immer(set => ({
  nMonthsToView: 0,
  setNMonthsToView: (v) => set(state => { 
    state.nMonthsToView = v
  }),
})))

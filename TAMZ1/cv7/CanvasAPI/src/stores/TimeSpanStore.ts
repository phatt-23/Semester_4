import { create } from "zustand";
import { immer } from "zustand/middleware/immer";

type Style = {
  startDate: Date
  endDate: Date
}

type Action = {
  setStartDate: (date: Date) => void
  setEndDate: (date: Date) => void
}

export const useTimeSpanStore = create<Style & Action>()(immer(set => ({
  startDate: new Date(),
  endDate: new Date(),
  setStartDate: (date) => set(() => ({ startDate: date })),
  setEndDate: (date) => set(() => ({ endDate: date })),
})))

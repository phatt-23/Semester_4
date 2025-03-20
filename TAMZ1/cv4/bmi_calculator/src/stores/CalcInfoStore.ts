import { create } from "zustand"

export type Sex = "male" | "female"

type CalcInfoState = {
  username?: string
  age?: number
  sex?: Sex
  height?: number
  weight?: number
}

export type CalcInfo = CalcInfoState

type CaclInfoActions = {
  setUsername: (username: string) => void
  setAge: (age: number) => void
  setSex: (sex: Sex) => void
  setHeight: (height: number) => void
  setWeight: (weight: number) => void
}

export const useCalcInfoStore = create<CalcInfoState & CaclInfoActions>()((set) => ({
  username: undefined,
  age: undefined,
  sex: undefined,
  height: undefined,
  weight: undefined,
  setUsername: (username) => set(() => ({ username: username })),
  setAge: (age) => set(() => ({ age: age })),
  setSex: (sex) => set(() => ({ sex: sex })),
  setHeight: (height) => set(() => ({ height: height })),
  setWeight: (weight) => set(() => ({ weight: weight })),
}))



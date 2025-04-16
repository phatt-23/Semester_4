import { create } from "zustand"
import { immer } from "zustand/middleware/immer"
import { CurrencyCode, CurrencyListItem } from "./CurrencyList"

type DateString = string
type RateNumber = number

export type CurrencyHistory = Map<CurrencyCode, Map<DateString, RateNumber>>

type State = {
  history: CurrencyHistory
  fetchedDates: Set<DateString>
}

type Action = {
  addRatesForCurrency: (code: CurrencyCode, rates: Map<DateString, RateNumber>) => void
  addRatesForDate: (date: string, rates: CurrencyListItem[]) => void
  addFetchedDate: (date: DateString) => void
}

export const useCurrencyHistoryStore = create<State & Action>()(
  immer(
    set => ({
      history: new Map(),
      fetchedDates: new Set(),

      addRatesForCurrency: (code: CurrencyCode, rates: Map<DateString, RateNumber>) => set(state => {
        const prevRates = state.history.get(code)!

        rates.forEach((rate, date) => {
          prevRates.set(date, rate)
        })

        state.history.set(code, prevRates)
      }),

      addRatesForDate: (date: string, rates: CurrencyListItem[]) => set(state => {
        console.info("Adding rates for date")
        rates.forEach(rate => {
          if (!state.history.has(rate.code)) 
            state.history.set(rate.code, new Map())

          state.history.get(rate.code)!.set(date, rate.rate)
        })
      }),

      addFetchedDate: (date) => set(state => {
        state.fetchedDates.add(date)
      })
    })
  )
)

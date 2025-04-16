import { CurrencyListItem } from "../stores/CurrencyList"

export async function fetchCurrencyRates(date: string) {
  const url = `http://linedu.vsb.cz/~mor03/TAMZ/cnb_json.php?date=${date}`
  const response = await fetch(url, {})
  if (!response.ok) {
    console.error(`Function 'fetchCurrencies' couldn't fetch: ${url}`)
    return []
  }

  const json = await response.json()  

  const currencies = json.data as Array<any>

  const currencyListItems: CurrencyListItem[] = currencies.map((value) => ({
    countryLabel: value.country_label,
    currencyLabel: value.curr_label,
    unit: value.unit,
    code: value.code,
    rate: value.rate,
  }))

  console.log(`Fetched JSON (on date ${date}):`, json, "and mapped:", currencyListItems)
  return currencyListItems
}


export function getLastNMonths(n: number): string[] {
  const dates: string[] = []
  const now = new Date()

  for (let i = n; i >= 0; i--) {
    const date = new Date(now.getFullYear(), now.getMonth() - i, 1)
    dates.push(getDate(date))
  }

  return dates
}


export const getDate = (date: Date) => date.toISOString().split("T")[0]


export const convertCurrency = (input: number, sourceExRate: number, destExRate: number): number => input * (sourceExRate / destExRate)



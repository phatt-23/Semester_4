import { Preferences } from "@capacitor/preferences";
import { nanoid } from "nanoid"
import { create, StateCreator } from "zustand"
import { CalcInfo } from "./CalcInfoStore";
import { calculateBmi } from "../lib/utils";


const capacitorPreferencesMiddleware = 
  <T>(key: string, config: StateCreator<T>): StateCreator<T> => 
    (set, get, store) => {
      // Load initial state from Preferences
      (async () => {
        try {
          const { value } = await Preferences.get({ key: key })
          if (value) {
            set(JSON.parse(value));
          }
        } catch (error) {
          console.error("Failed to parse local storage:", error);
        }
      })()

      
      return config(
        (args) => {
          set(args);
          Preferences
            .set({ key: key, value: JSON.stringify(get()) })
            .catch((error) => {
              console.error("Failed to save calcs list state:", error)
            })
        },
        get,
        store
      );
    };


export type CalcListItem = {
  id: string 
  calcInfo: CalcInfo
  bmi?: number
}


type CalcsListState = {
  items: CalcListItem[]
}


type CalcsListActions = {
  addItem: (calcInfo: CalcInfo) => void
  removeItem: (id: string) => void
  clear: () => void
}


export const useCalcsListStore = create<CalcsListState & CalcsListActions>()(
  capacitorPreferencesMiddleware("calcs-storage",
    (set) => ({
      items: [],
      addItem: (calcInfo) => 
        set((state) => ({
          items: [...state.items, { id: nanoid(), calcInfo: calcInfo, bmi: calculateBmi(calcInfo.weight!, calcInfo.height!) }]
        })),
      removeItem: (id) => 
        set((state) => ({
          items: state.items.filter(i => i.id !== id)
        })),
      clear: () => set(() => ({ items: [] })),
    }),
  )
)


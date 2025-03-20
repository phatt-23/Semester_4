import { create } from "zustand";


type EditItemState = {
  editingItemID: string | null
}


type EditItemActions = {
  setEditingItemID: (id: string) => void
  clearEditingID: () => void
}


export const useEditItemStore = create<EditItemState & EditItemActions>()(
  (set) => ({
    editingItemID: null,
    setEditingItemID: (id) => set(() => ({ editingItemID: id })),
    clearEditingID: () => set(() => ({ editingItemID: null })),
  })
)

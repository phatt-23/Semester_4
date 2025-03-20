import { create } from "zustand";
import { immer } from "zustand/middleware/immer"

type ResponseState = {
  secretData?: string
  decodedSecretData?: string
  finalMessage?: string
}

type ResponseActions = {
  setSecretData: (v: string) => void
  setDecodedSecretData: (v: string) => void
  setFinalMessage: (v: string) => void
}

export const useResponseStore = create<ResponseState & ResponseActions>()(
  immer((set) => ({
    secretData: undefined,
    decodedSecretData: undefined,
    finalMessage: undefined,
    setSecretData: (v: string) => 
      set((state) => { 
        state.secretData = v
      }),
    setDecodedSecretData: (v: string) => 
      set((state) => { 
        state.decodedSecretData = v
      }),
    setFinalMessage: (v: string) => 
      set((state) => { 
        state.finalMessage = v 
      }),
  })),
)


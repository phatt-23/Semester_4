import { 
  IonButton, 
  IonCard, 
  IonCardContent, 
  useIonAlert 
} from "@ionic/react"
import { useShallow } from "zustand/shallow"
import { useResponseStore } from "../stores/ResponseStore"
import { useQueryStore } from "../stores/QueryStore"


type GetMethods = "post" | "get"


const ActionButtonsCard: React.FC = () => {
  const [url, login] = useQueryStore(
    useShallow((state) => [
      state.url,
      state.login,
    ]))

  const [secretData, setSecretData, setDecodedSecretData, setFinalMessage] = useResponseStore(
    useShallow((state) => [
      state.secretData,
      state.setSecretData,
      state.setDecodedSecretData,
      state.setFinalMessage,
    ]))

  const [ionAlert] = useIonAlert()

  function handleGetCode(method: GetMethods) {
    if (!login) {
      ionAlert("Please, provide login!")
      return
    }
    
    const getMethod = async () => {
      const queryString = `${url}?user=${login}&timestamp=${new Date().getTime()}`
      const response = await fetch(queryString)
      const text = await response.text()
      const decoded = atob(text)
      setSecretData(text)
      setDecodedSecretData(decoded)
    }

    const postMethod = async () => {
      const formBody: Record<string, string> = {
        user: login,
        timestamp: new Date().getTime().toString(),
      }

      const postBody = Object.keys(formBody).map((key) =>
        `${encodeURIComponent(key)}=${encodeURIComponent(formBody[key])}`
      ).join("&")

      const res = await fetch(url!, {
        method: "post",
        body: postBody,
        headers: {
          "Content-Type": "application/x-www-form-urlencoded"
        }
      })

      const text = await res.text()
      const decoded = atob(text)

      setSecretData(text)
      setDecodedSecretData(decoded)
    }
    
    switch (method) {
      case "post":
        postMethod()
        break
      case "get":
        getMethod()
        break
      default:
        ionAlert("Unknown method")
    }
  }

  function handleSendCode() {
    (async () => {
      const body: Record<string, string> = {
        timestamp: new Date().getTime().toString()
      }

      const formBody = Object.keys(body).map((key) => 
          `${encodeURIComponent(key)}=${encodeURIComponent(body[key])}`
        ).join("&")

      const res = await fetch(url!, {
        method: "post",
        body: formBody,
        headers: {
          "Authorization": `Bearer ${secretData}`
        }
      })

      setFinalMessage(await res.text())
    })()
  }

  return (
    <IonCard>
      <IonCardContent>
        <IonButton expand="block" onClick={() => handleGetCode("get")}>
          Get Code (get)
        </IonButton>
        <IonButton expand="block" onClick={() => handleGetCode("post")}>
          Get Code (post)
        </IonButton>
        <IonButton expand="block" onClick={() => handleSendCode()}>
          Send Code
        </IonButton>
      </IonCardContent>
    </IonCard>
  )
} 

export default ActionButtonsCard

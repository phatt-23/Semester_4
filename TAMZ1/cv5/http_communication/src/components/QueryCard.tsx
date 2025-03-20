import { 
  IonCard, 
  IonCardContent, 
  IonCardTitle,
  IonInput,
  IonTitle,
  IonToolbar
} from "@ionic/react"
import { useEffect } from "react"
import { useQueryStore } from "../stores/QueryStore"
import { useShallow } from "zustand/shallow"


const QueryCard: React.FC = () => {
  const [url, login, setUrl, setLogin] = useQueryStore(
    useShallow((state) => [
      state.url,
      state.login,
      state.setUrl,
      state.setLogin,
    ]))

  // just for now, default values
  useEffect(() => {
    setUrl("https://homel.vsb.cz/~mor03/TAMZ/TAMZ22.php")
    setLogin("TRA0163")
  }, [])

  return (
    <IonCard>
      <IonCardTitle>
        <IonToolbar>
          <IonTitle>
            Query
          </IonTitle>
        </IonToolbar>
      </IonCardTitle>
      <IonCardContent>
        <IonInput
          label="URL"
          placeholder="Enter URL"
          value={url}
          onIonChange={({ detail }) => setUrl(detail.value as string)}
        >
        </IonInput>
        <IonInput
          label="Login"
          placeholder="Enter Login"
          value={login}
          onIonChange={({ detail }) => setLogin(detail.value as string)}
        >
        </IonInput>
      </IonCardContent>
    </IonCard>
  )
}

export default QueryCard


import { 
  IonCard, 
  IonCardContent, 
  IonCardHeader, 
  IonCardTitle,
  IonTextarea
} from "@ionic/react"
import { useResponseStore } from "../stores/ResponseStore"
import { useShallow } from "zustand/shallow"
 

const ResponseCard: React.FC = () => {
  const [secretData, decodedSecretData, finalMessage] = useResponseStore(
    useShallow((state) => [
      state.secretData,
      state.decodedSecretData,
      state.finalMessage,
    ]))

  return (
    <IonCard>
      <IonCardHeader>
        <IonCardTitle>
          Response
        </IonCardTitle>
      </IonCardHeader>
      <IonCardContent>
        <IonTextarea
          readonly
          label="Received Secret Data"
          labelPlacement="stacked"
          placeholder="Here will be the received secret data"
          value={secretData}
        >
        </IonTextarea>

        <IonTextarea
          readonly
          label="Decoded Secret Data"
          labelPlacement="stacked"
          placeholder="Here will be the decoded received secret data"
          value={decodedSecretData}
        >
        </IonTextarea>

        <IonTextarea
          readonly
          label="Final Message"
          labelPlacement="stacked"
          placeholder="Here will be the final message"
          value={finalMessage}
        >
        </IonTextarea>
      </IonCardContent>
    </IonCard>
  )
}

export default ResponseCard


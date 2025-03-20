import { 
  IonCard, 
  IonCardContent, 
  IonCardHeader, 
  IonCardTitle, 
  IonIcon, 
  IonInput, 
  IonItem 
} from "@ionic/react";
import { useCalcInfoStore } from "../stores/CalcInfoStore"
import { personOutline } from "ionicons/icons"
import { useEditItemStore } from "../stores/EditItemStore"
import { useRef } from "react";

export default function UsernameInputCard() {
  const setUsername = useCalcInfoStore((state) => state.setUsername)

  return (
    <IonCard>
      <IonCardHeader>
        <IonCardTitle>Username</IonCardTitle>
      </IonCardHeader>
      <IonCardContent>
        <IonItem lines="full">
          <IonIcon icon={personOutline} slot="start" color="medium" /> 
          <IonInput 
            placeholder="Enter username"
            type="text"
            clearInput
            debounce={200}
            onIonChange={({ detail }) => setUsername(detail.value as string)}
          />
        </IonItem>
      </IonCardContent>
    </IonCard>
  );
}

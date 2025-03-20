import { 
  IonCard, 
  IonCardContent, 
  IonCardHeader, 
  IonCardTitle, 
  IonInput, 
  IonItem, 
  IonIcon 
} from "@ionic/react";
import { calendarOutline } from "ionicons/icons";
import { useCalcInfoStore } from "../stores/CalcInfoStore";

export default function AgeInputCard() {
  const setAge = useCalcInfoStore((state) => state.setAge);

  return (
    <IonCard>
      <IonCardHeader>
        <IonCardTitle>Age</IonCardTitle>
      </IonCardHeader>
      <IonCardContent>
        <IonItem lines="full">
          <IonIcon icon={calendarOutline} slot="start" />
          <IonInput
            placeholder="Enter age"
            type="number"
            min="1"
            max="120"
            step="1"
            clearInput
            debounce={200}
            onIonChange={({ detail }) => {
              const value = parseInt(detail.value as string, 10);
              if (!isNaN(value)) setAge(value);
            }}
          />
        </IonItem>
      </IonCardContent>
    </IonCard>
  );
}


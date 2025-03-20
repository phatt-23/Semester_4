import { 
  IonCard, 
  IonCardContent, 
  IonCardHeader, 
  IonCardTitle, 
  IonLabel, 
  IonRange, 
  IonItem, 
  IonIcon 
} from "@ionic/react";
import { barbellOutline } from "ionicons/icons";
import { useCalcInfoStore } from "../stores/CalcInfoStore";
import { useShallow } from "zustand/shallow";

export default function WeightCard() {
  const [weight, setWeight] = useCalcInfoStore(
    useShallow((state) => [state.weight, state.setWeight])
  );

  return (
    <IonCard>
      <IonCardHeader>
        <IonCardTitle>Weight</IonCardTitle>
      </IonCardHeader>
      <IonCardContent>
        <IonItem lines="none">
          <IonIcon icon={barbellOutline} slot="start" />
          <IonLabel>
            Weight: <b>{weight ?? "-"}</b> kg
          </IonLabel>
        </IonItem>

        <IonRange
          min={30}
          max={200}
          step={1}
          value={weight ?? (() => {
            setWeight(70)// Default value of 70
            return weight
          })() 
          }
          debounce={10}
          onIonInput={({ detail }) => setWeight(detail.value as number)}
        />
      </IonCardContent>
    </IonCard>
  );
}


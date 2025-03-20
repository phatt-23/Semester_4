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
import { bodyOutline } from "ionicons/icons";
import { useCalcInfoStore } from "../stores/CalcInfoStore";
import { useShallow } from "zustand/shallow";

export default function HeightWeightCard() {
  const [height, setHeight] = useCalcInfoStore(
    useShallow((state) => [state.height, state.setHeight])
  );

  return (
    <IonCard>
      <IonCardHeader>
        <IonCardTitle>Height</IonCardTitle>
      </IonCardHeader>
      <IonCardContent>
        <IonItem lines="none">
          <IonIcon icon={bodyOutline} slot="start" />
          <IonLabel>
            Height: <b>{height ?? "-"}</b> cm
          </IonLabel>
        </IonItem>

        <IonRange
          min={50}
          max={250}
          step={1}
          value={height ?? (() => {
            setHeight(170) // Default value of 170
            return height
          })()} 
          debounce={10}
          onIonInput={({ detail }) => setHeight(detail.value as number)}
        />
      </IonCardContent>
    </IonCard>
  );
}


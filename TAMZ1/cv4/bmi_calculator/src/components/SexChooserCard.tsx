import { 
  IonCard, 
  IonRadioGroup, 
  IonRadio, 
  IonCardContent, 
  IonCardTitle, 
  IonCardHeader, 
  IonItem, 
  IonList, 
  IonIcon 
} from "@ionic/react";
import { femaleOutline, maleOutline } from "ionicons/icons"; 
import { Sex, useCalcInfoStore } from "../stores/CalcInfoStore";

export default function SexChooserCard() {
  const setSex = useCalcInfoStore((state) => state.setSex);

  return (
    <IonCard>
      <IonCardHeader>
        <IonCardTitle>Sex</IonCardTitle>
      </IonCardHeader>
      <IonCardContent>
        <IonList lines="full" style={{ "--ion-padding": "0px" }}>
          <IonRadioGroup
            onIonChange={({ detail }) => setSex(detail.value as Sex)}
          >
            <IonItem>
              <IonIcon icon={maleOutline} slot="start" />
              <IonRadio value="male" justify="space-between">
                Male
              </IonRadio>
            </IonItem>
            <IonItem>
              <IonIcon icon={femaleOutline} slot="start" />
              <IonRadio value="female" justify="space-between">
                Female
              </IonRadio>
            </IonItem>
          </IonRadioGroup>
        </IonList>
      </IonCardContent>
    </IonCard>
  );
}


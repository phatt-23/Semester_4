import { 
  IonPage, 
  IonHeader, 
  IonToolbar, 
  IonTitle, 
  IonContent,
  IonIcon,
  IonButton,
  IonItem,
} from "@ionic/react";

import UsernameInputCard from "../components/UsernameInputCard";
import AgeInputCard from "../components/AgeInputCard";
import SexChooserCard from "../components/SexChooserCard";
import HeightRangeCard from "../components/HeightRangeCard";
import WeightRangeCard from "../components/WeightRangeCard";
import CalculateBMIButton from "../components/CalculateBMIButton";
import { calculator } from "ionicons/icons";

export default function CalculatorTab() {
  return (
    <IonPage>
      <IonHeader id="header">
        <IonToolbar>
          <IonTitle slot="start">
            <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
              <IonIcon icon={calculator} />
              BMI Calculator
            </span>
          </IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent>

        <UsernameInputCard />
        <AgeInputCard />
        <SexChooserCard />
        <HeightRangeCard />
        <WeightRangeCard />
        <CalculateBMIButton />

      </IonContent>
    </IonPage>
  );
}


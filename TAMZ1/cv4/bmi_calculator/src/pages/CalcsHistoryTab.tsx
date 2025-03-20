import { IonContent, IonPage } from "@ionic/react";

import CalcHistoryHeader from "../components/CalcHistoryHeader";
import CalcHistoryList from "../components/CalcHistoryList";

export default function CalculationsHistory() {
  return (
    <IonPage>
      <CalcHistoryHeader />
      <IonContent className="ion-padding">
        <CalcHistoryList />
      </IonContent>
    </IonPage>
  );
}


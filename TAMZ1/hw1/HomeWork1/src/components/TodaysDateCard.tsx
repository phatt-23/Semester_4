import { IonCard, IonCardContent } from "@ionic/react";
import { memo } from "react";

export const TodaysDateCard: React.FC = 
memo(() => (
  <IonCard>
    <IonCardContent>
      Dnesni datum: {new Date().toLocaleDateString()}
    </IonCardContent>
  </IonCard>
));

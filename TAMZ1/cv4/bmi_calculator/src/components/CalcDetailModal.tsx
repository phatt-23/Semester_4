import { 
  IonButton, 
  IonButtons, 
  IonCard, 
  IonCardContent, 
  IonCardHeader, 
  IonCardTitle, 
  IonContent, 
  IonHeader, 
  IonItem, 
  IonLabel, 
  IonList, 
  IonPage, 
  IonTitle, 
  IonToolbar 
} from "@ionic/react";
import { calculateBmi, getBMIClassification, getColorFromBMI } from "../lib/utils";
import { CalcListItem } from "../stores/CalcsListStore";


type CalcDetailModalProps = { 
  item: CalcListItem
  dismiss: () => void 
}


function CalcDetailModal({ item, dismiss }: CalcDetailModalProps)
{
  const bmi = calculateBmi(item.calcInfo.weight as number, item.calcInfo.height as number)
  const bmiClass = getBMIClassification(bmi)

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle style={{ paddingLeft: 12 }} color={getColorFromBMI(bmi)}>
            BMI: {bmiClass}
          </IonTitle>
          <IonButtons slot="end">
            <IonButton color="medium" onClick={dismiss}>
              Close
            </IonButton>
          </IonButtons>
        </IonToolbar>
      </IonHeader>

      <IonContent className="ion-padding">
        <IonCard>
          <IonCardHeader>
            <IonCardTitle>Calculation Detail</IonCardTitle>
          </IonCardHeader>
          <IonCardContent>
            <IonList lines="none">
              <IonItem>
                <IonLabel color="medium">Username:</IonLabel>
                <IonLabel className="ion-text-right">{item.calcInfo.username}</IonLabel>
              </IonItem>
              <IonItem>
                <IonLabel color="medium">Age:</IonLabel>
                <IonLabel className="ion-text-right">{item.calcInfo.age}</IonLabel>
              </IonItem>
              <IonItem>
                <IonLabel color="medium">Sex:</IonLabel>
                <IonLabel className="ion-text-right">{item.calcInfo.sex}</IonLabel>
              </IonItem>
              <IonItem>
                <IonLabel color="medium">Height:</IonLabel>
                <IonLabel className="ion-text-right">{item.calcInfo.height} cm</IonLabel>
              </IonItem>
              <IonItem>
                <IonLabel color="medium">Weight:</IonLabel>
                <IonLabel className="ion-text-right">{item.calcInfo.weight} kg</IonLabel>
              </IonItem>
              <IonItem>
                <IonLabel color="medium">BMI:</IonLabel>
                <IonLabel className="ion-text-right">{item.bmi!.toPrecision(4)}</IonLabel>
              </IonItem>
            </IonList>
          </IonCardContent>
        </IonCard>
      </IonContent>
    </IonPage>
  )
}

export default CalcDetailModal;


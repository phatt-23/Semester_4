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
} from "@ionic/react"
import { useCalcInfoStore } from "../stores/CalcInfoStore"
import { useShallow } from "zustand/shallow"
import { calculateBmi, getBMIClassification, getColorFromBMI } from "../lib/utils"

type CalculationModalProps = { 
  dismiss: () => void 
}

export default function CalculationModal({ dismiss }: CalculationModalProps) 
{
  const [username, age, sex, height, weight] = useCalcInfoStore(
    useShallow((state) => [
      state.username,
      state.age,
      state.sex,
      state.height,
      state.weight
    ])
  )

  const bmi = calculateBmi(weight as number, height as number)
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
            <IonCardTitle>Calculation Summary</IonCardTitle>
          </IonCardHeader>
          <IonCardContent>
            <IonList lines="none">
              <IonItem>
                <IonLabel color="medium">Username:</IonLabel>
                <IonLabel className="ion-text-right">{username}</IonLabel>
              </IonItem>
              <IonItem>
                <IonLabel color="medium">Age:</IonLabel>
                <IonLabel className="ion-text-right">{age}</IonLabel>
              </IonItem>
              <IonItem>
                <IonLabel color="medium">Sex:</IonLabel>
                <IonLabel className="ion-text-right">{sex}</IonLabel>
              </IonItem>
              <IonItem>
                <IonLabel color="medium">Height:</IonLabel>
                <IonLabel className="ion-text-right">{height} cm</IonLabel>
              </IonItem>
              <IonItem>
                <IonLabel color="medium">Weight:</IonLabel>
                <IonLabel className="ion-text-right">{weight} kg</IonLabel>
              </IonItem>
              <IonItem>
                <IonLabel color="medium">BMI:</IonLabel>
                <IonLabel className="ion-text-right">{bmi.toPrecision(4)}</IonLabel>
              </IonItem>
            </IonList>
          </IonCardContent>
        </IonCard>
      </IonContent>
    </IonPage>
  )
}


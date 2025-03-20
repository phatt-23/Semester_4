import { IonButton, IonToast, IonLabel, IonModal, IonHeader, IonToolbar, IonTitle, useIonToast, useIonModal, IonContent, IonIcon } from "@ionic/react";
import { useCalcsListStore } from "../stores/CalcsListStore";
import { useCalcInfoStore, CalcInfo } from "../stores/CalcInfoStore";
import { useShallow } from "zustand/shallow";
import CalculationModal from "./CalculationModal";
import { rocket } from "ionicons/icons"

export default function CalculateBMIButton() {
  const addItem = useCalcsListStore((state) => state.addItem);
  const [username, age, sex, height, weight] = useCalcInfoStore(
    useShallow((state) => [state.username, state.age, state.sex, state.height, state.weight])
  );

  const [presentToast] = useIonToast();
  const [present, dismiss] = useIonModal(CalculationModal, {
    dismiss: () => dismiss(),
  });

  function handleClick() {
    if (!(username && age && sex && height && weight)) {
      presentToast({
        duration: 2000,
        position: "bottom",
        positionAnchor: "tab-bar",
        message: "Please, specify all fields for the calculation.",
        buttons: [{ text: "Dismiss", role: "cancel" }],
        translucent: true,
      });
      return;
    }

    const item: CalcInfo = {
      username: username,
      age: age,
      sex: sex,
      height: height,
      weight: weight,
    };

    addItem(item);

    present({
      breakpoints: [0, 0.2, 0.4, 0.6, 0.8, 1.0],
      initialBreakpoint: 0.6,
    });
  }

  return (
    <>
      <IonButton
        id="calculate-button"
        strong
        expand="block"
        shape="round"
        color="primary" 
        style={{ paddingTop: 0, paddingBottom: 10, paddingLeft: 10, paddingRight: 10 }}
        onClick={handleClick} 
      >
        <IonIcon icon={rocket} slot="end"/>
        <IonLabel slot="start"> 
          Calculate
        </IonLabel>
      </IonButton>
    </>
  );
}


import { 
  IonButton, 
  IonHeader, 
  IonIcon, 
  IonTitle, 
  IonToolbar, 
  useIonActionSheet 
} from "@ionic/react";
import { useCalcsListStore } from "../stores/CalcsListStore"
import { list, trashOutline } from "ionicons/icons";

export default function CalcHistoryHeader() {
  const clearItems = useCalcsListStore((state) => state.clear);
  const [present] = useIonActionSheet();

  return (
    <IonHeader>
      <IonToolbar>
        <IonTitle slot="start">
          <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
            <IonIcon icon={list} />
            History
          </span>
        </IonTitle>
        <IonButton
          strong
          slot="end"
          style={{ paddingRight: 10 }}
          color="danger"
          onClick={() => present({
            header: "Do you really want to clear all items?",
            buttons: [
              {
                text: 'Yes',
                role: 'destructive',
                data: {
                  action: 'delete',
                },
              },
              {
                text: 'No',
                role: 'cancel',
                data: {
                  action: 'cancel',
                },
              },
            ],
            onDidDismiss: ({ detail }) => {
              if (detail.role! === "destructive")
                clearItems();
            }
          })}
        >
          <IonIcon icon={trashOutline} slot="start" />
          Clear All
        </IonButton>
      </IonToolbar>
    </IonHeader>
  )
}

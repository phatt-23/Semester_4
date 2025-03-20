import {
  IonChip,
  IonIcon,
  IonItem,
  IonItemOption,
  IonItemOptions,
  IonItemSliding,
  IonLabel,
  IonList,
  useIonActionSheet,
  useIonModal
} from "@ionic/react";

import { createOutline, trashOutline } from "ionicons/icons";
import { CalcListItem, useCalcsListStore } from "../stores/CalcsListStore";
import { getBMIClassification, getColorFromBMI } from "../lib/utils";
import CalcDetailModal from "./CalcDetailModal";
import { useState } from "react";
import { useEditItemStore } from "../stores/EditItemStore";
import { useShallow } from "zustand/shallow";


export default function CalcHistoryContent() 
{
  const items = useCalcsListStore((state) => state.items);
  const removeItem = useCalcsListStore((state) => state.removeItem);

  const [editingItemID, setEditingItemID, clearEditingID] = useEditItemStore(
    useShallow((state) => 
      [
        state.editingItemID, 
        state.setEditingItemID,
        state.clearEditingID,
      ]
    ))

  const [present] = useIonActionSheet();

  const [clickedItem, setClickedItem] = useState<CalcListItem | null>(null)
  const [presentDetail, dismissDetail] = useIonModal(CalcDetailModal, {
    dismiss: () => dismissDetail(),
    item: clickedItem,
  });

  function handleEdit(itemID: string) {
    setEditingItemID(itemID)   
    console.log("editing item id set to:", editingItemID)
  }

  function handleItemClick(item: CalcListItem) {
    setClickedItem(() => item)

    presentDetail({
      breakpoints: [0, 0.2, 0.4, 0.6, 0.8, 1.0],
      initialBreakpoint: 0.6,
    })
  }

  return (
    <IonList lines="full">
      {items.map(item => (
        <IonItemSliding key={item.id}>
          <IonItem
            button
            onClick={() => handleItemClick(item)}
          >
            <IonLabel>
              <h3>{item.calcInfo.username}</h3>
              <p>
                {`${item.calcInfo.sex}, ${item.calcInfo.age} yo, ${item.calcInfo.height} cm, ${item.calcInfo.weight} kg`}
              </p>
            </IonLabel>
            <IonChip color={getColorFromBMI(item.bmi as number)}>
              {getBMIClassification(item.bmi!)}
            </IonChip>
          </IonItem>

          <IonItemOptions side="end">
            <IonItemOption 
              // disabled 
              expandable 
              color="tertiary" 
              onClick={() => handleEdit(item.id)}
            >
              <IonIcon slot="icon-only" icon={createOutline} />
            </IonItemOption>

            <IonItemOption
              expandable
              color="danger"
              onClick={() => present({
                header: "Do you really want to remove this item?",
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
                    removeItem(item.id);
                }
              })}
            >
              <IonIcon slot="icon-only" icon={trashOutline} />
            </IonItemOption>
          </IonItemOptions>

        </IonItemSliding>
      ))}
    </IonList>
  )
}

import { IonButton, IonIcon, IonInput, IonItem, IonSelect, IonSelectOption } from "@ionic/react";
import { Importance } from "../lib/types";
import { useEffect, useState } from "react";
import { add } from "ionicons/icons";

type ItemFormProps = {
  onAddOrUpdate?: (input: string, importance: Importance) => void;
  onSelectedImportanceChange?: (importance: Importance) => void;
  onInputChange?: (inputText: string) => void;
  editingText?: string;
};

const ItemForm: React.FC<ItemFormProps> = ({
  onAddOrUpdate,
  onSelectedImportanceChange,
  onInputChange,
  editingText
}) => {
  const [inputText, setInputText] = useState<string>("");
  const [selectedImportance, setSelectedImportance] = useState<Importance>("low");

  // Update when editing text changes
  useEffect(() => {
    if (editingText !== undefined) setInputText(editingText);
  }, [editingText]);

  return (
    <IonItem>
      <IonInput
        type="text"
        fill="solid"
        label="New item"
        labelPlacement="floating"
        value={inputText}
        onIonInput={(e) => {
          setInputText(e.target.value as string);
          if (onInputChange)
            onInputChange(inputText);
        }}
        onKeyDown={(e) => {
          if (e.key === "Enter" && onAddOrUpdate) {
            onAddOrUpdate(inputText, selectedImportance);
            setInputText("");
          }
        }}
      />

      <IonSelect
        slot="end"
        placeholder="Select Importance"
        value={selectedImportance}
        onIonChange={(e) => {
          setSelectedImportance(e.detail.value);
          if (onSelectedImportanceChange)
            onSelectedImportanceChange(selectedImportance);
        }}
      >
        <IonSelectOption value="low">Low</IonSelectOption>
        <IonSelectOption value="medium">Medium</IonSelectOption>
        <IonSelectOption value="high">High</IonSelectOption>
      </IonSelect>

      {onAddOrUpdate && (
        <IonButton slot="end" shape="round" onClick={() => {
          onAddOrUpdate(inputText, selectedImportance);
          setInputText("");
        }}>
          <IonIcon slot="icon-only" icon={add} />
        </IonButton>
      )}
    </IonItem>
  );
}

export default ItemForm;


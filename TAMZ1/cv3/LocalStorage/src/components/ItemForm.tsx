import { IonButton, IonIcon, IonInput, IonSelect, IonSelectOption } from "@ionic/react";
import { Importance } from "../lib/types";
import { useState } from "react";
import { add } from "ionicons/icons";

const ItemForm = ({ onAddOrUpdate, onSelectedImportanceChange, onInputChange }: {
  onAddOrUpdate?: (input: string, importance: Importance) => void;
  onSelectedImportanceChange?: (importance: Importance) => void;
  onInputChange?: (inputText: string) => void;
}) => {
  const [inputText, setInputText] = useState<string>("");
  const [selectedImportance, setSelectedImportance] = useState<Importance>("low");

  return (<>
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
      <IonButton slot="end" onClick={() => {
        onAddOrUpdate(inputText, selectedImportance);
        setInputText("");
      }}>
        <IonIcon icon={add} />
      </IonButton>
    )}
  </>);
}

export default ItemForm;


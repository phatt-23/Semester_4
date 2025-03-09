import { useState } from "react";
import { IonContent, IonFooter, IonHeader, IonPage, IonTitle, IonToolbar } from "@ionic/react";
import { Importance, ListItem } from "../lib/types";
import useItemList from "../hooks/useItemList";
import ItemList from "../components/ItemList";
import ItemForm from "../components/ItemForm";

function Home() {
  const { items, addItem, removeItem, updateItem } = useItemList();
  const [editingItemId, setEditingItemId] = useState<number | null>(null);
 
  const handleAddOrUpdate = (inputText: string, importance: Importance) => {
    if (!inputText.trim()) return;

    if (editingItemId) {
      const editingItem = items.find(item => item.id == editingItemId);
      if (editingItem) {
        updateItem(editingItemId, { 
          ...editingItem, 
          id: editingItemId, 
          label: inputText, 
          importance: importance 
        });
      }
    } else {
      addItem(inputText, importance);
    }

    setEditingItemId(null);
  }

  const handleItemRemove = (item: ListItem) => {
    removeItem(item.id);
  }

  const handleItemStrikethrough = (item: ListItem) => {
    updateItem(item.id, { ...item, strikethrough: !item.strikethrough });
  }

  const handleItemEdit = (item: ListItem) => {
    setEditingItemId(item.id);
  }

  return (
    <IonPage>
      <IonHeader translucent={true}>
        <IonToolbar>
          <IonTitle>Local Storage</IonTitle>
        </IonToolbar>
      </IonHeader>

      <IonContent fullscreen={true}>
        <ItemList 
          items={items} 
          onItemEditClick={item => handleItemEdit(item)} 
          onItemRemoveClick={item => handleItemRemove(item)}
          onItemStrikethroughClick={item => handleItemStrikethrough(item)}
        ></ItemList>
      </IonContent>

      <IonFooter translucent={true} collapse="fade">
        <IonToolbar>
          <ItemForm 
            onAddOrUpdate={(input, importance) => handleAddOrUpdate(input, importance)}
          ></ItemForm>
        </IonToolbar>
      </IonFooter>
    </IonPage>
  );
};

export default Home;


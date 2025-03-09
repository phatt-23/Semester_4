import { IonButton, IonIcon, IonItem, IonList, IonListHeader } from "@ionic/react";
import { ListItem } from "../lib/types";
import { create, ellipse, remove, trash } from "ionicons/icons";
import { ionColorFromImportance } from "../lib/utils";

type ItemListProps = {
  items: ListItem[];
  onItemStrikethroughClick?: (item: ListItem) => void;
  onItemEditClick?: (item: ListItem) => void;
  onItemRemoveClick?: (item: ListItem) => void;
};

const ItemList: React.FC<ItemListProps> = ({ 
  items, 
  onItemStrikethroughClick, 
  onItemEditClick, 
  onItemRemoveClick 
}) => {
  return (
    <IonList inset={true} lines="none">
      <IonListHeader>Items stored in local storage:</IonListHeader>
      {items.map((item) => (
        <IonItem key={item.id}>
          <IonIcon icon={ellipse} color={ionColorFromImportance(item.importance)} />

          {item.strikethrough ? (
            <del>{item.label}</del>
          ) : (
            <>{item.label}</>
          )}

          {onItemStrikethroughClick && (
            <IonButton slot="end" onClick={() => onItemStrikethroughClick(item)}>
              <IonIcon icon={remove}/>
            </IonButton>
          )}

          {onItemEditClick && (
            <IonButton slot="end" onClick={() => onItemEditClick(item)}>
              <IonIcon icon={create} />
            </IonButton>
          )}

          {onItemRemoveClick && (
            <IonButton slot="end" onClick={() => onItemRemoveClick(item)}>
              <IonIcon icon={trash}/>
            </IonButton>
          )}
        </IonItem>
      ))}
    </IonList>
  );
};

export default ItemList;


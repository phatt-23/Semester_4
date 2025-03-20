import { IonButton, IonButtons, IonIcon, IonItem, IonItemOption, IonItemOptions, IonItemSliding, IonLabel, IonList, IonListHeader } from "@ionic/react";
import { ListItem } from "../lib/types";
import { checkbox, create, ellipse, remove, trash } from "ionicons/icons";
import { ionColorFromImportance } from "../lib/utils";

type ItemListProps = {
  items: ListItem[];
  onItemStrikethroughClick?: (item: ListItem) => void;
  onItemEditClick?: (item: ListItem) => void;
  onItemRemoveClick?: (item: ListItem) => void;
  selectedEditItemId?: number | null;
};

const ItemList: React.FC<ItemListProps> = ({ 
  items, 
  onItemStrikethroughClick, 
  onItemEditClick, 
  onItemRemoveClick,
  selectedEditItemId
}) => {
  return (
    <IonList inset={true} lines="full">
      <IonListHeader>Items stored in local storage:</IonListHeader>
      {items.map((item) => (
        <IonItemSliding>
          <IonItem 
            key={item.id} 
            button={true} 
            color={item.id == selectedEditItemId ? "light" : ""}
            onClick={() => onItemStrikethroughClick && onItemStrikethroughClick(item)}
          >
            {/* Colored icon */}
            <IonIcon 
              icon={item.strikethrough ? checkbox : ellipse} 
              color={ionColorFromImportance(item.importance)} 
              slot="start"
            />

            {/* Normal or strikenthrouged text */}
            <IonLabel className="text-wrap">
              {item.strikethrough ? <del>{item.label}</del> : <>{item.label}</>}
            </IonLabel>
          </IonItem>

          {onItemEditClick && (
            <IonItemOptions side="start" onIonSwipe={() => onItemEditClick(item)}>
                <IonItemOption color="success" expandable={true}>
                  <IonIcon slot="icon-only" icon={create} onClick={() => onItemEditClick(item)}></IonIcon>
                </IonItemOption>
            </IonItemOptions>
          )}

          {onItemRemoveClick && (
            <IonItemOptions side="end">
                <IonItemOption color="danger" expandable={true}>
                  <IonIcon slot="icon-only" icon={trash} onClick={() => onItemRemoveClick(item)}></IonIcon>
                </IonItemOption>
            </IonItemOptions>
          )}
        </IonItemSliding>
      ))}
    </IonList>
  );
};

export default ItemList;


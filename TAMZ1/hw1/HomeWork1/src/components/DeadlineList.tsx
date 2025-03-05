import { IonIcon, IonItem, IonLabel, IonList } from "@ionic/react";
import { ellipse } from "ionicons/icons";
import { memo } from "react";
import { Deadline, getDaysUntil } from '../data/Deadline';


export interface DeadlineListProps {
  list: Deadline[];
}

export const DeadlineList: React.FC<DeadlineListProps> = 
memo(({ list }) => (
  <IonList lines='none'>

    {list.map((deadline, index) => (
      <IonItem key={index}>
        <IonIcon icon={ellipse} color={deadline.color}/>
        <IonLabel>
          {deadline.label}: {getDaysUntil(deadline.date)} [{deadline.date.toLocaleDateString('en-US')}]
        </IonLabel>
      </IonItem>
    ))}

  </IonList>
));


import { 
  IonDatetimeButton, IonDatetime, IonModal, IonCard, 
  IonCardTitle, IonCardContent, IonCardHeader, 
} from "@ionic/react"

import { Deadline, getDaysUntil } from "../data/Deadline";
import { getColorHex, getISODate } from "../lib/utils";


interface CalendarEntryCardProps {
  selectedDate?: Date;
  onChangeSelectedDate: (date: Date) => void;
  highlightedDeadlines: Deadline[];
}

export const CalendarEntryCard: React.FC<CalendarEntryCardProps> = 
({ selectedDate, onChangeSelectedDate, highlightedDeadlines }) => {

  const deadlines = highlightedDeadlines.map((deadline) => {
    return {
      date: getISODate(deadline.date),
      backgroundColor: getColorHex(deadline.color),
    }
  });
  
  if (selectedDate) {
    deadlines.push({
      date: getISODate(selectedDate),
      backgroundColor: getColorHex("primary"),
    })
  }

  return (
    <IonCard>
      <IonCardHeader>
        <IonCardTitle>
          <div className="ion-text-center">Zadej datum </div>
        </IonCardTitle>
      </IonCardHeader>

      <IonDatetimeButton datetime="datetime"></IonDatetimeButton>

      <IonModal keepContentsMounted={true}>
        <IonDatetime 
          id="datetime" 
          presentation="date"
          highlightedDates={deadlines}
          onIonChange={(event) => typeof event.detail.value === "string" &&
              onChangeSelectedDate(new Date(event.detail.value))
          }
        />
      </IonModal>

      <IonCardContent>
        Pocet dnu do zvoleneho data: {selectedDate ? getDaysUntil(selectedDate) : "---"}
      </IonCardContent>
    </IonCard>
  );
};


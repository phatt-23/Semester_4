import { 
  IonCard, 
  IonCardContent,
  IonDatetime,
  IonDatetimeButton,
  IonModal
} from "@ionic/react"
import { useState } from "react"
import { useTimeSpanStore } from "../stores/TimeSpanStore"
import { useShallow } from "zustand/shallow"

const TimeSpanSelectCard = () => {
  const [startDate, endDate, setStartDate, setEndDate] = useTimeSpanStore(useShallow(s => 
    [s.startDate, s.endDate, s.setStartDate, s.setEndDate]))

  const selectedDates = [startDate.toISOString(), endDate.toISOString()].map(x => ({ date: x, backgroundColor: "primary" }))

  return (
    <IonCard>
      <IonCardContent>
        <IonDatetimeButton datetime="datetime" />

        <IonModal keepContentsMounted={true}>
          <IonDatetime 
            id="datetime" 
            presentation="date"
            showDefaultButtons={true}
            highlightedDates={selectedDates}
            onIonChange={(event) => {
              if (typeof event.detail.value !== "string") return 

              const clickedDate = new Date(event.detail.value)
              console.log("clicked date:", clickedDate)

              const dates = [clickedDate, startDate, endDate]
              // TODO:
              // clickedDate.getTime()
              //
              // if (clickedDate.getTime()  Math.min(...dates.map(x => x.getTime()))) {
              //   setStartDate(clickedDate)
              // } else {
              //   setEndDate(clickedDate)
              // }
              //
              console.log("start date:", startDate)
              console.log("end date:", endDate)
            }}
          />
        </IonModal>
      </IonCardContent>
    </IonCard>
  ) 
}

export default TimeSpanSelectCard

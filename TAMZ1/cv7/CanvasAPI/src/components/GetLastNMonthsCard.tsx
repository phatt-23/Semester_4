import {
  IonButton,
  IonCard,
  IonCardContent,
  IonCol,
  IonGrid,
  IonInput,
  IonItem,
  IonLabel,
  IonLoading,
  IonRow,
  IonToast
} from "@ionic/react"
import { useCurrencyHistoryStore } from '../stores/CurrencyHistory'
import { useShallow } from "zustand/shallow"
import { fetchCurrencyRates, getLastNMonths } from "../lib/utils"
import { useState } from "react"
import { useNMonthsStore } from "../stores/nMonthsStore"

const GetLastNMonthsCard: React.FC = () => {
  const [addRatesForDate, fetchedDates, addFetchedDate] = useCurrencyHistoryStore(useShallow(s => [
    s.addRatesForDate, s.fetchedDates, s.addFetchedDate
  ]))

  const [nMonthsToView, setNMonthsToView] = useNMonthsStore(useShallow(s => [s.nMonthsToView, s.setNMonthsToView]))

  // local state for loading and success/error feedback
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [showToast, setShowToast] = useState<boolean>(false)
  const [toastMessage, setToastMessage] = useState<string>("")

  // selected start and end dates
  const

  // load the history
  async function loadRates() {
    setIsLoading(true) // show loading indicator
    setToastMessage("") // reset any previous toast messages

    try {


      getLastNMonths(nMonthsToView).forEach(date => {
        console.info(fetchedDates, date)

        if (fetchedDates.has(date)) {
          console.info("Skipping")
          return
        }

        addFetchedDate(date)

        fetchCurrencyRates(date).then(rates => {
          addRatesForDate(date, rates)
        }).catch(error => {
          console.error(error)
          setToastMessage("Error fetching data for " + date)
          setShowToast(true)
        })
      })

      setToastMessage("Rates fetched successfully!")
      setShowToast(true)
    } catch (error) {
      console.error(error)
      setToastMessage("Something went wrong. Please try again.")
      setShowToast(true)
    } finally {
      setIsLoading(false) // hide loading indicator
    }
  }

  return (
    <IonCard>
      <IonCardContent>
        <IonLabel position="stacked">Look back how many months?</IonLabel>
        <IonItem lines="none">
          <IonGrid>
            <IonRow>
              <IonCol size="8">
                <IonInput
                  type="number"
                  min={10}
                  max={1_000}
                  defaultValue={100}
                  placeholder="Enter number of months"
                  onIonChange={({ detail }) => { 
                    if (typeof detail.value === "string")
                      setNMonthsToView( Number.parseInt(detail.value) )
                  }}
                  onKeyDown={(e) => {
                    if (e.code == "Enter")
                      loadRates()
                  }}
                  fill="outline"
                />
              </IonCol>
              <IonCol size="4">
                <IonButton
                  expand="block"
                  onClick={loadRates}
                  disabled={isLoading}
                  color="primary"
                  style={{ height: "100%", paddingBottom: 8 }}
                >
                  {isLoading ? 'Fetching...' : 'Fetch Rates'}
                </IonButton>
              </IonCol>
            </IonRow>
          </IonGrid>
        </IonItem>
      </IonCardContent>

      <IonLoading isOpen={isLoading} message="Fetching currency rates..." />

      <IonToast
        isOpen={showToast}
        message={toastMessage}
        duration={3000}
        onDidDismiss={() => setShowToast(false)}
        color={toastMessage.includes("Error") ? "danger" : "success"}
      />
    </IonCard>
  )
}

export default GetLastNMonthsCard

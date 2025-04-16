import {
  IonButton,
  IonChip,
  IonCol,
  IonContent,
  IonFooter,
  IonGrid,
  IonHeader,
  IonItem,
  IonLabel,
  IonList,
  IonPage,
  IonRow,
  IonSearchbar,
  IonToolbar
} from "@ionic/react"

import { useState } from "react"
import { useShallow } from "zustand/shallow"
import { useCurrencyListStore } from "../stores/CurrencyList"

type CurrencySelectModalProps = {
  dismiss: () => void
}

export const CurrencySelectModal: React.FC<CurrencySelectModalProps> = ({ dismiss }) => {
  const [currencList, setSelected] = useCurrencyListStore(useShallow(state => [
    state.list, 
    state.setSelected,
  ]))

  const [searchText, setSearchText] = useState<string>("")

  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonSearchbar
            debounce={100}
            value={searchText}
            placeholder="Search currency by name, code, or country"
            onIonInput={({ detail }) => setSearchText(detail.value as string)}>
          </IonSearchbar>
        </IonToolbar>
      </IonHeader>
      <IonContent>
        <IonList lines="full">
          {currencList
            .filter(currency =>
              currency.code.toLowerCase().includes(searchText.toLowerCase()) ||
              currency.countryLabel.toLowerCase().includes(searchText.toLowerCase()) ||
              currency.currencyLabel.toLowerCase().includes(searchText.toLowerCase())
            )
            .map((item, index) => (
              <IonItem
                key={index}
                button
                onClick={() => {
                  setSelected([item.code])
                  dismiss()
                }}
              >
                <IonGrid>
                  <IonRow className="ion-align-items-center">
                    {/* Currency Code & Name */}
                    <IonCol size="8">
                      <IonLabel>
                        <strong>{item.code}</strong> - {item.currencyLabel} ({item.countryLabel})
                      </IonLabel>
                    </IonCol>
                    
                    {/* Exchange Rate */}
                    <IonCol size="4" className="ion-text-right">
                      <IonChip color="primary">
                        {(item.rate / item.unit).toFixed(2)}
                      </IonChip>
                    </IonCol>
                  </IonRow>
                </IonGrid>
              </IonItem>
            ))}
        </IonList>
      </IonContent>
      <IonFooter className="ion-padding">
        <IonButton expand="block" color="medium" onClick={dismiss}>
          Close
        </IonButton>
      </IonFooter>
    </IonPage>
  )
}


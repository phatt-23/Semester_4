import {
  IonCard,
  IonCardContent,
  IonChip,
  IonCol,
  IonGrid,
  IonItem,
  IonLabel,
  IonRow,
  useIonModal
} from "@ionic/react"
import { useCurrencyListStore } from "../stores/CurrencyList"
import { useShallow } from "zustand/shallow"
import { CurrencySelectModal } from "./CurrencySelectModal"

const CurrencySelectCard: React.FC = () => {
  const [currencyList, selectedCurrencies] = useCurrencyListStore(useShallow((s) => [s.list, s.selected]))
  const [presentModal, dismissModal] = useIonModal(CurrencySelectModal, { 
    dismiss: () => dismissModal() 
  })

  function handleModalOpen() {
    presentModal()
  }

  return (
    <IonCard>
      <IonCardContent>
        <IonItem button onClick={handleModalOpen} className="ion-activatable ripple-parent" lines="full">
          <IonLabel className="ion-text-wrap">
            {selectedCurrencies.length !== 0
              ? (
                <IonGrid>
                  <IonRow className="ion-align-items-center">
                    {/* Currency Code & Name */}
                    <IonCol size="8">
                      <IonLabel>
                        <strong>{currencyList.find(x => x.code == selectedCurrencies[0])?.code}</strong> - {currencyList.find(x => x.code == selectedCurrencies[0])?.currencyLabel}
                      </IonLabel>
                    </IonCol>

                    {/* Exchange Rate */}
                    <IonCol size="4" className="ion-text-right">
                      <IonChip color="primary">
                        {currencyList.find(x => x.code == selectedCurrencies[0])!.rate / currencyList.find(x => x.code == selectedCurrencies[0])!.unit}
                      </IonChip>
                    </IonCol>
                  </IonRow>
                </IonGrid>
              ) : (
                <IonGrid>
                  <IonRow className="ion-align-items-center">
                    <IonCol size="8">
                      <IonLabel>Select Currency</IonLabel>
                    </IonCol>
                    <IonCol size="4" className="ion-text-right">
                      <IonLabel color="danger">(Required)</IonLabel>
                    </IonCol>
                  </IonRow>
                </IonGrid>
              )}
          </IonLabel>
        </IonItem>
      </IonCardContent>
    </IonCard >
  )
}

export default CurrencySelectCard

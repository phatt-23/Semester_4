import {
  IonContent,
  IonHeader,
  IonPage,
  IonTitle,
  IonToolbar,
} from '@ionic/react'
import QueryCard from '../components/QueryCard'
import ResponseCard from '../components/ResponseCard'
import ActionButtonsCard from '../components/ActionButtonsCard'


const Home: React.FC = () => (
  <IonPage>
    <IonHeader>
      <IonToolbar>
        <IonTitle>HTTP</IonTitle>
      </IonToolbar>
    </IonHeader>
    <IonContent fullscreen>
      <IonHeader collapse="condense">
        <IonToolbar>
          <IonTitle size="large">HTTP</IonTitle>
        </IonToolbar>
      </IonHeader>

      <QueryCard />
      <ResponseCard />
      <ActionButtonsCard />

    </IonContent>
  </IonPage>
)

export default Home;

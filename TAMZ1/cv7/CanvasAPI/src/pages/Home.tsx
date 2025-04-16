import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar } from '@ionic/react';
import './Home.css';
import CurrencySelectCard from '../components/CurrencySelectCard'
import CurrencyRatesCanvasCard from '../components/CurrencyRatesCanvasCard';
import GetLastNMonths from '../components/GetLastNMonthsCard';
import GetLastNMonthsCard from '../components/GetLastNMonthsCard';
import TimeSpanSelectCard from '../components/TimeSpanSelectCard';

const Home: React.FC = () => {

  // components vars
  const title = "Canvas API"


  return (
    <IonPage>
      <IonHeader>
        <IonToolbar>
          <IonTitle>{title}</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen>
        <IonHeader collapse="condense">
          <IonToolbar>
            <IonTitle size="large">{title}</IonTitle>
          </IonToolbar>
        </IonHeader>

        <CurrencySelectCard />
        <TimeSpanSelectCard />
        <GetLastNMonthsCard />
        <CurrencyRatesCanvasCard />

      </IonContent>
    </IonPage>
  );
};

export default Home;

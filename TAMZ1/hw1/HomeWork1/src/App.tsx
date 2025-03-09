import {
  IonApp,
  IonCard,
  IonContent,
  IonHeader,
  IonTitle,
  IonToolbar,
  isPlatform,
  setupIonicReact
} from '@ionic/react';

/* Core CSS required for Ionic components to work properly */
import '@ionic/react/css/core.css';

/* Basic CSS for apps built with Ionic */
import '@ionic/react/css/normalize.css';
import '@ionic/react/css/structure.css';
import '@ionic/react/css/typography.css';

/* Optional CSS utils that can be commented out */
import '@ionic/react/css/padding.css';
import '@ionic/react/css/float-elements.css';
import '@ionic/react/css/text-alignment.css';
import '@ionic/react/css/text-transformation.css';
import '@ionic/react/css/flex-utils.css';
import '@ionic/react/css/display.css';

/* Ionic Dark Mode */
import '@ionic/react/css/palettes/dark.system.css';

/* Theme variables */
import './theme/variables.css';


import { StatusBar, Style } from '@capacitor/status-bar';
import { useEffect } from 'react';

import { TodaysDateCard } from './components/TodaysDateCard';
import { DeadlineList } from './components/DeadlineList';
import { CalendarEntryCard } from './components/CalendarEntryCard';
import { ZodiacSignCard } from './components/ZodiacSignCard';
import { useDeadlines } from './hooks/useDeadlines';


setupIonicReact();

const App: React.FC = () => {
  useEffect(() => {
    if (isPlatform("hybrid")) {
      StatusBar.setOverlaysWebView({ overlay: false });
      StatusBar.setStyle({ style: Style.Default });
    } 
  },[]);

  const { deadlines, selectedDate, setSelectedDate } = useDeadlines();

  return (
    <IonApp>
      <IonHeader>
        <IonToolbar>
          <IonTitle>Terminy</IonTitle>
        </IonToolbar>
      </IonHeader>
      <IonContent fullscreen={true} forceOverscroll={false}>
        <TodaysDateCard />

        <IonCard>
          <DeadlineList list={deadlines} />
        </IonCard>

        <CalendarEntryCard 
          selectedDate={selectedDate} 
          onChangeSelectedDate={(date) => setSelectedDate(date)}
          highlightedDeadlines={deadlines} 
        />

        <ZodiacSignCard selectedDate={selectedDate} />
      </IonContent>
    </IonApp>
  );
}

export default App;


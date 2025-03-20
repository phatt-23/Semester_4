import { Redirect, Route } from 'react-router-dom';
import {
  IonApp,
  IonIcon,
  IonLabel,
  IonRouterOutlet,
  IonTabBar,
  IonTabButton,
  IonTabs,
  isPlatform,
  setupIonicReact
} from '@ionic/react';
import { IonReactRouter } from '@ionic/react-router';
import { calculator, calculatorOutline, list, listOutline } from 'ionicons/icons';

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

import '@ionic/react/css/palettes/dark.system.css';

/* Theme variables */
import './theme/variables.css';

import { useEffect } from 'react';
import { StatusBar, Style } from '@capacitor/status-bar';
import { Keyboard, KeyboardResize } from '@capacitor/keyboard';
import CalculatorTab from './pages/CalculatorTab';
import CalcsHistoryTab from './pages/CalcsHistoryTab';

setupIonicReact();

const App: React.FC = () => {
  useEffect(() => {
    if (isPlatform("hybrid")) {
      StatusBar.setOverlaysWebView({ overlay: false });
      StatusBar.setStyle({ style: Style.Light });
      Keyboard.setScroll({ isDisabled: false });
      Keyboard.setResizeMode({ mode: KeyboardResize.Native });
    } 
  },[]);

  return (
    <IonApp>
      <IonReactRouter>
        <IonTabs>
          <IonRouterOutlet>
            <Route exact path="/calculator">
              <CalculatorTab />
            </Route>
            <Route exact path="/history">
              <CalcsHistoryTab />
            </Route>
            <Route exact path="/">
              <Redirect to="/calculator" />
            </Route>
          </IonRouterOutlet>
          <IonTabBar id="tab-bar" slot="bottom">
            <IonTabButton tab="tab1" href="/calculator">
              <IonIcon aria-hidden="true" icon={calculatorOutline} />
              <IonLabel>Calculator</IonLabel>
            </IonTabButton>
            <IonTabButton tab="tab2" href="/history">
              <IonIcon aria-hidden="true" icon={listOutline} />
              <IonLabel>History</IonLabel>
            </IonTabButton>
          </IonTabBar>
        </IonTabs>
      </IonReactRouter>
    </IonApp>
  );
}

export default App;

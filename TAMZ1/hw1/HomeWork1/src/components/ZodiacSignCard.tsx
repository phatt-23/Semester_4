import { firstLetterUppercase } from "../lib/utils";
import { IonCard, IonCardContent, IonCardHeader, IonCardTitle, IonImg, IonText } from "@ionic/react";
import "./ZodiacSignCard.css";

// Import images explicitly
import kozoroh from "../assets/imgs/kozoroh.png";
import vodnar from "../assets/imgs/vodnar.png";
import ryby from "../assets/imgs/ryby.png";
import beran from "../assets/imgs/beran.png";
import byk from "../assets/imgs/byk.png";
import blizenci from "../assets/imgs/blizenci.png";
import rak from "../assets/imgs/rak.png";
import lev from "../assets/imgs/lev.png";
import panna from "../assets/imgs/panna.png";
import vahy from "../assets/imgs/vahy.png";
import stir from "../assets/imgs/stir.png";
import strelec from "../assets/imgs/strelec.png";
import { memo, useMemo } from "react";

// Map zodiac names to their respective images
const zodiacImages: Record<string, string> = {
  kozoroh, 
  vodnar, 
  ryby, 
  beran, 
  byk, 
  blizenci, 
  rak, 
  lev, 
  panna, 
  vahy, 
  stir, 
  strelec
};



interface ZodiacSignCardProps {
  selectedDate?: Date;
}


export const ZodiacSignCard: React.FC<ZodiacSignCardProps> = 
memo(({ selectedDate }) => {

  const zodiacNames = useMemo(() => [ 
    "kozoroh", 
    "vodnar", 
    "ryby", 
    "beran", 
    "byk", 
    "blizenci", 
    "rak", 
    "lev", 
    "panna", 
    "vahy", 
    "stir", 
    "strelec" 
  ], []); 

  const breakDate = useMemo(() => [ 
    21, 20, 21, 21, 21, 22, 
    23, 24, 23, 23, 23, 22 
  ], []);

  let monthIndex: number 

  if (selectedDate) {
    monthIndex = selectedDate.getMonth();
    if (selectedDate.getDate() >= breakDate[selectedDate.getMonth()]) 
      monthIndex += 1;

    monthIndex %= zodiacNames.length;
  } else {
    monthIndex = new Date().getMonth();
  }

  const displayName = firstLetterUppercase(zodiacNames[monthIndex]);
  const imagePath = zodiacImages[zodiacNames[monthIndex]];

  return (
    <IonCard>
      <IonCardHeader>
        <IonCardTitle>
          Zverokruh
        </IonCardTitle>
      </IonCardHeader>
      <IonCardContent>
        <IonImg className="center" src={imagePath} alt={imagePath}></IonImg>
        <IonText>{displayName}</IonText> 
      </IonCardContent>
    </IonCard>
  );
});


import { useCallback, useEffect, useState } from "react";
import { Deadline } from "../data/Deadline";
import { Preferences } from "@capacitor/preferences";

export const DEADLINES_STORAGE_KEY = 'deadlines';

export function useDeadlines() {
  const [deadlines, setDeadlines] = useState<Deadline[]>([
    { date: new Date("2025-05-17"), label: "Konec semestru", color: "danger", },
    { date: new Date("2025-03-26"), label: "Vedecka rada",   color: "success", },
    { date: new Date("2025-04-23"), label: "Sportovni den",  color: "primary", },
  ]);

  const [selectedDate, setSelectedDate] = useState<Date | undefined>();

  const addDeadline = useCallback((newDeadline: Deadline) => {
    setDeadlines(prevDeadlines => [newDeadline, ...prevDeadlines]);
  }, []);


  useEffect(() => {
    const loadSaved = async () => {
      const {value} = await Preferences.get({ key: DEADLINES_STORAGE_KEY }); 
      const deadlinesInPreferences = (value ? JSON.parse(value) : []) as Deadline[];
      setDeadlines(prevDeadlines => [...deadlinesInPreferences, ...prevDeadlines]); 
    };
    loadSaved();
  }, []);

  return { 
    deadlines, 
    setDeadlines, 
    addDeadline,
    selectedDate,
    setSelectedDate,
  } as const;
}

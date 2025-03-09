import { useEffect, useRef, useState } from "react";
import { iota } from "../lib/utils";
import { Importance, ListItem } from "../lib/types";
import { Preferences } from "@capacitor/preferences";
import { isPlatform } from "@ionic/react";

const ITEM_LIST_STORAGE_KEY = "ITEM_LIST_STORAGE";

function useItemList() {
  // state
  const [items, setItems] = useState<ListItem[]>([]);
  const localIota = useRef(iota());

  // provided functions
  const addItem = async (label: string, importance: Importance) => {
    const item: ListItem = {
      id: localIota.current(),
      label: label,
      importance: importance,
      strikethrough: false,
    };

    setItems(prevItems => [...prevItems, item]);
  };

  const removeItem = async (id: number) => {
    setItems(prevItems => prevItems.filter(item => item.id != id))
  }

  const updateItem = async (id: number, newItem: ListItem) => {
    setItems(prevItems => prevItems.map(item => item.id == id ? newItem : item));
  }

  // load items from the storage on mount
  useEffect(() => {
    const loadItemsFromStorageNative = async () => {
      const { value } = await Preferences.get({ key: ITEM_LIST_STORAGE_KEY });
      const parsedList = (value ? JSON.parse(value) : []) as ListItem[];
      setItems(prev => [...prev, ...parsedList]); 
    };
  
    const loadItemsFromStorageWeb = () => {
      const value = localStorage.getItem(ITEM_LIST_STORAGE_KEY);
      const parsedList = (value ? JSON.parse(value) : []) as ListItem[];
      setItems(prev => [...prev, ...parsedList]); 
    };

    if (isPlatform('hybrid'))
      loadItemsFromStorageNative();
    else
      loadItemsFromStorageWeb(); 
  }, []);

  useEffect(() => {
    const updateStorageWeb = () => {
      localStorage.setItem(ITEM_LIST_STORAGE_KEY, JSON.stringify(items));
    };

    const updateStorageNative = async () => {
      await Preferences.set({ key: ITEM_LIST_STORAGE_KEY, value: JSON.stringify(items) });
    };
    
    if (isPlatform('hybrid'))
      updateStorageNative();
    else
      updateStorageWeb();
  }, [items]);

  return {
    items, 
    setItems,
    addItem,
    removeItem,
    updateItem,
  } as const;
}

export default useItemList;


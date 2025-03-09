import { Importance } from "./types";

export function iota(): () => number {
  let id = 0;

  function increment() {
    return id++;
  }

  return increment;
}


export function ionColorFromImportance(importance: Importance) {
  switch (importance) {
    case "low":     
      return "success";
    case "medium":  
      return "primary";
    case "high":    
      return "danger";
  }
}

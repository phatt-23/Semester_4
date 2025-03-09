
export type Importance = "low" | "medium" | "high";

export type ListItem = {
  id: number;
  label: string;
  importance: Importance;
  strikethrough: boolean;
}

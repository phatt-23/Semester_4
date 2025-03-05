export interface Deadline {
  date: Date,
  label: string,
  color: string,
}

export const getDaysUntil = (untilDate: Date) => Math.floor((untilDate.getTime() - (new Date()).getTime()) / (1000 * 60 * 60 * 24)) + 1;

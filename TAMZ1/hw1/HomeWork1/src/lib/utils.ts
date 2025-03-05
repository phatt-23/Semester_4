export function firstLetterUppercase(text: string) {
  return text.charAt(0).toUpperCase() + text.slice(1);
}


export function getColorHex(ionicColor: string): string {
  const colorMap: Record<string, string> = {
    danger: "#ff4d4d",    // Red
    success: "#28a745",   // Green
    primary: "#007bff",   // Blue
    warning: "#ffc107",   // Yellow
    secondary: "#6c757d", // Gray
  };
  return colorMap[ionicColor] || "#ffffff"; // Default to white if not found
};


export function getISODate(date: Date) {
  return date.toISOString().split('T')[0];
}

import { BMIClassification } from "./types"

export function getBMIClassification(bmiScore: number)
{
  if (bmiScore < 16) return BMIClassification.SEVERE_THINNESS
  if (bmiScore < 17) return BMIClassification.MODERATE_THINNESS
  if (bmiScore < 18.5) return BMIClassification.MILD_THINNESS
  if (bmiScore < 25) return BMIClassification.NORMAL
  if (bmiScore < 30) return BMIClassification.OVERWEIGHT
  if (bmiScore < 35) return BMIClassification.OBESE_CLASS_I
  if (bmiScore < 40) return BMIClassification.OBESE_CLASS_II
  return BMIClassification.OBESE_CLASS_III
}

export function getColorFromBMI(bmiScore: number)
{
  if (bmiScore < 18.5) return "primary"
  if (bmiScore < 30) return "success"
  return "danger"
}

export function calculateBmi(weight: number, height: number)
{
  return weight * 10000 / (height * height)
}

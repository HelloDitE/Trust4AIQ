export type PollutantStatus = "Bon" | "Moyen" | "Mauvais";

export interface Pollutant {
  id: string;
  name: string;
  value: number;
  unit: string;
  threshold: number;
  status: PollutantStatus;
  description: string;
}
export type RiskLevel = "OPTIMAL" | "MODÉRÉ" | "ÉLEVÉ" | "CRITIQUE";

export type PollutantStatus = "BON" | "MODERE" | "ELEVE" | "CRITIQUE";

export interface PollutantData {
  value: number;
  limit: number;
  unit: string;
  status: PollutantStatus;
}

export interface Patient {
  id: string;
  vuln_score: number;
  risk_score: number;
  risk_category: RiskLevel;
  actions: string[];
}


export interface DashboardData {
  patients: Patient[];
  most_critical_patient: Patient;
  pollutants: Record<string, PollutantData>;
  selected_patient_id: string;
  risk_score: number;
  risk_category: RiskLevel;
  actions: string[];
  last_update: string;
}
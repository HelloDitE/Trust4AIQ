from config.settings import POLLUTANTS_REF

class RiskEngine:
    @staticmethod
    def calculate_pollutant_index(measurements: dict) -> float:
        """
        Calcule l'Index Global (I_global) basé sur le pire polluant.
        measurements: dictionnaire ex: {"CO2": 1200, "PM2.5": 15}
        """
        max_index = 0.0
        
        for pollutant, value in measurements.items():
            if pollutant in POLLUTANTS_REF:
                limit = POLLUTANTS_REF[pollutant]["limit"]
                # Formule : Valeur / Limite
                # Attention aux unités ! On suppose ici que les unités d'entrée sont correctes.
                current_index = value / limit
                
                if current_index > max_index:
                    max_index = current_index
                    
        return max_index

    @staticmethod
    def calculate_patient_risk(patient_vuln_score: float, global_pollutant_index: float) -> float:
        """
        Formule : Risk = Index_Polluant * (1 + Vulnérabilité)
        """
        return global_pollutant_index * (1 + patient_vuln_score)

    @staticmethod
    def get_risk_category(risk_score: float) -> str:
        """Retourne la couleur/catégorie de l'alerte"""
        if risk_score < 1.0:
            return "VERT"
        elif 1.0 <= risk_score < 1.5:
            return "JAUNE"
        elif 1.5 <= risk_score < 2.0:
            return "ORANGE"
        else:
            return "ROUGE"
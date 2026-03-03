import pandas as pd
from pathlib import Path
from domain.models import Patient
from core.security import decrypt_data
from config.settings import PATIENTS_REF

EXCEL_PATH = Path("data") / "patients_reels.xlsx"

class PatientService:

    def _evaluate_condition(self, value: float, condition_str: str) -> bool:
        """
        Transforme le texte du JSON (ex: "< 10") en vraie condition mathématique.
        """
        condition_str = condition_str.strip()
        
        try:
            # Cas 1 : Inférieur à (ex: "< 10")
            if condition_str.startswith("<"):
                limit = float(condition_str.replace("<", "").strip())
                return value < limit
                
            # Cas 2 : Supérieur à (ex: "> 65")
            elif condition_str.startswith(">"):
                limit = float(condition_str.replace(">", "").strip())
                return value > limit
                
            # Cas 3 : Intervalle (ex: "10-65")
            elif "-" in condition_str:
                parts = condition_str.split("-")
                min_val = float(parts[0].strip())
                max_val = float(parts[1].strip())
                return min_val <= value <= max_val
                
        except ValueError:
            print(f"Erreur de lecture de la condition : {condition_str}")
            
        return False

    def _calculate_vuln_score(self, patient_data: dict) -> float:
        """Calcule le score 100% dynamiquement depuis patients_ref.json"""
        score = 0.0
        
        # 1. Âge (Lecture dynamique des conditions)
        age = patient_data["age"]
        for category, data in PATIENTS_REF["age"].items():
            if self._evaluate_condition(age, data["condition"]):
                score += data["coeff"]
                break # On a trouvé la bonne tranche d'âge, on arrête la boucle
                
        # 2. Pathologie Respiratoire (Correspondance directe)
        resp = patient_data["respiratory"]
        if resp in PATIENTS_REF["respiratory"]:
            score += PATIENTS_REF["respiratory"][resp]
            
        # 3. Fumeur
        if patient_data["smoking"] == "yes":
            score += PATIENTS_REF["smoking"]["yes"]
            
        # 4. Grossesse
        if patient_data["pregnancy"] == "yes":
            score += PATIENTS_REF["pregnancy"]["yes"]
            
        # 5. Immunité
        immunite = patient_data.get("immune", "no")
        if immunite == "yes" or immunite == "low":
            score += PATIENTS_REF["immuno"]["yes"]
        
        # 6. Post-opératoire
        post_op = patient_data.get("post_op", "no")
        if post_op == "yes":
            score += PATIENTS_REF["post_op"]["yes"]
        
        # 7. Cardio
        cardio = patient_data.get("cardio", "none")
        # On vérifie si la pathologie ("hypertension", etc.) existe dans le JSON
        if cardio in PATIENTS_REF["cardio"]:
            score += PATIENTS_REF["cardio"][cardio]

        # 8. IMC
        bmi = patient_data.get("bmi", 22.0)
        for category, data in PATIENTS_REF["bmi"].items():
            # Dans le JSON, vous aviez peut-être appelé la clé "range" ou "condition" pour l'IMC
            condition_str = data.get("range", data.get("condition", ""))
            
            # On utilise notre super fonction d'évaluation !
            if condition_str and self._evaluate_condition(bmi, condition_str):
                score += data["coeff"]
                break # On a trouvé la bonne tranche d'IMC, on arrête la boucle
        
        return round(score, 2)

    def get_all_patients(self) -> list[Patient]:
        """Lit l'Excel chiffré, le déchiffre et calcule le score"""
        patients_list = []
        try:
            df = pd.read_excel(EXCEL_PATH)
            
            for index, row in df.iterrows():
                # 1. DÉCHIFFREMENT des données de l'Excel
                resp = decrypt_data(str(row["Pathologie_Respiratoire"]))
                cardio = decrypt_data(str(row["Cardio"]))
                fumeur = decrypt_data(str(row["Fumeur"]))
                grossesse = decrypt_data(str(row["Grossesse"]))
                immunite = decrypt_data(str(row["Immunité"]))
                post_op = decrypt_data(str(row["Post-op"]))
                
                # 2. PRÉPARATION du dictionnaire pour le calcul
                p_data = {
                    "age": int(row["Age"]),
                    "gender": str(row["Sexe"]),
                    "bmi": float(row["IMC"]),
                    "respiratory": resp,
                    "cardio": cardio,
                    "smoking": fumeur,
                    "pregnancy": grossesse,
                    "immune": immunite,
                    "post_op": post_op
                }
                
                # 3. CALCUL DU SCORE à la volée
                calculated_score = self._calculate_vuln_score(p_data)
                
                # 4. CRÉATION DE L'OBJET
                p = Patient(
                    id=str(row["ID_Patient"]),
                    **p_data,
                    vuln_score=calculated_score
                )
                patients_list.append(p)
                
            return patients_list
            
        except FileNotFoundError:
            print("❌ Erreur : Fichier patients_reels.xlsx introuvable.")
            return []
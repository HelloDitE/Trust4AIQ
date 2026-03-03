import random
from services.patient_service import PatientService
from services.sensor_service import SensorService
from domain.risk_engine import RiskEngine
from domain.action_engine import ActionEngine

def run_excel_pipeline():
    print("--- 🏥 DÉMARRAGE DU PIPELINE QAI (PROJET 2 - EXCEL) ---")

    # 1. Récupération des données depuis l'Excel (Dernière ligne)
    indoor, outdoor = SensorService.get_latest_measurements()
    
    if not indoor:
        print("❌ Arrêt : Impossible de lire les capteurs. Avez-vous généré l'Excel ?")
        return

    print(f"\n📊 DERNIÈRES MESURES (Extrait de capteurs_reels.xlsx) :")
    print(f"   🏠 Intérieur : CO2={indoor['CO2']}ppm | PM2.5={indoor['PM2.5']}µg/m3 | NO2={indoor['NO2']}µg/m3 | COV={indoor['COV']}µg/m3 | CO={indoor['CO']}mg/m3 | Ozone={indoor['Ozone']}ppb | Radon={indoor['Radon']}Bq/m3 | Formaldéhyde={indoor['Formaldéhyde']}ppb | Humidité={indoor['Humidité']}%")
    print(f"   🌳 Extérieur : PM2.5={outdoor['PM2.5']}µg/m3 | NO2={outdoor['NO2']}µg/m3 | Ozone={outdoor['Ozone']}ppb | Température={outdoor['Temp']}°C")


    # 2. Calcul de l'Index de Pollution Global
    global_pollutant_index = RiskEngine.calculate_pollutant_index(indoor)
    print(f"\n🌍 INDEX POLLUTION (Environnement seul) : {global_pollutant_index:.2f}")

    # 3. Récupération de la cohorte de patients depuis l'Excel
    patient_service = PatientService()
    all_patients = patient_service.get_all_patients()
    
    if not all_patients:
        print("❌ Arrêt : La base de patients Excel est vide ou introuvable.")
        return

    # Tirage au sort d'un patient de l'Excel pour le test
    random_patient = random.choice(all_patients)
    print(f"\n👤 PROFIL PATIENT DÉTECTÉ (Extrait de patients_reels.xlsx) :")
    print(f"   ID: {random_patient.id} | Âge: {random_patient.age} ans | Sexe: {random_patient.gender} | IMC: {random_patient.bmi}")
    print(f"   Pathologie Respiratoire: {random_patient.respiratory} | Fumeur: {random_patient.smoking} | Cardio: {random_patient.cardio} | Post-op: {random_patient.post_op} | Immunité: {random_patient.immune} | Grossesse: {random_patient.pregnancy}")
    print(f"   Score Vulnérabilité: {random_patient.vuln_score}")

    # 4. Calcul du Risque
    risk_score = RiskEngine.calculate_patient_risk(random_patient.vuln_score, global_pollutant_index)
    risk_color = RiskEngine.get_risk_category(risk_score)
    
    print(f"\n🎯 RÉSULTAT DU MODÈLE :")
    print(f"   RISQUE CALCULÉ : {risk_score:.2f}")
    print(f"   NIVEAU D'ALERTE : {risk_color}")

    # 5. Moteur d'Actions
    actions = ActionEngine.determine_actions(indoor, outdoor, risk_score)
    
    print(f"\n📢 ACTIONS RECOMMANDÉES :")
    for action in actions:
        print(f"   👉 {action}")

if __name__ == "__main__":
    run_excel_pipeline()
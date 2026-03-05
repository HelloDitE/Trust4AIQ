from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random

from services.sensor_service import SensorService
from services.patient_service import PatientService
from domain.risk_engine import RiskEngine
from domain.action_engine import ActionEngine
from config.settings import POLLUTANTS_REF

app = FastAPI()

# -----------------------------
# CORS (autorise le frontend)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Sélection patient au démarrage
# -----------------------------
patient_service = PatientService()
all_patients = patient_service.get_all_patients()

if not all_patients:
    raise ValueError("❌ Aucun patient trouvé.")

patients_count = random.randint(1, 10)
selected_patients = random.sample(all_patients, patients_count)

print("🎲 Patients sélectionnés au démarrage :", [p.id for p in selected_patients])

# -----------------------------
# Fonction statut polluant
# -----------------------------
def evaluate_pollutant(value, limit):
    ratio = value / limit

    if ratio <= 1:
        return "BON"
    elif ratio <= 1.2:
        return "MODERE"
    elif ratio <= 1.5:
        return "ELEVE"
    else:
        return "CRITIQUE"


# -----------------------------
# Endpoint principal
# -----------------------------
@app.get("/dashboard")
def get_dashboard():

    # 1️⃣ Capteurs
    indoor, outdoor = SensorService.get_latest_measurements()

    if not indoor:
        return {"error": "Capteurs indisponibles"}

    # 2️⃣ Polluants enrichis
    pollutants_data = {}

    for pollutant, value in indoor.items():
        if pollutant in POLLUTANTS_REF:
            ref = POLLUTANTS_REF[pollutant]
            limit = ref["limit"]
            unit = ref["unit"]

            pollutants_data[pollutant] = {
                "value": value,
                "limit": limit,
                "unit": unit,
                "status": evaluate_pollutant(value, limit)
            }

    # 3️⃣ Index pollution (commun à tous)
    pollutant_index = RiskEngine.calculate_pollutant_index(indoor)
    
    # 4️⃣ Calcul risque pour CHAQUE patient
    patients_results = []

    for patient in selected_patients:

        risk_score = RiskEngine.calculate_patient_risk(
            patient.vuln_score,
            pollutant_index
        )

        risk_category = RiskEngine.get_risk_category(risk_score)

        actions = ActionEngine.determine_actions(
            indoor,
            outdoor,
            risk_score
        )

        patients_results.append({
            "id": patient.id,
            "vuln_score": patient.vuln_score,
            "risk_score": round(risk_score, 2),
            "risk_category": risk_category,
            "actions": actions
        })

    # 5️⃣ Patient le plus vulnérable
    most_critical_patient = max(
        patients_results,
        key=lambda x: x["risk_score"]
    )

    # 6️⃣ Date/heure
    now = datetime.now().strftime("%d/%m %Hh%M")

    # 7️⃣ Retour API
    return {
        "pollutants": pollutants_data,
        "outdoor": outdoor,
        "patients_count": patients_count,
        "patients": patients_results,
        "most_critical_patient": most_critical_patient,
        "last_update": now
    }
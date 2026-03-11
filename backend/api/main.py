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
# Chargement patients
# -----------------------------
patient_service = PatientService()
all_patients = patient_service.get_all_patients()

if not all_patients:
    raise ValueError("❌ Aucun patient trouvé.")

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
# Génération des chambres au démarrage
# -----------------------------
rooms = {}

rooms_count = random.randint(1, 10)

for i in range(rooms_count):

    room_id = str(100 + i)

    # 1️⃣ Capteurs propres à la chambre
    base_indoor, base_outdoor = SensorService.get_latest_measurements()

    #  Variation aléatoire des polluants
    indoor = {}

    for pollutant, value in base_indoor.items():

        variation = random.uniform(-0.3, 0.3)  # ±30%
        new_value = value * (1 + variation)

        indoor[pollutant] = round(max(new_value, 0), 2)

    outdoor = base_outdoor

    # 2️⃣ Sélection patients uniques
    patients_count = random.randint(1, min(10, len(all_patients)))
    selected_patients = random.sample(all_patients, patients_count)

    # 3️⃣ Calcul index pollution
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

    # 6️⃣ Stockage final de la chambre
    rooms[room_id] = {
        "indoor": indoor,
        "outdoor": outdoor,
        "patients": patients_results,
        "most_critical_patient": most_critical_patient
    }

print("🏥 Chambres générées :", list(rooms.keys()))

# -----------------------------
# Endpoint 1 : Liste des chambres
# -----------------------------
@app.get("/rooms")
def get_rooms():

    rooms_summary = []

    # 🔹 Compteurs statistiques
    total_rooms = len(rooms)
    rooms_optimal = 0
    rooms_moderate = 0
    rooms_danger = 0

    for room_id, room_data in rooms.items():

        category = room_data["most_critical_patient"]["risk_category"]
        score = room_data["most_critical_patient"]["risk_score"]

        # 🔹 Comptage catégories
        if category == "OPTIMAL":
            rooms_optimal += 1
        elif category == "MODÉRÉ":
            rooms_moderate += 1
        else:
            rooms_danger += 1

        rooms_summary.append({
            "room_id": room_id,
            "patients_count": len(room_data["patients"]),
            "risk_score": score,
            "risk_category": category
        })

    return {
        "rooms": rooms_summary,
        "stats": {
            "totalRooms": total_rooms,
            "roomsOptimal": rooms_optimal,
            "roomsInVigilance": rooms_moderate,
            "roomsInDanger": rooms_danger
        }
    }

# -----------------------------
# Endpoint 2 : Détail d’une chambre
# -----------------------------
@app.get("/rooms/{room_id}")
def get_room_detail(room_id: str):

    if room_id not in rooms:
        return {"error": "Chambre introuvable"}

    room_data = rooms[room_id]
    indoor = room_data["indoor"]
    outdoor = room_data["outdoor"]

    # 1️⃣ Polluants enrichis
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

    # 2️⃣ Date/heure
    now = datetime.now().strftime("%d/%m %Hh%M")

    # 3️⃣ Retour API
    return {
        "room_id": room_id,
        "pollutants": pollutants_data,
        "outdoor": outdoor,
        "patients_count": len(room_data["patients"]),
        "patients": room_data["patients"],
        "most_critical_patient": room_data["most_critical_patient"],
        "last_update": now
    }
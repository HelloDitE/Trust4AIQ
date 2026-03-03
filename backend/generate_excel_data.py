import pandas as pd
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path

# On ré-importe notre module de sécurité pour chiffrer l'Excel
from core.security import encrypt_data

# Dossier de destination
DATA_DIR = Path("data")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def generate_sensor_excel(rows=100):
    """Génère un historique de mesures de capteurs sur plusieurs heures"""
    print("📊 Génération du fichier Excel des capteurs...")
    
    data = []
    start_time = datetime.now() - timedelta(minutes=10 * rows)
    
    for i in range(rows):
        current_time = start_time + timedelta(minutes=10 * i)
        data.append({
            "Timestamp": current_time.strftime("%Y-%m-%d %H:%M:%S"),
            "CO2": random.randint(400, 1200),
            "PM2.5": random.randint(5, 35),
            "NO2": random.randint(10, 45),
            "COV": random.randint(100, 600),
            "CO": round(random.uniform(0.5, 3.0), 2),
            "Ozone": random.randint(10, 40),
            "Radon": random.randint(20, 150),
            "Formaldéhyde": random.randint(5, 30),
            "Humidité": random.randint(40, 65),
            "Ext_PM2.5": random.randint(10, 50),
            "Ext_NO2": random.randint(15, 50),
            "Ext_Ozone": random.randint(20, 60),
            "Ext_Temp": random.randint(10, 25)
        })
        
    df = pd.DataFrame(data)
    filepath = DATA_DIR / "capteurs_reels.xlsx"
    df.to_excel(filepath, index=False)
    print(f"✅ Fichier sauvegardé : {filepath}")

def generate_patients_excel(rows=50):
    """Génère un fichier Excel de patients bruts (chiffrés) sans calcul de score"""
    print("👤 Génération du fichier Excel des patients (avec chiffrement)...")
    
    data = []
    for _ in range(rows):
        age = random.randint(5, 90)
        gender = random.choice(["M", "F"])
        
        # LOGIQUE RÉALISTE DES PROFILS
        resp = random.choice(["none", "none", "mild", "severe"])
        cardio = random.choice(["none", "hypertension"]) if age > 40 else "none"
        fumeur = random.choice(["yes", "no", "no"]) if age > 15 else "no"
        grossesse = "yes" if (gender == "F" and 18 <= age <= 45 and random.random() < 0.1) else "no"
        immunite = random.choice(["low", "normal", "normal"])
        post_op = random.choice(["yes", "no", "no", "no"])
            
        # ON CHIFFRE LES DONNÉES SENSIBLES AVANT D'ÉCRIRE DANS EXCEL
        data.append({
            "ID_Patient": str(uuid.uuid4())[:8],
            "Age": age,
            "Sexe": gender,
            "IMC": round(random.uniform(18.5, 35.0), 1),
            # Colonnes Chiffrées :
            "Pathologie_Respiratoire": encrypt_data(resp),
            "Cardio": encrypt_data(cardio),
            "Fumeur": encrypt_data(fumeur),
            "Grossesse": encrypt_data(grossesse),
            "Immunité": encrypt_data(immunite),
            "Post-op": encrypt_data(post_op)
            # NOTE: Le Score_Vulnérabilité a été supprimé !
        })
        
    df = pd.DataFrame(data)
    filepath = DATA_DIR / "patients_reels.xlsx"
    df.to_excel(filepath, index=False)
    print(f"✅ Fichier sauvegardé : {filepath}")

if __name__ == "__main__":
    generate_sensor_excel()
    generate_patients_excel()
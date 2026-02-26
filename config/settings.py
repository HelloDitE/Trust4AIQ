#Ce script va lire vos JSON et votre clé secrète pour les rendre disponibles partout dans le projet.

import os
import json
from pathlib import Path
from dotenv import load_dotenv

# 1. Charger les variables du fichier .env
load_dotenv()

# 2. Définir les chemins
BASE_DIR = Path(__file__).resolve().parent.parent
POLLUTANTS_REF_PATH = BASE_DIR / "config" / "pollutants_ref.json"
PATIENTS_REF_PATH = BASE_DIR / "config" / "patients_ref.json"

# 3. Récupérer la clé de sécurité
SECRET_KEY = os.getenv("ENCRYPTION_KEY")
if not SECRET_KEY:
    raise ValueError("ERREUR: La clé ENCRYPTION_KEY est absente du fichier .env !")

# 4. Fonctions pour charger les règles JSON
def load_pollutants_ref():
    with open(POLLUTANTS_REF_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def load_patients_ref():
    with open(PATIENTS_REF_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

# On charge les références une fois pour toutes
POLLUTANTS_REF = load_pollutants_ref()
PATIENTS_REF = load_patients_ref()
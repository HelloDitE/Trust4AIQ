import pandas as pd
from pathlib import Path

EXCEL_PATH = Path("data") / "capteurs_reels.xlsx"

class SensorService:
    @staticmethod
    def get_latest_measurements():
        """Lit l'Excel et retourne la toute dernière ligne de mesures"""
        try:
            # On lit le fichier Excel
            df = pd.read_excel(EXCEL_PATH)
            
            # On prend la dernière ligne (iloc[-1]) et on la transforme en dictionnaire
            latest_data = df.iloc[-1].to_dict()
            
            # On sépare les données intérieures et extérieures
            indoor = {
                "CO2": latest_data["CO2"],
                "PM2.5": latest_data["PM2.5"],
                "NO2": latest_data["NO2"],
                "COV": latest_data["COV"],
                "CO": latest_data["CO"],
                "Ozone": latest_data["Ozone"],
                "Radon": latest_data["Radon"],
                "Formaldéhyde": latest_data["Formaldéhyde"],
                "Humidité": latest_data["Humidité"]
            }
            
            outdoor = {
                "PM2.5": latest_data["Ext_PM2.5"],
                "NO2": latest_data["Ext_NO2"],
                "Ozone": latest_data["Ext_Ozone"],
                "Temp": latest_data["Ext_Temp"]
            }
            
            return indoor, outdoor
            
        except FileNotFoundError:
            print("❌ Erreur : Fichier capteurs_reels.xlsx introuvable.")
            return {}, {}
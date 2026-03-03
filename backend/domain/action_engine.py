from config.settings import POLLUTANTS_REF

class ActionEngine:
    @staticmethod
    def determine_actions(indoor_measures: dict, outdoor_measures: dict, global_risk: float = 0.0) -> list[str]:
        """
        Détermine les actions en respectant l'arbre de décision :
        1. Urgence Vitale (CO)
        2. Vérification Air Extérieur (Can_Open_Window)
        3. Actions par polluant intérieur
        """
        actions = []

        # --- ÉTAPE 1 : URGENCE ABSOLUE (Monoxyde de Carbone) ---
        co_limit = float(POLLUTANTS_REF.get("CO", {}).get("limit", 10))
        if indoor_measures.get("CO", 0) >= co_limit:
            # Ne pas vérifier l'air extérieur. On ouvre tout, on évacue, on appelle le 112. Gaz mortel inodore.
            actions.append("🚨 URGENCE VITALE (CO) : ÉVACUATION IMMÉDIATE. Ouvrez tout et appelez le 112. Gaz mortel inodore.")
            return actions  # On bloque tout le reste, la priorité est l'évacuation !

        # --- ÉTAPE 2 : VÉRIFICATION DE L'AIR EXTÉRIEUR (Clé de l'algorithme) ---
        can_open_window = True

        # S'il y a un pic de PM2.5 (>15) ou d'Ozone (>50) à l'extérieur
        if outdoor_measures.get("PM2.5", 0) > 15 or outdoor_measures.get("Ozone", 0) > 50 or outdoor_measures.get("NO2", 0) > 25:
            can_open_window = False

        # --- ÉTAPE 3 : TRAITEMENT DES POLLUANTS INTÉRIEURS ---
        is_perfect = True

        # 1. RADON (Priorité spéciale : le risque radioactif prime sur l'air extérieur)
        radon_limit = float(POLLUTANTS_REF.get("Radon", {}).get("limit", 100))
        if indoor_measures.get("Radon", 0) >= radon_limit:
            is_perfect = False
            actions.append("☢️ RADON : Aérer longuement (Le risque Radon prime sur la pollution extérieure). Nécessite une VMC en sous-sol à long terme.")

        # 2. DIOXYDE DE CARBONE (CO2)
        co2_limit = float(POLLUTANTS_REF.get("CO2", {}).get("limit", 800))
        if indoor_measures.get("CO2", 0) >= co2_limit:
            is_perfect = False
            if can_open_window:
                actions.append("💨 CO2 : Aérer : Ouvrir les fenêtres (10 min) + VMC. Le CO2 ne se filtre pas, seul l'apport d'air neuf le fait baisser.")
            else:
                actions.append("🔄 CO2 : Ne pas ouvrir. Ventilation mécanique seule : Forcer la VMC (double flux avec filtres).")

        # 3. PARTICULES FINES (PM2.5)
        pm25_limit = float(POLLUTANTS_REF.get("PM2.5", {}).get("limit", 15))
        if indoor_measures.get("PM2.5", 0) >= pm25_limit:
            is_perfect = False
            if can_open_window:
                actions.append("🧹 PM2.5 : Aérer + Épurer (Si la source est intérieure comme poussière ou travaux).")
            else:
                actions.append("🛡️ PM2.5 : Confinement + Épuration. Fermer fenêtres et allumer un purificateur avec Filtre HEPA (seule barrière mécanique validée).")

        # 4. COMPOSÉS ORG. VOLATILS (COV)
        cov_limit = float(POLLUTANTS_REF.get("COV", {}).get("limit", 500))
        if indoor_measures.get("COV", 0) >= cov_limit:
            is_perfect = False
            if can_open_window:
                actions.append("🧪 COV : Aérer massivement pour diluer les gaz. Identifier la source (produits ménagers, hydroalcoolique).")
            else:
                actions.append("🔌 COV : Épuration spécifique. Allumer purificateur avec Filtre Charbon Actif.")

        # 5. FORMALDÉHYDE
        ch2o_limit = float(POLLUTANTS_REF.get("Formaldehyde", {}).get("limit", 27))
        if indoor_measures.get("Formaldéhyde", 0) >= ch2o_limit:
            is_perfect = False
            if can_open_window:
                actions.append("🪑 FORMALDÉHYDE : Aérer. Souvent émis par le mobilier neuf ou les colles.")
            else:
                actions.append("🔌 FORMALDÉHYDE : Épuration spécifique (Filtre Charbon Actif + VMC).")

        # 6. DIOXYDE D'AZOTE (NO2)
        no2_limit = float(POLLUTANTS_REF.get("NO2", {}).get("limit", 25))
        if indoor_measures.get("NO2", 0) >= no2_limit:
            is_perfect = False
            if can_open_window:
                actions.append("🔥 NO2 : Aérer. Stoppez toute combustion interne (cuisinière gaz, encens).")
            else:
                actions.append("🚗 NO2 : Fermer fenêtres (Le NO2 vient souvent du trafic routier). Utiliser un Filtre Charbon.")

        # 7. OZONE (O3)
        o3_limit = float(POLLUTANTS_REF.get("Ozone", {}).get("limit", 25))
        if indoor_measures.get("Ozone", 0) >= o3_limit:
            is_perfect = False
            if can_open_window:
                actions.append("⚡ OZONE : Aérer. Désactiver immédiatement les purificateurs à ionisation/plasma qui en génèrent.")
            else:
                actions.append("⚡ OZONE : Fermer fenêtres (C'est un polluant très fréquent en été à l'extérieur).")

        # 8. HUMIDITÉ / MOISISSURES
        hum_limit = float(POLLUTANTS_REF.get("Humidité", {}).get("limit", 60))
        if indoor_measures.get("Humidité", 0) >= hum_limit:
            is_perfect = False
            if can_open_window:
                actions.append("💧 HUMIDITÉ : Déshumidifier + Aérer pour évacuer l'air humide. Chercher la fuite ou le pont thermique.")
            else:
                actions.append("💧 HUMIDITÉ : Déshumidificateur électrique + VMC. Ne pas faire entrer d'air extérieur s'il pleut/très humide.")

        # --- ÉTAPE 4 : TOUT EST NORMAL ---
        if is_perfect:
            actions.append("✅ Qualité de l'air saine. L'environnement est optimal.")

        return actions
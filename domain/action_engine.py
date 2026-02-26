class ActionEngine:
    @staticmethod
    def determine_actions(indoor_measures: dict, outdoor_measures: dict, global_risk: float) -> list[str]:
        """
        Détermine les actions correctives basées sur :
        1. Le niveau de risque global (Vert/Jaune/Orange/Rouge)
        2. La comparaison pollution Intérieure vs Extérieure
        """
        actions = []

        # --- NIVEAU 1 : URGENCE VITALE (Rouge) ---
        if global_risk >= 2.5:
            actions.append("🚨 URGENCE : Évacuer la pièce ou porter un masque FFP2/FFP3.")
            # On vérifie si c'est du CO (Monoxyde de carbone)
            if indoor_measures.get("CO", 0) > 10: # Seuil critique
                actions.append("⚠️ DANGER CO : Appeler les secours / Vérifier chaudière.")

        # --- NIVEAU 2 : Actions Spécifiques par Polluant (Orange/Rouge) ---
        if global_risk >= 1.5:
            
            # Cas A : Problème de Confinement (CO2 ou COV)
            # Si CO2 élevé (> 1000) ou COV élevés
            if indoor_measures.get("CO2", 400) > 1000 or indoor_measures.get("COV", 0) > 500:
                # Si l'air extérieur est "respirable" sur ces paramètres, on ventile
                if outdoor_measures.get("PM2.5", 0) < 25: # On ne ventile pas si dehors c'est très pollué en particules
                    actions.append("💨 VENTILATION : Ouvrez les fenêtres pour diluer le CO2/COV.")
                else:
                    actions.append("🔄 VMC FORCÉE : Augmentez la ventilation mécanique (filtres). Évitez d'ouvrir les fenêtres (pollution ext).")

            # Cas B : Problème de Particules (PM2.5)
            # Exemple : Cuisine, Bougies, Ménage
            if indoor_measures.get("PM2.5", 0) > 15:
                # EST-CE QUE DEHORS C'EST PIRE ?
                if outdoor_measures.get("PM2.5", 0) > indoor_measures.get("PM2.5", 0):
                    # OUI -> Protection
                    actions.append("🛡️ CONFINEMENT : Gardez fenêtres fermées (Pollution extérieure plus forte).")
                    actions.append("🔌 PURIFICATION : Activez purificateur d'air (HEPA) en mode recyclage.")
                else:
                    # NON -> Dehors c'est mieux, on évacue la pollution intérieure
                    actions.append("💨 VENTILATION : Ouvrez pour évacuer les fumées/particules.")

            # Cas C : Humidité
            if indoor_measures.get("Humidité", 50) > 60:
                actions.append("💧 HUMIDITÉ : Risque moisissures. Déshumidifier ou chauffer.")

        # --- NIVEAU 3 : Tout va bien (Vert) ---
        if not actions:
            actions.append("✅ Qualité de l'air saine. Aucune action requise.")

        return actions
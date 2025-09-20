import random
class Enemy:
    def __init__(self):
        # Tes attributs existants...
        # NOUVELLES FONCTIONNALITÉS :
        self.stratégie_actuelle = "neutre"
        self.actions_disponibles = ["espionnage", "sabotage", "recrutement", "attaque"]
        
    def action_intelligente(self, player):
        """L'ennemi choisit une action basée sur l'état du joueur"""
        
        # Analyse de la situation
        if player.calculer_puissance_totale() > self.calculer_puissance_totale():
            # Joueur plus fort -> défensive/espionnage
            actions_prioritaires = ["espionnage", "recrutement", "sabotage"]
        else:
            # Ennemi plus fort -> offensive
            actions_prioritaires = ["attaque", "sabotage", "vol_territoire"]
        
        action_choisie = random.choice(actions_prioritaires)
        return self.exécuter_action(action_choisie, player)
    
    def exécuter_action(self, action, player):
        """Exécute l'action choisie contre le joueur"""
        résultats = {
            "espionnage": {
                "description": "L'organisation rivale tente d'espionner vos opérations !",
                "test_réussite": lambda: random.randint(1, 100) <= 60,
                "effet_succès": {"information_volée": True, "sécurité": -10},
                "effet_échec": {"contre_espionnage": True, "réputation": +5}
            },
            
            "sabotage": {
                "description": "Sabotage de vos équipements !",
                "test_réussite": lambda: random.randint(1, 100) <= 45,
                "effet_succès": {"argent": -random.randint(2000, 5000), "moral": -10},
                "effet_échec": {"preuve_contre_ennemi": True}
            },
            
            "attaque": {
                "description": "Attaque directe contre vos subordonnés !",
                "test_réussite": lambda: random.randint(1, 100) <= 35,
                "effet_succès": {"subordonné_blessé": True, "guerre_ouverte": True},
                "effet_échec": {"réputation": +10, "moral": +15}
            }
        }
        
        if action in résultats:
            résultat = résultats[action]
            print(f"\n⚔️ ACTION ENNEMIE: {résultat['description']}")
            
            if résultat["test_réussite"]():
                print("💥 L'action ennemie réussit !")
                return résultat["effet_succès"]
            else:
                print("✅ Vous avez contré l'action ennemie !")
                return résultat["effet_échec"]
        
        return {}
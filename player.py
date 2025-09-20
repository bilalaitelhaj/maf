import random
class Player:
    def __init__(self, nom_boss):
        # Tes attributs existants...
        self.nom_boss = nom_boss
        self.argent = 10000
        self.subordonnes = []
        
        # NOUVELLES FONCTIONNALITÉS :
        self.réputation = 0  # -100 à +100
        self.niveau_organisation = 1
        self.territoires_contrôlés = []
        self.compétences_organisation = []
        self.dette = 0
        self.moral_général = 70
        self.missions_réussies = 0
        self.missions_échouées = 0
        self.tour_actuel = 1
        self.événements_en_cours = []
        
    def calculer_puissance_totale(self):
        """Calcule la puissance totale de l'organisation"""
        return sum(sub.puissance for sub in self.subordonnes)
    
    def calculer_loyauté_moyenne(self):
        """Calcule la loyauté moyenne des subordonnés"""
        if not self.subordonnes:
            return 0
        return sum(sub.loyauté for sub in self.subordonnes) / len(self.subordonnes)
    
    def peut_recruter(self):
        """Vérifie si le joueur peut recruter (limite par niveau)"""
        limites = {1: 4, 2: 8, 3: 12, 4: 20}
        return len(self.subordonnes) < limites.get(self.niveau_organisation, 4)
    
    def promouvoir_subordonné(self, subordinate_index):
        """Promeut un subordonné (coûte de l'argent, boost loyauté/stats)"""
        if subordinate_index < len(self.subordonnes):
            sub = self.subordonnes[subordinate_index]
            coût = sub.niveau * 2000
            
            if self.argent >= coût:
                self.argent -= coût
                sub.loyauté += 20
                sub.puissance += random.randint(3, 8)
                sub.moral += 15
                return f"{sub.nom} a été promu ! Loyauté et stats améliorées."
            else:
                return "Pas assez d'argent pour la promotion."
        return "Subordonné introuvable."
    
    def gérer_événement_loyauté(self, subordinate_index):
        """Gère un événement de loyauté pour un subordonné"""
        if subordinate_index < len(self.subordonnes):
            sub = self.subordonnes[subordinate_index]
            événement = sub.événement_personnel()
            
            print(f"\n🎭 ÉVÉNEMENT PERSONNEL - {sub.nom}")
            print(f"📖 {événement['description']}")
            print(f"❓ {événement['demande']}")
            
            choix = input("\nAcceptez-vous ? (o/n): ").lower()
            
            if choix == 'o':
                effets = événement['impact_si_oui']
                message = f"✅ Vous acceptez la demande de {sub.nom}."
            else:
                effets = événement['impact_si_non']
                message = f"❌ Vous refusez la demande de {sub.nom}."
            
            # Applique les effets
            for effet, valeur in effets.items():
                if hasattr(sub, effet):
                    if isinstance(valeur, int):
                        setattr(sub, effet, getattr(sub, effet) + valeur)
                    else:
                        setattr(sub, effet, valeur)
            
            print(message)
            return True
        return False
    
    def entraîner_équipe(self):
        """Entraîne toute l'équipe contre de l'argent"""
        coût_par_subordonné = 1000
        coût_total = len(self.subordonnes) * coût_par_subordonné
        
        if self.argent >= coût_total:
            self.argent -= coût_total
            améliorés = 0
            
            for sub in self.subordonnes:
                if not sub.fatigué:
                    sub.puissance += random.randint(1, 3)
                    sub.discrétion += random.randint(0, 2)
                    sub.intelligence += random.randint(0, 2)
                    sub.moral += 5
                    améliorés += 1
            
            return f"✅ {améliorés} subordonnés entraînés ! Coût: {coût_total}$"
        else:
            return f"❌ Pas assez d'argent (besoin: {coût_total}$)"
    
    def vérifier_montée_niveau(self):
        """Vérifie si l'organisation peut monter de niveau"""
        conditions = {
            2: {"argent": 50000, "réputation": 25, "missions_réussies": 10, "subordonnés": 6},
            3: {"argent": 200000, "réputation": 60, "missions_réussies": 25, "subordonnés": 10},
            4: {"argent": 1000000, "réputation": 90, "missions_réussies": 50, "subordonnés": 15}
        }
        
        niveau_suivant = self.niveau_organisation + 1
        if niveau_suivant in conditions:
            cond = conditions[niveau_suivant]
            
            if (self.argent >= cond["argent"] and 
                self.réputation >= cond["réputation"] and
                self.missions_réussies >= cond["missions_réussies"] and
                len(self.subordonnes) >= cond["subordonnés"]):
                return True
        return False
    
    def monter_niveau_organisation(self):
        """Monte d'un niveau l'organisation"""
        noms_niveaux = {1: "Petite bande", 2: "Gang organisé", 3: "Cartel régional", 4: "Empire criminel"}
        
        if self.vérifier_montée_niveau():
            self.niveau_organisation += 1
            nouveau_nom = noms_niveaux.get(self.niveau_organisation, "Organisation mystérieuse")
            
            # Bonus de niveau
            bonus_argent = self.niveau_organisation * 10000
            self.argent += bonus_argent
            
            # Nouvelles compétences débloquées
            nouvelles_compétences = {
                2: ["Corruption police", "Planque sécurisée"],
                3: ["Réseau d'espions", "Territoire contrôlé", "Blanchiment d'argent"],
                4: ["Empire légitime", "Corruption politique", "Réseau international"]
            }
            
            if self.niveau_organisation in nouvelles_compétences:
                self.compétences_organisation.extend(nouvelles_compétences[self.niveau_organisation])
            
            return f"🎉 PROMOTION ! Vous êtes maintenant: {nouveau_nom} (Niveau {self.niveau_organisation})\n💰 Bonus: +{bonus_argent}$"
        
        return "Conditions non remplies pour la promotion."
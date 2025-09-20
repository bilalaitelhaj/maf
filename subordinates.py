# =====================================================
# SUBORDINATES.PY - Version corrigée
# =====================================================

import random
import json

class Subordinate:
    def __init__(self, nom=None, role=None):
        self.nom = nom or self._generate_name()
        self.role = role or self._generate_role()
        self.puissance = random.randint(10, 25)
        self.niveau = 1

        # NOUVELLES FONCTIONNALITÉS :
        self.loyauté = random.randint(40, 80)
        self.discrétion = random.randint(10, 20)
        self.intelligence = random.randint(10, 20)
        self.charisme = random.randint(10, 20)
        self.moral = random.randint(60, 100)
        self.fatigué = False
        self.blessé = False
        self.expérience = 0
        self.compétences_spéciales = []
        self.histoire_personnelle = self._generate_personal_story()
        self.relation_joueur = 50  # -100 à +100

    # ---------- Méthodes utilitaires ----------
    def _generate_name(self):
        """Génère un nom aléatoire pour le subordonné"""
        noms = ["Alex", "Jordan", "Sam", "Morgan", "Taylor", "Riley", "Casey", "Cameron"]
        return random.choice(noms)

    def _generate_role(self):
        """Génère un rôle aléatoire si non fourni"""
        roles = ["Soldat", "Espion", "Recruteur"]
        return random.choice(roles)

    def _generate_personal_story(self):
        """Génère une histoire personnelle pour le subordonné"""
        stories = [
            f"{self.nom} était comptable avant de découvrir la corruption de son patron.",
            f"{self.nom} a rejoint après que sa famille ait été ruinée par des usuriers.",
            f"{self.nom} est un ancien soldat qui cherche un nouveau sens à sa vie.",
            f"{self.nom} était petit délinquant avant de vouloir voir plus grand.",
            f"{self.nom} a une dette d'honneur envers vous après que vous l'ayez sauvé.",
        ]
        return random.choice(stories)

    # ---------- Dialogues et événements ----------
    def dialogue_recrutement(self):
        dialogues = {
            "Soldat": [
                "Je suis prêt à me battre pour la bonne cause.",
                "Donnez-moi des ordres clairs et je les exécuterai.",
                "J'ai l'expérience du terrain, vous ne le regretterez pas."
            ],
            "Espion": [
                "L'information, c'est le pouvoir. Je peux vous en procurer.",
                "Je connais les secrets de beaucoup de gens importants...",
                "Personne ne me remarque, c'est ma plus grande force."
            ],
            "Recruteur": [
                "Je connais du monde dans tous les milieux.",
                "Laissez-moi vous amener les meilleurs éléments.",
                "J'ai un don pour repérer les talents cachés."
            ]
        }
        return random.choice(dialogues.get(self.role, ["Je ferai de mon mieux pour vous."]))

    def test_loyauté(self):
        test_scenarios = [
            {
                "situation": f"{self.nom} trouve un portefeuille avec 2000$ dans la rue.",
                "choix": {
                    "Le garder": {"loyauté": -5, "argent_personnel": +2000},
                    "Vous le donner": {"loyauté": +10, "honnêteté": +5},
                    "Le rendre": {"loyauté": +5, "réputation_publique": +3}
                }
            },
            {
                "situation": f"Un rival offre 5000$ à {self.nom} pour des informations sur vous.",
                "choix": {
                    "Accepter l'argent": {"loyauté": -30, "trahison": True},
                    "Refuser et vous prévenir": {"loyauté": +20, "confiance": +15},
                    "Faire semblant d'accepter": {"loyauté": +10, "intelligence": +5}
                }
            }
        ]
        return random.choice(test_scenarios)

    def événement_personnel(self):
        événements = [
            {
                "type": "famille",
                "description": f"La sœur de {self.nom} a des problèmes avec des usuriers.",
                "demande": "Peut-il prendre un jour de congé pour s'en occuper ?",
                "impact_si_oui": {"loyauté": +15, "moral": +10, "disponible": False},
                "impact_si_non": {"loyauté": -10, "moral": -15, "stress": +20}
            },
            {
                "type": "ambition",
                "description": f"{self.nom} pense mériter plus de responsabilités.",
                "demande": "Veut diriger la prochaine mission importante.",
                "impact_si_oui": {"loyauté": +20, "confiance": +15, "risque_mission": +10},
                "impact_si_non": {"loyauté": -8, "ambition_frustrée": True}
            },
            {
                "type": "doute_moral",
                "description": f"{self.nom} commence à douter de vos méthodes.",
                "demande": "Demande à éviter les missions violentes.",
                "impact_si_oui": {"loyauté": +10, "moral": +20, "limites": "pas_violence"},
                "impact_si_non": {"loyauté": -15, "moral": -20, "obéissance": +10}
            }
        ]
        return random.choice(événements)

    # ---------- Progression et compétences ----------
    def gagner_expérience(self, points):
        self.expérience += points
        xp_needed = self.niveau * 100
        if self.expérience >= xp_needed:
            self.niveau += 1
            self.expérience -= xp_needed
            self.améliorer_stats()
            return True
        return False

    def améliorer_stats(self):
        améliorations = {
            "puissance": random.randint(2, 5),
            "discrétion": random.randint(1, 3),
            "intelligence": random.randint(1, 3),
            "charisme": random.randint(1, 3)
        }
        for stat, bonus in améliorations.items():
            setattr(self, stat, getattr(self, stat) + bonus)

    def apprendre_compétence(self, compétence):
        compétences_disponibles = {
            "Combat rapproché": {"puissance": +5, "survie": +10},
            "Piratage informatique": {"intelligence": +8, "missions_tech": True},
            "Charme mortel": {"charisme": +6, "séduction": True},
            "Filature experte": {"discrétion": +7, "espionnage": True},
            "Premiers secours": {"soins": True, "moral_équipe": +5},
            "Contacts police": {"information": True, "corruption": +10},
            "Maîtrise des armes": {"puissance": +8, "intimidation": +5}
        }

        if compétence in compétences_disponibles and compétence not in self.compétences_spéciales:
            self.compétences_spéciales.append(compétence)
            effets = compétences_disponibles[compétence]
            for effet, valeur in effets.items():
                if isinstance(valeur, int):
                    if hasattr(self, effet):
                        setattr(self, effet, getattr(self, effet) + valeur)
                    else:
                        setattr(self, effet, valeur)
                else:
                    setattr(self, effet, valeur)
            return f"{self.nom} a appris : {compétence} !"
        return "Compétence non disponible ou déjà acquise."
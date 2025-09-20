import random
def événements_aléatoires_améliorés(player):
    """Version améliorée de tes événements aléatoires"""
    
    # Événements basés sur le contexte du joueur
    événements_contextuels = []
    
    # Si peu d'argent
    if player.argent < 5000:
        événements_contextuels.extend([
            {
                "nom": "Prêteur sur gages",
                "description": "Un usurier vous propose un prêt de 10000$ à 50% d'intérêts.",
                "choix": {
                    "Accepter": {"argent": +10000, "dette": +15000, "réputation": -5},
                    "Refuser": {"événement_futur": "Finances difficiles"}
                }
            },
            {
                "nom": "Mission désespérée",
                "description": "Un client douteux offre beaucoup d'argent pour une mission très risquée.",
                "choix": {
                    "Accepter": {"mission_spéciale": True, "risque": 200, "récompense": 15000},
                    "Refuser": {"sécurité": True}
                }
            }
        ])
    
    # Si beaucoup de subordonnés
    if len(player.subordonnes) >= 6:
        événements_contextuels.append({
            "nom": "Tensions internes",
            "description": "Des rivalités apparaissent entre vos subordonnés.",
            "choix": {
                "Organiser une réunion": {"moral_général": +10, "temps": -1},
                "Laisser faire": {"risque_départ": True, "autonomie": +5},
                "Punir les fauteurs de trouble": {"discipline": +15, "loyauté": -8}
            }
        })
    
    # Si réputation élevée
    if player.réputation > 50:
        événements_contextuels.append({
            "nom": "Proposition d'alliance",
            "description": "Un autre gang propose une alliance temporaire.",
            "choix": {
                "Accepter": {"allié": True, "missions_communes": True, "indépendance": -10},
                "Refuser": {"réputation": +5, "ennemi_potentiel": True}
            }
        })
    
    # Ajoute tes événements existants
    événements_classiques = [
        {"nom": "Découverte d'argent", "effet": {"argent": random.randint(1000, 5000)}},
        {"nom": "Problèmes de loyauté", "effet": {"loyauté_tous": -random.randint(5, 15)}},
        {"nom": "Informateur", "effet": {"information_ennemi": True}},
    ]
    
    tous_événements = événements_contextuels + événements_classiques
    return random.choice(tous_événements)

def missions_complexes(player, subordinate_index):
    """Nouvelles missions avec choix multiples"""
    
    missions_avancées = {
        "Infiltration Casino": {
            "description": "Voler les gains de la soirée poker VIP",
            "phases": [
                {
                    "nom": "Préparation",
                    "choix": {
                        "Étudier les plans": {"intelligence": +10, "temps": 2, "discrétion": +5},
                        "Soudoyer un employé": {"argent": -2000, "accès_facile": True, "risque_trahison": 20},
                        "Improviser": {"risque": +15, "rapidité": True}
                    }
                },
                {
                    "nom": "Infiltration", 
                    "choix": {
                        "Déguisement client": {"charisme_requis": 15, "discrétion": "haute"},
                        "Conduits d'aération": {"discrétion_requise": 20, "difficile": True},
                        "Diversion extérieure": {"complice_requis": True, "attention": "détournée"}
                    }
                }
            ],
            "récompense_base": 12000,
            "risques": ["Arrestation", "Blessure", "Échec mission"]
        },
        
        "Sabotage Industriel": {
            "description": "Saboter l'usine de l'organisation rivale",
            "phases": [
                {
                    "nom": "Reconnaissance",
                    "choix": {
                        "Surveillance nocturne": {"temps": 3, "information": "complète", "fatigue": +10},
                        "Infiltration jour": {"audace": True, "risque": +20, "rapidité": True},
                        "Contacts internes": {"réseau_requis": True, "fiabilité": "élevée"}
                    }
                }
            ],
            "conséquences_morales": {
                "sabotage_propre": {"réputation": +5, "moral": +5},
                "sabotage_sale": {"réputation": -10, "efficacité": +20, "moral": -15}
            }
        }
    }
    
    return random.choice(list(missions_avancées.values()))

def next_turn_amélioré(player, rival, turn_number):
    """Version améliorée de ta fonction next_turn"""
    
    print(f"\n🔄 TOUR {turn_number}")
    
    # 1. Vérification événements de loyauté
    for i, sub in enumerate(player.subordonnes):
        if random.randint(1, 100) <= 10:  # 10% de chance
            print(f"\n💭 {sub.nom} semble avoir quelque chose à vous dire...")
            if input("Voulez-vous lui parler ? (o/n): ").lower() == 'o':
                player.gérer_événement_loyauté(i)
    
    # 2. Récupération automatique
    for sub in player.subordonnes:
        if sub.fatigué:
            if random.randint(1, 100) <= 30:  # 30% de chance de récupérer
                sub.fatigué = False
                print(f"💪 {sub.nom} a récupéré de sa fatigue.")
        
        if sub.blessé:
            if random.randint(1, 100) <= 20:  # 20% de chance de guérir
                sub.blessé = False
                print(f"🏥 {sub.nom} s'est remis de ses blessures.")
    
    # 3. Événement aléatoire contextuel
    if random.randint(1, 100) <= 30:  # 30% de chance
        événement = événements_aléatoires_améliorés(player)
        print(f"\n🎲 ÉVÉNEMENT: {événement['nom']}")
        print(événement['description'])
        
        if 'choix' in événement:
            choix_dispo = list(événement['choix'].keys())
            for i, choix in enumerate(choix_dispo, 1):
                print(f"{i}. {choix}")
            
            try:
                choix_idx = int(input("Votre choix: ")) - 1
                choix_sélectionné = choix_dispo[choix_idx]
                effets = événement['choix'][choix_sélectionné]
                
                # Applique les effets
                for effet, valeur in effets.items():
                    if effet == "argent":
                        player.argent += valeur
                        print(f"💰 Argent: {valeur:+d}$ (Total: {player.argent}$)")
                    elif effet == "réputation":
                        player.réputation += valeur
                        print(f"⭐ Réputation: {valeur:+d} (Total: {player.réputation})")
                        
            except (ValueError, IndexError):
                print("Choix invalide, événement ignoré.")
    
    # 4. Vérification montée de niveau
    if player.vérifier_montée_niveau():
        print(f"\n🎉 Votre organisation peut évoluer !")
        if input("Voulez-vous faire évoluer votre organisation ? (o/n): ").lower() == 'o':
            résultat = player.monter_niveau_organisation()
            print(résultat)
    
    # 5. Tes autres événements existants...
    
    player.tour_actuel += 1
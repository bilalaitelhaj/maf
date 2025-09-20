import os
import random

# Importe tes modules existants
# Adapte selon le nom de tes classes dans tes fichiers existants
try:
    from game_engine import *  # Importe tout de ton game_engine
    from player import Player
    from enemies import Enemy
    from subordinates import Subordinate
except ImportError as e:
    print(f"Erreur d'import: {e}")
    print("Assure-toi que tes fichiers game_engine.py, player.py, etc. existent")
    exit()

def clear_screen():
    """Efface l'écran pour une meilleure lisibilité"""
    os.system('cls' if os.name == 'nt' else 'clear')

def afficher_logo():
    """Affiche le logo du jeu"""
    logo = """
    ╔═══════════════════════════════════════╗
    ║           ORGANIZATION GAME           ║
    ║         Dirigez votre Empire          ║
    ╚═══════════════════════════════════════╝
    """
    print(logo)

def afficher_stats_détaillées(player):
    """Affiche les statistiques détaillées du joueur"""
    clear_screen()
    afficher_logo()
    
    print(f"👑 BOSS: {player.nom_boss}")
    print("═" * 50)
    
    # Stats principales
    print(f"💰 Argent: {player.argent:,}$ ", end="")
    if player.dette > 0:
        print(f"(Dette: {player.dette:,}$)")
    else:
        print()
    
    print(f"⭐ Réputation: {player.réputation}/100")
    print(f"🏢 Niveau: {player.niveau_organisation} - {get_organization_name(player.niveau_organisation)}")
    print(f"🎯 Missions réussies: {player.missions_réussies}")
    print(f"❌ Missions échouées: {player.missions_échouées}")
    
    # Stats équipe
    if player.subordonnes:
        loyauté_moyenne = player.calculer_loyauté_moyenne()
        puissance_totale = player.calculer_puissance_totale()
        
        print(f"\n👥 ÉQUIPE ({len(player.subordonnes)} membres):")
        print(f"💪 Puissance totale: {puissance_totale}")
        print(f"❤️  Loyauté moyenne: {loyauté_moyenne:.1f}/100")
        print(f"😊 Moral général: {player.moral_général}/100")
    
    # Compétences organisation
    if player.compétences_organisation:
        print(f"\n🎖️  COMPÉTENCES ACQUISES:")
        for compétence in player.compétences_organisation:
            print(f"  • {compétence}")
    
    # Territoires contrôlés
    if player.territoires_contrôlés:
        print(f"\n🗺️  TERRITOIRES CONTRÔLÉS:")
        for territoire in player.territoires_contrôlés:
            print(f"  • {territoire}")
    
    input("\nAppuyez sur Entrée pour continuer...")

def afficher_équipe_détaillée(player):
    """Affiche l'équipe avec détails complets"""
    clear_screen()
    afficher_logo()
    
    if not player.subordonnes:
        print("❌ Aucun subordonné dans votre organisation.")
        input("Appuyez sur Entrée pour continuer...")
        return
    
    print(f"👥 VOTRE ÉQUIPE ({len(player.subordonnes)} membres)")
    print("═" * 70)
    
    for i, sub in enumerate(player.subordonnes, 1):
        statut = ""
        if sub.fatigué:
            statut += "😴 "
        if sub.blessé:
            statut += "🤕 "
        
        print(f"\n{i}. {sub.nom} - {sub.role} {statut}")
        print(f"   📊 Niveau {sub.niveau} | 💪 Puissance: {sub.puissance}")
        print(f"   ❤️  Loyauté: {sub.loyauté}/100 | 😊 Moral: {sub.moral}/100")
        print(f"   🔍 Discrétion: {sub.discrétion} | 🧠 Intelligence: {sub.intelligence}")
        
        if sub.compétences_spéciales:
            print(f"   🎖️  Compétences: {', '.join(sub.compétences_spéciales)}")
        
        # Affiche l'histoire personnelle
        print(f"   📖 {sub.histoire_personnelle}")
    
    print("\n" + "═" * 70)
    print("1. Promouvoir un subordonné")
    print("2. Entraîner l'équipe")
    print("3. Parler à un subordonné")
    print("4. Enseigner une compétence")
    print("0. Retour")
    
    choix = input("\nVotre choix: ")
    
    if choix == "1":
        gérer_promotion(player)
    elif choix == "2":
        résultat = player.entraîner_équipe()
        print(f"\n{résultat}")
        input("Appuyez sur Entrée pour continuer...")
    elif choix == "3":
        parler_subordonné(player)
    elif choix == "4":
        enseigner_compétence(player)

def gérer_promotion(player):
    """Gère la promotion d'un subordonné"""
    print("\n👑 PROMOTION DE SUBORDONNÉ")
    print("Quel subordonné voulez-vous promouvoir ?")
    
    for i, sub in enumerate(player.subordonnes, 1):
        coût = sub.niveau * 2000
        print(f"{i}. {sub.nom} (Coût: {coût}$)")
    
    try:
        choix = int(input("Numéro: ")) - 1
        if 0 <= choix < len(player.subordonnes):
            résultat = player.promouvoir_subordonné(choix)
            print(f"\n{résultat}")
        else:
            print("Subordonné invalide.")
    except ValueError:
        print("Choix invalide.")
    
    input("Appuyez sur Entrée pour continuer...")

def menu_marché_noir(player):
    """Menu du marché noir structuré par catégories"""
    clear_screen()
    print("🏪 MARCHÉ NOIR")
    print("═" * 50)

    # Définition des catégories et des articles
    marché = {
        "Équipements": [
            {"nom": "Équipement furtif", "prix": 5000, "effet": "Discrétion équipe +10"},
            {"nom": "Armes avancées", "prix": 8000, "effet": "Puissance équipe +15"},
            {"nom": "Véhicules blindés", "prix": 15000, "effet": "Sécurité +25"},
            {"nom": "Gants anti-traces", "prix": 2000, "effet": "Discrétion +5"},
            {"nom": "Masques divers", "prix": 1000, "effet": "Discrétion +3"}
        ],
        "Technologies": [
            {"nom": "Système de surveillance", "prix": 12000, "effet": "Intelligence missions +20"},
            {"nom": "Drones espions", "prix": 8000, "effet": "Surveillance +15"},
            {"nom": "Caméras invisibles", "prix": 5000, "effet": "Espionnage +10"},
            {"nom": "Logiciel de piratage", "prix": 10000, "effet": "Accès bases de données"},
        ],
        "Services": [
            {"nom": "Corruption policière", "prix": 20000, "effet": "Réduction risques missions"},
            {"nom": "Informateurs", "prix": 7000, "effet": "Infos secrètes sur rivaux"},
            {"nom": "Avocat véreux", "prix": 12000, "effet": "Réduction pénalités légales"},
            {"nom": "Gang de muscle", "prix": 15000, "effet": "Support physique en mission"},
        ],
        "Véhicules": [
            {"nom": "Voiture sportive blindée", "prix": 20000, "effet": "Évasion +20"},
            {"nom": "Camion discret", "prix": 12000, "effet": "Transport marchandises +15"},
            {"nom": "Moto furtive", "prix": 8000, "effet": "Évasion rapide +10"},
        ],
        "Produits illégaux": [
            {"nom": "Armes illégales", "prix": 10000, "effet": "Puissance missions +15"},
            {"nom": "Drogues rares", "prix": 15000, "effet": "Vente lucrative +20"},
            {"nom": "Faux papiers", "prix": 5000, "effet": "Subordonnés non détectés"},
        ]
    }

    # Affiche les catégories
    categories = list(marché.keys())
    for i, cat in enumerate(categories, 1):
        print(f"{i}. {cat}")

    print("0. Retour")
    try:
        choix_cat = int(input("\nSélectionnez une catégorie: "))
        if 1 <= choix_cat <= len(categories):
            cat_choisie = categories[choix_cat-1]
            articles = marché[cat_choisie]

            clear_screen()
            print(f"🏪 {cat_choisie.upper()}")
            print("═" * 50)

            for j, art in enumerate(articles, 1):
                prix = art.get('prix', 0)
                effet = art.get('effet', 'Aucun effet')
                print(f"{j}. {art['nom']} - {prix:,}$ ({effet})")
            print("0. Retour")

            choix_art = int(input("\nQue voulez-vous acheter ? "))
            if 1 <= choix_art <= len(articles):
                article_choisi = articles[choix_art-1]
                prix = article_choisi.get('prix', 0)
                if player.argent >= prix:
                    player.argent -= prix
                    print(f"✅ Vous avez acheté: {article_choisi['nom']}")
                    # Ici tu peux ajouter l'effet sur le joueur ou son organisation
                else:
                    print(f"❌ Pas assez d'argent ! (Besoin: {prix:,}$)")
    except (ValueError, IndexError):
        print("Choix invalide.")
    input("Appuyez sur Entrée pour continuer...")

def parler_subordonné(player):
    """Permet de parler à un subordonné"""
    print("\n💬 CONVERSATION")
    print("À qui voulez-vous parler ?")
    
    for i, sub in enumerate(player.subordonnes, 1):
        print(f"{i}. {sub.nom} (Loyauté: {sub.loyauté}/100)")
    
    try:
        choix = int(input("Numéro: ")) - 1
        if 0 <= choix < len(player.subordonnes):
            sub = player.subordonnes[choix]
            
            # Test de loyauté aléatoire
            test = sub.test_loyauté()
            print(f"\n📖 SITUATION:")
            print(test["situation"])
            
            choix_dispo = list(test["choix"].keys())
            for i, option in enumerate(choix_dispo, 1):
                print(f"{i}. {option}")
            
            choix_test = int(input("Votre réaction: ")) - 1
            option_choisie = choix_dispo[choix_test]
            effets = test["choix"][option_choisie]
            
            print(f"\n✅ Vous choisissez: {option_choisie}")
            
            # Applique les effets
            for effet, valeur in effets.items():
                if effet == "loyauté":
                    sub.loyauté = max(0, min(100, sub.loyauté + valeur))
                    print(f"❤️  Loyauté de {sub.nom}: {valeur:+d} (Total: {sub.loyauté})")
                elif effet == "trahison" and valeur:
                    print(f"⚠️  {sub.nom} pourrait vous trahir plus tard...")
                    sub.relation_joueur -= 30
                    
        else:
            print("Subordonné invalide.")
    except (ValueError, IndexError):
        print("Choix invalide.")
    
    input("Appuyez sur Entrée pour continuer...")

def enseigner_compétence(player):
    """Permet d'enseigner une compétence à un subordonné"""
    compétences_disponibles = [
        "Combat rapproché", "Piratage informatique", "Charme mortel",
        "Filature experte", "Premiers secours", "Contacts police", "Maîtrise des armes"
    ]
    
    print("\n🎓 ENSEIGNEMENT DE COMPÉTENCES")
    print("Quel subordonné voulez-vous former ?")
    
    for i, sub in enumerate(player.subordonnes, 1):
        print(f"{i}. {sub.nom} (Niveau {sub.niveau})")
    
    try:
        choix_sub = int(input("Numéro: ")) - 1
        if 0 <= choix_sub < len(player.subordonnes):
            sub = player.subordonnes[choix_sub]
            
            print(f"\nQuelle compétence enseigner à {sub.nom} ?")
            compétences_apprises = sub.compétences_spéciales
            compétences_restantes = [c for c in compétences_disponibles if c not in compétences_apprises]
            
            if not compétences_restantes:
                print("Ce subordonné connaît déjà toutes les compétences !")
                input("Appuyez sur Entrée pour continuer...")
                return
            
            for i, comp in enumerate(compétences_restantes, 1):
                coût = 3000
                print(f"{i}. {comp} (Coût: {coût}$)")
            
            choix_comp = int(input("Numéro: ")) - 1
            if 0 <= choix_comp < len(compétences_restantes):
                compétence = compétences_restantes[choix_comp]
                coût = 3000
                
                if player.argent >= coût:
                    player.argent -= coût
                    résultat = sub.apprendre_compétence(compétence)
                    print(f"\n{résultat}")
                    print(f"💰 Coût: -{coût}$ (Reste: {player.argent}$)")
                else:
                    print(f"❌ Pas assez d'argent ! (Besoin: {coût}$)")
            else:
                print("Compétence invalide.")
        else:
            print("Subordonné invalide.")
    except (ValueError, IndexError):
        print("Choix invalide.")
    
    input("Appuyez sur Entrée pour continuer...")

def menu_missions_avancé(player, game_engine):
    """Menu de missions avec plus d'options"""
    clear_screen()
    afficher_logo()
    
    print("🎯 CENTRE DE MISSIONS")
    print("═" * 50)
    
    if not player.subordonnes:
        print("❌ Aucun subordonné disponible pour les missions.")
        input("Appuyez sur Entrée pour continuer...")
        return
    
    # Affiche subordonnés disponibles
    disponibles = [sub for sub in player.subordonnes if not sub.fatigué and not sub.blessé]
    
    print(f"👥 Subordonnés disponibles: {len(disponibles)}/{len(player.subordonnes)}")
    
    if not disponibles:
        print("❌ Tous vos subordonnés sont fatigués ou blessés.")
        print("💡 Attendez le prochain tour pour qu'ils récupèrent.")
        input("Appuyez sur Entrée pour continuer...")
        return
    
    print("\n📋 TYPES DE MISSIONS:")
    print("1. Mission simple (rapide)")
    print("2. Mission complexe (plusieurs phases)")  
    print("3. Mission spéciale (selon votre niveau)")
    print("0. Retour")
    
    choix_type = input("\nType de mission: ")
    
    if choix_type == "1":
        # Mission simple (ton système existant)
        print("\nQui envoyer en mission ?")
        for i, sub in enumerate(disponibles, 1):
            print(f"{i}. {sub.nom} - {sub.role} (Puissance: {sub.puissance})")
        
        try:
            choix = int(input("Numéro: ")) - 1
            if 0 <= choix < len(disponibles):
                game_engine.mission(player, disponibles[choix])
        except (ValueError, IndexError):
            print("Choix invalide.")
    
    elif choix_type == "2":
        # Mission complexe
        lancer_mission_complexe(player, disponibles)
    
    elif choix_type == "3":
        # Mission spéciale
        missions_spéciales_par_niveau(player, disponibles)
    
    input("Appuyez sur Entrée pour continuer...")

def lancer_mission_complexe(player, disponibles):
    """Lance une mission complexe avec choix multiples"""
    mission_exemple = {
        "nom": "Infiltration Casino Royal",
        "description": "Voler les recettes de la soirée poker VIP (Récompense estimée: 15,000$)",
        "phases": [
            {
                "nom": "Reconnaissance",
                "choix": {
                    "Étudier les plans du bâtiment": {"bonus_intelligence": 10, "temps": 2},
                    "Soudoyer un employé": {"coût": 2000, "accès_facile": True},
                    "Surveillance extérieure": {"bonus_discrétion": 5, "information": "partielle"}
                }
            },
            {
                "nom": "Infiltration",
                "choix": {
                    "Se déguiser en client VIP": {"charisme_requis": 15, "discrétion_max": True},
                    "Passer par les conduits": {"discrétion_requise": 20, "physique": True},
                    "Créer une diversion": {"complice_nécessaire": True, "attention_détournée": True}
                }
            }
        ]
    }
    
    print(f"\n🎯 MISSION: {mission_exemple['nom']}")
    print(f"📖 {mission_exemple['description']}")
    
    print("\nQui envoyer ?")
    for i, sub in enumerate(disponibles, 1):
        print(f"{i}. {sub.nom} - Intelligence:{sub.intelligence}, Discrétion:{sub.discrétion}, Charisme:{sub.charisme}")
    
    try:
        choix_sub = int(input("Numéro: ")) - 1
        if 0 <= choix_sub < len(disponibles):
            agent = disponibles[choix_sub]
            
            # Exécute chaque phase
            bonus_total = 0
            coût_total = 0
            
            for phase in mission_exemple["phases"]:
                print(f"\n🎬 PHASE: {phase['nom']}")
                choix_dispo = list(phase["choix"].keys())
                
                for i, option in enumerate(choix_dispo, 1):
                    print(f"{i}. {option}")
                
                choix_phase = int(input("Votre stratégie: ")) - 1
                option_choisie = choix_dispo[choix_phase]
                effets = phase["choix"][option_choisie]
                
                print(f"✅ {agent.nom} exécute: {option_choisie}")
                
                # Traite les effets
                for effet, valeur in effets.items():
                    if "bonus" in effet:
                        bonus_total += valeur
                    elif "coût" in effet or effet == "coût":
                        coût_total += valeur
                        if player.argent >= valeur:
                            player.argent -= valeur
                            print(f"💰 Coût: -{valeur}$")
                        else:
                            print("❌ Pas assez d'argent ! Mission compromise.")
                            bonus_total -= 20
            
            # Calcul du résultat final
            chances_succès = 50 + bonus_total
            if agent.intelligence >= 15:
                chances_succès += 10
            if agent.discrétion >= 18:
                chances_succès += 15
            
            résultat = random.randint(1, 100)
            
            if résultat <= chances_succès:
                récompense = random.randint(12000, 18000)
                player.argent += récompense
                player.missions_réussies += 1
                agent.gagner_expérience(50)
                
                print(f"\n🎉 MISSION RÉUSSIE !")
                print(f"💰 Gain: +{récompense}$")
                print(f"⭐ Réputation: +10")
                player.réputation += 10
                
            else:
                print(f"\n💥 MISSION ÉCHOUÉE !")
                player.missions_échouées += 1
                agent.fatigué = True
                if résultat <= 20:
                    agent.blessé = True
                    print(f"🤕 {agent.nom} a été blessé !")
                
        else:
            print("Choix invalide.")
    except (ValueError, IndexError):
        print("Choix invalide.")

def menu_développement_organisation(player):
    """Menu pour développer l'organisation avec progression immersive"""
    clear_screen()
    print("📈 DÉVELOPPEMENT DE L'ORGANISATION")
    print("═" * 50)
    
    niveaux = {
        1: "Petite bande",
        2: "Gang organisé",
        3: "Cartel régional",
        4: "Empire criminel"
    }
    
    niveau_actuel = player.niveau_organisation
    nom_niveau = niveaux.get(niveau_actuel, "Organisation inconnue")
    print(f"🌟 Niveau actuel: {niveau_actuel} - {nom_niveau}")
    
    # Conditions pour passer au niveau supérieur
    conditions = {
        2: {"argent": 50000, "réputation": 25, "missions_réussies": 10},
        3: {"argent": 200000, "réputation": 60, "missions_réussies": 25},
        4: {"argent": 1000000, "réputation": 90, "missions_réussies": 50}
    }
    
    niveau_suivant = niveau_actuel + 1
    if niveau_suivant in conditions:
        req = conditions[niveau_suivant]
        print(f"\nConditions pour passer au niveau {niveau_suivant} - {niveaux[niveau_suivant]}:")
        print(f"💰 Argent: {player.argent:,}/{req['argent']:,}")
        print(f"⭐ Réputation: {player.réputation}/{req['réputation']}")
        print(f"🎯 Missions réussies: {player.missions_réussies}/{req['missions_réussies']}")
    else:
        print("\n🎉 Vous êtes au maximum de développement !")
    
    # Options immersives pour le joueur
    print("\n📋 Actions disponibles:")
    print("1. Monter le niveau de l'organisation (si conditions remplies)")
    print("2. Débloquer de nouvelles capacités")
    print("3. Améliorer l'infrastructure")
    print("4. Recruter des subordonnés clés")
    print("0. Retour au menu principal")
    
    choix = input("\nVotre choix: ")
    
    if choix == "1":
        if player.vérifier_montée_niveau():  # fonction à créer dans Player
            résultat = player.monter_niveau_organisation()  # augmente le niveau
            print(f"\n🎉 {résultat}")
        else:
            print("\n❌ Conditions non remplies pour monter de niveau.")
    
    elif choix == "2":
        print("\n💡 Capacités disponibles pour débloquer :")
        capacites = [
            "Amélioration des profits", "Discrétion accrue des missions",
            "Augmentation de la loyauté des subordonnés", "Réseau de renseignement"
        ]
        for i, c in enumerate(capacites, 1):
            print(f"{i}. {c}")
        choix_cap = input("Choisissez une capacité à débloquer: ")
        print("✅ Capacité débloquée (à implémenter selon ton système)")
    
    elif choix == "3":
        print("\n🏢 Infrastructure :")
        infrastructures = ["QG sécurisé", "Entrepôt", "Garage de véhicules", "Laboratoire"]
        for i, infra in enumerate(infrastructures, 1):
            print(f"{i}. {infra}")
        choix_infra = input("Choisissez une infrastructure à améliorer: ")
        print("✅ Amélioration appliquée (à implémenter selon ton système)")
    
    elif choix == "4":
        print("\n🧑‍🤝‍🧑 Subordonnés clés :")
        print("Cette option permettra de recruter des membres spéciaux avec compétences uniques.")
    
    input("\nAppuyez sur Entrée pour continuer...")
def missions_spéciales_par_niveau(player, disponibles):
    """Missions spéciales débloquées selon le niveau d'organisation"""
    missions_par_niveau = {
        1: ["Protection de témoin", "Vol de voiture"],
        2: ["Chantage politique", "Guerre de territoire", "Sabotage industriel"],
        3: ["Assassinat ciblé", "Blanchiment d'argent", "Corruption de juge"],
        4: ["Opération internationale", "Empire économique", "Renversement politique"]
    }
    
    missions_disponibles = missions_par_niveau.get(player.niveau_organisation, [])
    
    if not missions_disponibles:
        print("❌ Aucune mission spéciale disponible à votre niveau.")
        return
    
    print(f"\n🌟 MISSIONS SPÉCIALES - NIVEAU {player.niveau_organisation}")
    for i, mission in enumerate(missions_disponibles, 1):
        print(f"{i}. {mission}")
    
    print("Ces missions sont plus risquées mais plus lucratives !")

def get_organization_name(niveau):
    """Retourne le nom de l'organisation selon le niveau"""
    noms = {1: "Petite bande", 2: "Gang organisé", 3: "Cartel régional", 4: "Empire criminel"}
    return noms.get(niveau, "Organisation mystérieuse")

def menu_principal_amélioré():
    """Menu principal avec toutes les nouvelles options"""
    # Initialisation du jeu
    clear_screen()
    afficher_logo()
    
    nom_boss = input("👑 Entrez le nom de votre boss: ")
    player = Player(nom_boss)
    rival = Enemy()
    
    # Pas besoin de GameEngine, on utilise directement tes fonctions
    turn_number = 1
    
    while True:
        clear_screen()
        afficher_logo()
        
        # Affichage rapide des stats
        print(f"👑 {player.nom_boss} | 💰 {player.argent:,}$ | ⭐ {getattr(player, 'réputation', 0)}")
        print(f"👥 Équipe: {len(player.subordonnes)} | 🎯 Tour: {turn_number}")
        print("═" * 50)
        
        # Menu principal
        print("1. 📊 Voir mon organisation (détaillé)")
        print("2. 👥 Gérer mon équipe")
        print("3. 🆕 Recruter un subordonné")
        print("4. 🎯 Envoyer en mission")
        print("5. 🔍 Voir l'organisation rivale")
        print("6. 🏪 Marché noir (achats/ventes)")
        print("7. 📈 Développer l'organisation")
        print("8. ⏭️  Passer au tour suivant")
        print("0. 🚪 Quitter")
        
        choix = input("\nVotre choix: ")
        
        if choix == "1":
            afficher_stats_détaillées(player)
        elif choix == "2":
            afficher_équipe_détaillée(player)
        elif choix == "3":
            # Utilise ta fonction de recrutement existante
            recruter_subordonné_amélioré(player)
        elif choix == "4":
            # Utilise ta fonction de mission existante
            menu_mission_simple(player)
        elif choix == "5":
            # Utilise ta fonction d'espionnage existante
            voir_organisation_rivale(rival)
        elif choix == "6":
            menu_marché_noir(player)
        elif choix == "7":
            menu_développement_organisation(player)
        elif choix == "8":
            # Utilise ta fonction next_turn existante
            passer_au_tour_suivant(player, rival, turn_number)
            turn_number += 1
        elif choix == "0":
            print("👋 Merci d'avoir joué à Organization Game !")
            break
        else:
            print("❌ Choix invalide.")
            input("Appuyez sur Entrée pour continuer...")

# =====================================================
# FONCTIONS ADAPTÉES À TON CODE EXISTANT
# =====================================================

def recruter_subordonné_amélioré(player):
    """Version améliorée de ton recrutement existant"""
    clear_screen()
    print("🆕 RECRUTEMENT DE SUBORDONNÉ")
    print("═" * 40)
    
    # Vérifie s'il peut recruter
    max_subs = getattr(player, 'max_subordonnes', 10)  # Limite par défaut
    if len(player.subordonnes) >= max_subs:
        print(f"❌ Limite atteinte ! Maximum {max_subs} subordonnés.")
        input("Appuyez sur Entrée pour continuer...")
        return
    
    coût_recrutement = 2000
    if player.argent < coût_recrutement:
        print(f"❌ Pas assez d'argent ! Coût: {coût_recrutement}$")
        input("Appuyez sur Entrée pour continuer...")
        return
    
    # Génère un candidat avec tes méthodes existantes
    candidat = Subordinate()
    
    print(f"👤 CANDIDAT: {candidat.nom}")
    print(f"🎭 Rôle: {candidat.role}")
    print(f"💪 Puissance: {candidat.puissance}")
    
    # Ajoute les nouvelles stats si elles existent
    if hasattr(candidat, 'intelligence'):
        print(f"🧠 Intelligence: {candidat.intelligence}")
    if hasattr(candidat, 'discrétion'):
        print(f"🔍 Discrétion: {candidat.discrétion}")
    if hasattr(candidat, 'loyauté'):
        print(f"❤️  Loyauté: {candidat.loyauté}")
    
    # Dialogue de recrutement
    if hasattr(candidat, 'dialogue_recrutement'):
        print(f"\n💬 {candidat.nom} dit: '{candidat.dialogue_recrutement()}'")
    
    # Histoire personnelle
    if hasattr(candidat, 'histoire_personnelle'):
        print(f"📖 Histoire: {candidat.histoire_personnelle}")
    
    print(f"\n💰 Coût du recrutement: {coût_recrutement}$")
    choix = input("\nRecrutez-vous ce candidat ? (o/n): ").lower()
    
    if choix == 'o':
        player.argent -= coût_recrutement
        player.subordonnes.append(candidat)
        print(f"✅ {candidat.nom} a rejoint votre organisation !")
    else:
        print("❌ Vous déclinez l'offre.")
    
    input("Appuyez sur Entrée pour continuer...")

def menu_mission_simple(player):
    """Menu de missions adapté à ton système"""
    clear_screen()
    print("🎯 MISSIONS DISPONIBLES")
    print("═" * 30)
    
    if not player.subordonnes:
        print("❌ Aucun subordonné disponible.")
        input("Appuyez sur Entrée pour continuer...")
        return
    
    # Affiche subordonnés disponibles
    print("👥 QUI ENVOYER EN MISSION ?")
    disponibles = []
    
    for i, sub in enumerate(player.subordonnes):
        statut = ""
        disponible = True
        
        if hasattr(sub, 'fatigué') and sub.fatigué:
            statut += " 😴"
            disponible = False
        if hasattr(sub, 'blessé') and sub.blessé:
            statut += " 🤕"
            disponible = False
            
        if disponible:
            disponibles.append((i, sub))
            print(f"{len(disponibles)}. {sub.nom} - {sub.role} (Puissance: {sub.puissance}){statut}")
    
    if not disponibles:
        print("❌ Tous vos subordonnés sont indisponibles.")
        input("Appuyez sur Entrée pour continuer...")
        return
    
    print("0. Retour")
    
    try:
        choix = int(input("\nVotre choix: "))
        if 1 <= choix <= len(disponibles):
            _, subordonné = disponibles[choix-1]
            lancer_mission_simple(player, subordonné)
        elif choix != 0:
            print("Choix invalide.")
    except ValueError:
        print("Choix invalide.")
    
    if choix != 0:
        input("Appuyez sur Entrée pour continuer...")

def lancer_mission_simple(player, subordonné):
    """Lance une mission simple"""
    missions = [
        {"nom": "Vol à l'étalage", "difficulté": 20, "gain": (500, 1500)},
        {"nom": "Extorsion locale", "difficulté": 35, "gain": (1000, 3000)},
        {"nom": "Cambriolage", "difficulté": 50, "gain": (2000, 5000)},
        {"nom": "Braquage", "difficulté": 70, "gain": (3000, 8000)},
        {"nom": "Infiltration", "difficulté": 85, "gain": (5000, 12000)}
    ]
    
    mission = random.choice(missions)
    
    print(f"\n🎯 MISSION: {mission['nom']}")
    print(f"📊 Difficulté: {mission['difficulté']}/100")
    print(f"💰 Gain estimé: {mission['gain'][0]}-{mission['gain'][1]}$")
    
    if input("\nLancer la mission ? (o/n): ").lower() != 'o':
        return
    
    # Calcul des chances de succès
    chances = min(95, max(5, subordonné.puissance + random.randint(-10, 10) - mission['difficulté'] + 50))
    
    print(f"🎲 Chances de succès: {chances}%")
    résultat = random.randint(1, 100)
    
    if résultat <= chances:
        gain = random.randint(mission['gain'][0], mission['gain'][1])
        player.argent += gain
        
        print(f"✅ MISSION RÉUSSIE !")
        print(f"💰 Gain: +{gain}$")
        
        # XP et amélioration
        if hasattr(subordonné, 'gagner_expérience'):
            level_up = subordonné.gagner_expérience(25)
            if level_up:
                print(f"🎉 {subordonné.nom} monte de niveau !")
        
        # Augmente les stats du joueur
        if hasattr(player, 'missions_réussies'):
            player.missions_réussies += 1
        if hasattr(player, 'réputation'):
            player.réputation += 5
            
    else:
        print(f"💥 MISSION ÉCHOUÉE !")
        
        # Conséquences
        if hasattr(subordonné, 'fatigué'):
            subordonné.fatigué = True
            print(f"😴 {subordonné.nom} est fatigué.")
        
        if résultat <= 15:  # Échec critique
            if hasattr(subordonné, 'blessé'):
                subordonné.blessé = True
                print(f"🤕 {subordonné.nom} a été blessé !")
        
        if hasattr(player, 'missions_échouées'):
            player.missions_échouées += 1

def voir_organisation_rivale(rival):
    """Affiche l'organisation rivale"""
    clear_screen()
    print("🔍 ORGANISATION RIVALE")
    print("═" * 30)
    
    print(f"🏢 {getattr(rival, 'nom', 'Organisation Mystérieuse')}")
    
    if hasattr(rival, 'subordonnes') and rival.subordonnes:
        print(f"👥 Membres: {len(rival.subordonnes)}")
        for sub in rival.subordonnes:
            print(f"  • {sub.nom} - {sub.role} (Puissance: {sub.puissance})")
    else:
        print("❓ Informations limitées sur leurs membres.")
    
    if hasattr(rival, 'réputation'):
        print(f"⭐ Réputation: {rival.réputation}")
    
    print("\n💡 Utilisez l'espionnage pour obtenir plus d'informations.")
    input("Appuyez sur Entrée pour continuer...")

def passer_au_tour_suivant(player, rival, turn_number):
    """Gère le passage au tour suivant"""
    clear_screen()
    print(f"⏭️  PASSAGE AU TOUR {turn_number + 1}")
    print("═" * 40)
    
    # Récupération automatique
    récupérés = 0
    for sub in player.subordonnes:
        if hasattr(sub, 'fatigué') and sub.fatigué:
            if random.randint(1, 100) <= 40:  # 40% de chance
                sub.fatigué = False
                print(f"💪 {sub.nom} a récupéré.")
                récupérés += 1
        
        if hasattr(sub, 'blessé') and sub.blessé:
            if random.randint(1, 100) <= 25:  # 25% de chance
                sub.blessé = False
                print(f"🏥 {sub.nom} s'est remis de ses blessures.")
    
    if récupérés > 0:
        print(f"✅ {récupérés} subordonné(s) ont récupéré.")
    
    # Événement aléatoire simple
    if random.randint(1, 100) <= 40:  # 40% de chance
        événements_possibles = [
            {"nom": "Découverte d'argent", "effet": lambda p: setattr(p, 'argent', p.argent + random.randint(1000, 3000))},
            {"nom": "Informations utiles", "effet": lambda p: print("🔍 Vous obtenez des renseignements sur vos ennemis.")},
            {"nom": "Problème de loyauté", "effet": lambda p: print("⚠️  Des tensions apparaissent dans votre équipe.")},
            {"nom": "Opportunité", "effet": lambda p: print("💡 Une nouvelle opportunité se présente...")},
        ]
        
        événement = random.choice(événements_possibles)
        print(f"\n🎲 ÉVÉNEMENT: {événement['nom']}")
        événement["effet"](player)
    
    print(f"\n🎯 Tour {turn_number + 1} commence !")
    input("Appuyez sur Entrée pour continuer...")

# Point d'entrée principal
if __name__ == "__main__":
    menu_principal_amélioré()

def get_max_subordinates(niveau):
    """Retourne le nombre max de subordonnés par niveau"""
    limites = {1: 4, 2: 8, 3: 12, 4: 20}
    return limites.get(niveau, 4)

def menu_marché_noir(player):
    """Menu du marché noir pour acheter des équipements"""
    clear_screen()
    print("🏪 MARCHÉ NOIR")
    print("═" * 30)
    
    articles = {
        "Équipement furtif": {"prix": 5000, "effet": "Discrétion équipe +10"},
        "Armes avancées": {"prix": 8000, "effet": "Puissance équipe +15"},
        "Système de surveillance": {"prix": 12000, "effet": "Intelligence missions +20"},
        "Véhicules blindés": {"prix": 15000, "effet": "Sécurité +25"},
        "Corruption policière": {"prix": 20000, "effet": "Réduction risques missions"}
    }
    
    for i, (article, info) in enumerate(articles.items(), 1):
        print(f"{i}. {article} - {info['prix']:,}$ ({info['effet']})")
    
    print("0. Retour")
    
    try:
        choix = int(input("\nQue voulez-vous acheter ? "))
        if 1 <= choix <= len(articles):
            article_choisi = list(articles.keys())[choix-1]
            prix = articles[article_choisi]["prix"]
            
            if player.argent >= prix:
                player.argent -= prix
                print(f"✅ Vous avez acheté: {article_choisi}")
                # Ajouter les effets selon l'article
            else:
                print(f"❌ Pas assez d'argent ! (Besoin: {prix:,}$)")
    except (ValueError, IndexError):
        pass
    
    input("Appuyez sur Entrée pour continuer...")

def menu_développement_organisation(player):
    """Menu pour développer l'organisation"""
    clear_screen()
    print("📈 DÉVELOPPEMENT ORGANISATION")
    print("═" * 40)
    
    if player.vérifier_montée_niveau():
        print("🎉 Votre organisation peut évoluer !")
        if input("Voulez-vous faire évoluer votre organisation ? (o/n): ").lower() == 'o':
            résultat = player.monter_niveau_organisation()
            print(résultat)
    else:
        print("Conditions pour le niveau suivant:")
        # Afficher les conditions requises
        conditions = {
            2: {"argent": 50000, "réputation": 25, "missions_réussies": 10},
            3: {"argent": 200000, "réputation": 60, "missions_réussies": 25},
            4: {"argent": 1000000, "réputation": 90, "missions_réussies": 50}
        }
        
        niveau_cible = player.niveau_organisation + 1
        if niveau_cible in conditions:
            req = conditions[niveau_cible]
            print(f"💰 Argent: {player.argent:,}/{req['argent']:,}")
            print(f"⭐ Réputation: {player.réputation}/{req['réputation']}")
            print(f"🎯 Missions réussies: {player.missions_réussies}/{req['missions_réussies']}")
    
    input("Appuyez sur Entrée pour continuer...")

# =====================================================
# RESOURCES/ - Fichiers de données
# =====================================================

# resources/noms_subordinates.json
noms_data = {
    "prenoms": [
        "Alex", "Morgan", "Jordan", "Casey", "Riley", "Avery", "Quinn", "Blake",
        "Taylor", "Cameron", "Parker", "Sage", "River", "Phoenix", "Skyler",
        "Remy", "Harper", "Finley", "Emery", "Reese"
    ],
    "noms": [
        "Steel", "Shadow", "Cross", "Stone", "Wild", "Fox", "Wolf", "Raven",
        "Storm", "Frost", "Knight", "Hunter", "Sharp", "Quick", "Dark",
        "Silver", "Gold", "Iron", "Swift", "Black"
    ]
}

# resources/histoires_recrutement.json
histoires_recrutement = {
    "backgrounds": [
        "Ancien employé de banque licencié pour avoir découvert des irrégularités",
        "Ex-militaire cherchant un nouveau sens à sa vie",
        "Petit délinquant voulant passer au niveau supérieur",
        "Informaticien génial mais socialement inadapté",
        "Ancien flic désabusé par la corruption du système",
        "Artiste martial expert cherchant des défis",
        "Négociateur expérimenté avec un passé mystérieux"
    ],
    "motivations": [
        "Venge la mort de sa famille",
        "Cherche à prouver sa valeur",
        "A une dette d'honneur envers vous",
        "Fuit un passé compromettant",
        "Veut l'argent pour sauver quelqu'un",
        "Admire votre réputation",
        "N'a nulle part ailleurs où aller"
    ]
}

print("""
🎯 INTÉGRATION DANS TON CODE EXISTANT :

1. **subordinates.py** : Copie les nouvelles méthodes dans ta classe Subordinate
2. **player.py** : Ajoute les nouveaux attributs et méthodes à ta classe Player  
3. **game_engine.py** : Remplace ta fonction next_turn() par next_turn_amélioré()
4. **enemies.py** : Ajoute les méthodes d'IA à ta classe Enemy
5. **resources/** : Crée les fichiers JSON pour les données

✨ NOUVELLES FONCTIONNALITÉS DÉBLOQUÉES :
- Loyauté dynamique et événements personnels
- Système d'expérience et de niveau pour les subordonnés
- Missions complexes avec choix multiples
- IA ennemie intelligente qui s'adapte
- Progression d'organisation avec déblocages
- Événements contextuels basés sur l'état du jeu
""")
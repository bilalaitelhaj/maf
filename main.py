from player import Player
from subordinate import Subordinate

def main():
    print("=== Bienvenue dans Organization Game ===")
    name = input("Entre le nom de ton Boss: ")
    player = Player(name)

    # Subordonnés disponibles
    soldier = Subordinate("Marc", "Soldat", power=10, cost=30)
    spy = Subordinate("Luc", "Espion", power=5, cost=20)

    while True:
        print("\n--- Menu ---")
        print("1. Voir mon organisation")
        print("2. Recruter un Soldat (30)")
        print("3. Recruter un Espion (20)")
        print("4. Quitter")

        choice = input("Ton choix: ")

        if choice == "1":
            player.show_team()
        elif choice == "2":
            player.recruit(soldier)
        elif choice == "3":
            player.recruit(spy)
        elif choice == "4":
            print("Merci d'avoir joué !")
            break
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    main()
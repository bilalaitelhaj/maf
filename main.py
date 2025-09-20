# main.py

# ======= Subordonnés =======
class Subordinate:
    def __init__(self, name, role, power, cost):
        self.name = name
        self.role = role
        self.power = power
        self.cost = cost

    def __str__(self):
        return f"{self.name} ({self.role}) - Puissance: {self.power}, Coût: {self.cost}"

# ======= Joueur =======
class Player:
    def __init__(self, name):
        self.name = name
        self.money = 100
        self.team = []

    def recruit(self, subordinate: Subordinate):
        if self.money >= subordinate.cost:
            self.team.append(subordinate)
            self.money -= subordinate.cost
            print(f"{subordinate.name} a rejoint ton organisation !")
        else:
            print("💸 Pas assez d'argent pour recruter.")

    def show_team(self):
        print(f"\nOrganisation de {self.name} (💰 {self.money}):")
        if not self.team:
            print(" - Aucun subordonné pour l'instant.")
        for s in self.team:
            print(f" - {s}")

# ======= Jeu principal =======
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
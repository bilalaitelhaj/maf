from subordinate import Subordinate

class Player:
    def __init__(self, name):
        self.name = name
        self.money = 100  # argent de départ
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
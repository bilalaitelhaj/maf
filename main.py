import random

# ======= Subordonnés avec IA =======
name_syllables = ["ka", "lu", "mi", "ra", "so", "vi", "el", "na", "to"]
roles = ["Soldat", "Espion", "Recruteur", "Capitaine"]
qualities = ["courageux", "intelligent", "rapide", "fidéle", "discret"]
flaws = ["impulsif", "paresseux", "têtu", "curieux", "colérique"]
story_templates = [
    "Vous l'avez rencontré {} et il/elle a décidé de rejoindre votre organisation.",
    "Alors que vous {} , {} a remarqué votre puissance et a accepté de vous suivre.",
    "{} vous a défié à un duel et, impressionné par votre force, a rejoint votre équipe."
]

def generate_name():
    return "".join(random.choice(name_syllables).capitalize() for _ in range(2))

class Subordinate:
    def __init__(self):
        self.name = generate_name()
        self.role = random.choice(roles)
        self.power = random.randint(5, 15)
        self.level = 1
        self.quality = random.choice(qualities)
        self.flaw = random.choice(flaws)
        template = random.choice(story_templates)
        event = random.choice(["dans une taverne sombre", "en train de fouiller vos affaires", "dans la rue"])
        self.story = template.format(event, self.name)

    def __str__(self):
        return (f"{self.name} ({self.role}) - Niveau: {self.level}, Puissance: {self.power}\n"
                f"Qualité: {self.quality}, Défaut: {self.flaw}\nHistoire: {self.story}")


# ======= Joueur =======
class Player:
    def __init__(self, name):
        self.name = name
        self.money = 100
        self.team = []

    def recruit(self):
        if self.money >= 20:  # coût de base
            new_sub = Subordinate()
            self.team.append(new_sub)
            self.money -= 20
            print("\n🎉 Nouveau subordonné recruté !")
            print(new_sub)
            print(f"💰 Argent restant : {self.money}")
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

    turn = 1
    while True:
        print(f"\n--- Tour {turn} ---")
        print("1. Voir mon organisation")
        print("2. Recruter un subordonné")
        print("3. Quitter")

        choice = input("Ton choix: ")

        if choice == "1":
            player.show_team()
        elif choice == "2":
            player.recruit()
        elif choice == "3":
            print("Merci d'avoir joué !")
            break
        else:
            print("Choix invalide.")

        turn += 1

if __name__ == "__main__":
    main()

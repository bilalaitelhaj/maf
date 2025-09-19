class Subordinate:
    def __init__(self, name, role, power, cost):
        self.name = name
        self.role = role
        self.power = power
        self.cost = cost

    def __str__(self):
        return f"{self.name} ({self.role}) - Puissance: {self.power}, Coût: {self.cost}"
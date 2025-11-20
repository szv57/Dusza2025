class Card:
    TYPES    = ("fold", "levego", "viz", "tuz")
    TYPES_HU = ("föld", "levegő", "víz", "tűz")


    def __init__(self, name: str, damage: int, hp: int, type: str):
        self.name   = name   if len(name) <= 16         else name[:16]
        self.damage = damage if 2 <= int(damage) <= 100 else 2
        self.hp     = hp     if 1 <= int(hp) <= 100     else 1
        self.type   = type   if type in self.TYPES      else "fold"


class Leader(Card):
    def __init__(self, name: str, base: Card, mod: str):
        super().__init__(name, base.damage, base.hp, base.type)

        if   mod == "sebzes":  self.damage *= 2
        elif mod == "eletero": self.hp     *= 2
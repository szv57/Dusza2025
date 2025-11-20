from collections import OrderedDict
from pathlib     import Path

from card    import Card, Leader
from dungeon import Dungeon


class World:
    def __init__(self):
        self.cards    = OrderedDict()
        self.leaders  = OrderedDict()
        self.dungeons = OrderedDict()
    

    def add_card(self, card: Card):
        self.cards[card.name] = card
    

    def add_leader(self, leader: Leader):
        self.leaders[leader.name] = leader
    

    def add_dungeon(self, dungeon: Dungeon):
        self.dungeons[dungeon.name] = dungeon
    

    def load(self, path: str):
        if not Path(path).is_file():
            return
        
        lines = []
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        for line in lines:
            if not line.strip():
                continue
            
            parts = [part.strip() for part in line.strip().split(";")]
            if parts[0] == "kartya":
                card_name, card_damage, card_hp, card_type = parts[1:]
                card = Card(card_name, int(card_damage), int(card_hp), card_type)
                self.add_card(card)

            elif parts[0] == "vezer":
                leader_name, leader_base_name, leader_mod = parts[1:]
                leader_base = self.cards[leader_base_name]
                leader = Leader(leader_name, leader_base, leader_mod)
                self.add_leader(leader)

            elif parts[0] == "kazamata":
                dungeon_type, dungeon_name = parts[1:2]
                dungeon_cards_names = [name.strip() for name in parts[3].strip().split(",")]
                dungeon_cards = [card for card in self.cards]

                dungeon = Dungeon(dungeon_type, dungeon_name, dungeon_cards)
                self.add_dungeon(dungeon)

    

    def save(self, path: str):
        lines = []

        for card in self.cards.values():
            lines.append(f"kartya;{card.name};{card.damage};{card.hp};{card.type}")
        
        lines.append("")

        for leader in self.leaders.values():
            lines.append(f"vezer;{leader.name};{leader.damage};{leader.hp};{leader.type}")
        
        lines.append("")

        for dungeon in self.dungeons.values():
            card_names = ",".join(card.name for card in dungeon.cards)
            if   dungeon.type == "egyszeru":
                lines.append(f"kazamata;{dungeon.type};{dungeon.name};{card_names};{dungeon.prize}")
            elif dungeon.type == "kis":
                leader_name = dungeon.leader.name if dungeon.leader else ""
                lines.append(f"kazamata;{dungeon.type};{dungeon.name};{card_names};{leader_name};{dungeon.prize}")
            elif dungeon.type == "nagy":
                leader_name = dungeon.leader.name if dungeon.leader else ""
                lines.append(f"kazamata;{dungeon.type};{dungeon.name};{card_names};{leader_name}")

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))
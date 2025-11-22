from pathlib import Path
from typing  import Dict, List

import json

from card    import Card, load_card
from dungeon import Dungeon, load_dungeon


class World:
    def __init__(self, name: str) -> None:
        self.name = name[:20]

        self.cards    : Dict[str, Card]    = {}
        self.leaders  : Dict[str, Card]    = {}
        self.dungeons : Dict[str, Dungeon] = {}

        self.card_order   : List[str] = []
        self.leader_order : List[str] = []
    

    def ___(self) -> str:
        cards    = ", ".join(self.cards.keys())
        leaders  = ", ".join(self.leaders.keys())
        dungeons = ", ".join(self.dungeons.keys())

        card_order   = ", ".join(self.card_order)
        leader_order = ", ".join(self.leader_order)

        string  = f"{self.name}\n"
        string += "\n"
        string += f"Cards:    {cards}\n"
        string += f"Leaders:  {leaders}\n"
        string += f"Dungeons: {dungeons}\n"
        string += "\n"
        string += f"Card order:   {card_order}\n"
        string += f"Leader order: {leader_order}"
        return string
    

    def save(self, path: str) -> None:
        d = {
            "name"         : self.name,
            "cards"        : [card.name for card in self.cards.values()],
            "leaders"      : [leader.name for leader in self.leaders.values()],
            "dungeons"     : [dungeon.name for dungeon in self.dungeons.values()],
            "card_order"   : self.card_order,
            "leader_order" : self.leader_order
        }

        with open(path, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=4, ensure_ascii=False)
        
        for card in self.cards.values():
            card.save(f"{card.name}.json")
        
        for leader in self.leaders.values():
            leader.save(f"{leader.name}.json")
        
        for dungeon in self.dungeons.values():
            dungeon.save(f"{dungeon.name}.json")
    

    def get_card(self, name: str) -> "Card | None":
        return self.cards.get(name)
    

    def get_leader(self, name: str) -> "Card | None":
        return self.leaders.get(name)
    

    def get_dungeon(self, name: str) -> "Dungeon | None":
        return self.dungeons.get(name)
    

    def add_card(self, card: Card) -> bool:
        if card.leader:
            return False
        
        if card.name in self.cards or card.name in self.card_order:
            return False
        
        self.cards[card.name] = card
        self.card_order.append(card.name)
        return True
    

    def add_leader(self, leader: Card) -> bool:
        if not leader.leader:
            return False
        
        if leader.name in self.leaders or leader.name in self.leader_order:
            return False
        
        self.leaders[leader.name] = leader
        self.leader_order.append(leader.name)
        return True
    

    def add_dungeon(self, dungeon: Dungeon) -> bool:
        if dungeon.name in self.dungeons:
            return False
        
        self.dungeons[dungeon.name] = dungeon
        return True
    

    def export(self, path: str) -> None:
        lines = []

        for card in self.cards.values():
            lines.append(f"kartya;{card.name};{card.damage};{card.hp};{card.type}")
        
        lines.append("")

        for leader in self.leaders.values():
            lines.append(f"vezer;{leader.name};{leader.damage};{leader.hp};{leader.type}")
        
        lines.append("")

        for dungeon in self.dungeons.values():
            cards = ",".join(card for card in dungeon.cards)
            
            if dungeon.type == "egyszeru":
                lines.append(f"kazamata;{dungeon.type};{dungeon.name};{cards};{dungeon.reward}")
            
            elif dungeon.type == "kis":
                lines.append(f"kazamata;{dungeon.type};{dungeon.name};{cards};{dungeon.leader};{dungeon.reward}")
            
            elif dungeon.type == "nagy":
                lines.append(f"kazamata;{dungeon.type};{dungeon.name};{cards};{dungeon.leader}")

        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))


def load_world(path: str) -> "World | None":
    file_path = Path(path)
    if not file_path.is_file():
        return None
     
    with open(path, "r", encoding="utf-8") as f:
        d = json.load(f)
        
    world = World(d["name"])

    for card_name in d["cards"]:
        card_obj = load_card(f"{card_name}.json")
        if not card_obj:
            return None
            
        if not world.add_card(card_obj):
            return None
        
    for leader_name in d["leaders"]:
        leader_obj = load_card(f"{leader_name}.json")
        if not leader_obj:
            return None

        if not leader_obj.leader:
            leader_obj.leader = True
            
        if not world.add_leader(leader_obj):
            return None
        
    for dungeon_name in d["dungeons"]:
        dungeon_obj = load_dungeon(f"{dungeon_name}.json")
        if not dungeon_obj:
            return None
            
        if not world.add_dungeon(dungeon_obj):
            return None

    for card_name in d["card_order"]:
        if card_name not in world.card_order and card_name in world.cards:
            world.card_order.append(card_name)
        else:
            return None
        
    for leader_name in d["leader_order"]:
        if leader_name not in world.leader_order and leader_name in world.leaders:
            world.leader_order.append(leader_name)
        else:
            return None

    return None
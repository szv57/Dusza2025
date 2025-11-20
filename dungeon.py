from typing import List, Optional

from card import Card, Leader


class Dungeon:
    TYPES    = ("egyszeru", "kis", "nagy")
    TYPES_HU = ("egyszerű", "kis", "nagy")


    def __init__(self, type: str, name: str, cards: List[Card], leader: Optional[Leader] = None, prize: Optional[str] = None):
        self.type   = type if type in self.TYPES else "egyszeru"
        self.name   = name if len(name) <= 20    else name[:20]
        self.cards  = []
        self.leader = leader
        self.prize  = prize

        for card in cards:
            if not any(c.name == card.name for c in self.cards):
                self.cards.append(card)
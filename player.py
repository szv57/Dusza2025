from __future__  import annotations
from dataclasses import dataclass, field
from typing      import Dict, List

from card import CardTemplate


@dataclass
class PlayerCard:
    name   : str
    damage : int
    hp     : int
    type   : str


@dataclass
class PlayerState:
    collection_order : List[str] = field(default_factory=list)
    collection       : Dict[str, PlayerCard] = field(default_factory=dict)
    deck             : List[str] = field(default_factory=list)

    def add_to_collection_from_template(self, tmpl: CardTemplate) -> None:
        if tmpl.name not in self.collection:
            self.collection[tmpl.name] = PlayerCard(tmpl.name, tmpl.damage, tmpl.hp, tmpl.type)
            self.collection_order.append(tmpl.name)

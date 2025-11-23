from __future__  import annotations
from dataclasses import dataclass
from typing      import Set, FrozenSet


CARD_TYPES = ["fold", "levego", "viz", "tuz"]

STRONG_PAIRS : Set[FrozenSet[str]] = {
    frozenset(("levego", "fold")),
    frozenset(("levego", "viz")),
    frozenset(("tuz",    "fold")),
    frozenset(("tuz",    "viz")),
}

WEAK_PAIRS   : Set[FrozenSet[str]] = {
    frozenset(("levego", "tuz")),
    frozenset(("fold",   "viz")),
}


@dataclass
class CardTemplate:
    name   : str
    damage : int
    hp     : int
    type   : str


def calculate_damage(att_type: str, def_type: str, base_damage: int) -> int:
    if att_type == def_type:
        return base_damage

    pair = frozenset((att_type, def_type))

    if pair in STRONG_PAIRS:
        return base_damage * 2
    if pair in WEAK_PAIRS:
        return base_damage // 2

    return base_damage

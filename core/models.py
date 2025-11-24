from dataclasses import dataclass
from typing import List, Dict, Optional


# Értékhalmazok és segédfüggvények


CARD_TYPES = {"fold", "levego", "viz", "tuz"}
DUNGEON_TYPES = {"egyszeru", "kis", "nagy"}
REWARD_TYPES = {"sebzes", "eletero"}


def parse_element(element_text: str) -> str:
    """
    Szövegből elem string.

    Engedélyezett értékek: "fold", "levego", "viz", "tuz".
    """

    element = element_text.strip().lower()
    if element not in CARD_TYPES:
        raise ValueError(f"Ismeretlen elem típus: {element_text}")
    return element


def parse_dungeon_type(dungeon_type_text: str) -> str:
    """
    Szövegből kazamata típus string.

    Engedélyezett értékek: "egyszeru", "kis", "nagy".
    """

    dungeon_type = dungeon_type_text.strip().lower()
    if dungeon_type not in DUNGEON_TYPES:
        raise ValueError(f"Ismeretlen kazamata típus: {dungeon_type_text}")
    return dungeon_type


def parse_reward_type(reward_type_text: str) -> str:
    """
    Szövegből jutalom típus string.

    Engedélyezett értékek: "sebzes", "eletero".
    """

    reward_type = reward_type_text.strip().lower()
    if reward_type not in REWARD_TYPES:
        raise ValueError(f"Ismeretlen jutalom típus: {reward_type_text}")
    return reward_type


# Alap adatszerkezetek


@dataclass
class Card:
    """
    Egy kártya (sima vagy vezér).

    damage: sebzés érték
    health: életerő
    element: "fold" / "levego" / "viz" / "tuz"
    """

    name: str
    damage: int
    health: int
    element: str


@dataclass
class Dungeon:
    """
    Egy kazamata leírása a világban.

    dungeon_type: "egyszeru" / "kis" / "nagy"
    simple_cards: a sima kártyák nevei sorrendben
    leader_name: vezér kártya neve (egyszerű kazamatánál None)
    reward: egyszerű és kis kazamatánál "sebzes" vagy "eletero", nagy kazamatánál None (ott új kártyát kapunk).
    """

    name: str
    dungeon_type: str
    simple_cards: List[str]
    leader_name: Optional[str]
    reward: Optional[str]


@dataclass
class Player:
    """
    A játékos állapota: gyűjtemény + pakli.
    """

    collection: Dict[str, Card]
    collection_order: List[str]
    deck: List[str]  # kártyanevek a gyűjteményből

    def __init__(self) -> None:
        self.collection = {}
        self.collection_order = []
        self.deck = []

    def add_to_collection(self, card: Card) -> None:
        if card.name in self.collection:
            return
        self.collection[card.name] = card
        self.collection_order.append(card.name)

    def max_deck_size(self) -> int:
        """
        A pakli maximális mérete: a gyűjtemény fele (felfelé kerekítve).
        """

        collection_size = len(self.collection_order)
        return (collection_size + 1) // 2

    def set_deck(self, card_names: List[str]) -> bool:
        """
        Új pakli beállítása. Visszatérés: sikerült-e.
        """

        if len(card_names) > self.max_deck_size():
            return False

        for name in card_names:
            if name not in self.collection:
                return False

        self.deck = list(card_names)
        return True

from typing import Dict, List, Optional

from .models import Card, Dungeon, Player, parse_element


class World:
    """
    A világ: sima kártyák, vezérek, kazamaták.
    A sorrendeket listákkal tároljuk az export miatt.
    """

    def __init__(self) -> None:
        self.simple_cards: Dict[str, Card] = {}
        self.simple_order: List[str] = []

        self.leaders: Dict[str, Card] = {}
        self.leader_order: List[str] = []

        self.dungeons: Dict[str, Dungeon] = {}
        self.dungeon_order: List[str] = []

    # Kártyák

    def add_simple_card(
        self, name: str, damage: int, health: int, element: str
    ) -> None:
        element_text = parse_element(element)
        card = Card(name=name, damage=damage, health=health, element=element_text)
        self.simple_cards[name] = card
        self.simple_order.append(name)

    def add_leader_from(self, new_name: str, base_name: str, mode: str) -> None:
        """
        Vezér létrehozása egy meglévő sima kártyából (teszt mód + játékmester).
        """

        base_card = self.simple_cards[base_name]
        if mode == "sebzes":
            card = Card(
                new_name, base_card.damage * 2, base_card.health, base_card.element
            )
        elif mode == "eletero":
            card = Card(
                new_name, base_card.damage, base_card.health * 2, base_card.element
            )
        else:
            raise ValueError("Ismeretlen vezér típusa: " + mode)
        self.leaders[new_name] = card
        self.leader_order.append(new_name)

    def add_leader_direct(
        self, name: str, damage: int, health: int, element: str
    ) -> None:
        """
        Vezér közvetlen felvétele adott adatokkal.
        Játékkörnyezet betöltésénél használjuk (JSON-ból).
        """

        element_text = parse_element(element)
        card = Card(name=name, damage=damage, health=health, element=element_text)
        self.leaders[name] = card
        self.leader_order.append(name)

    # Kazamaták

    def add_dungeon(
        self,
        name: str,
        dungeon_type: str,
        simple_cards: List[str],
        leader_name: Optional[str],
        reward: Optional[str],
    ) -> None:
        dungeon = Dungeon(
            name=name,
            dungeon_type=dungeon_type,
            simple_cards=list(simple_cards),
            leader_name=leader_name,
            reward=reward,
        )
        self.dungeons[name] = dungeon
        self.dungeon_order.append(name)

    # Segédfüggvények

    def first_missing_simple_card_for_player(self, player: Player) -> Optional[Card]:
        """
        Nagy kazamatánál: az első olyan sima kártya a világban, ami még nincs a játékos gyűjteményében.
        """

        for card_name in self.simple_order:
            if card_name not in player.collection:
                base_card = self.simple_cards[card_name]
                return Card(
                    base_card.name,
                    base_card.damage,
                    base_card.health,
                    base_card.element,
                )
        return None


class GameState:
    """
    Közös állapot teszt mód és játék mód számára.
    """

    def __init__(self) -> None:
        self.world = World()
        self.player = Player()
        self.difficulty: int = 0

    def add_collection_card_from_world(self, name: str) -> None:
        """
        Gyűjteménybe felvétel: mindig a világ sima kártyájáról készítünk másolatot.
        """

        base_card = self.world.simple_cards[name]
        copy_card = Card(
            base_card.name,
            base_card.damage,
            base_card.health,
            base_card.element,
        )
        self.player.add_to_collection(copy_card)


# Példa világ + játékos játék módban


def create_classic_game() -> GameState:
    """
    A klasszikus alap világ és játékos.
    """

    game = GameState()
    world = game.world

    # Sima kártyák (világ)
    world.add_simple_card("Arin", 2, 5, "fold")
    world.add_simple_card("Liora", 2, 4, "levego")
    world.add_simple_card("Nerun", 3, 3, "tuz")
    world.add_simple_card("Selia", 2, 6, "viz")
    world.add_simple_card("Torak", 3, 4, "fold")
    world.add_simple_card("Emera", 2, 5, "levego")
    world.add_simple_card("Vorn", 2, 7, "viz")
    world.add_simple_card("Kael", 3, 5, "tuz")
    world.add_simple_card("Myra", 2, 6, "fold")
    world.add_simple_card("Thalen", 3, 5, "levego")
    world.add_simple_card("Isara", 2, 6, "viz")

    # Vezérek
    world.add_leader_from("Lord Torak", "Torak", "sebzes")
    world.add_leader_from("Priestess Selia", "Selia", "eletero")

    # Kazamaták
    world.add_dungeon(
        name="Barlangi Portya",
        dungeon_type="egyszeru",
        simple_cards=["Nerun"],
        leader_name=None,
        reward="sebzes",
    )

    world.add_dungeon(
        name="Osi Szentely",
        dungeon_type="kis",
        simple_cards=["Arin", "Emera", "Selia"],
        leader_name="Lord Torak",
        reward="eletero",
    )

    world.add_dungeon(
        name="A melyseg kiralynoje",
        dungeon_type="nagy",
        simple_cards=["Liora", "Arin", "Selia", "Nerun", "Torak"],
        leader_name="Priestess Selia",
        reward=None,
    )

    # Játékos gyűjteménye
    for name in [
        "Arin",
        "Liora",
        "Selia",
        "Nerun",
        "Torak",
        "Emera",
        "Kael",
        "Myra",
        "Thalen",
        "Isara",
    ]:
        game.add_collection_card_from_world(name)

    return game

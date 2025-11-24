import json

from typing import Dict, Any

from .gamestate import GameState
from .models import parse_element


ENVIRONMENT_VERSION = 1


def save_environment(game: GameState, file_path: str) -> None:
    """
    Játékkörnyezet mentése JSON-be.

    - világ sima kártyái
    - vezérek (aktuális sebzés/életerő/elem)
    - kazamaták
    - kezdő gyűjtemény (névlista)
    """

    world = game.world
    player = game.player

    data: Dict[str, Any] = {
        "version": ENVIRONMENT_VERSION,
        "simple_cards": [],
        "leaders": [],
        "dungeons": [],
        "starting_collection": list(player.collection_order),
    }

    for name in world.simple_order:
        card = world.simple_cards[name]
        data["simple_cards"].append(
            {
                "name": card.name,
                "damage": card.damage,
                "health": card.health,
                "element": card.element,
            }
        )

    for name in world.leader_order:
        card = world.leaders[name]
        data["leaders"].append(
            {
                "name": card.name,
                "damage": card.damage,
                "health": card.health,
                "element": card.element,
            }
        )

    for name in world.dungeon_order:
        dungeon = world.dungeons[name]
        data["dungeons"].append(
            {
                "name": dungeon.name,
                "type": dungeon.dungeon_type,
                "simple_cards": list(dungeon.simple_cards),
                "leader": dungeon.leader_name,
                "reward": dungeon.reward,
            }
        )

    with open(file_path, "w", encoding="utf-8") as output_file:
        json.dump(data, output_file, ensure_ascii=False, indent=4)


def load_environment(file_path: str) -> GameState:
    """
    Játékkörnyezet betöltése JSON-ből új GameState példányba.

    A játékos gyűjteménye a starting_collection lista alapján áll össze.
    Pakli üresen indul.
    Nehézség: 0 (új játék indításakor a játékos adja meg).
    """

    with open(file_path, "r", encoding="utf-8") as input_file:
        data = json.load(input_file)

    game = GameState()
    world = game.world

    # Sima kártyák
    for card_data in data.get("simple_cards", []):
        element_text = parse_element(card_data["element"])
        world.add_simple_card(
            card_data["name"],
            int(card_data["damage"]),
            int(card_data["health"]),
            element_text,
        )

    # Vezérek
    for card_data in data.get("leaders", []):
        element_text = parse_element(card_data["element"])
        world.add_leader_direct(
            card_data["name"],
            int(card_data["damage"]),
            int(card_data["health"]),
            element_text,
        )

    # Kazamaták
    for dungeon_data in data.get("dungeons", []):
        dungeon_type = dungeon_data["type"]
        simple_cards = list(dungeon_data.get("simple_cards", []))
        leader_name = dungeon_data.get("leader")
        reward_type = dungeon_data.get("reward")
        world.add_dungeon(
            dungeon_data["name"],
            dungeon_type,
            simple_cards,
            leader_name,
            reward_type,
        )

    # Kezdő gyűjtemény
    game.player.collection = {}
    game.player.collection_order = []
    game.player.deck = []

    for name in data.get("starting_collection", []):
        game.add_collection_card_from_world(name)

    game.difficulty = 0
    return game

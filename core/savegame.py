import json

from typing import Dict, Any, Tuple

from .environment import load_environment
from .gamestate import GameState
from .models import Card, parse_element


SAVEGAME_VERSION = 1


def save_game(game: GameState, environment_file: str, save_file: str) -> None:
    """
    Aktuális játék mentése.
    """

    player = game.player

    data: Dict[str, Any] = {
        "version": SAVEGAME_VERSION,
        "environment_file": environment_file,
        "difficulty": game.difficulty,
        "collection": [],
        "deck": list(player.deck),
    }

    for name in player.collection_order:
        card = player.collection[name]
        data["collection"].append(
            {
                "name": card.name,
                "damage": card.damage,
                "health": card.health,
                "element": card.element,
            }
        )

    with open(save_file, "w", encoding="utf-8") as output_file:
        json.dump(data, output_file, ensure_ascii=False, indent=4)


def load_game(save_file: str) -> Tuple[GameState, str]:
    """
    Mentett játék betöltése.

    Visszatérés:
    - GameState példány (világgal, kazamatákkal, játékos állapotával)
    - environment_file: az a játékkörnyezet file, amiből a játék indult
    """

    with open(save_file, "r", encoding="utf-8") as input_file:
        data = json.load(input_file)

    environment_file = data["environment_file"]
    game = load_environment(environment_file)

    game.player.collection = {}
    game.player.collection_order = []
    game.player.deck = []

    for card_data in data.get("collection", []):
        element_text = parse_element(card_data["element"])
        card = Card(
            card_data["name"],
            int(card_data["damage"]),
            int(card_data["health"]),
            element_text,
        )
        game.player.add_to_collection(card)

    game.player.deck = list(data.get("deck", []))
    game.difficulty = int(data.get("difficulty", 0))

    return game, environment_file

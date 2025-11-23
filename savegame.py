from __future__  import annotations
from dataclasses import asdict
from pathlib     import Path
from typing      import Dict, Any, Tuple

import json

from player import PlayerState, PlayerCard


def save_game(path: Path, file: str, difficulty: int, player: PlayerState) -> None:
    data: Dict[str, Any] = {
        "file": file,
        "difficulty": int(difficulty),
        "player": {
            "collection": [
                asdict(player.collection[name]) for name in player.collection_order
            ],
            "collection_order": player.collection_order,
            "deck": player.deck,
        },
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_game(path: Path) -> Tuple[str, int, PlayerState]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    file       : str = data["file"]
    difficulty : int = int(data.get("difficulty", 0))

    p = PlayerState()
    p.collection_order = list(data["player"].get("collection_order", []))
    for pc in data["player"]["collection"]:
        card = PlayerCard(pc["name"], int(pc["damage"]), int(pc["hp"]), pc["type"])
        p.collection[card.name] = card
    p.deck = list(data["player"].get("deck", []))

    return file, difficulty, p

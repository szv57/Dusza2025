from __future__  import annotations
from dataclasses import asdict
from pathlib     import Path
from typing      import Tuple, Dict, Any

import json

from world   import World
from player  import PlayerState, PlayerCard
from card    import CardTemplate
from dungeon import Dungeon


def save_environment(path: Path, name: str, world: World, initial_player: PlayerState) -> None:
    data: Dict[str, Any] = {
        "name": name,
        "world": {
            "cards": [
                asdict(world.cards[name]) for name in world.card_order
            ],
            "card_order": world.card_order,
            "leaders": [
                asdict(world.leaders[name]) for name in world.leader_order
            ],
            "leader_order": world.leader_order,
            "dungeons": [
                {
                    "name": d.name,
                    "kind": d.kind,
                    "enemy_sima": d.enemy_sima,
                    "leader": d.leader,
                    "reward_type": d.reward_type,
                }
                for d in world.dungeons.values()
            ],
        },
        "initial_collection": [
            asdict(initial_player.collection[name]) for name in initial_player.collection_order
        ],
        "initial_collection_order": initial_player.collection_order,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_environment(path: Path) -> Tuple[str, World, PlayerState]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    name: str = data.get("name", "Ismeretlen környezet")
    w = World()

    w.card_order = list(data["world"].get("card_order", []))
    for c in data["world"]["cards"]:
        tmpl = CardTemplate(c["name"], int(c["damage"]), int(c["hp"]), c["type"])
        w.cards[tmpl.name] = tmpl

    w.leader_order = list(data["world"].get("leader_order", []))
    for v in data["world"]["leaders"]:
        tmpl = CardTemplate(v["name"], int(v["damage"]), int(v["hp"]), v["type"])
        w.leaders[tmpl.name] = tmpl

    for d in data["world"]["dungeons"]:
        dungeon = Dungeon(
            name        = d["name"],
            kind        = d["kind"],
            enemy_sima  = list(d["enemy_sima"]),
            leader      = d.get("leader"),
            reward_type = d.get("reward_type"),
        )
        w.dungeons[dungeon.name] = dungeon

    p = PlayerState()
    p.collection_order = list(data.get("initial_collection_order", []))
    for pc in data["initial_collection"]:
        card = PlayerCard(pc["name"], int(pc["damage"]), int(pc["hp"]), pc["type"])
        p.collection[card.name] = card

    return name, w, p

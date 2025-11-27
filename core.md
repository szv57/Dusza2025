# Játéklogika API

## init

`ELEMENT_ORDER`

## Battle

`def damage_multiplier(att_type: str, def_type: str) -> float`

`class BattleResult`:
- `log_lines: list[str]`
- `outcome: Literal["win", "lose"]`
- `last_player_attacker_name: str | None`

`def run_battle(world: World, player: Player, dungeon: Dungeon, difficulty: int = 0, rng: random.Random | None = None) -> BattleResult | Literal[False]`

`def apply_damage(att_card: CardDefinition, def_card: CardDefinition, difficulty: int, rng: random.Random, is_enemy: bool) -> float`

## Environment

`class Environment`:
- `name: str`
- `world: World`
- `starting_collection: dict`

- `def from_world_and_player(name: str, world: World, player: Player) -> "Environment"`

- `def new_game(difficulty: int) -> State`

## Models

`class CardDefinition`:
- `name: str`
- `damage: int`
- `health: int`
- `element: str`

- `def copy() -> "CardDefinition"`

`class Dungeon`:
- `name: str`
- `kind: str`
- `simple_card_names: list`
- `leader_name: str | None = None`
- `reward_type: str | None = None`

- `def card_sequence(world: "World") -> list | Literal[False]`

`class World`:
- `simple_cards: dict`
- `leader_cards: dict`
- `dungeons: dict`

- `def add_simple_card(name: str, damage: int, health: int, element: str) -> Literal[True] | Literal[False]`
- `def add_leader_card(name: str, base_card_name: str, mode: str) -> Literal[True] | Literal[False]`
- `def add_dungeon(dungeon: Dungeon) -> Literal[True] | Literal[False]`
- `def get_simple_card(name: str) -> CardDefinition | Literal[False]`
- `def get_leader_card(name: str) -> CardDefinition | Literal[False]`
- `def get_dungeon(name: str) -> Dungeon | Literal[False]`
- `def iter_simple_cards()`
- `def iter_leader_cards()`
- `def iter_dungeons()`

`class Player`:
- `collection: dict`
- `deck: list`

- `def add_card_from_world(world: World, card_name: str) -> Literal[True] | Literal[False]`
- `def max_deck_size() -> int`
- `def set_deck(card_names: list) -> Literal[True] | Literal[False]`
- `def has_deck() -> bool`

`class State`:
- `player: Player`
- `difficulty: int`
- `environment_name: str | None = None`

## Storage

`def _card_to_dict(card: CardDefinition) -> dict`

`def _card_from_dict(d: dict) -> CardDefinition`

`def _dungeon_to_dict(dungeon: Dungeon) -> dict`

`def _dungeon_from_dict(d: dict) -> Dungeon`

`def world_to_dict(world: World) -> dict`

`def world_from_dict(data: dict) -> World`

`def player_to_dict(player: Player) -> dict`

`def player_from_dict(data: dict) -> Player`

`def environment_to_dict(env: Environment) -> dict`

`def environment_from_dict(data: dict) -> Environment`

`def save_environment_to_file(env: Environment, filepath: str)`

`def load_environment_from_file(filepath: str) -> Environment`

`def state_to_dict(state: State) -> dict`

`def state_from_dict(data: dict) -> State`

`def save_state_to_file(state: State, filepath: str)`

`def load_state_from_file(filepath: str) -> State`
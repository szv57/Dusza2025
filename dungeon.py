from __future__  import annotations
from dataclasses import dataclass
from typing      import List, Optional


@dataclass
class Dungeon:
    name        : str
    kind        : str
    enemy_sima  : List[str]
    leader      : Optional[str]
    reward_type : Optional[str]

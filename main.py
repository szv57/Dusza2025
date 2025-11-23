from __future__ import annotations
from pathlib    import Path

import sys

from test                import run_test_mode
from default_environment import create_default_world_and_player
from environment         import save_environment


def ensure_default_environment() -> None:
    path = Path("default.env.json")
    if path.is_file():
        return

    name, world, player = create_default_world_and_player()
    save_environment(path, name, world, player)


def main() -> None:
    args = sys.argv[1:]
    if len(args) == 1 and args[0] == "--ui":
        pass
    elif len(args) == 1:
        base_dir = Path(args[0])
        run_test_mode(base_dir)
    else:
        print("Használat:")
        print("  python main.py <mappautvonal>   # teszt mód (in.txt ebben a mappában)")
        print("  python main.py --ui             # játék mód")


if __name__ == "__main__":
    main()

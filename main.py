import sys

from test import run_test_mode
from game.test import run_ui_mode


def main() -> None:
    if len(sys.argv) < 2:
        print("Használat:")
        print("  python main.py <teszt_mappa>")
        print("  python main.py --ui")
        return

    arg = sys.argv[1]
    if arg == "--ui":
        run_ui_mode()
    else:
        run_test_mode(arg)


if __name__ == "__main__":
    main()

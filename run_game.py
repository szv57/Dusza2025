import os

# Ne írja ki az üdvözlő üzenetet.
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "hide"

import pygame

from game.game import Game


def run_ui_mode():
    pygame.init()
    pygame.font.init()

    game = Game(width=800, height=450, title="Damareen")
    game.run()

    pygame.quit()

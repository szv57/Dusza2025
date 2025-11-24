import pygame

from menu import MainMenu


def run_ui_mode():
    pygame.init()

    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Damareen")

    menu = MainMenu(screen)
    menu.run()

    pygame.quit()

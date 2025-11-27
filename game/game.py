import pygame

from .scene_manager import SceneManager
from .scenes.title_scene import TitleScene
from .scenes.mode_select_scene import ModeSelectScene
from .scenes.text_scene import TextScene


class Game:
    """
    Fő játékobjektum.
    - inicializálja az ablakot
    - létrehozza a SceneManager-t
    - regisztrálja a jeleneteket
    - futtatja a fő ciklust
    """

    def __init__(self, width: int, height: int, title: str = "Damareen"):
        self.width = width
        self.height = height
        self.title = title

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

        self.clock = pygame.time.Clock()
        self.running = True

        # Jelenetkezelő
        self.scene_manager = SceneManager(self)

        # Jelenetek regisztrálása
        self._register_scenes()

    def _register_scenes(self):
        sm = self.scene_manager

        # Főmenü
        sm.register("title", TitleScene(self))

        # Játékmód választó (Player / GM popup)
        sm.register("mode_select", ModeSelectScene(self))

        # Egyszerű szöveges jelenetek – később lecserélhetitek
        sm.register(
            "options",
            TextScene(
                self, title="BEÁLLÍTÁSOK MÓD", description="Itt lesznek a beállítások."
            ),
        )
        sm.register(
            "load",
            TextScene(
                self, title="BETÖLTÉS MÓD", description="Itt lesz a betöltés menü."
            ),
        )
        sm.register(
            "player",
            TextScene(
                self, title="JÁTÉKOS MÓD", description="Itt lesz a játékos felülete."
            ),
        )
        sm.register(
            "gamemaster",
            TextScene(
                self, title="JÁTÉKMESTER MÓD", description="Itt lesz a játékmester UI."
            ),
        )

        # Kezdő jelenet
        sm.go_to("title")

    # Külső API jelenetváltáshoz
    def go_to(self, scene_name: str):
        self.scene_manager.go_to(scene_name)

    def quit(self):
        self.running = False

    def run(self):
        """
        Fő játékhurok.
        """

        while self.running:
            dt = self.clock.tick(60) / 1000.0  # másodperc

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                else:
                    self.scene_manager.handle_event(event)

            self.scene_manager.update(dt)
            self.scene_manager.draw(self.screen)

            pygame.display.flip()

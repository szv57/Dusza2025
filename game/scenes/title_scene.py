import pygame

from .base_scene import Scene
from ..ui.button import Button


class TitleScene(Scene):
    """
    Főmenü:
    - Start -> "mode_select" jelenet
    - Load  -> "load" jelenet
    - Options -> "options"
    - Quit -> game.quit()
    """

    def __init__(self, game):
        super().__init__(game)

        self.screen_width = game.width
        self.screen_height = game.height

        self.background = None
        self.buttons = []

        self._load_assets()
        self._create_buttons()

    def _load_assets(self):
        # Háttér
        bg_raw = pygame.image.load("Assets/Images/Misc/MainMenuBG.png").convert()
        self.background = pygame.transform.smoothscale(
            bg_raw, (self.screen_width, self.screen_height)
        )

    def _create_buttons(self):
        spacing = int(self.screen_height / 10.5)
        default_button_width = int(self.screen_width / 7)
        default_button_height = int(self.screen_height / 13)
        default_y = self.screen_height / 2 + self.screen_height / 11
        default_x = self.screen_width / 2 - default_button_width / 2

        # Start
        start_btn = Button.from_images(
            x=int(default_x),
            y=int(default_y),
            width=default_button_width,
            height=default_button_height,
            normal_path="Assets/Images/Buttons/NormalStart.png",
            hover_path="Assets/Images/Buttons/HoverStart.png",
            callback=lambda: self.game.go_to("mode_select"),
        )

        # Load
        load_btn = Button.from_images(
            x=int(default_x),
            y=int(default_y + spacing),
            width=default_button_width,
            height=default_button_height,
            normal_path="Assets/Images/Buttons/NormalLoad.png",
            hover_path="Assets/Images/Buttons/HoverLoad.png",
            callback=lambda: self.game.go_to("load"),
        )

        # Options
        options_btn = Button.from_images(
            x=int(default_x),
            y=int(default_y + spacing * 2),
            width=default_button_width,
            height=default_button_height,
            normal_path="Assets/Images/Buttons/NormalOption.png",
            hover_path="Assets/Images/Buttons/HoverOption.png",
            callback=lambda: self.game.go_to("options"),
        )

        # Quit
        quit_btn = Button.from_images(
            x=int(default_x),
            y=int(default_y + spacing * 3),
            width=default_button_width,
            height=default_button_height,
            normal_path="Assets/Images/Buttons/NormalQuit.png",
            hover_path="Assets/Images/Buttons/HoverQuit.png",
            callback=self.game.quit,
        )

        self.buttons = [start_btn, load_btn, options_btn, quit_btn]

    # Scene interface

    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)

    def update(self, dt: float):
        mouse_pos = pygame.mouse.get_pos()
        for b in self.buttons:
            b.update(mouse_pos)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.background, (0, 0))
        for b in self.buttons:
            b.draw(surface)

import pygame

from .base_scene import Scene
from ..ui.button import Button


class TextScene(Scene):
    """
    Egyszerű placeholder scene:
    - egy cím
    - egy leírás sor
    - egy Back gomb, ami visszavisz a főmenübe
    """

    def __init__(self, game, title: str, description: str = ""):
        super().__init__(game)
        self.title = title
        self.description = description

        self.font_title = pygame.font.SysFont("comicsans", 40)
        self.font_desc = pygame.font.SysFont("comicsans", 28)

        self.back_button = None
        self._create_back_button()

    def _create_back_button(self):
        w = int(self.game.width * 0.15)
        h = int(self.game.height * 0.07)
        x = int(self.game.width * 0.9 - w)
        y = int(self.game.height * 0.9 - h)

        self.back_button = Button.from_images(
            x=x,
            y=y,
            width=w,
            height=h,
            normal_path="Assets/2, Admin or Player/NoHoverBack.png",
            hover_path="Assets/2, Admin or Player/HoverBack.png",
            callback=lambda: self.game.go_to("title"),
        )

    # Scene interface

    def handle_event(self, event):
        self.back_button.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.go_to("title")

    def update(self, dt: float):
        mouse_pos = pygame.mouse.get_pos()
        self.back_button.update(mouse_pos)

    def draw(self, surface: pygame.Surface):
        surface.fill("black")

        title_surf = self.font_title.render(self.title, True, "white")
        title_rect = title_surf.get_rect(
            center=(self.game.width // 2, self.game.height // 2 - 40)
        )
        surface.blit(title_surf, title_rect)

        if self.description:
            desc_surf = self.font_desc.render(self.description, True, "white")
            desc_rect = desc_surf.get_rect(
                center=(self.game.width // 2, self.game.height // 2 + 10)
            )
            surface.blit(desc_surf, desc_rect)

        self.back_button.draw(surface)

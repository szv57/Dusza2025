import pygame

from typing import Callable, Optional, Tuple


class Button:
    """
    Egyszerű, újrafelhasználható gomb.
    - kezeli a hover állapotot
    - callback-et hív kattintáskor
    """

    def __init__(
        self,
        rect: pygame.Rect,
        image_normal: pygame.Surface,
        image_hover: Optional[pygame.Surface] = None,
        callback: Optional[Callable[[], None]] = None,
    ):
        self.rect = rect
        self.image_normal = image_normal
        self.image_hover = image_hover if image_hover is not None else image_normal

        self.callback = callback
        self.hovered = False

    @classmethod
    def from_images(
        cls,
        x: int,
        y: int,
        width: int,
        height: int,
        normal_path: str,
        hover_path: Optional[str] = None,
        callback: Optional[Callable[[], None]] = None,
    ) -> "Button":
        normal = pygame.image.load(normal_path).convert_alpha()
        normal = pygame.transform.smoothscale(normal, (width, height))

        if hover_path:
            hover = pygame.image.load(hover_path).convert_alpha()
            hover = pygame.transform.smoothscale(hover, (width, height))
        else:
            hover = None

        rect = pygame.Rect(x, y, width, height)
        return cls(rect, normal, hover, callback)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.hovered and self.callback:
                self.callback()

    def update(self, mouse_pos: Tuple[int, int]):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def draw(self, surface: pygame.Surface):
        img = self.image_hover if self.hovered else self.image_normal
        surface.blit(img, self.rect.topleft)

import pygame

from .base_scene import Scene
from ..ui.button import Button


class ModeSelectScene(Scene):
    """
    Játékmód választó: Player / Gamemaster + Back.
    Vizualisan hasonló a régi popup-hoz.
    """

    def __init__(self, game):
        super().__init__(game)

        self.screen_width = game.width
        self.screen_height = game.height

        self.background = None
        self.overlay = None
        self.popup = None
        self.popup_rect = None

        self.buttons = []
        self.back_button = None

        self._load_assets()
        self._create_buttons()

    def _load_assets(self):
        # Háttérnek újrahasznosíthatjuk a főmenü hátterét is, vagy sima fekete
        bg_raw = pygame.image.load(
            "Assets/1, MainMenu/MainMenuEmptySizedCorrect.png"
        ).convert()
        self.background = pygame.transform.smoothscale(
            bg_raw, (self.screen_width, self.screen_height)
        )

        # Sötét overlay
        self.overlay = pygame.Surface((self.screen_width, self.screen_height))
        self.overlay.set_alpha(220)
        self.overlay.fill((20, 20, 20))

        # Popup ablak
        popup_raw = pygame.image.load(
            "Assets/2, Admin or Player/PlayerOrAdminPopUp.png"
        ).convert_alpha()

        popup_scale = 0.6
        popup_w = int(self.screen_width * popup_scale)
        popup_h = int(self.screen_height * popup_scale)

        self.popup = pygame.transform.smoothscale(popup_raw, (popup_w, popup_h))
        self.popup_rect = self.popup.get_rect(
            center=(self.screen_width // 2, self.screen_height // 2)
        )

    def _create_buttons(self):
        sample_btn = pygame.image.load("Assets/1, MainMenu/NoHoverStart.png")
        orig_w, orig_h = sample_btn.get_size()
        aspect = orig_h / orig_w

        btn_w = int(self.screen_width * 0.25)
        btn_h = int(btn_w * aspect)

        player_y = int(self.popup_rect.top + self.popup_rect.height * 0.40)
        gm_y = int(self.popup_rect.top + self.popup_rect.height * 0.65)
        x = self.screen_width // 2 - btn_w // 2

        player_btn = Button.from_images(
            x=x,
            y=player_y,
            width=btn_w,
            height=btn_h,
            normal_path="Assets/2, Admin or Player/NoHoverPlayer.png",
            hover_path="Assets/2, Admin or Player/HoverPlayer.png",
            callback=lambda: self.game.go_to("player"),
        )

        gm_btn = Button.from_images(
            x=x,
            y=gm_y,
            width=btn_w,
            height=btn_h,
            normal_path="Assets/2, Admin or Player/NoHoverGamemaster.png",
            hover_path="Assets/2, Admin or Player/HoverGamemaster.png",
            callback=lambda: self.game.go_to("gamemaster"),
        )

        back_btn_w = int(btn_w * 0.5)
        back_btn_h = int(btn_h * 0.5)

        back_btn = Button.from_images(
            x=int(self.screen_width * 0.9 - back_btn_w),
            y=int(self.screen_height * 0.9 - back_btn_h),
            width=back_btn_w,
            height=back_btn_h,
            normal_path="Assets/2, Admin or Player/NoHoverBack.png",
            hover_path="Assets/2, Admin or Player/HoverBack.png",
            callback=lambda: self.game.go_to("title"),
        )

        self.buttons = [player_btn, gm_btn]
        self.back_button = back_btn

    # Scene interface

    def handle_event(self, event):
        for b in self.buttons:
            b.handle_event(event)
        self.back_button.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.go_to("title")

    def update(self, dt: float):
        mouse_pos = pygame.mouse.get_pos()
        for b in self.buttons:
            b.update(mouse_pos)
        self.back_button.update(mouse_pos)

    def draw(self, surface: pygame.Surface):
        surface.blit(self.background, (0, 0))
        surface.blit(self.overlay, (0, 0))
        surface.blit(self.popup, self.popup_rect.topleft)

        for b in self.buttons:
            b.draw(surface)
        self.back_button.draw(surface)

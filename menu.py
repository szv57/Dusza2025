import pygame

from core.environment import load_environment
from core.gamestate import create_classic_game
from core.savegame import load_game


WHITE = (255, 255, 255)


class ImageButton:
    def __init__(
        self,
        x,
        y,
        callback,
        image_normal_path,
        image_hover_path,
        text="",
        font=None,
        scale_to=None,
    ):
        normal = pygame.image.load(image_normal_path).convert_alpha()
        hover = pygame.image.load(image_hover_path).convert_alpha()

        # Smooth scale kell, hogy ne legyen pixeles.
        if scale_to is not None:
            normal = pygame.transform.smoothscale(normal, scale_to)
            hover = pygame.transform.smoothscale(hover, scale_to)

        self.image_normal = normal
        self.image_hover = hover
        self.image = self.image_normal

        self.rect = self.image.get_rect(topleft=(x, y))
        self.callback = callback
        self.hover = False
        self.text = text
        self.font = font

    def update(self, mouse_pos):
        self.hover = self.rect.collidepoint(mouse_pos)
        self.image = self.image_hover if self.hover else self.image_normal

    def draw(self, surface):
        surface.blit(self.image, self.rect)

        if self.text and self.font:
            text_surface = self.font.render(self.text, True, WHITE)
            text_rect = text_surface.get_rect(center=self.rect.center)
            surface.blit(text_surface, text_rect)

    def click(self):
        self.callback()


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 30)

        self.buttons = []
        spacing = 125
        start_y = 75

        self.buttons.append(
            ImageButton(
                250,
                start_y,
                self.start_new_game,
                "assets/images/Buttons/NormalStart.png",
                "assets/images/Buttons/HoverStart.png",
                text="",
                font=self.font,
                scale_to=(300, 100),
            )
        )

        self.buttons.append(
            ImageButton(
                250,
                start_y + spacing,
                self.load_environment_game,
                "assets/images/Buttons/NormalLoad.png",
                "assets/images/Buttons/HoverLoad.png",
                text="",
                font=self.font,
                scale_to=(300, 100),
            )
        )

        self.buttons.append(
            ImageButton(
                250,
                start_y + spacing * 2,
                self.load_saved_game,
                "assets/images/Buttons/NormalSave.png",
                "assets/images/Buttons/HoverSave.png",
                text="",
                font=self.font,
                scale_to=(300, 100),
            )
        )

        self.buttons.append(
            ImageButton(
                250,
                start_y + spacing * 3,
                self.exit_game,
                "assets/images/Buttons/NormalQuit.png",
                "assets/images/Buttons/HoverQuit.png",
                text="",
                font=self.font,
                scale_to=(300, 100),
            )
        )

        self.running = True

    # Callback függvények

    def start_new_game(self):
        print("Új játék indítása…")
        game = create_classic_game()
        # TODO: Továbbirányítás játék UI-ra
        # run_game_screen(game)

    def load_environment_game(self):
        print("Játékkörnyezet betöltése…")
        try:
            game = load_environment("world1.json")
            # TODO: Tovább a játék UI-ra
        except Exception as error:
            print("Hiba:", error)

    def load_saved_game(self):
        print("Mentett játék betöltése…")
        try:
            game, env_file = load_game("save1.json")
            # TODO: Tovább a játék UI-ra
        except Exception as error:
            print("Hiba:", error)

    def exit_game(self):
        self.running = False

    # Menü loop

    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for b in self.buttons:
                        if b.hover:
                            b.click()

            for b in self.buttons:
                b.update(mouse_pos)

            self.screen.fill((20, 20, 20))

            for b in self.buttons:
                b.draw(self.screen)

            pygame.display.flip()
            clock.tick(60)

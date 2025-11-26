import pygame

from .buttonclass import Button

class TitleScreen:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen

        self.screen_width = screen_width
        self.screen_height = screen_height

        self.menu_buttons = []
        self.startmenu_buttons = []

        spacing = int(screen_height / 10.5)

        default_button_width = self.screen_width / 7
        default_button_height = screen_height / 13
        default_y = screen_height / 2 + screen_height / 11
        default_x = screen_width / 2

        self.enable_menu_click = True
        self.enable_gamemode_click = False
        self.enable_options_click = False
        

        self.dict_modes = {
            "gamemode": "Játékmód",
            "options": "Beállítások",
            "load": "Betöltés",
            "player": "Játékos",
            "gamemaster": "Játékmester",
        }

        self.list_backbutton_modes = ["gamemode", "options", "load"]

        self.mode = "menu"
        self.font = pygame.font.SysFont("comicsans", 30)

        self.background_raw = pygame.image.load("Assets/Images/Misc/MainMenuBG.png")

        self.background = pygame.transform.smoothscale(
            self.background_raw, (screen_width, screen_height)
        )

        self.popup_win_raw = pygame.image.load(
            "Assets/Images/Misc/PlayerOrAdminPopUp.png"
        )

        popup_scale = 0.6
        popup_scaled_w = int(self.screen_width * popup_scale)
        ratio = popup_scaled_w / self.popup_win_raw.get_width()

        popup_scaled_h = int(self.screen_height * popup_scale)

        self.popup_win_scaled = pygame.transform.smoothscale(
            self.popup_win_raw, (popup_scaled_w, popup_scaled_h)
        )

        sample_button_img = pygame.image.load("Assets/Images/Buttons/NormalStart.png")
        orig_w, orig_h = sample_button_img.get_size()
        aspect = orig_h / orig_w

        self.popup_x = self.screen_width / 2 - popup_scaled_w / 2
        self.popup_y = self.screen_height / 2 - popup_scaled_h / 2

        pgm_button_w = self.screen_width * 0.25
        pgm_button_h = pgm_button_w * aspect

        player_y = self.popup_y + popup_scaled_h * 0.40
        gamemaster_y = self.popup_y + popup_scaled_h * 0.65

        player_gm_x = self.screen_width / 2 - pgm_button_w / 2

        self.start_button = Button(
            pos=(default_x - default_button_width / 2, default_y),
            normal_path="Assets/Images/Buttons/NormalStart.png",
            callback_func=self.start_pressed,
            hover_path="Assets/Images/Buttons/HoverStart.png",
            scale_w=default_button_width,
            scale_h=default_button_height,
        )

        self.load_button = Button(
            pos=(default_x - default_button_width / 2, default_y + spacing),
            normal_path="Assets/Images/Buttons/NormalLoad.png",
            callback_func=self.load_pressed,
            hover_path="Assets/Images/Buttons/HoverLoad.png",
            scale_w=default_button_width,
            scale_h=default_button_height,
        )

        self.options_button = Button(
            pos=(default_x - default_button_width / 2, default_y + spacing * 2),
            normal_path="Assets/Images/Buttons/NormalOption.png",
            callback_func=self.options_pressed,
            hover_path="Assets/Images/Buttons/HoverOption.png",
            scale_w=default_button_width,
            scale_h=default_button_height,
        )

        self.quit_button = Button(
            pos=(default_x - default_button_width / 2, default_y + spacing * 3),
            normal_path="Assets/Images/Buttons/NormalQuit.png",
            callback_func=self.quit_pressed,
            hover_path="Assets/Images/Buttons/HoverQuit.png",
            scale_w=default_button_width,
            scale_h=default_button_height,
        )

        self.player_button = Button(
            pos=(player_gm_x, player_y),
            normal_path="Assets/Images/Buttons/NoHoverPlayer.png",
            callback_func=self.player_pressed,
            hover_path="Assets/Images/Buttons/HoverPlayer.png",
            scale_w=pgm_button_w,
            scale_h=pgm_button_h,
        )

        self.gamemaster_button = Button(
            pos=(player_gm_x, gamemaster_y),
            normal_path="Assets/Images/Buttons/NoHoverGameMaster.png",
            callback_func=self.gamemaster_pressed,
            hover_path="Assets/Images/Buttons/HoverGameMaster.png",
            scale_w=pgm_button_w,
            scale_h=pgm_button_h,
        )

        self.back_button = Button(
            pos=(
                self.screen_width * 0.9 - default_button_height * 0.7,
                self.screen_height * 0.9,
            ),
            normal_path="Assets/Images/Buttons/NoHoverBack.png",
            callback_func=self.back_button_pressed,
            hover_path="Assets/Images/Buttons/HoverBack.png",
            scale_w=int(default_button_width * 0.7),
            scale_h=int(default_button_height * 0.7),
        )

        self.menu_buttons.append(self.start_button)
        self.menu_buttons.append(self.load_button)
        self.menu_buttons.append(self.options_button)
        self.menu_buttons.append(self.quit_button)

        self.startmenu_buttons = [
            self.gamemaster_button,
            self.player_button,
            self.back_button,
        ]
        self.options_buttons = [
            self.back_button
        ]

        self.menu_map = {
            "menu" : self.menu_buttons,
            "gamemode" : self.startmenu_buttons,
            "options" : self.options_buttons,
            "gamemaster" : [self.back_button],
            "player" : [self.back_button],
            "load" : [self.back_button]
        }

        self.running = True


    def start_pressed(self):
        self.mode = "gamemode"

        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(230)
        overlay.fill((20, 20, 20))
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(
            self.popup_win_scaled,
            (self.popup_x, self.popup_y),
        )



    def load_pressed(self):
        self.mode = "load"

    def options_pressed(self):
        self.mode = "options"

    def quit_pressed(self):
        self.running = False

    def player_pressed(self):
        self.mode = "player"

    def gamemaster_pressed(self):
        self.mode = "gamemaster"

    def back_button_pressed(self):
        dict_mode_back = {"gamemode":"menu",
                          "player" : "menu",
                          "gamemaster" : "menu",
                          "options" : "menu",
                          "load" : "menu"}
        mode_tmp = dict_mode_back[self.mode]
        self.mode = mode_tmp

    def _drawmode(self, mouse_pos):
        if self.mode == "menu":
                self.screen.blit(self.background, (0, 0))

                for button in self.menu_buttons:
                    button.update(mouse_pos)
                    button.screen_update(self.screen)

        elif self.mode == "gamemode":
            self.player_button.update(mouse_pos)
            self.player_button.screen_update(self.screen)
            self.gamemaster_button.update(mouse_pos)
            self.gamemaster_button.screen_update(self.screen)
        elif self.mode != "menu":
            if self.mode != "gamemode":
                self.screen.fill("black")
                title = f"{self.dict_modes[self.mode].upper()} MÓD"
                text = self.font.render(title, 1, "white")
                self.screen.blit(
                    text,
                    (
                        self.screen_width / 2 - text.get_width() / 2,
                        self.screen_height / 2 - text.get_height() / 2,
                    ),
                )

                info = self.font.render("Nyomj ESC-et a visszatéréshez", 1, "white")
                self.screen.blit(
                    info,
                    (
                        self.screen_width / 2 - info.get_width() / 2,
                        self.screen_height / 2 - text.get_height() / 2 + 60,
                    ),
                )
            self.back_button.update(mouse_pos)
            self.back_button.screen_update(self.screen)


    def run(self):
        clock = pygame.time.Clock()

        while self.running:
            clock.tick(60)

            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for button in self.menu_map.get(self.mode):
                        if button.b_hover:
                            button.do_callback()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.mode = "menu"
                        self.enable_menu_click = True

            if self.mode in self.list_backbutton_modes:
                self.back_button.update(mouse_pos)
                self.back_button.screen_update(self.screen)

            self._drawmode(mouse_pos)


            pygame.display.flip()

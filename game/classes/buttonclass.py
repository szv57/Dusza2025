import pygame


class Button:
    def __init__(
        self,
        pos,
        normal_path,
        callback_func,
        hover_path=None,
        scale_w=None,
        scale_h=None,
    ):
        normal = pygame.image.load(normal_path).convert_alpha()

        if hover_path is not None:
            hover = pygame.image.load(hover_path).convert_alpha()
        else:
            hover = None

        if (scale_w and scale_h) is not None:
            normal = pygame.transform.smoothscale(normal, (scale_w, scale_h))
            if hover is not None:
                hover = pygame.transform.smoothscale(hover, (scale_w, scale_h))

        self.image_normal = normal
        self.image_hover = hover
        self.display = self.image_normal
        self.width = scale_w
        self.height = scale_h

        self.rect = self.image_normal.get_rect(topleft=(int(pos[0]), int(pos[1])))
        self.b_hover = False

        self.callback = callback_func

    def update(self, mouse_pos, scale=None):
        self.b_hover = self.rect.collidepoint(mouse_pos)
        if self.b_hover and self.image_hover is not None:
            self.display = self.image_hover
        elif scale is not None:
            self.display = pygame.transform.smoothscale(
                self.display, (self.width * scale, self.height * scale)
            )
        else:
            self.display = self.image_normal

    def screen_update(self, screen):
        screen.blit(self.display, self.rect)

    def do_callback(self):
        self.callback()
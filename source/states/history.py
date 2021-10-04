import pygame
from pygame import draw
from .. import setup
from .. import tools
from .. import constants as C
from ..components import button, info


class History:
    def start(self, game_info):
        self.game_info = game_info
        self.info = info.Info("history", self.game_info)
        self.setup_background()
        self.setup_buttons()
        self.finished = False
        self.next = "main_menu"

    def setup_background(self):
        self.background = setup.GRAPHICS["background"]
        self.background_rect = self.background.get_rect()
        self.viewport = setup.SCREEN.get_rect()

    def setup_buttons(self):
        self.buttons = button.Button(0, (50, 50))
        # self.buttons.image=setup.GRAPHICS['']
        # rect = self.buttons.image.get_rect()

    def update_buttons(self, mouse):
        if mouse[0] and self.buttons.button_rect.collidepoint(mouse[1]):
            self.finished = True

    def update(self, surface, mouse):

        self.update_buttons(mouse)

        surface.blit(self.background, self.viewport)
        # surface.blit(self.caption, self.caption_rect)

        # self.info.update(self.game_info)
        self.info.draw(surface)
        self.draw(surface)

    def draw(self, surface):
        font = pygame.font.Font(C.FONT, 30)
        i = 0
        with open(C.HISTORY, "r") as f:
            for line in f.readlines():
                image = font.render(line[0:-1], 1, C.BLACK)
                rect = image.get_rect()
                rect.center = 240, 100 + 40 * i
                surface.blit(image, rect)
                i += 1

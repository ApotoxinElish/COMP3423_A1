import pygame
from .. import setup
from .. import tools
from .. import constants as C
from ..components import button, info


class MainMenu:
    def __init__(self):
        game_info = {
            "score": 0,
            "lives": 3,
            "time_rest": 30,
        }
        self.start(game_info)

    def start(self, game_info):
        self.game_info = game_info
        self.setup_background()
        self.setup_buttons()
        self.info = info.Info("main_menu", self.game_info)
        self.finished = False
        self.next = "game_play"
        self.reset_game_info()

    def setup_background(self):
        self.background = setup.GRAPHICS["background"]
        self.background_rect = self.background.get_rect()
        self.background = pygame.transform.scale(
            self.background,
            (
                int(self.background_rect.width * C.BG_MULTI),
                int(self.background_rect.height * C.BG_MULTI),
            ),
        )
        self.viewport = setup.SCREEN.get_rect()
        self.caption = setup.GRAPHICS["enemy3_n1"]
        self.caption_rect = self.caption.get_rect()
        self.caption_rect.center = (C.SCREEN_W / 2, 200)

    def setup_buttons(self):
        self.buttons = []
        self.buttons.append(button.Button(0, (240, 450)))
        self.buttons.append(button.Button(1, (240, 550)))
        self.buttons.append(button.Button(2, (240, 650)))
        # self.buttons.image=setup.GRAPHICS['']
        # rect = self.buttons.image.get_rect()

    def update_buttons(self, mouse):
        if mouse[0] and self.buttons[0].button_rect.collidepoint(mouse[1]):
            self.finished = True
        elif mouse[0] and self.buttons[1].button_rect.collidepoint(mouse[1]):
            self.next = "history"
            self.finished = True
        elif mouse[0] and self.buttons[2].button_rect.collidepoint(mouse[1]):
            self.finished = True

    def update(self, surface, mouse):

        self.update_buttons(mouse)

        surface.blit(self.background, self.viewport)
        surface.blit(self.caption, self.caption_rect)

        # self.info.update(self.game_info)
        self.info.draw(surface)

    def reset_game_info(self):
        self.game_info.update(
            {
                "score": 0,
                "lives": 3,
                "time_rest": 30,
            }
        )

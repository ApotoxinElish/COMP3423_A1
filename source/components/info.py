import pygame
from .. import constants as C
from .. import setup, tools

pygame.font.init()


class Info:
    def __init__(self, state, game_info):
        self.state = state
        self.game_info = game_info
        self.create_state_labels()
        self.create_info_labels()

    def create_state_labels(self):
        self.state_labels = []
        if self.state == "main_menu":
            self.state_labels.append((self.create_label("PLAY"), (195, 400)))
            self.state_labels.append((self.create_label("HISTORY"), (150, 500)))
            self.state_labels.append((self.create_label("TABLE"), (175, 600)))
        
        elif self.state == "history":
            self.state_labels.append((self.create_label("Back"), (0, 0)))

        elif self.state == "game_play":
            # 绘制得分
            self.state_labels.append(
                (
                    self.create_label("Score : {}".format(self.game_info["score"])),
                    (10, 5),
                )
            )

            # 绘制生命值
            self.state_labels.append(
                (
                    self.create_label("Lives : {}".format(self.game_info["lives"])),
                    (10, 50),
                )
            )
            # self.player_image = setup.GRAPHICS["life"]

    def create_info_labels(self):
        self.info_labels = []

    def create_label(self, label, size=40, width_scale=1.25, height_scale=1):
        font = pygame.font.Font(C.FONT, size)
        label_image = font.render(label, 1, C.BLACK)
        rect = label_image.get_rect()
        label_image = pygame.transform.scale(
            label_image,
            (int(rect.width * width_scale), int(rect.height * height_scale)),
        )
        return label_image

    def update(self, game_info):
        self.game_info = game_info
        self.create_state_labels()

    def draw(self, surface):
        for label in self.state_labels:
            surface.blit(label[0], label[1])
        for label in self.info_labels:
            surface.blit(label[0], label[1])

        # if self.state == "game_play":
        #     surface.blit(self.player_image, (10, 50))

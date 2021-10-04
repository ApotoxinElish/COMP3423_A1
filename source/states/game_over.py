import pygame
import sys
import time
from .. import constants as C
from .. import setup
from ..components import button, info


class GameOver:
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = "main_menu"
        self.background = setup.GRAPHICS["background"]

        # 用于阻止重复打开记录文件
        self.recorded = False

        # 游戏结束画面
        self.gameover_font = pygame.font.Font(C.FONT, 48)
        self.again_image = setup.GRAPHICS["again"]
        self.again_rect = self.again_image.get_rect()
        self.gameover_image = setup.GRAPHICS["gameover"]
        self.gameover_rect = self.gameover_image.get_rect()

        if not self.recorded:
            self.recorded = True
            # 读取历史最高得分
            with open(C.RECORD, "r") as f:
                self.record_score = int(f.read())

            # 如果玩家得分高于历史最高得分，则存档
            if self.game_info["score"] > self.record_score:
                with open(C.RECORD, "w") as f:
                    f.write(str(self.game_info["score"]))

            with open(C.HISTORY, "a") as f:
                f.write(
                    str(
                        time.asctime(time.localtime(time.time()))
                        + "    "
                        + str(self.game_info["score"])
                        + "\n"
                    )
                )

    def update(self, surface, mouse):
        if mouse[0]:
            # 如果用户点击 “重新开始”
            if self.again_rect.collidepoint(mouse[1]):
                # 调用main函数，重新开始游戏
                self.finished = True
            # 如果用户点击 “结束游戏”
            elif self.gameover_rect.collidepoint(mouse[1]):
                # 退出游戏
                pygame.quit()
                sys.exit()

        self.draw(surface)

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        # 绘制结束界面
        record_score_text = self.gameover_font.render(
            "Best : %d" % self.record_score, True, C.BLACK
        )
        surface.blit(record_score_text, (50, 50))

        gameover_text1 = self.gameover_font.render("Your Score", True, C.BLACK)
        gameover_text1_rect = gameover_text1.get_rect()
        gameover_text1_rect.left, gameover_text1_rect.top = (
            C.SCREEN_W - gameover_text1_rect.width
        ) // 2, C.SCREEN_H // 3
        surface.blit(gameover_text1, gameover_text1_rect)

        gameover_text2 = self.gameover_font.render(
            str(self.game_info["score"]), True, C.BLACK
        )
        gameover_text2_rect = gameover_text2.get_rect()
        gameover_text2_rect.left, gameover_text2_rect.top = (
            C.SCREEN_W - gameover_text2_rect.width
        ) // 2, gameover_text1_rect.bottom + 10
        surface.blit(gameover_text2, gameover_text2_rect)

        self.again_rect.left, self.again_rect.top = (
            C.SCREEN_W - self.again_rect.width
        ) // 2, gameover_text2_rect.bottom + 50
        surface.blit(self.again_image, self.again_rect)

        self.gameover_rect.left, self.gameover_rect.top = (
            C.SCREEN_W - self.again_rect.width
        ) // 2, self.again_rect.bottom + 10
        surface.blit(self.gameover_image, self.gameover_rect)

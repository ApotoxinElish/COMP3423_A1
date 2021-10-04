from math import trunc
from ..components import info
import pygame
from .. import tools, setup
from .. import constants as C
import sys
from random import *
from ..components import button, question, timer


class GamePlay:
    def start(self, game_info):
        self.game_info = game_info
        self.finished = False
        self.next = "game_over"
        self.info = info.Info("game_play", self.game_info)
        self.setup_background()
        self.setup_pause()
        self.setup_question()
        self.setup_buttons()
        self.setup_timer()

        self.update_question()
        self.answer_timer.start(self.level)

    def setup_background(self):
        self.background = setup.GRAPHICS["background"]
        self.background_rect = self.background.get_rect()

    def setup_pause(self):
        # 标志是否暂停游戏
        self.paused = False
        self.pause_nor_image = setup.GRAPHICS["pause_nor"]
        self.pause_pressed_image = setup.GRAPHICS["pause_pressed"]
        self.resume_nor_image = setup.GRAPHICS["resume_nor"]
        self.resume_pressed_image = setup.GRAPHICS["resume_pressed"]
        self.paused_rect = self.pause_nor_image.get_rect()
        self.paused_rect.topleft = C.SCREEN_W - self.paused_rect.width - 10, 10
        self.paused_image = self.pause_nor_image

    def setup_question(self):
        # 题目
        self.center_question = question.Question((240, 250))

    def update_question(self):
        self.center_question.update()
        for each in self.buttons:
            each.update()
            while each.num == self.center_question.answer:
                each.update()

        self.correct_answer = randint(0, 3)
        self.buttons[self.correct_answer].update(self.center_question.answer)

    def setup_buttons(self):
        # 按钮
        centers = [(120, 438), (360, 438), (120, 613), (360, 613)]
        self.buttons = []
        for i in range(4):
            self.buttons.append(button.Button(i, centers[i]))

    def setup_timer(self):
        # 设置难度级别
        self.level = 1
        self.correct_times = 0
        self.answer_timer = timer.Timer((240, 100))

    def update(self, surface, mouse):
        if mouse[0] and self.paused_rect.collidepoint(mouse[1]):
            self.paused = not self.paused
            self.answer_timer.pause(self.paused)

        elif mouse[0] and not self.paused and self.game_info["lives"] > 0:
            for each in self.buttons:
                if each.button_rect.collidepoint(mouse[1]):
                    if each.id == self.correct_answer:
                        self.game_info["score"] += 10
                        self.correct_times += 1
                        if self.correct_times == 3:
                            self.level += 1
                            self.correct_times = 0
                    else:
                        self.game_info["lives"] -= 1
                        self.correct_times = 0

                    # 更新题目和按钮
                    self.update_question()
                    self.answer_timer.start(self.level)
                    break

        elif not mouse[0]:
            if self.paused_rect.collidepoint(mouse[1]):
                if self.paused:
                    self.paused_image = self.resume_pressed_image
                else:
                    self.paused_image = self.pause_pressed_image
            else:
                if self.paused:
                    self.paused_image = self.resume_nor_image
                else:
                    self.paused_image = self.pause_nor_image

        self.answer_timer.update()

        if self.answer_timer.rest < 0:
            self.game_info["lives"] -= 1
            self.correct_times = 0
            self.update_question()
            self.answer_timer.start(self.level)

        self.info.update(self.game_info)
        if self.game_info["lives"] > 0:
            self.draw(surface)
        else:
            self.finished = True

    def draw(self, surface):
        surface.blit(self.background, (0, 0))
        # 绘制暂停按钮
        surface.blit(self.paused_image, self.paused_rect)

        if not self.paused:
            self.info.draw(surface)
            # 绘制题目
            self.center_question.draw(surface)

            # 绘制按钮
            for each in self.buttons:
                each.draw(surface)

            # 绘制计时器
            self.answer_timer.draw(surface)

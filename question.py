import pygame
from random import *


class Question:
    def __init__(self, center):
        self.center = center
        self.button_rect = pygame.Rect(0, 0, 300, 100)
        self.button_rect.center = center
        self.font = pygame.font.Font("font/font.ttf", 60)
        self.update()

    def show(self, screen):
        screen.fill((0, 0, 0), self.button_rect)
        screen.blit(self.text, self.rect)

    def update(self):
        self.left_num = randint(1, 10)
        self.right_num = randint(1, 10)
        self.answer = self.left_num * self.right_num
        self.text = self.font.render(
            "%d * %d = ?" % (self.left_num, self.right_num), True, (255, 255, 255)
        )
        self.rect = self.text.get_rect()
        self.rect.center = self.center

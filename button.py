import pygame
from random import *


class Button:
    def __init__(self, id, center):
        self.id = id
        self.center = center
        self.button_rect = pygame.Rect(0, 0, 150, 100)
        self.button_rect.center = center
        self.font = pygame.font.Font("font/font.ttf", 48)
        self.update()

    def show(self, screen):
        screen.fill((0, 0, 0), self.button_rect)
        screen.blit(self.text, self.rect)

    def update(self, num=0):
        self.num = randint(1, 100)
        if num:
            self.num = num
        self.text = self.font.render("%d" % self.num, True, (255, 255, 255))
        self.rect = self.text.get_rect()
        self.rect.center = self.center

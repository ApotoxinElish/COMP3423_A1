import pygame
import time


class Timer:
    def __init__(self, center):
        self.center = center
        self.button_rect = pygame.Rect(0, 0, 100, 50)
        self.button_rect.center = center
        self.font = pygame.font.Font("font/font.ttf", 48)

        self.origin = 30

    def show(self, screen):
        self.update()
        screen.fill((0, 0, 0), self.button_rect)
        screen.blit(self.text, self.rect)

    def start(self, level):
        self.time_level = int(self.origin / level)
        self.begin = time.time()

    def update(self):
        self.now = time.time()
        self.rest = self.time_level - (self.now - self.begin)
        self.text = self.font.render("%ds" % self.rest, True, (255, 255, 255))
        self.rect = self.text.get_rect()
        self.rect.center = self.center

    def pause(self, paused):
        if paused:
            self.pause_rest = self.rest
        else:
            self.begin = time.time() - (self.time_level - self.pause_rest)

    def get_time(self):
        time.asctime(time.localtime(time.time()))

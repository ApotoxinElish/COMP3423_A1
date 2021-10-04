# 工具和游戏主控
import pygame
import os


class Game:
    def __init__(self, state_dict, start_state):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.mouse = pygame.mouse.get_pressed()[0], pygame.mouse.get_pos()
        self.state_dict = state_dict
        self.state = self.state_dict[start_state]

    def update(self):
        if self.state.finished:
            game_info = self.state.game_info
            next_state = self.state.next
            self.state.finished = False
            self.state = self.state_dict[next_state]
            self.state.start(game_info)
        self.state.update(self.screen, self.mouse)

    def run(self):
        delay = 3
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse = pygame.mouse.get_pressed()[0], pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse = pygame.mouse.get_pressed()[0], pygame.mouse.get_pos()
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse = pygame.mouse.get_pressed()[0], pygame.mouse.get_pos()

            delay -= 1
            if not delay:
                self.update()
                delay = 3

            pygame.display.update()
            self.clock.tick(30)


def load_graphics(path, accept=(".jpg", ".png", ".bmp", ".gif")):
    graphics = {}
    for pic in os.listdir(path):
        name, ext = os.path.splitext(pic)
        if ext.lower() in accept:
            img = pygame.image.load(os.path.join(path, pic))
            if img.get_alpha():
                img = img.convert_alpha()
            else:
                img = img.convert()
            graphics[name] = img
    return graphics


def get_image(sheet, x, y, width, height, colorkey, scale):
    image = pygame.Surface((width, height))
    # colorkey = (0, 1, 0)
    image.fill(colorkey)
    # 0,0 代表画到哪个位置, x,y,w,h 代表sheet里哪个区域要取出来
    image.blit(sheet, (0, 0), (x, y, width, height))
    image.set_colorkey(colorkey)
    image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
    return image

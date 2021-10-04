import pygame
import sys
import traceback

import question
import button
import timer

from pygame.locals import *
from random import *

pygame.init()

bg_size = width, height = 480, 700
screen = pygame.display.set_mode(bg_size)
pygame.display.set_caption("Multiplication Tables")

background = pygame.image.load("images/background.png").convert()

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


def creatButton():
    centers = [(120, 438), (360, 438), (120, 613), (360, 613)]
    buttons = []
    for i in range(4):
        buttons.append(button.Button(i, centers[i]))
    return buttons


def update_question(center_question, buttons):
    center_question.update()
    for each in buttons:
        each.update()

    correct_id = randint(0, 3)
    buttons[correct_id].update(center_question.answer)
    return correct_id


def main():
    clock = pygame.time.Clock()

    # count score
    score = 0
    score_font = pygame.font.Font("font/font.ttf", 36)

    # 标志是否暂停游戏
    paused = False
    pause_nor_image = pygame.image.load("images/pause_nor.png").convert_alpha()
    pause_pressed_image = pygame.image.load("images/pause_pressed.png").convert_alpha()
    resume_nor_image = pygame.image.load("images/resume_nor.png").convert_alpha()
    resume_pressed_image = pygame.image.load(
        "images/resume_pressed.png"
    ).convert_alpha()
    paused_rect = pause_nor_image.get_rect()
    paused_rect.left, paused_rect.top = width - paused_rect.width - 10, 10
    paused_image = pause_nor_image

    # 设置难度级别
    level = 1
    correct_times = 0
    answer_timer = timer.Timer((240, 100))

    # 生命数量
    # life_image = pygame.image.load("images/life.png").convert_alpha()
    # life_rect = life_image.get_rect()
    life_num = 3

    # 题目
    center_question = question.Question((240, 250))

    # 按钮
    buttons = creatButton()
    correct_answer = update_question(center_question, buttons)
    answer_timer.start(level)

    # 用于阻止重复打开记录文件
    recorded = False

    # 游戏结束画面
    gameover_font = pygame.font.Font("font/font.TTF", 48)
    again_image = pygame.image.load("images/again.png").convert_alpha()
    again_rect = again_image.get_rect()
    gameover_image = pygame.image.load("images/gameover.png").convert_alpha()
    gameover_rect = gameover_image.get_rect()

    # 用于延迟
    delay = 10

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1 and paused_rect.collidepoint(event.pos):
                    paused = not paused
                    answer_timer.pause(paused)
                if event.button == 1 and not paused and life_num > 0:
                    for each in buttons:
                        if each.button_rect.collidepoint(event.pos):
                            if each.id == correct_answer:
                                score += 10
                                correct_times += 1
                                if correct_times == 3:
                                    level += 1
                                    correct_times = 0
                            else:
                                life_num -= 1
                                correct_times = 0
                            # 更新题目和按钮
                            correct_answer = update_question(center_question, buttons)
                            answer_timer.start(level)

            elif event.type == MOUSEMOTION:
                if paused_rect.collidepoint(event.pos):
                    if paused:
                        paused_image = resume_pressed_image
                    else:
                        paused_image = pause_pressed_image
                else:
                    if paused:
                        paused_image = resume_nor_image
                    else:
                        paused_image = pause_nor_image

        screen.blit(background, (0, 0))

        if life_num > 0 and not paused:
            # 绘制得分
            score_text = score_font.render("Score : %s" % str(score), True, WHITE)
            screen.blit(score_text, (10, 5))

            # 绘制生命值
            score_text = score_font.render("Life : %s" % str(life_num), True, WHITE)
            screen.blit(score_text, (10, 50))

            # 绘制计时器
            answer_timer.show(screen)
            if answer_timer.rest < 0:
                life_num -= 1
                correct_times = 0
                correct_answer = update_question(center_question, buttons)
                answer_timer.start(level)

            # 绘制题目
            center_question.show(screen)

            # 绘制按钮
            for i in range(4):
                buttons[i].show(screen)

        elif paused:
            pass

        # 绘制游戏结束画面
        elif life_num <= 0:
            if not recorded:
                recorded = True
                # 读取历史最高得分
                with open("record.txt", "r") as f:
                    record_score = int(f.read())

                # 如果玩家得分高于历史最高得分，则存档
                if score > record_score:
                    with open("record.txt", "w") as f:
                        f.write(str(score))

            # 绘制结束界面
            record_score_text = score_font.render(
                "Best : %d" % record_score, True, WHITE
            )
            screen.blit(record_score_text, (50, 50))

            gameover_text1 = gameover_font.render("Your Score", True, (255, 255, 255))
            gameover_text1_rect = gameover_text1.get_rect()
            gameover_text1_rect.left, gameover_text1_rect.top = (
                width - gameover_text1_rect.width
            ) // 2, height // 3
            screen.blit(gameover_text1, gameover_text1_rect)

            gameover_text2 = gameover_font.render(str(score), True, (255, 255, 255))
            gameover_text2_rect = gameover_text2.get_rect()
            gameover_text2_rect.left, gameover_text2_rect.top = (
                width - gameover_text2_rect.width
            ) // 2, gameover_text1_rect.bottom + 10
            screen.blit(gameover_text2, gameover_text2_rect)

            again_rect.left, again_rect.top = (
                width - again_rect.width
            ) // 2, gameover_text2_rect.bottom + 50
            screen.blit(again_image, again_rect)

            gameover_rect.left, gameover_rect.top = (
                width - again_rect.width
            ) // 2, again_rect.bottom + 10
            screen.blit(gameover_image, gameover_rect)

            # 检测用户的鼠标操作
            # 如果用户按下鼠标左键
            delay -= 1
            if pygame.mouse.get_pressed()[0] and delay < 0:
                # 获取鼠标坐标
                pos = pygame.mouse.get_pos()
                # 如果用户点击 “重新开始”
                if (
                    again_rect.left < pos[0] < again_rect.right
                    and again_rect.top < pos[1] < again_rect.bottom
                ):
                    # 调用main函数，重新开始游戏
                    main()
                # 如果用户点击 “结束游戏”
                elif (
                    gameover_rect.left < pos[0] < gameover_rect.right
                    and gameover_rect.top < pos[1] < gameover_rect.bottom
                ):
                    # 退出游戏
                    pygame.quit()
                    sys.exit()

        # 绘制暂停按钮
        screen.blit(paused_image, paused_rect)

        pygame.display.flip()
        clock.tick(30)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        pass
    except:
        traceback.print_exc()
        pygame.quit()
        input()

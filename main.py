# 游戏主要入口

from source import tools
from source.states import main_menu, game_play, game_over


def main():

    state_dict = {
        "main_menu": main_menu.MainMenu(),
        "game_play": game_play.GamePlay(),
        # "level": level.Level(),
        "game_over": game_over.GameOver(),
    }
    game = tools.Game(state_dict, "main_menu")
    game.run()


if __name__ == "__main__":
    main()

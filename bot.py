from utils.constants import GAME_WINDOW_WIDTH
from utils.gui import get_and_move_display, save_window_screenshot
from utils.skills import cut_wood, light_fire, mine_rocks, fish, kill, steal_cakes
import os

class Bot:
    def __init__(self, character_name='cuptastic', x=0):
        # move display to starting position
        get_and_move_display(character_name, x)

        # remove all files beginning with .screenshot
        for file in os.listdir("."):
            if file.startswith(".screenshot"):
                os.remove(file)

        # save screenshot of display
        save_window_screenshot()

    
    def cut_wood(self):
        print("Cutting wood")
        cut_wood()
    
    def light_fire(self, wood_type):
        print("Lighting Fire")
        light_fire(wood_type)
    
    def mine_rocks(self, rock_type):
        print("Mining rocks")
        mine_rocks(rock_type)
    
    def fish(self, *fish_type):
        print("Fishing")
        fish(*fish_type)
    
    def kill(self):
        print("Killing")
        kill()
    
    def steal_cakes(self):
        print("Stealing cakes")
        steal_cakes()


if __name__ == '__main__':
    # get argument from command line
    import sys

    if not len(sys.argv) > 1:
        print("No bot name provided")
        exit()
    else:
        bots = []
        x=0
        for name in sys.argv[1:]: 
            bot = Bot(name, x)
            bot.fish('shrimp', 'anchovies')

            # bots.append(bot)
            # x += GAME_WINDOW_WIDTH
            
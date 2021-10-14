from utils.gui import get_and_move_display, save_window_screenshot
from utils.skills import cut_wood, light_fire, mine_rocks, fish, kill
import os

class Bot:
    def __init__(self):
        # move display to starting position
        get_and_move_display()

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


if __name__ == '__main__':
    b = Bot()
    # b.light_fire('oak')
    # b.cut_wood()
    # b.mine_rocks('iron')
    # b.fish('trout', 'salmon')
    b.kill()
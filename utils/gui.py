from Xlib import display, X
from constants import GAME_WINDOW_HEIGHT, GAME_WINDOW_WIDTH, GAME_WINDOW_X, GAME_WINDOW_Y
from pyautogui import screenshot


def get_and_move_display():
    WINDOW_NAME = 'RuneLite - cuptastic'

    d = display.Display()
    r = d.screen().root

    x = GAME_WINDOW_X
    y = GAME_WINDOW_Y
    width = GAME_WINDOW_WIDTH
    height = GAME_WINDOW_HEIGHT

    window_ids = r.get_full_property(
        d.intern_atom('_NET_CLIENT_LIST'), X.AnyPropertyType
    ).value
    for window_id in window_ids:
        window = d.create_resource_object('window', window_id)
        print(window.get_wm_name())
        if window.get_wm_name() == WINDOW_NAME:
            print('Moving Window')
            window.set_input_focus(X.RevertToParent, X.CurrentTime)
            window.configure(
                x=x,
                y=y,
                width=width,
                height=height,
                border_width=0,
                stack_mode=X.Above
            )
            # TODO: figure out how to rise above other windows

            d.sync()
    

def save_window_screenshot():
    game_window = screenshot(region=(GAME_WINDOW_X, GAME_WINDOW_Y, GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT))

    # save to relative path ./live_images/game_screenshot.png
    game_window.save('./live_images/game_window.png')

    # TODO make this work for any window size
    invent_left = GAME_WINDOW_WIDTH - 240
    invent_top = GAME_WINDOW_HEIGHT - 320
    invent_width = 200
    invent_height = 270


    inventory = screenshot(region=(invent_left, invent_top, invent_width, invent_height))
    inventory.save('./live_images/inventory.png')




if __name__ == "__main__":
    get_and_move_display()
    save_window_screenshot()

from Xlib import display, X
from constants import GAME_WINDOW_HEIGHT, GAME_WINDOW_WIDTH, GAME_WINDOW_X, GAME_WINDOW_Y
import pyautogui
import cv2
import numpy as np
import random
import time
from utils.obfuscate import get_mouse_x_y_path


def get_and_move_display():
    """
    Find Runelite running window, resize it and move it to the upper left of the screen.
    """
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
    """
    Take a screenshot of the entire game window.
    """
    game_window = pyautogui.screenshot(region=(GAME_WINDOW_X, GAME_WINDOW_Y, GAME_WINDOW_WIDTH, GAME_WINDOW_HEIGHT))

    # save to relative path ./live_images/game_screenshot.png
    game_window.save('./live_images/game_window.png')


def save_inventory_screenshot():
    """
    Take a screenshot of the inventory section of the game.
    """
    # TODO make this work for any window size
    invent_left = GAME_WINDOW_WIDTH - 240
    invent_top = GAME_WINDOW_HEIGHT - 320
    invent_width = 200
    invent_height = 270


    inventory = pyautogui.screenshot(region=(invent_left, invent_top, invent_width, invent_height))
    inventory.save('./live_images/inventory.png')


def click_image(image):
    """
    args:
        image: path to image to search for
    returns:
        coordinates of image
    """
    # find image on screen
    
    loc = pyautogui.locateOnScreen(image) #Box type with attributes, left, top, width, height
    point = pyautogui.center(loc)

    # icons are 20x20

    x, y = point

    #get random int between 0 and 8
    x = x + random.randint(-8, 8)
    y = y + random.randint(-8, 8)

    pyautogui.click(x, y) # click center of image

def drop_icon(image):
    with pyautogui.hold('shift'):
        click_image(image)


def find_contour_object():
    """
    Take screenshot of current game instance. return x, y coordinates of item.
    """
    save_window_screenshot()
    image = cv2.imread('./live_images/game_window.png')


    red = ([0, 0, 180], [80, 80, 255])
    boundaries = [red]
    # loop over the boundaries
    for (lower, upper) in boundaries:
        lower = np.array(lower, dtype="uint8")
        upper = np.array(upper, dtype="uint8")

        mask = cv2.inRange(image, lower, upper)
        _, thresh = cv2.threshold(mask, 40, 255, 0)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) != 0:
        c = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(c)

        x = random.randrange(x + 5, x + max(w - 5, 6))  # 950,960
        print('x: ', x)
        y = random.randrange(y + 5, y + max(h - 5, 6))  # 490,500
        print('y: ', y)
    
    return x, y


def move_mouse_to_coords(dest_x, dest_y):
    # start at random y coord on x coord GAME_WINDOW_X
    start_x = GAME_WINDOW_WIDTH
    start_y = random.randrange(GAME_WINDOW_Y, GAME_WINDOW_Y + GAME_WINDOW_HEIGHT)
    points = get_mouse_x_y_path(start_x, start_y, dest_x, dest_y)

    for point in points:
        # get random time between 0.01 and 0.05
        rand_duration = random.uniform(0.01, 0.02)
        pyautogui.moveTo(point[0], point[1], duration=rand_duration)

def mouse_click():
    rand_duration = random.uniform(0.1, 0.23)
    pyautogui.click(duration=rand_duration)


if __name__ == "__main__":
    get_and_move_display()
    click_image('./images/icons/tinderbox.png')
    click_image('./images/icons/wood.png')
    time.sleep(5.6)
    click_image('./images/icons/tinderbox.png')
    click_image('./images/icons/wood.png')
    time.sleep(5.5)
    click_image('./images/icons/tinderbox.png')
    click_image('./images/icons/wood.png')
    time.sleep(4.5)
    click_image('./images/icons/tinderbox.png')
    click_image('./images/icons/wood.png')


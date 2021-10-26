import itertools
from Xlib import display, X
from utils.constants import GAME_WINDOW_HEIGHT, GAME_WINDOW_WIDTH, GAME_WINDOW_X, GAME_WINDOW_Y
import pyautogui
import cv2
import numpy as np
import random
import time
from utils.obfuscate import get_mouse_x_y_path
from utils.images import save_crop_image
from itertools import chain

pyautogui.MINIMUM_DURATION = 0.0
pyautogui.PAUSE = 0.0
pyautogui.MINIMUM_SLEEP = 0.0001
pyautogui.DARWIN_CATCH_UP_TIME = 0.0



def get_and_move_display(character='cuptastic', x = GAME_WINDOW_X, y = GAME_WINDOW_Y):
    """
    Find Runelite running window, resize it and move it to the upper left of the screen.
    """
    WINDOW_NAME = 'RuneLite - {}'.format(character)

    d = display.Display()
    r = d.screen().root

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
    

def save_mini_map_screenshot():
    """
    Take a screenshot of the minimap
    """
    mini_map = pyautogui.screenshot(region=(630, 65, 100, 75))
    mini_map.save('./live_images/mini_map.png')
    return mini_map


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


def get_icon_coords(icon, region=None):
    """
    args:
        icon: name to search for
    returns:
        coordinates of image
    """
    icon_path = './images/icons/{}.png'.format(icon)
    loc = None
    while not loc:
        print('looking for', icon)
        if region:
            loc = pyautogui.locateOnScreen(icon_path, region=region, confidence=0.5)
        else:
            loc = pyautogui.locateOnScreen(icon_path, confidence=.75) #Box type with attributes, left, top, width, height
        if not loc:
            time.sleep(1.5)
    point = pyautogui.center(loc)

    # icons are 20x20

    x, y = point

    #get random int between 0 and 8
    x = x + random.randint(-8, 8)
    y = y + random.randint(-8, 8)

    return x, y

def count_inventory(*icons):
    """
    Count the number of items in inventory.
    """
    icon_paths = ['./images/icons/{}.png'.format(icon) for icon in icons]
    icons = itertools.chain(*[pyautogui.locateAllOnScreen(icon_path) for icon_path in icon_paths])
     # returns generator
    total = len(list(icons))
    print('total,', total)
    return total # count items in generator


    
def empty_inventory(*icons):
    """
    Shift Click all items in inventory.
    """
    icon_paths = ['./images/icons/{}.png'.format(icon) for icon in icons]
    icon_gens = [pyautogui.locateAllOnScreen(icon_path) for icon_path in icon_paths]

    icons = sorted(list(chain(*icon_gens)), key=lambda x: x.top)
    
    with pyautogui.hold('shift'):
        for loc in icons:
            x, y = pyautogui.center(loc)
            x = x + random.randint(-8, 8)
            y = y + random.randint(-8, 8)
            move_mouse_to_coords(x, y, click_and_off_screen=False)
            pyautogui.click(_pause=False)


def get_map_coords(image):
    """
    TODO:
    args:
        image: path to image to search for
    returns:
        coordinates of image
    """
    # find image on screen
    loc = pyautogui.locateOnScreen(image) #Box type with attributes, left, top, width, height
    point = pyautogui.center(loc)

    x, y = point

    #get random int between 0 and 8
    x = x + random.randint(-2, 2)
    y = y + random.randint(-2, 2)

    return x, y


def click_icon(image):
    x, y = get_icon_coords(image)
    move_mouse_to_coords(x, y, click_and_off_screen=False)
    pyautogui.click(_pause=False)



def drop_icon(image):
    with pyautogui.hold('shift'):
        click_icon(image)


def find_contour_object(color='purple', contmax=False, xmin=False, xmax=False, ymin=False, ymax=False):
    """
    return x, y coordinates of item.
    """
    while True:
        image = cv2.imread('./live_images/game_window.png')
        # set upper half of image to be black
        image[0:int(image.shape[0]/3), :] = 0
        # convert image to hsv
        image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        # save has image
        cv2.imwrite('./live_images/game_window_hsv.png', image_hsv)
        # HSV min is (0, 0, 0) and max is (179, 255, 255)

        # very saturated and dark colors
        S_min = 240
        S_max = 255
        V_min = 240
        V_max = 255

        # hsv hues https://stackoverflow.com/questions/10948589/choosing-the-correct-upper-and-lower-hsv-boundaries-for-color-detection-withcv
        if color == 'red':
            H_min = 0
            H_max = 10
        elif color == 'purple':
            H_min = 140
            H_max = 160
        lower = np.array([H_min, S_min, V_min], dtype="uint8")
        upper = np.array([H_max, S_max, V_max], dtype="uint8")
        mask = cv2.inRange(image_hsv, lower, upper)
        cv2.imwrite('./live_images/mask.png', mask)
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        if not contours:
            print('No contours found')
            # if we return negative, it wasn't found on the screen
            return -1, -1
        coordinate_contours = {'x_least': 0, 'y_least': 0, 'x_most': 0, 'y_most': 0}
        x_max_coord = 0
        x_min_coord = 500_000 # sufficiently large
        y_max_coord = 0
        y_min_coord = 500_000 # sufficiently large
        for i, c in enumerate(contours):
            x_coordinate = c[0][0][0]
            y_coordinate = c[0][0][1]
            if x_coordinate < x_min_coord:
                x_min_coord = x_coordinate
                coordinate_contours['x_least'] = c
            if x_coordinate > x_max_coord:
                x_max_coord = x_coordinate
                coordinate_contours['x_most'] = c
            if y_coordinate < y_min_coord:

                y_min_coord = y_coordinate
                coordinate_contours['y_least'] = c
            if y_coordinate > y_max_coord:
                y_max_coord = y_coordinate
                coordinate_contours['y_most'] = c
        
        if xmin:
            contour = coordinate_contours['x_least']
        
        elif xmax:
            contour = coordinate_contours['x_most']
        elif ymin:
            contour = coordinate_contours['y_least']
        
        elif ymax:
            contour = coordinate_contours['y_most']
        else:
            contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(contour)
        print(x, y, w, h, 'bounding rect')

        x = random.randrange(x, x + w)
        print('x: ', x)
        y = random.randrange(y, y + h)
        print('y: ', y)
        return x, y


def move_mouse_to_coords(dest_x, dest_y, click_and_off_screen=True, fast=False):
    if fast:
        pyautogui.moveTo(dest_x, dest_y)
        return
    start_x, start_y = pyautogui.position()
    points = get_mouse_x_y_path(start_x, start_y, dest_x, dest_y)

    rand_duration = random.uniform(.1, .3) / (len(points) + 1)

    for point in points:
        # get random time between 0.01 and 0.05
        pyautogui.moveTo(point[0], point[1], _pause=False, duration=rand_duration)
    
    if click_and_off_screen:
        pyautogui.click()
        x = GAME_WINDOW_WIDTH
        y = random.randrange(GAME_WINDOW_Y, GAME_WINDOW_Y + GAME_WINDOW_HEIGHT)
        move_mouse_to_coords(x, y, False)


if __name__ == "__main__":
    get_and_move_display()
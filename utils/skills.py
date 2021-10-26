import pyautogui
import random
import time
from utils.constants import GAME_WINDOW_HEIGHT


from utils.gui import (
    click_icon,
    drop_icon,
    empty_inventory,
    find_contour_object,
    get_icon_coords,
    move_mouse_to_coords,
    save_window_screenshot,
    count_inventory,
    empty_inventory,
)
from utils.images import save_crop_image, find_image_within_image, find_rgb_within_image


def agility(where='varrock'):
    while True:        
        save_map_screenshot()
        # loop through imagines in ./images/agility/varrock
        import os
        for image in os.listdir(f'./images/agility/{where}'):
            print(image)


def steal_cakes(static=True):
    # you need to have a red box screen marker on your screen which, when clicked,
    #  will either steal a player or click the ground such that the player won't move
    while True:
        
        save_window_screenshot()
        x, y = find_contour_object(color='red')
        if x < 0 and y < 0:
            # we couldn't find the red object on the screen
            continue
        else:
            # x, y = find_contour_object(color='purple')
            # move_mouse_to_coords(x, y, click_and_off_screen=False)
            pyautogui.click()
        pastries = ['cake', 'cake_third', 'cake_third_double','cake_chocolate_third', 'bread']
        num_items = count_inventory(*pastries)
        if num_items > 14:
            empty_inventory(*pastries)
            save_window_screenshot()
            x, y = find_contour_object(color='purple')
            move_mouse_to_coords(x, y, click_and_off_screen=False)


def fish(*fish_type):
    fish_spot = fish_type[0]
    while True:
        x, y = get_icon_coords(fish_spot, region=(0, 0, 540, GAME_WINDOW_HEIGHT))
        move_mouse_to_coords(x, y, click_and_off_screen=True)
        pyautogui.click()
        # check if fishing
        # random float between 1 and 3
        time.sleep(random.uniform(1, 3))
        while check_if_fishing():
            time.sleep(random.uniform(1, 3))
        num_items = count_inventory(*fish_type)
        if num_items > 20:
            # empty_inventory(*fish_type)
            cook('trout')
            break


def cook(fish_type):
    while True:
        x, y = get_icon_coords(fish_type)
        move_mouse_to_coords(x, y, click_and_off_screen=False)
        pyautogui.click()

        # find contour
        x, y = find_contour_object(color='purple')
        move_mouse_to_coords(x, y, click_and_off_screen=False)
        pyautogui.click()
        time.sleep(random.uniform(3, 5))
        # click space
        pyautogui.press('space')
        # check if cooking
        while check_if_cooking():
            continue
        num_items = count_inventory('burnt_' + fish_type, 'cooked_' + fish_type)
        if num_items > 20:
            empty_inventory('burnt_' + fish_type, 'cooked_' + fish_type)
            break


def kill():
    while True:
        save_window_screenshot()
        # get current mouse position
        current_x, current_y = pyautogui.position()
        x, y = find_contour_object()
        pyautogui.moveTo(x, y)
        pyautogui.click(duration=random.uniform(.02, .11))
        # move mouse back to original position
        pyautogui.moveTo(current_x, current_y)
        time.sleep(random.uniform(3, 6))
        while check_if_killing():
            time.sleep(random.uniform(1, 3))
        # find ./images/ground_markers/feathers.png on screen
        loc = pyautogui.locateOnScreen('./images/ground_markers/feathers.png', confidence=0.5)
        if loc:
            point = pyautogui.center(loc)
            x, y = point
            pyautogui.click(x, y)
            time.sleep(random.uniform(2, 3))
        else:
            print('Could not find feathers')        

def cut_wood():
    while True:
        save_window_screenshot()
        x, y = find_contour_object()
        move_mouse_to_coords(x, y)
        pyautogui.click()
        # check if woodcutting
        time.sleep(random.uniform(1, 3))
        while check_if_cutting():
            time.sleep(random.uniform(1, 3))
            

def mine_rocks(rock_type):
    # icon = f'./images/icons/{rock_type}.png'
    while True:
        x, y = find_contour_object(color='purple')
        move_mouse_to_coords(x, y, click_and_off_screen=False)
        pyautogui.click()
        time.sleep(random.uniform(.75, 1.4))
        while check_if_mining():
            continue
        num_items = count_inventory(rock_type)
        if num_items > 20:
            empty_inventory(rock_type)


def check_if_cooking():
    save_window_screenshot()

    if pyautogui.locateOnScreen('./images/indicators/not_cooking.png', confidence=.5):
        print('Not Cooking')
        return True
    else:
        print('Cooking')
        return False


def check_if_mining():
    save_window_screenshot()
    
    if pyautogui.locateOnScreen('./images/indicators/not_mining.png', confidence=0.5):
        print('Not Mining')
        return False
    else:
        print('Mining')
        return True


def check_if_killing():
    # look for image on screen
    # if found, return true
    # else, return false
    health_bar = pyautogui.screenshot(region=(10, 70, 30, 15))
    health_bar.save('./live_images/health.png')

    rgb_low = (52, 136, 4)
    rgb_high = (58, 141, 9)
    result = find_rgb_within_image(image='./live_images/health.png', rgb_low=rgb_low, rgb_high=rgb_high)

    if result:
        print('Killing')
        return True
    else:
        print('Not Killing')
        return False


def check_if_cutting():
    # retake screenshot
    save_window_screenshot()
    if pyautogui.locateOnScreen('./images/indicators/not_cutting.png', confidence=.75):
        print('Not Cutting')
        return False
    else:
        print('Cutting')
        return True


def check_if_fishing():
    # retake screenshot
    save_window_screenshot()
    if pyautogui.locateOnScreen('./images/indicators/not_fishing.png', confidence=.75):
        print('Not Fishing')
        return False
    else:
        print('Fishing')
        return True


def light_fire(wood_type):
    while True:
        click_icon('tinderbox')
        print('lighting', wood_type)
        click_icon(wood_type)
        while not check_for_xp_drop('firemaking'):
            continue


def check_for_xp_drop(skill, threshold=.9):
    # retake screenshot
    save_window_screenshot()
    # remove_top_bar
    save_crop_image('./live_images/game_window.png', y_crop=90)

    # find firemaking xp in top_cropped_window
    result = find_image_within_image(image='./live_images/cropped_image.png', sub_image=f'./images/xp/{skill}.png', threshold=threshold)

    if not result:
        print('no xp')
        return False
    else:
        print('xp drop!')
        return True
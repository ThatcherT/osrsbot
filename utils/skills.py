from gui import get_and_move_display, click_icon, drop_icon
from utils.gui import (
    find_contour_object,
    mouse_click,
    move_mouse_to_coords,
)
def cut_wood():
    x, y = find_contour_object()
    move_mouse_to_coords(x, y)
    mouse_click()

def drop_wood():
    drop_icon('./images/icon/wood.png')

def use_icons(image0, image1):
    click_icon(image0)
    click_icon(image1)

def light_fire():
    use_icons('./images/icon/tinderbox.png', './images/icon/wood.png')


if __name__ == "__main__":
    get_and_move_display()
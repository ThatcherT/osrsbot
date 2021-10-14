import cv2
import numpy as np


def save_crop_image(image, x_crop=0, y_crop=0, width_crop=0, height_crop=0):
    """
    args:
        image: path to image to crop
        x_crop: number of pixels to crop from left
        y_crop: number of pixels to crop from top
        width_crop: number of pixels to crop from bottom
        height_crop: number of pixels to crop from right
    returns:
        cropped image
    """
    img = cv2.imread(image)
    cropped_img = img[y_crop:img.shape[0]-y_crop, x_crop:img.shape[1]-x_crop]
    # save as new png with path ./live_images/cropped_image.png
    cv2.imwrite('./live_images/cropped_image.png', cropped_img)

    return cropped_img


def find_image_within_image(image, sub_image):
    """
    args:
        image: path to image to search for
        sub_image: path to image to search for within image
    returns:
        coordinates of image
    """
    method = cv2.TM_CCOEFF_NORMED
    # Read the images from the file
    small_image = cv2.imread(sub_image).astype(np.uint8)
    large_image = cv2.imread(image).astype(np.uint8)
    
    result = cv2.matchTemplate(small_image, large_image, method)
    threshold = .9
    loc = np.where(result >= threshold)
    pts = loc[::-1]
    for p in pts:
        if not p.size == 0:
            return True
    return False


def find_rgb_within_image(image, rgb_low, rgb_high):
    """
    args:
        image: path to image to search for
        rgb_low: lower bound of rgb values
        rgb_high: upper bound of rgb values
    returns:
        True if any rgb values are within rgb_low and rgb_high
    """
    img = cv2.imread(image)
    for row in img:
        for pixel in row:
            print(pixel)
            if rgb_low[0] <= pixel[0] <= rgb_high[0] and rgb_low[1] <= pixel[1] <= rgb_high[1] and rgb_low[2] <= pixel[2] <= rgb_high[2]:
                return True
    return False
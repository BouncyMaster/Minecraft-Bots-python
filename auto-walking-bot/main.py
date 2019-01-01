import numpy as np
from grabscreen import grab_screen
import cv2
from directkeys import PressKey, ReleaseKey, D
import time


def draw_lines(img, lines):
    try:
        for line in lines:
            return True

    except Exception:
        pass


def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked


def process_img(original_img):
    processed_img = cv2.Canny(original_img, 100, 300)
    processed_img = cv2.GaussianBlur(processed_img, (5, 5), 0)

    vertices = np.array([[300, 450], [300, 120], [500, 120], [500, 450]])
    processed_img = roi(processed_img, [vertices])

    lines = cv2.HoughLinesP(processed_img, 1, np.pi / 180,
                            180, np.array([]), 250, 15)
    blockInFront = draw_lines(processed_img, lines)

    return processed_img, blockInFront


paused, blockInFront, blockWasInFront = False, False, False

while(True):
    if not paused:
        screen, blockInFront = process_img(
            # Where the minecraft window is on the screen
            grab_screen(region=(3, 30, 800, 530)))
        last_time = 0
        # Removing the parenthesis gives SyntaxError
        if blockInFront & (not blockWasInFront):
            last_time = time.time()
            PressKey(D)
        if time.time() - last_time > 1:
            ReleaseKey(D)
            last_time = 0

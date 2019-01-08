import numpy as np
from grabscreen import grab_screen
import cv2
from directkeys import PressKey, ReleaseKey, D, W
import time


def roi(img, vertices):
    mask = np.zeros_like(img)
    cv2.fillPoly(mask, vertices, 255)
    masked = cv2.bitwise_and(img, mask)
    return masked


def processImg(originalImg):
    processedImg = cv2.Canny(originalImg, 100, 300)
    processedImg = cv2.GaussianBlur(processedImg, (5, 5), 0)

    vertices = np.array([[300, 450], [300, 120], [500, 120], [500, 450]])
    processedImg = roi(processedImg, [vertices])

    lines = cv2.HoughLinesP(processedImg, 1, np.pi / 180,
                            180, np.array([]), 250, 15)

    try:
        if lines.any():
            return True
    except Exception:
        return False


startingTime = 0
blockWasInFront = False

PressKey(W)
while True:
    blockInFront = processImg(grab_screen(region=(3, 30, 800, 530)))
    if blockInFront & (not blockWasInFront):
        startingTime = time.time()
        blockWasInFront = True
        PressKey(D)

    if (time.time() - startingTime > 0.5) & blockWasInFront:
        startingTime = 0
        blockWasInFront = False
        ReleaseKey(D)

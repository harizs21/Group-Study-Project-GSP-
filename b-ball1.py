import mss
import pyautogui
from PIL import Image
import numpy as np
import time


def take_screenshot():
    with mss.mss() as mss_obj:
        mss_obj.shot(output='screencap.png')


def execute_swipe(X, Y):
    pyautogui.moveTo(1024, 605)
    pyautogui.mouseDown(button='left')
    pyautogui.dragTo(X, Y, 0.5, button='left')
    pyautogui.mouseUp(button='left')


x = 687
y = 500
t = 3
moving = False
a = input('Start?')
if a == 's':
    while (1):
        take_screenshot()
        image = Image.open('screencap.png')
        image = np.array(image)

        while (x < 1024):
            if list(image[235][x]) <= [97, 57, 46] and list(image[280][x]) >= [90, 50, 40]:
                X = 174 + x
                x1 = x
                break
            x += 1
        x = 687
        while (y > 250):
            if list(image[y][1024]) == [97, 57, 46]:
                Y = y - 60

                break
            y -= 1
        y = 500

        take_screenshot()
        image = Image.open('screencap.png')
        image = np.array(image)

        while (x < 1024):
            if list(image[235][x]) <= [97, 57, 46] and list(image[280][x]) >= [90, 50, 40]:
                X = 174 + x
                x2 = x
                break
            x += 1
        x = 687
        while (y > 250):
            if list(image[y][1024]) == [97, 57, 46]:
                Y = y - 60

                break
            y -= 1
        y = 500

        if x1 != x2:
            moving = True

        if X > 1024:
            X -= (X - 1024) * 0.15

        else:
            X += (1024 - X) * 0.15

        if moving == True:
            t = 5
            time.sleep(6.5)

        execute_swipe(X, Y)
        moving = False
        time.sleep(t)

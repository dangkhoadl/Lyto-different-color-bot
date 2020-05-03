#!/usr/bin/env python3

import numpy as np
import cv2
from mss import mss
from PIL import Image

import pyautogui
from time import sleep

from collections import defaultdict


with mss() as sct:
    # Monitor config
    mon = sct.monitors[2]
    monitor = {
        "top": mon["top"] + 400,  # 290px from the top
        "left": mon["left"] + 240,  # 240px from the left
        "width": 470,
        "height": 600,
        "mon": 2,
    }

    # Show the preset cv2 window for setup
    sct_img = sct.grab(monitor)
    img = np.array(sct_img)         # shape = (750, 470, 4)

    
    while "Screen Capturing":
        # Get img
        sct_img = sct.grab(monitor)

        # Convert sct_img to np.array
        img = np.array(sct_img)

        # Detect circles in the image
        gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(image=gray, method=cv2.HOUGH_GRADIENT,
            dp=1.5, minDist=7)

        if circles is not None:
            # Convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            # Get color samples from circles
            samples = defaultdict(list)
            for index, (x, y, r) in enumerate(circles):
                samples[tuple(img[y,x,:][:3])].append(index)

            # Detect the abnormal color
            abnorm_circle = -1
            for color, indices in samples.items():
                if len(indices) == 1: abnorm_circle = indices[0]

            # Draw cirles: Loop over the (x, y) coordinates and radius of the circles
            for index, (x, y, r) in enumerate(circles):
                if index == abnorm_circle:
                    # CLick
                    sleep(0.1)
                    pyautogui.click(x + monitor["left"], y + monitor["top"]);

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

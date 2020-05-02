#!/usr/bin/env python3

import numpy as np
import cv2
from mss import mss
from PIL import Image
from collections import defaultdict


with mss() as sct:
    # Monitor config
    mon = sct.monitors[2]
    monitor = {
        "top": mon["top"] + 290,  # 290px from the top
        "left": mon["left"] + 240,  # 240px from the left
        "width": 470,
        "height": 750,
        "mon": 2,
    }

    while "Screen Capturing":
        # Get img
        sct_img = sct.grab(monitor)

        # Convert sct_img to np.array
        img = np.array(sct_img)         # shape = (750, 470, 4)

        # Detect circles in the image
        gray = cv2.cvtColor(src=img, code=cv2.COLOR_BGR2GRAY)
        circles = cv2.HoughCircles(image=gray, method=cv2.HOUGH_GRADIENT,
            dp=1.2, minDist=8)

        if circles is not None:
            # Convert the (x, y) coordinates and radius of the circles to integers
            circles = np.round(circles[0, :]).astype("int")

            # Get color samples from circles
            samples = defaultdict(list)
            for index, (x, y, r) in enumerate(circles):
                samples[tuple(img[y,x,:][:3])].append(index)

            # Detect the abnormal color
            abnorm_circle = None
            for color, indices in samples.items():
                if len(indices) == 1: abnorm_circle = indices[0]
                print("{}: {}".format(color, indices))

            # Draw cirles: Loop over the (x, y) coordinates and radius of the circles
            for index, (x, y, r) in enumerate(circles):
                if index == abnorm_circle:
                    # Draw the circle in the output image
                    cv2.circle(
                        img=img, center=(x, y), radius=r,
                        color=(255,239,213), thickness=4)

                # Draw a rectangle corresponding to the center of all detected circles
                cv2.rectangle(
                    img=img, pt1=(x - 5, y - 5), pt2=(x + 5, y + 5),
                    color=(0, 128, 255), thickness=-1)

        # Show the output image
        cv2.imshow("Ahihi, Ez vkl", img)

        # Press "q" to quit
        if cv2.waitKey(25) & 0xFF == ord("q"):
            cv2.destroyAllWindows()
            break

import numpy as np
import cv2
import time
from matplotlib import pyplot as plt
from sklearn.cluster import KMeans

'''
* @param  image                 the frame to be processed
* @param  count                 count of current frame
* @return                       a tuple that contains (ball center x-coordinate, ball center y-coordinate, ball radius)
* @Note: prints all frames detected in a file called img
'''


def ballDetector(image, count, printing):
    # blur = cv2.GaussianBlur(gray,(3,3),0)
    sensitivity = 35
    lower_white2 = np.array([0,0,255-sensitivity])
    upper_white2 = np.array([255,sensitivity,255])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.medianBlur(gray, 5)

    newim = image.copy()

    circles = cv2.HoughCircles(blur,
                               cv2.HOUGH_GRADIENT,
                               minDist=30,
                               dp=5,
                               param1=400,  # sensitivity, high won't find enough circles, low too many
                               param2=2,  # accuracy, no of edges needed, high not enough, low too many
                               minRadius=3,
                               maxRadius=4)
    if circles is not None:
        circles = np.round(circles[0, :].astype("int"))

        for (x, y, r) in circles:
            player_img = image[y-10:y+10, x-10:x+10]
            if(not np.any(player_img)):
                continue
            player_hsv = cv2.cvtColor(player_img, cv2.COLOR_BGR2HSV)
            mask1 = cv2.inRange(player_hsv, lower_white2, upper_white2)
            # cv2.imshow("image", mask1)
            # cv2.waitKey(0)
            # cv2.destroyAllWindows()
            res1 = cv2.bitwise_and(player_img, player_img, mask=mask1)
            res1 = cv2.cvtColor(res1, cv2.COLOR_HSV2BGR)
            res1 = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)
            nzCount = cv2.countNonZero(res1)
            if(nzCount>=8):
                cv2.circle(newim, (x, y), r+5, (255, 255, 0), 2)
            # if printing:
                # cv2.imshow('ball',newim)

        return (x, y, r)
    return 0, 0, 0

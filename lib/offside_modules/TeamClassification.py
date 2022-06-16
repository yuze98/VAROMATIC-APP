import numpy as np
import cv2
import AdditionalFunctions
'''
* @param  frame     the frame to be processed
* @param  boxes     the properties of all bounding boxes of detected players
* @param  keptBoxes the indices of the remaining bounding boxes of detected players after non-maxima suppression
* @param  colors    the three colors of players' jerseys (team 0 "their goal is on the left", team 1 "their goal is on the right" and the referees team respectively)
* @return           the given properties of all bounding boxes of detected players with the team number property appended
'''


def teamsClassification(frame, boxes, keptBoxes, colors):
    # For printing purposes

    colorIndices = {"gray": (128, 128, 128),
                    "green": (0, 128, 0),
                    "yellow": (0, 255, 255),
                    "purple": (128, 0, 128),
                    "blue": (255, 0, 0),
                    "red1": (0, 0, 255),
                    "red2": (0, 0, 255),
                    "orange": (0, 165, 255),
                    "black": (0, 0, 0),
                    "white": (255, 255, 255)}
    # colorIndices1 = {"blue": (255, 0, 0), "red": (0, 0, 255), "orange": (0, 165, 255), "black": (0, 0, 0), "white": (255, 255, 255)}

    # hsvLowerBounds = {"blue": np.array([90, 150, 20]), "red": np.array([151, 150, 20]), "orange": np.array([[0, 150, 20]]), "black": np.array([0, 0, 0]), "white": np.array([0, 0, 20])}
    # hsvUpperBounds = {"blue": np.array([150, 255, 255]), "red": np.array([180, 255, 255]), "orange": np.array([[89, 255, 255]]), "black": np.array([180, 255, 19]), "white": np.array([255, 25, 255])}
    # For printing purposes
    outputFrame = frame.copy()

    for box in keptBoxes:
        (topLeftX, topLeftY, width, height) = (
            boxes[box][0], boxes[box][1], boxes[box][2], boxes[box][3])
        boxImage = frame[topLeftY: topLeftY +
                         height, topLeftX: topLeftX + width, :]
        if ((boxImage.shape[0] != 0) and (boxImage.shape[1] != 0)):
            hsvBox = cv2.cvtColor(boxImage, cv2.COLOR_BGR2HSV)
            # hsvBox = boxImage
            nonBlackOverTotalRatio = {}
            for color in colors:
                # print("Lower bound is",color_dict_HSV[color][0])
                # print("Upper bound is",color_dict_HSV[color][1])
                colorMask = cv2.inRange(hsvBox, np.array(
                    AdditionalFunctions.color_dict_HSV[color][0]), np.array(AdditionalFunctions.color_dict_HSV[color][1]))
                filteredBox = cv2.bitwise_and(
                    boxImage, boxImage, mask=colorMask)
                greyFilteredBox = cv2.cvtColor(filteredBox, cv2.COLOR_BGR2GRAY)
                nonBlackOverTotalRatio[color] = cv2.countNonZero(
                    greyFilteredBox) / (greyFilteredBox.shape[0] * greyFilteredBox.shape[1])
            maxColor = max(nonBlackOverTotalRatio,
                           key=nonBlackOverTotalRatio.get)
            # print("nonBlackOverTotalRatio ", nonBlackOverTotalRatio)
            # print("maxColor ", maxColor)

            # For printing purposes
            if nonBlackOverTotalRatio[colors[0]] <= 0.05 and nonBlackOverTotalRatio[colors[1]] <= 0.05:
                # cv2.rectangle(outputFrame, (topLeftX, topLeftY), (topLeftX +
                #                                                 width, topLeftY + height), (0, 0, 0), 2)
                continue
            cv2.rectangle(outputFrame, (topLeftX, topLeftY), (topLeftX +
                          width, topLeftY + height), colorIndices[maxColor], 2)
            # print(maxColor)
            if (maxColor == colors[0]):
                # left team
                boxes[box].append(0)
                # print("Colors [0] is : ",colors[0])
            elif (maxColor == colors[1]):
                # right team
                boxes[box].append(1)
                # print("Colors [1] is : ",colors[1])

        else:
            boxes[box].append(None)

    # cv2.imshow("Frame", outputFrame)

    return boxes, outputFrame

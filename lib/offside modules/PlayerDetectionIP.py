import numpy as np
import cv2
import AdditionalFunctions
'''
* This function is to return all the detection of the players for the first
* frame only so we can apply Kmeans and fetch the teams' jersey color
* @param  image-  the directory of the input video
* @param  contours- the contours which is obtained from the detection for the (x,y,h,w)
* @return           the image containing the bounded rectangles of each player and their coordinates  
'''

def findingContours(image, contours):
    idx = 0
    boxes = []
    keptBoxes = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        # Detect players
        if(h >= (1.2)*w):
            if (h > 60 or h < 20 or w < 8 or w > 30):
                continue
            # print('in',h,w)
            cv2.rectangle(image, (x-5, y-10), (x+w+5, y+h+5), (255, 255, 255), 3)
            boxes.append([x-5, y-10, int(w+5), int(h+5)])
            keptBoxes.append(idx)
            idx = idx+1
    # print('Found players:', idx)

    return image, boxes, keptBoxes

'''
* This function is modified to find boxes more accurately using each team jerseys' colors
* @param  image  the frame input to be used to detect players
* @param  contours   the contours which is obtained from the detection for the (x,y,h,w)
* @return            the image containing the bounded rectangles of each player and their coordinates  
'''

def findingContoursWithJersey(image, contours, clr1, clr2):
    idx = 0
    clr1 = np.array(clr1)
    clr2 = np.array(clr2)
    boxes = []
    keptBoxes = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)

    # Detect players
        if(h >= (1.2)*w):
            if (h > 60 or h < 20 or w < 8 or w > 30):
                continue
            player_img = image[y:y+h, x:x+w]
            # plt.imshow(player_img)
            player_hsv = cv2.cvtColor(player_img, cv2.COLOR_BGR2HSV)
            # If player has clr1 jersy
            # print(clr1[0])
            mask1 = cv2.inRange(player_hsv, clr1[0], clr1[1])
            res1 = cv2.bitwise_and(player_img, player_img, mask=mask1)
            res1 = cv2.cvtColor(res1, cv2.COLOR_HSV2BGR)
            res1 = cv2.cvtColor(res1, cv2.COLOR_BGR2GRAY)
            nzCount = cv2.countNonZero(res1)

            # If player has clr2 jersy
            mask2 = cv2.inRange(player_hsv, clr2[0], clr2[1])
            res2 = cv2.bitwise_and(player_img, player_img, mask=mask2)
            res2 = cv2.cvtColor(res2, cv2.COLOR_HSV2BGR)
            res2 = cv2.cvtColor(res2, cv2.COLOR_BGR2GRAY)
            nzCountred = cv2.countNonZero(res2)
            
            if(nzCount >= 20 ):
                # Mark clr1 jersy players as france
             #   cv2.rectangle(image, (x-5, y-10), (x+w+5, y+h+5), (255, 0, 0), 2)
                boxes.append([x-5, y-10, int(w+5), int(h+5)])
                keptBoxes.append(idx)
                idx = idx+1
                # print('detected player counters',nzCount,nzCountred)
            else:
                pass

            if(nzCountred >= 20):
                # Mark clr1 jersy players as france
             #   cv2.rectangle(image, (x-5, y-10), (x+w+5, y+h+5), (0, 255, 255), 2)
                boxes.append([x-5, y-10, int(w+5), int(h+5)])
                keptBoxes.append(idx)
                idx = idx+1
                # print('detected player counters',nzCount,nzCountred)
            else:
                pass
            
    # print('Found players with jersey:', idx)

    return image, boxes, keptBoxes


'''
    'black': [[0, 0, 0],    [180, 255, 30]],
    'gray':  [[0, 0, 30],	[180, 25, 190]],
    'white': [[0, 0, 190],  [180, 25, 255]],
    'red1':  [[159, 25, 70], [180, 255, 255]],
    'red2':  [[0, 25, 70],  [10, 255, 255]],
    'orange': [[10, 25, 70], [25, 255, 255]],
    'yellow': [[25, 25, 70], [35, 255, 255]],
    'green': [[35, 25, 70], [90, 255, 255]],
    'blue':  [[90, 25, 70], [129, 255, 255]],
    'purple': [[129, 25, 70], [159, 255, 255]]
'''


'''
* This function is used to detect players using image processing to detect players
* @param  image  the frame input to be used to detect players
* @param  clr1   the first color for detecting players with jerseys color
* @param  clr2   the second color for detecting players with jerseys color
* @return           the image containing the bounded rectangles of each player and their coordinates  
'''
def playersDetectionIP(image1, clr1=None, clr2=None):

    image = image1.copy()
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # green range for FootballField
    lowerGreen = np.array([40, 40, 40])
    upperGreen = np.array([70, 255, 255])

    # Define a mask ranging from lower to uppper
    mask = cv2.inRange(hsv, lowerGreen, upperGreen)

    # Do masking
    res = cv2.bitwise_and(image, image, mask=mask)

    # convert to hsv to gray
    resGray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)
    # Defining a kernel to do morphological operation in threshold #image to get better output.
    # Removing back audiences

    kernel = np.ones((5, 5), np.uint8)
    thresh1 = cv2.threshold(
        resGray, 127, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    thresh = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)

    erosion = cv2.erode(thresh, (10, 10), iterations=10)
    dilate = cv2.dilate(erosion, (20, 20), iterations=20)
    # Finding contours and drawing bounded Rectangles
    edged = cv2.Canny(dilate, 30, 200)

    contours, _ = cv2.findContours(
        edged, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    if((clr1 is not None) or (clr2 is not None)):
        img, boxes, keptBoxes = findingContoursWithJersey(
            image, contours, AdditionalFunctions.color_dict_HSV[clr1], AdditionalFunctions.color_dict_HSV[clr2])
    else:
        img, boxes, keptBoxes = findingContours(image, contours)

    # cv2.imwrite('teamOut.jpg', img)
    # cv2.imwrite('WB_removed.jpg', erosion)
    # cv2.imwrite('WB1_removed.jpg', dilate)

    return img, boxes, keptBoxes

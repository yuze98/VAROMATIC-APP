import numpy as np
import cv2

'''
This is the dictionary of the lower and upper bounds of HSVs
'''

color_dict_HSV = {  
        'black': [[0, 0, 0],    [180, 255, 30]],
        'gray':  [[0, 0, 30],    [180, 25, 190]],
        'white': [[0, 0, 190],  [180, 25, 255]],
        'red1':  [[159, 25, 70],[180, 255, 255]],
        'red2':  [[0, 25, 70],  [10, 255, 255]],
        'orange':[[10, 25, 70], [25, 255, 255]],
        'yellow':[[25, 25, 70], [35, 255, 255]],
        'green': [[35, 25, 70], [90, 255, 255]],
        'blue':  [[90, 25, 70], [129, 255, 255]],
        'purple':[[129, 25, 70],[159, 255, 255]]
        }
#white range
lower_white = np.array([0,0,0])
upper_white = np.array([0,0,255])

'''
* This function just computes the mean to be used for line intersection averaging
* @param  arrpoints  the points to be processed
* @return           the averaged points of intersection vanishing point 
'''
def pointMean(arrPoints):
    sumX=0
    sumY=0
    for x,y in arrPoints:
        sumX += x
        sumY += y
    arrLength = len(arrPoints)
    return (sumX/arrLength,sumY/arrLength)
# Making a list of possible vp intersection


'''
* This function is to get all the possible list of vp 
* @param  neededpoints  points to be made into a list to obtain the average 
* @return           the final vanishing point after averaging
'''
def gettingMeanVP(neededpoints):
    possibleVPs=[]
    for i in range(len(neededpoints)):
        for j in range(len(neededpoints)):
            if(j+1!=len(neededpoints)):
                intersected = line_intersection(neededpoints[i], neededpoints[j+1])
                # if intersection got (0,0) then there are no intersection happend don't append it.
                if(intersected[0]!=0 and intersected[1]!=0):
                    possibleVPs.append(line_intersection(neededpoints[i], neededpoints[j+1]))
    
    xv, yv = pointMean(possibleVPs)
    
    return xv,yv

'''
* This function is to show the final result as an image viewing video 
* @param  frame  the frame input to be used to detect players
* @param  decision   the final decision to be printed on the image
* @param  imgToShow   the image to be shown in the imshow function
* @return           the final output shown with the results and the boundry lines of each player 
'''
def PrintFinalVisuals(frame, ind, decision,imgToShow):
    cv2.putText(img=frame, text='Offside Decision: '+str(decision), org=(540, 520),
                fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=1, color=(100, 30, 100), thickness=1)
    # cv2.imwrite("Final_OutPut/outputFrame"+str(ind)+".jpg", frame)
    cv2.imshow("Frame", imgToShow)
    return
'''
* This function is used to get the intersection of both line if exists 
* @param  line1,line2  the 2 lines for intersection checking
* @return           the point of intersection if exists
'''
def line_intersection(line1, line2):
    xdiff = (line1[0][0] - line1[1][0], line2[0][0] - line2[1][0])
    ydiff = (line1[0][1] - line1[1][1], line2[0][1] - line2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    # if (0,0) came then no intersection happend
    if div == 0:
        return (0,0)

    d = (det(*line1), det(*line2))
    x = det(d, xdiff) / div
    y = det(d, ydiff) / div
    return x, y

'''
* This function is used to get the slope 
* @param  x1,y1,x2,y2  the points of the 2 lines to get the slope of 
* @return           the slope od the line 
'''
def slopee(x1, y1, x2, y2):
    x = (y2 - y1) / (x2 - x1)
    return x

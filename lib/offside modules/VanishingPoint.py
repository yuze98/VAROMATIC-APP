import cv2
from AdditionalFunctions import slopee, line_intersection
import numpy as np
'''
* This function is used to get the vanishing point 
* @param  img  the image to get the vanishing point from
* @return           the final processed vanishing point
'''

def vanishingPoint(img):

    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    bilarImg = cv2.bilateralFilter(gray, 7, 7, 7)
    image_enhanced = cv2.equalizeHist(bilarImg)
    masked_edges = cv2.Canny(image_enhanced, 100, 100, apertureSize=3)

    # Define the Hough transform parameters
    # Make a blank the same size as our image to draw on
    rho = 2  # distance resolution in pixels of the Hough grid
    theta = np.pi/180  # angular resolution in radians of the Hough grid
    # minimum number of votes (intersections in Hough grid cell)
    threshold = 110
    min_line_length = 90  # minimum number of pixels making up a line
    max_line_gap = 20   # maximum gap in pixels between connectable line segments
    # Run Hough on edge detected image
    lines = cv2.HoughLinesP(masked_edges, rho, theta, threshold, np.array([]),
                            min_line_length, max_line_gap)
    # Iterate over the output "lines" and draw lines on the blank
    # draw line which makes a slope rather than the redundent horizontal lines
    line_image = np.copy(img) #creating a blank to draw lines on

    neededpoints = []
    for line in lines:
            for x1, y1, x2, y2 in line:
                slp = slopee(x1, y1, x2, y2)
                # slp>10 or slp<-7
                # print('slp:',slp)
                if slp >= 1 or slp <= -1 or slp == float('-inf') or slp == float('inf'):
                    neededpoints.append([[x1, y1], [x2, y2]])
                    cv2.line(line_image,(x1,y1),(x2,y2),(255,255,255),2)
    
    # We have to sort them by the x point ascendingly order
    neededpoints.sort(key=lambda i:i[0],reverse=False)
    # Getting the possible vanishing point by having the intersection of the first and last line
    possibleVP = line_intersection(neededpoints[0],neededpoints[len(neededpoints)-1])  
    if(possibleVP == (0,0)):
        raise Exception('No intersection!')
    else:
        xv,yv = possibleVP
    # print('what are they???',neededpoints[0],neededpoints[len(neededpoints)-1])
    return int(xv), int(yv)


'''
* This function is used to draw a line from the vanishing point to the player 
* @param  p  the co-ordinate of the player
* @param  img  the image for drawing the line on
* @param  vp  the vanishing point to form the line
* @param  clr  the color of the line
* @return           an image with the line drawn on and the slope of the player's line
'''
def drawLine(p, img, vp, clr=(255, 255, 255)):
    # drawing a line from the vanishing point to the player coordinate
    if clr == (255, 255, 255):
        return slopee(p[0],p[1], vp[0],vp[1])
    cv2.line(img, (p), (vp), clr, 2)

    return slopee(p[0],p[1], vp[0],vp[1])

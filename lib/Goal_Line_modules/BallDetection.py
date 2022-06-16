import cv2
import numpy as np
'''
* @param  image                 the frame to be processed
* @param  count                 count of current frame
* @return                       a tuple that contains (ball center x-coordinate, ball center y-coordinate, ball radius)
* @Note: prints all frames detected in a file called img
'''

def ballDetector(image, count):
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(17,17),0) 
    newim = image.copy()
    # cv2.imwrite("img\image" + str(count+100) +".jpg",blur)
    circles = cv2.HoughCircles(blur,
                            cv2.HOUGH_GRADIENT,
                            minDist=100,
                            dp=1.2,
                            param1=120, #sensitivity, high won't find enough circles, low too many
                            param2=20, #accuracy, no of edges needed, high not enough, low too many
                            minRadius=1,
                            maxRadius=40)
    if circles is not None:
        circles = np.round(circles[0, :].astype("int"))
        for (x,y,r) in circles:
            #if y > 50 and y < 450 and image[y,x][0] > 200 and image[y,x][1] > 200 and image[y,x][2] > 200: #TO AVOID STANDS AND HUD AND DIFFERENTLY COLORED BALLS
            # print("look here pls", image[y,x])
            cv2.circle(newim,(x,y),r,(0,255,255),2)
            return (x,y,r),newim
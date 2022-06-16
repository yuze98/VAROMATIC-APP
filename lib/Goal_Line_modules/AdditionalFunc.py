import cv2


import cv2
'''
* This function is to show the final result as an image viewing video 
* @param  frame  the frame input to be used to detect players
* @param  decision   the final decision to be printed on the image
* @param  imgToShow   the image to be shown in the imshow function
* @param  res  the resolution of the final output
* @return           the final output shown with the results and the boundry lines of each player 
'''
def PrintFinalVisuals(frame, ind, decision,imgToShow,res):
    cv2.putText(img=frame, text='Goal Decision: '+str(decision), org=(300, 1800),
                fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=2, color=(0, 0, 0), thickness=1)
    # cv2.imwrite("Final_OutPut/outputFrame"+str(ind)+".jpg", frame)
    imgToShow_reized = cv2.resize(imgToShow, res)                    # Resize image
    # prev = time.time()
    cv2.imshow("Frame", imgToShow_reized)
    # print(time.time()-prev)

    return
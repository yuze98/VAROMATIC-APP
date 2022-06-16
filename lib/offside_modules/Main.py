import cv2
import time
from OffsideProcess import *
from PlayerDetectionYOLO import loadYolo

'''
* This is the testing phase runining the process LIVE
# # Folders to print in: 
# # img,ball_img,img_class,Final_OutPut
'''
def mainProcess(isYolo,fileName):
    clip = cv2.VideoCapture("assets/"+fileName+".mp4")
    index = 0
    col1=None
    col2=None
    prevFrame = None
    direction = 'right'
    frame_rate = 30 #current frame rate of the video is 30 
    prev = 0
    vp = None
    model = None
    outputLayers = None
    if isYolo:
        model, outputLayers = loadYolo("D:/UNI STUFF/Fourth year comp/sem 2/GGP/VAROMATIC-APP/assets/yolov3.cfg", "D:/UNI STUFF/Fourth year comp/sem 2/GGP/VAROMATIC-APP/assets/yolov3.weights")
    while True:
        time_elapsed = time.time() - prev
        res, frame = clip.read()

        if frame is None:
            break 
        
        if time_elapsed > 1./frame_rate:
            prev = time.time()
            try:
                col1,col2, vp = processing(frame, index, prevFrame, col1, col2, vp, direction, model, outputLayers, isYolo)
            except Exception:
                pass
            index += 1
            prevFrame = frame
            k = cv2.waitKey(30) & 0xff
            # print(time_elapsed,1./frame_rate)
            if k == 27: # this is the escape button
                break
        
    clip.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)

# mainProcess(False)
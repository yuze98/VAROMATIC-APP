import cv2
import time
from OffsideProcess import *
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot

import numpy as np

'''
* This is the testing phase runining the process LIVE
# # Folders to print in: 
# # img,ball_img,img_class,Final_OutPut
'''
# class OffsideDetection(QThread):
#     change_pixmap_signal = pyqtSignal(np.ndarray)

def mainProcess(self):
    clip = cv2.VideoCapture("assets/new1.mp4")
    index = 0
    col1=None
    col2=None
    prevFrame = None
    direction = 'right'
    frame_rate = 30 #current frame rate of the video is 30 
    prev = 0
    vp = None
    while True:
        time_elapsed = time.time() - prev
        res, frame = clip.read()

        if frame is None:
            break 
        
        if time_elapsed > 1./frame_rate:
            prev = time.time()
            try:
                col1,col2, vp,finaloutput = processing(frame,index,prevFrame,col1,col2,vp,direction)
                self.change_pixmap_signal.emit(finaloutput)

            except Exception:
                # print('entered here')
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

# mainProcess()
import cv2
import time
from GoalDecision import goalDetection
from BallDetection import ballDetector
from PostDetection import goalPostDetection
from AdditionalFunc import PrintFinalVisuals
'''
* Here we run the program using video capture for streaming the video with each frame
* in order to test it by useing goal post detection and using the ball detector
* then we use the goal detection algorithm to extracct the output
'''

def GoalLineProcess():
    clip = cv2.VideoCapture("assets/rec.mp4")
    index = 0
    frame_rate = 20  # current frame rate of the video is 30
    prev = 0
    while True:
        time_elapsed = time.time() - prev
        res, frame = clip.read()

        if frame is None:
            break

        if time_elapsed > 1./frame_rate:
            prev = time.time()
            try:
                goalPostX = goalPostDetection(frame, 3, 80, 5)
                # preve = time.time()

                ballProperties, img = ballDetector(frame, index)
                # print(time.time()-preve)

                decision = (goalDetection(goalPostX, ballProperties))
                PrintFinalVisuals(img, index, decision, img, res=(600, 760))
            except Exception:
                pass

            index += 1
            k = cv2.waitKey(30) & 0xff
            # print(time_elapsed,1./frame_rate)
            if k == 27:  # this is the escape button
                break

    clip.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)

# GoalLineProcess()
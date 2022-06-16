
import cv2

'''
* @param  frame                 the frame to be processed
* @param  confirmationSteps     number of steps for confirming the thickness of the goal post
* @param  postInclinationFactor a factor to handle the goal post inclination in the frame (if there is)
* @param  framePartition        the part of the frame in terms of rows at which the goal post is located
* @return                       the inner x-coordinate of the goal post
'''

def goalPostDetection(frame, confirmationSteps, postInclinationFactor, framePartition):
    firstWhitePixelPosition = []
    lengthVote = []
    voteWithMaxLength = 0
    # outputFrame = frame.copy()
    frameGray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frameEdge = cv2.Canny(frameGray, 250, 255, apertureSize = 3)
    modifiedFrame = cv2.erode(frameEdge, (3, 3))
    for i in range(confirmationSteps):
        whitePixelCounterVote = 0
        for j in range (modifiedFrame.shape[1]):
            if (modifiedFrame[int(modifiedFrame.shape[0] / framePartition), (j + i)] == 255):
                whitePixelCounterVote = whitePixelCounterVote + 1
                if (whitePixelCounterVote == 1):
                    firstWhitePixelPosition.append(j)
                if (whitePixelCounterVote == 3):
                    lengthVote.append(j - firstWhitePixelPosition[i])
                    break
    voteWithMaxLength = lengthVote.index(max(lengthVote))
    # cv2.line(outputFrame, (firstWhitePixelPosition[voteWithMaxLength] - postInclinationFactor, int(modifiedFrame.shape[0] / framePartition)), (firstWhitePixelPosition[voteWithMaxLength] + lengthVote[voteWithMaxLength] - postInclinationFactor, int(modifiedFrame.shape[0] / framePartition)), (0, 255, 0), 2, cv2.LINE_4)
    # cv2.imwrite("goalPost.jpg", outputFrame)
    return (firstWhitePixelPosition[voteWithMaxLength] + lengthVote[voteWithMaxLength] - postInclinationFactor)
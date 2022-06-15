import imp
from PlayerDetectionIP import playersDetectionIP
from ColorExtraction import KmeansImage
from VanishingPoint import vanishingPoint
from TeamClassification import teamsClassification
from OffsideDecisionMaker import offsideDecision
from AdditionalFunctions import PrintFinalVisuals
'''
* This function processes everything in one iteration to find the offside and call all the functions
* @param  frame  the frame to be processed
* @param  index  the index of the current frame loop
* @param  prevFrame  the previoud frame to be used in the direction
* @param  col1,col2  the first and second color of each team
* @param  vp  the vanishing point of the football field
* @param  direction  the direction of the play
* @return           a processed frame of the final result video
'''
def processing(frame,index,prevFrame,col1,col2,vp,direction):

    if index == 0:
        img, allBoxes, keptBoxes = playersDetectionIP(frame)
    else:
        img, allBoxes, keptBoxes = playersDetectionIP(frame, col1, col2)
        # direction = AttackDirection(prevFrame,frame,index)
        # cv2.imwrite('img/teamOut'+str(index)+'.jpg', img)

    if index == 0:
        # print(index)
        col1, col2, keptBoxes = KmeansImage(frame, allBoxes, keptBoxes)
        # print("hi ", col1, col2)
        vp = vanishingPoint(frame)
        # cv2.imshow("image", img)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()

    # cv2.imshow("image", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imwrite('pdimg/teamOut'+str(c)+'.jpg',img)
    # print(allBoxes)
    # print(keptBoxes)
    # previ = time.time()
    boxes,outputFrame = teamsClassification(frame, allBoxes, keptBoxes, [col1, col2])
    # cv2.imwrite('img_class/classification'+str(index)+'.jpg', outputFrame)
    # print('pllayer det time:',previ - time.time())   

    decision = offsideDecision(direction, frame, boxes, vp)
    PrintFinalVisuals(frame, index, decision,imgToShow=frame)

    return col1, col2, vp


import numpy as np
import cv2
from VanishingPoint import drawLine

'''
* This function is used to find the final decision of the offside
* @param  dir  the direction of the attacker team 
* @param  frame  the frame to find the final decision of
* @param  finalboxes  the boxes to find which team box assigned to by the clf
* @param  vp  the vanishing point of the frame
* @return           the decision of the offside
'''
def offsideDecision(dir,frame,finalboxes,vp):

    red,white = detectLast2P(frame,finalboxes,vp,dir)
    xL0 = red[0]
    yL0 = red[1]
    xL1 = white[0]
    yL1 = white[1]
    slp0 = drawLine((xL0,yL0),frame,vp,(0,0,255))
    slp1 = drawLine((xL1,yL1),frame,vp,(0,255,255))
    if(dir == 'left'):
        decision = comparatorL(xL0,yL0,slp0,xL1,yL1,slp1)
    else:
        decision = comparatorR(xL0,yL0,slp0,xL1,yL1,slp1)
        
    return decision
        

def comparatorL(x0, y0, m0, x1, y1, m1):
    c0 = y0 - m0 * x0
    y2 = m0 * x1 + c0
    if(y1 < y2):  #If team 1 passed team 0 and team 0's goal is left -> offside
        return True
    else:
        return False

def comparatorR(x0, y0, m0, x1, y1, m1):
    c1 = y1 - m1 * x1
    y2 = m1 * x0 + c1
    if(y2 > y0):  #If team 1 passed team 0 and team 0's goal is left -> offside
        return True
    else:
        return False


'''
* This function is used to find the last 2 opponent players in the field
* @param  frame  the frame to be processed 
* @param  finalboxes  the boxes with each player's assigned team
* @param  vp  the vanishing point to form the line
* @param  dir  the direction of the attacking team
* @return           the 2 players' boxes coordinates
'''
def detectLast2P(frame,finalboxes,vp,dir):

     # print("\n\n","******************************************NEXT FRAME******************************************")
     outputFrame = frame.copy()
     redBox = []
     # print("\n")
     # print("Vanishing point is ",vp)


     newBox =[x for x in finalboxes if len(x)==5]

     # print(newBox)
     for box in newBox:
          if(box[4] == 1):
           redBox.append(box)

     # print(redBox)
     # print("Red box is ",redBox)

     whiteBox = [white for white in newBox if white not in redBox]

     if dir == "left":
          rightRed=min([sublist for sublist in redBox])
     else:
          rightRed=max([sublist for sublist in redBox])
          # print("Decision red is ",dir)

     # print(rightRed)

     topLeftXR = rightRed[0]
     topLeftYR = rightRed[1]
     widthR = rightRed[2]
     heightR = rightRed[3]
     curMinR = (int(topLeftXR+widthR/2), int(topLeftYR+heightR/2))

     

     slp0 = drawLine(curMinR,frame,vp)
     cv2.rectangle(outputFrame, (topLeftXR, topLeftYR), (topLeftXR + widthR, topLeftYR + heightR), (0,0,255), 2)
#     #  show_images([outputFrame])
     # cv2.imwrite("last2pLredold.jpg", outputFrame)
     # print("Old red player is",rightRed)
     # print("Slope red is",slp0)
     # print(redBox)
     for players in redBox:
          if players == rightRed:
               continue
          LeftXR = players[0]
          LeftYR = players[1]
          width  = players[2]
          height = players[3]
          newRedX = int(LeftXR + width / 2) 
          newRedY = int(LeftYR + height / 2) 
          if dir == "left":
               decision = comparatorL(curMinR[0],curMinR[1],slp0,newRedX,newRedY,0)
          else:
               decision = comparatorR(newRedX,newRedY,0,curMinR[0],curMinR[1],slp0)

          if decision:
               # print("New red player is",players)
               topLeftXR = LeftXR
               topLeftYR = LeftYR
               widthR    = width
               heightR   = height
               curMinR    = (int(topLeftXR + widthR / 2), int(topLeftYR + heightR / 2)) # Red player 
               slp0 = drawLine(curMinR,frame,vp)


     # print("FINAL RED: ",[ topLeftXR,topLeftYR,widthR,heightR])

               # break
     # print("\n**************************************************************************\n")
     
     # print("White box is ",whiteBox)

     if dir == "left":
          rightWhite=min([sublist for sublist in whiteBox])
     else:
          rightWhite=max([sublist for sublist in whiteBox])
          # print("Decision white is ",dir)



     topLeftXW = rightWhite[0]
     topLeftYW = rightWhite[1]
     widthW = rightWhite[2]
     heightW = rightWhite[3]
     curMinW=(int(topLeftXW+widthW/2),int(topLeftYW+heightW/2))
     # print(rightWhite)
     slp1 = drawLine(curMinW,frame,vp)
     # cv2.rectangle(outputFrame, (topLeftXW, topLeftYW), (topLeftXW + widthW, topLeftYW + heightW), (255,255,255), 2)
     # cv2.imwrite("last2pLwhiteold.jpg", outputFrame)
     # print("Old yellow player is",rightWhite)
     # print("Slope yellow is",slp1)

     for players in whiteBox:
          if players == rightWhite:
               continue
          LeftXW = players[0]
          LeftYW = players[1]
          width  = players[2]
          height = players[3]
          newWhiteX = int(LeftXW+width/2) 
          newWhiteY = int(LeftYW+height/2) 
          if dir == "left":
               decision = comparatorL(curMinW[0],curMinW[1],slp1,newWhiteX,newWhiteY,0)
          else:
               decision = comparatorR(newWhiteX,newWhiteY,0,curMinW[0],curMinW[1],slp1)


          if decision:
               # print("New yellow player is",players)
               topLeftXW = LeftXW
               topLeftYW = LeftYW
               widthW    = width
               heightW   = height
               curMinW   = (int(topLeftXW+widthW/2),int(topLeftYW+heightW/2)) # white player 
               slp1 = drawLine(curMinW,frame,vp)

               # break
     # print("FINAL YELLOW: ",[ topLeftXW,topLeftYW,widthW,heightW])

     cv2.rectangle(outputFrame, (topLeftXW, topLeftYW), (topLeftXW + widthW, topLeftYW + heightW), (0,255,255), 2)

    #  show_images([outputFrame])
     # cv2.imwrite("last2pL.jpg", outputFrame)

     return curMinR,curMinW
     



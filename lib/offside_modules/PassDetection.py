from BallDetector import ballDetector
'''
* This function is used to find the attacking direction by finding the ball direction of play
* @param  firstFrame  the previous frame to fetch the ball's location
* @param  secondFrame  the current frame to fetch the ball's location
* @return           the direction of the play
'''
def AttackDirection(firstFrame,secondFrame,it):
    # track ball from prev frame 
    x_f,_,_ = ballDetector(firstFrame,it,1)
    x_s,_,_ = ballDetector(secondFrame,it+1,1)
    if(x_f <x_s):
        direction='right'
    else:
        direction = 'left'
    return direction

    # Takes the boxes[index] of the passer, reciever and checks if they are same team 0 and 0 or 1 and 1
'''
* This function is used to find if the passer and the reciever of the ball are same team or not
* @param  passer  the passer's team number
* @param  reciever  the reciever's team number
* @return           if both are in the same team or not
'''
def SameTeamChecker(passer,reciever):
    if(passer == reciever):
        return True  
    return False
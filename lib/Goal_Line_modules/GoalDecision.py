'''
* @param  goalPostX      the inner x-coordinate of the goal post
* @param  ballProperties a tuple that contains (ball center x-coordinate, ball center y-coordinate, ball radius)
* @return                true if there is a goal and false otherwise
'''

def goalDetection(goalPostX, ballProperties):
    if ((ballProperties[0] - ballProperties[2]) > goalPostX):
        return True
    else:
        return False
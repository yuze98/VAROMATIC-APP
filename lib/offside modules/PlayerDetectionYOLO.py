import numpy as np
import cv2

'''
* @param  configPath  the path to the yolo configuration file
* @param  weightsPath the path to the yolo weights file
* @return             the yolo model
* @return             the output layers of the yolo model
'''

def loadYolo(configPath, weightsPath):
    model = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
    allLayers = model.getLayerNames()
    outputLayers = [allLayers[layer - 1] for layer in model.getUnconnectedOutLayers()]
    return model, outputLayers


'''
* @param  frame        the frame to be processed
* @param  model        the yolo model
* @param  outputLayers the output layers of the yolo model
* @param  confidence   the confidence hyper-parameter of yolo (from 0 to 1)
* @return              the properties of all bounding boxes of detected players
* @return              the properties of the remaining bounding boxes of detected players after non-maxima suppression
'''

def playersDetection(frame, model, outputLayers, confidence):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]
    preprocessedFrame = cv2.dnn.blobFromImage(frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    model.setInput(preprocessedFrame)
    layersOutputs = model.forward(outputLayers)
    boxes = []
    predictedClassProbabilities = []
    predictedClassIds = []
    for output in layersOutputs:
        for detection in output:
            probabilities = detection[5:]
            predictedClassId = np.argmax(probabilities)
            predictedClassProbability = probabilities[predictedClassId]
            if ((predictedClassProbability > confidence) and (predictedClassId == 0)):
                boxProperties = np.multiply(np.array(detection[:4]), np.array([frameWidth, frameHeight, frameWidth, frameHeight]))
                (centerX, centerY, width, height) = boxProperties.astype("int")
                topLeftX = int(centerX - (width / 2))
                topLeftY = int(centerY - (height / 2))
                boxes.append([topLeftX, topLeftY, int(width), int(height)])
                predictedClassProbabilities.append(float(predictedClassProbability))
                predictedClassIds.append(predictedClassId)
    keptBoxes = cv2.dnn.NMSBoxes(boxes, predictedClassProbabilities, confidence, 0.3)
    # for i in keptBoxes:
    #     (topLeftX, topLeftY, width, height) = (boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3])
    return boxes, keptBoxes
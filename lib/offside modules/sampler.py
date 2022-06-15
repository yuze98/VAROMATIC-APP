import cv2
'''
* @param  videoPath  the directory of the input video
* @param  skipRate   the rate at which frames are skipped
* @return            the frames of the input video with a skip of <skipRate> frames between each two original frames
'''

#TODO: Adapt clip to capture from live streams

def sampler(videoPath, skipRate):
  clip = cv2.VideoCapture(videoPath)
  framesCount = clip.get(cv2.CAP_PROP_FRAME_COUNT)
  outputFrames = []
  if (not clip.isOpened()): 
    print("Video could not be opened!")
  else:
    for i in range(0, int(framesCount), skipRate):
      clip.set(cv2.CAP_PROP_POS_FRAMES, i)
      isRead, frame = clip.read()
      if (isRead):
        outputFrames.append(frame)
  return outputFrames
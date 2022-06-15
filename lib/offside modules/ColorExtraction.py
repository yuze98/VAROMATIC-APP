import numpy as np
import cv2
import time
from AdditionalFunctions import color_dict_HSV
from sklearn.cluster import KMeans

'''
* This function is responsible for obtaining a histogram for the 
  image that has K-Means clustering applied to it
* @param  clt  Number of clusters
* @return     A histogram based on no. of pixels associated to each cluster
'''


def centroid_histogram(clt):
	# grab the number of different clusters and create a histogram
	# based on the number of pixels assigned to each cluster
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)
	# normalize the histogram, such that it sums to one
	hist = hist.astype("float")
	hist /= hist.sum()
	# return the histogram
	return hist


'''
* The function gives a better visualization of the color output of Kmeans clustering
* @param  hist  histogram of clusters 
* @param  centroids the centers of the KMeans clusters
* @returns bar plot containing k colors in the image
'''

def plot_colors(hist, centroids):
	# initialize the bar chart representing the relative frequency
	# of each of the colors
	bar = np.zeros((50, 300, 3), dtype = "uint8")
	startX = 0
	# loop over the percentage of each cluster and the color of
	# each cluster
	for (percent, color) in zip(hist, centroids):
		# plot the relative percentage of each cluster
		# print("Color Array: ",color)
		# print("Percents is ", percent)

		endX = startX + (percent * 300)
		cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
			color.astype("uint8").tolist(), -1)
		startX = endX
		C = None
		
		for colors in color_dict_HSV:
			lower = color_dict_HSV[colors][0]
			upper = color_dict_HSV[colors][1]
			
			if (lower[0] < color[0] < upper[0] and
			lower[1]<color[1]<upper[1] and
			lower[2]<color[2]<upper[2]):
				# print("Lower bound is",lower)
				# print("Upper bound is",upper)
				# print("\n")
				C = colors

		# C = color
		# print("Color is ", C,"\n")
	# return the bar chart
	return bar



'''
* @param  hist  histogram of clusters and then create a figure
* @param  centroids the centers of the KMeans clusters
* @return the voted color of the player given the color ranges in HSV
'''
def vote_colors(hist,centroids):
	Colors = []
	Percents = []
	for (percent, color) in zip(hist, centroids):
		Colors.append(color)
		Percents.append(percent)
	if len(Percents) == 0:
		return None
	max_value = max(Percents)
	max_index = Percents.index(max_value)
	# print("Percent list is ",Percents)
	# print("Colors list is ",Colors)

	Percents.remove(max_value)
	Colors.pop(max_index)
	# print("New Percent list is ",Percents)
	# print("New Colors list is ",Colors)
	# if (len(Percents) == 0):
	# 	return None
	max_value = max(Percents)
	max_index = Percents.index(max_value)
	max_color = Colors.pop(max_index)
	C = None
	for colors in color_dict_HSV:
			lower = color_dict_HSV[colors][0]
			upper = color_dict_HSV[colors][1]
			
			if (lower[0] < max_color[0] < upper[0] and
			lower[1] < max_color[1] < upper[1] and
			lower[2] < max_color[2] < upper[2]):
				C = colors
	# print("Max color is ",C)
	return C



'''
* This function is responsible for obtaining each player's box and performing K-Means clustering 
* @param  image  the individual player box to be applied with K-Means
* @return             the voted color of the player's team color
'''

def KmeansPlayer(image):
	
    # cluster the pixel intensities
    # reshape the image to be a list of pixels
	image = image.reshape((image.shape[0] * image.shape[1], 3))
	
	clt = KMeans(n_clusters = 3)
	clt.fit(image)

    # build a histogram of clusters and then create a figure
    # representing the number of pixels labeled to each color
	hist = centroid_histogram(clt)

	# bar = plot_colors(hist, clt.cluster_centers_)

	player_color = vote_colors(hist,clt.cluster_centers_) #Votes individual player's color
    # show our color bart
	# plt.figure()
	# plt.axis("off")
	# plt.imshow(bar)
	# plt.show()
	return player_color
 

'''
* This function is used to get the colors of each team using the first frame
* @param  frame1  the frame to be processed 
* @param  boxes  the boxes containing each player's coorindates 
* @param  keptBoxes  the indicies of each player
* @return           the color of each team and the players box indicies
'''
def KmeansImage(frame1, boxes,keptBoxes):
	frame = frame1.copy()
	frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	PlayerColors = []
	removed = []
	for i in keptBoxes:
		(topLeftX, topLeftY, width, height) = (boxes[i][0], boxes[i][1], boxes[i][2], boxes[i][3])
		kMeansStart = time.time()
		
		
		player_color = KmeansPlayer(frame[topLeftY:topLeftY+int(height),topLeftX:topLeftX+width])
		kMeansEnd = time.time()
		##print("[INFO] kMeansPlayer took {:.6f} seconds".format(kMeansEnd - kMeansStart))

		##print("final player color is", player_color)     
		PlayerColors.append(player_color)

        # KMeansImage(frame[topLeftX:topLeftX+width,topLeftY:topLeftY+height])
	# print("All player colors are: ",PlayerColors)
	# print("hollaa", PlayerColors)
	PlayerColors = list(filter(lambda a: a != "green" and a != None, PlayerColors))
	# print("All player colors are: ",PlayerColors)
	
	team1 =  max(set(PlayerColors), key=PlayerColors.count)
	
	
	# print("Team 1: ",team1)
	PlayerColors = list(filter(lambda a: a != team1 and a != None and a != "green", PlayerColors))
	team2 =  max(set(PlayerColors), key=PlayerColors.count)
	
  
	# [1,2,3,4,5,6,7] === delete 3 ===> [1,2,4,5,6,7]
	# [10,30,50,60,70] ====> []
	# print("Team 2: ",team2)
	return team1,team2,keptBoxes

import colorsys
from PIL import Image
import time
import random
import math
import os


def genAvgRGB(img):
	
	#converting image to rgb
	img = img.convert("RGB")
	
	#getting colors
	colors = img.getcolors(img.size[0] * img.size[1])
	
	#one line average
	avg = tuple([sum([y[1][x] * y[0] for y in colors]) / sum([z[0] for z in colors]) for x in range(3)])
	
	return avg

def genAvgHSV(img):
	
	#converting image to rgb
	img = img.convert("RGB")
	
	#getting colors
	colors = img.getcolors(img.size[0] * img.size[1])
	
	#converting colors to hsv
	colors = [(w,colorsys.rgb_to_hls(*[y / 255. for y in x])) for w,x in colors]
	
	#one line average
	avg = [sum([y[1][x] * y[0] for y in colors]) / sum([z[0] for z in colors]) for x in range(3)]
	
	#converting back to rgb
	avg = colorsys.hsv_to_rgb(*avg)
	avg = tuple([int(x*255) for x in avg])
	
	return avg

def genAvgHue(img):
	
	#getting average hsv
	avgHSV = genAvgHSV(img)
	avgHSV = colorsys.rgb_to_hsv(*[x/255. for x in avgHSV])
	
	#highest value and saturation
	avgHSV = [avgHSV[0], 1.0, 1.0]
	
	avgHSV = colorsys.hsv_to_rgb(*avgHSV)
	
	avgHSV = tuple([int(x * 255) for x in avgHSV])
	
	return avgHSV
	
def kmeans(img):
	img = img.convert("RGB")
	
	#getting colors
	colors = img.getcolors(img.size[0] * img.size[1])
	
	#helping methods
	def genRandColor():
		return (random.randint(0,255), random.randint(0,255), random.randint(0,255))
	
	def calcDist(p1, p2):
		return math.sqrt(sum([(p1[x]-p2[x])**2 for x in range(len(p1))]))
	
	numCenters = 5
	centers = []
	
	#gotta put a check here if number of colors is less than number of centers 
	if len(colors) < numCenters:
		centers = [x for _,x in colors]
		numCenters = len(colors)
	
	
	#choosing random starting centers
	while len(centers) != numCenters:
		randColor = random.choice(colors)[1]
		if randColor not in centers:
			centers.append(randColor)
	
	
	for recalc in range(20):
		
		prevCenters = centers[:]
	
		colorGroups = [[] for x in range(numCenters)]
		
		for color in colors:
			
			#calculate the center with the smallest distance to the color
			minDistIndex = sorted(range(numCenters), key = lambda x: calcDist(centers[x], color[1]))[0]
			
			#appending the color to the group
			colorGroups[minDistIndex].append(color)
			
		
		#calculate new centers - in a one liner for some reason, prolly so its harder for me to understand im the future or something
		centers = [tuple([sum([y[1][x] * y[0] for y in group]) / sum([z[0] for z in group]) for x in range(3)]) for group in colorGroups]
		
			
		#print centers
		
		#calculate center difference
		diff = sum([calcDist(centers[x], prevCenters[x]) for x in range(numCenters)])
		
		#breakoff point
		if diff < 4:
			break
	
	#print [sum([y[0] for y in colorGroups[x]]) for x in range(numCenters)],sorted(range(numCenters), key = lambda x: sum([y[0] for y in colorGroups[x]]))
		
	#getting group with largest number of colors
	return centers[sorted(range(numCenters), key = lambda x: sum([y[0] for y in colorGroups[x]]))[-1]]
		
def getCommon(img):
	
	colors = img.getcolors(img.size[0] * img.size[1])
	
	return sorted(colors)[-1][1]
	

#creates images folder
if not os.path.isdir("images"):
        os.mkdir("images")


	
	
	
#the title of the image
title = "got-s08e03"


#choose what method to get the color
#options: rgb, hsv, hue, kmeans, common
method = "kmeans"

#getting images - images must be number only filenames
images = ["images/"+x for x in os.listdir("images/")]
images.sort(key=lambda x: int(x[7:-4]))


barColors = []

#getting the color for each frame
for img in images:
	print img
	img = Image.open(img).resize((25,25))
	
	#applying correct method
	if method.lower() == "rgb":
		color = genAvgRGB(img)
	elif method.lower() == "hsv":
		color = genAvgHSV(img)
	elif method.lower() == "hue":
		color = genAvgHue(img)
	elif method.lower() == "kmeans":
		color = kmeans(img)
	elif method == "common":
		color = getCommon(img)
	else:
		color = genAvgRGB(img)
		
	barColors.append(color)
	
#creating bar image
barImg = Image.new("RGB",(len(barColors), max([1,int(len(barColors)/2.5)])))

#adding bars to the image
barFullData = [x for x in barColors] * barImg.size[1]
barImg.putdata(barFullData)

#saving image
barImg.save("{}_{}.png".format(title,method))
#barImg.show()


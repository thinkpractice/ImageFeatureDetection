from skimage.io import imread
from skimage import exposure
from skimage import filters
from skimage import feature
from matplotlib import pyplot as plt
import numpy as np
import sys
import math
import os
import glob

def getIntensity(image, weights=[]):
    if not weights:
        weights = [1/3, 1/3, 1/3]
    return np.dot(image, np.array(weights))

def filterImage(image):
    #equalizedImage = exposure.equalize_adapthist(image)
    equalizedImage = exposure.adjust_sigmoid(image)
    #redMinusBlue = np.nan_to_num(equalizedImage[:,:,0] - equalizedImage[:,:,1]) #/ getIntensity(equalizedImage,[1,1,1]))
    #equalizedImage = exposure.equalize_hist(redMinusBlue)
    threshold = filters.threshold_otsu(equalizedImage[:,:,2],35)
    return equalizedImage[:,:,2]  #> threshold

def getAxes(axes, row, column, numberOfImages):
    if numberOfImages <= 2:
        return axes[column]
    else:
        return axes[row, column]

def getFiles(directory, numberOfImages):
    return [os.path.join(directory, filename) for index, filename in enumerate(glob.glob1(directory,"*.png"))  if index < numberOfImages]

def main(argv):
    if len(argv) <= 2:
        print("usage: FilterImages <directory> <numberOfImages>")
        exit(1)
    directory = argv[1]
    numberOfImages = int(argv[2])
    
    filenames = getFiles(directory, numberOfImages)

    numberOfRows = math.ceil(numberOfImages / 2)
    f, axes = plt.subplots(numberOfRows, 4)
    for fileIndex, filename in enumerate(filenames):
        imageRow = fileIndex // 2
        imageColumn = fileIndex % 2 + fileIndex % 2
        image = imread(filename)
        filteredImage = filterImage(image)
        getAxes(axes, imageRow, imageColumn, numberOfImages).imshow(image)
        axes2 = getAxes(axes, imageRow, imageColumn+1, numberOfImages)
        axes2.imshow(filteredImage)
        coordinates = feature.peak_local_max(filteredImage,min_distance=5)
        axes2.plot(coordinates[:,1], coordinates[:,0], 'r.')
    plt.show()

if __name__ == "__main__":
    main(sys.argv)


import sys
import os
import glob
import numpy as np
from skimage.io import imread
import matplotlib.pyplot as plt
from matplotlib.pyplot import hist

def getImagesInDirectory(directory):
    for filename in glob.glob1(directory, "*.png"):
        yield os.path.join(directory, filename)

def plotHistogram(data, title):
    minValue = min(data)
    maxValue = max(data)
    bins = np.linspace(minValue, maxValue, maxValue-minValue+1)
    plt.figure()
    plt.title(title)
    hist(data, bins)
    

def calculateSizeDistribution(directory):
    widths = []
    heights = []
    for filename in getImagesInDirectory(directory):
        image = imread(filename)
        heights.append(image.shape[0])
        widths.append(image.shape[1])
    plotHistogram(widths, "Histogram of image widths")
    plotHistogram(heights, "Histogram of image heights")
    plt.show()

def main(argv):
    if len(argv) <= 1:
        print("usage: CalculateSizeDistributions.py <imageDirectory>")
        exit(0)
    imageDirectory = argv[1]
    calculateSizeDistribution(imageDirectory)

if __name__ == "__main__":
    main(sys.argv)


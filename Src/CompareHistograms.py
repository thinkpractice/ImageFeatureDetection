from skimage.io import imread
from matplotlib import pyplot as plt
from scipy.stats import skew
from scipy.stats import kurtosis
from skimage.measure import shannon_entropy
import sys
import math

def filterImage(image):
    #filter black background color out of the image
    filteredColors = image.reshape(image.shape[0]*image.shape[1], 3)
    flatColorArray = filteredColors[filteredColors[:,:] != (0,0,0)] * 1.0
    return flatColorArray.reshape(len(flatColorArray) // 3, 3)

def plotHistogram(axes, imageComponent, plotColor, binRange):
    return axes.hist(imageComponent, 255, range=binRange, color=plotColor)

def stdHist(bins, n):
    total = n.sum()
    mean = (1/total) * bins * n
    return math.sqrt((1/total) * (n * ((bins - mean) ** 2)).sum())

def getIntensity(image):
    w1 = 1/3
    w2 = 1/3
    w3 = 1/3
    return (w1 * image[:,0]) + (w2 * image[:,1]) + (w3 * image[:,2])

def calc(filteredImage, ax, componentIndex, colors):
    intensityImage = getIntensity(filteredImage)
    if componentIndex == 3:
        n, _, _ = plotHistogram(ax, intensityImage, colors[componentIndex],[0, 255])
    elif componentIndex == 4:
        histogramImage = filteredImage[:,0] - filteredImage[:,2]
        normalizedImage = histogramImage / intensityImage.astype(float)
        n, bins, _ = plotHistogram(ax, normalizedImage, colors[componentIndex],[-1, 1])
        #TODO add skewness for histogram?
        print("skewness={}".format(skew(normalizedImage)))
        #print(skew(n))
        #print(skew(n[n > 0]))
        print("std={}".format(stdHist(bins[0:-1], n)))
        #print(n[n > 0].std())
    elif componentIndex == 5:
        histogramImage = filteredImage[:,1] - filteredImage[:,2]
        n, _, _ = plotHistogram(ax, histogramImage / intensityImage.astype(float), colors[componentIndex],[-1, 1])
    elif componentIndex == 6:
        histogramImage = filteredImage[:,0] - filteredImage[:,1]
        n, _, _ = plotHistogram(ax, histogramImage / intensityImage.astype(float), colors[componentIndex],[-1, 1])
    elif componentIndex == 7:
        histogramImage = filteredImage[:,0] - getIntensity(filteredImage)
        n, _, _ = plotHistogram(ax, histogramImage / intensityImage.astype(float), colors[componentIndex],[-1, 1])

def plotHistograms(axes, image, numberOfImages, fileIndex):
    colors = ["red", "green", "blue", "black", "purple", "black", "orange","black"]
    redMinusBlue = image[:,:,0] - image[:,:,2]
    print("entropy={}".format(shannon_entropy(redMinusBlue)))
    for componentIndex in range(9):
        if numberOfImages == 1:
            ax = axes[componentIndex]
        else:
            ax = axes[fileIndex, componentIndex]
        
        filteredImage = filterImage(image)
        calc(filteredImage, ax, componentIndex, colors)
        if componentIndex == 8:
            ax.imshow(image)
        elif componentIndex < 3:
            histogramImage = filteredImage[:, componentIndex]
            plotHistogram(ax, histogramImage, colors[componentIndex],[0, 255])

def main(argv):
    if len(argv) <= 1:
        print("usage: CompareHistograms <filename1> <filename2> ... <filenamex>")
        exit(1)
    
    numberOfImages = len(argv) - 1
    f, axes = plt.subplots(numberOfImages, 9)
    for fileIndex, filename in enumerate(argv[1:]):
        image = imread(filename)
        plotHistograms(axes, image, numberOfImages, fileIndex)
    plt.show()

if __name__ == "__main__":
    main(sys.argv)

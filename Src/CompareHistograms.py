from skimage.io import imread
from matplotlib import pyplot as plt
from scipy.stats import skew
from scipy.stats import kurtosis
import sys

def filterImage(image):
    #filter black background color out of the image
    filteredColors = image.reshape(image.shape[0]*image.shape[1], 3)
    flatColorArray = filteredColors[filteredColors[:,:] != (0,0,0)] * 1.0
    return flatColorArray.reshape(len(flatColorArray) // 3, 3)

def plotHistogram(axes, imageComponent, plotColor, binRange):
    return axes.hist(imageComponent.ravel(), 255, range=binRange, color=plotColor)

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
        print(normalizedImage)
        n, _, _ = plotHistogram(ax, normalizedImage, colors[componentIndex],[-255, 255])
        print(skew(n))
        print(skew(n[n > 0]))
    elif componentIndex == 5:
        histogramImage = filteredImage[:,1] - filteredImage[:,2]
        n, _, _ = plotHistogram(ax, histogramImage / intensityImage.astype(float), colors[componentIndex],[-255, 255])
    elif componentIndex == 6:
        histogramImage = filteredImage[:,0] - filteredImage[:,1]
        n, _, _ = plotHistogram(ax, histogramImage / intensityImage.astype(float), colors[componentIndex],[-255, 255])

def plotHistograms(axes, image, numberOfImages, fileIndex):
    colors = ["red", "green", "blue", "black", "purple", "black", "orange"]
    for componentIndex in range(8):
        if numberOfImages == 1:
            ax = axes[componentIndex]
        else:
            ax = axes[fileIndex, componentIndex]
        
        filteredImage = filterImage(image)
        calc(filteredImage, ax, componentIndex, colors)
        if componentIndex == 7:
            ax.imshow(image)
        elif componentIndex < 3:
            histogramImage = filteredImage[:, componentIndex]
            plotHistogram(ax, histogramImage, colors[componentIndex],[0, 255])

def main(argv):
    if len(argv) <= 1:
        print("usage: CompareHistograms <filename1> <filename2> ... <filenamex>")
        exit(1)
    
    numberOfImages = len(argv) - 1
    f, axes = plt.subplots(numberOfImages, 8)
    for fileIndex, filename in enumerate(argv[1:]):
        image = imread(filename)
        plotHistograms(axes, image, numberOfImages, fileIndex)
    plt.show()

if __name__ == "__main__":
    main(sys.argv)

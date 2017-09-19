from skimage.io import imread
from matplotlib import pyplot as plt
from scipy.stats import skew
from scipy.stats import kurtosis
import sys

def filterImage(image):
    #filter black background color out of the image
    return image[image[:,:] != 0]  * 1.0

def plotHistogram(axes, imageComponent, plotColor, binRange):
    return axes.hist(imageComponent.ravel(), 255, range=binRange, color=plotColor)

def plotHistograms(axes, image, numberOfImages, fileIndex):
    colors = ["red", "green", "blue", "purple", "black", "orange"]
    for componentIndex in range(7):
        if numberOfImages == 1:
            ax = axes[componentIndex]
        else:
            ax = axes[fileIndex, componentIndex]

        if componentIndex == 3:
            histogramImage = filterImage(image[:,:,0]) - filterImage(image[:,:,2])
            n, _, _ = plotHistogram(ax, histogramImage, colors[componentIndex],[-255, 255])
            print(skew(n))
            print(skew(n[n > 0]))
        elif componentIndex == 4:
            histogramImage = filterImage(image[:,:,1]) - filterImage(image[:,:,2])
            n, _, _ = plotHistogram(ax, histogramImage, colors[componentIndex],[-255, 255])
        elif componentIndex == 5:
            histogramImage = filterImage(image[:,:,0]) - filterImage(image[:,:,1])
            n, _, _ = plotHistogram(ax, histogramImage, colors[componentIndex],[-255, 255])
        elif componentIndex == 6:
            ax.imshow(image)
        else:
            histogramImage = filterImage(image[:,:, componentIndex])
            plotHistogram(ax, histogramImage, colors[componentIndex],[0, 255])

def main(argv):
    if len(argv) <= 1:
        print("usage: CompareHistograms <filename1> <filename2> ... <filenamex>")
        exit(1)
    
    numberOfImages = len(argv) - 1
    f, axes = plt.subplots(numberOfImages, 7)
    for fileIndex, filename in enumerate(argv[1:]):
        image = imread(filename)
        plotHistograms(axes, image, numberOfImages, fileIndex)
    plt.show()

if __name__ == "__main__":
    main(sys.argv)

import os
import glob
from skimage.io import imread
from collections import defaultdict
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

class GenerateHistogram(object):
    def __init__(self, imageDirectory):
        self.__imageDirectory = imageDirectory

    @property
    def imageDirectory(self):
        return self.__imageDirectory

    def generateHistogram(self):
        imageFilenames = glob.glob1(self.imageDirectory, "*.png")
        totalNumberOfFiles = len(imageFilenames)
        histogramForAllImages = dict()
        for index, filename in enumerate(imageFilenames):
            histogramForImage = self.generateHistogramForFile(filename)
            histogramForAllImages = self.reduceByKey(histogramForAllImages, histogramForImage)
            print("Generated histogram for {}, file {} out of {}".format(filename, index, totalNumberOfFiles))
        return histogramForAllImages

    def generateHistogramForFile(self, filename):
        histogram = defaultdict(int)
        image = imread(filename)
        shape = image.shape
        for row in range(shape[0]):
            for column in range(shape[1]):
                key = image[row, column, :]
                histogram[key] += 1
        return histogram

    def reduceByKey(self, originalList, addedList):
        for key, value in addedList:
            reducedValue = value
            if key in originalList:
               reducedValue = value + originalList[key]
            originalList[key] = reducedValue
        return originalList

    def plot(self, histogram):
        fig = pyplot.figure()
        ax = Axes3D(fig)

        r = []
        g = []
        b = []
        for key, _ in histogram:
            x,y,z = key
            r.append(x)
            g.append(y)
            b.append(z)
        ax.scatter(r, g, b)
        pyplot.show()

if __name__ == "__main__":
    generateHistogram = GenerateHistogram(r'/home/tjadejong/Documents/CBS/ZonnePanelen/Images')
    histogram = generateHistogram.generateHistogram()
    generateHistogram.plot(histogram)
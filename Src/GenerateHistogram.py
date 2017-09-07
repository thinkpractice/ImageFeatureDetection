import os
import glob
import csv
import sys
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
            imagePath = os.path.join(self.imageDirectory, filename)
            histogramForImage = self.generateHistogramForFile(imagePath)
            histogramForAllImages = self.reduceByKey(histogramForAllImages, histogramForImage)
            #print("Generated histogram for {}, file {} out of {}".format(filename, index, totalNumberOfFiles))
        return histogramForAllImages

    def generateHistogramForFile(self, filename):
        histogram = defaultdict(int)
        image = imread(filename)
        shape = image.shape
        for row in range(shape[0]):
            for column in range(shape[1]):
                key = (image[row, column, 0], image[row, column, 1], image[row, column, 2])
                histogram[key] += 1
        return histogram

    def reduceByKey(self, originalList, addedList):
        for key, value in addedList.items():
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
        for key, _ in histogram.items():
            x,y,z = key
            r.append(x)
            g.append(y)
            b.append(z)
        ax.scatter(r, g, b)
        pyplot.show()


def createHistogram(imageDirectory, filename):
    generateHistogram = GenerateHistogram(imageDirectory)
    histogram = generateHistogram.generateHistogram()
    with open(filename, 'w') as csvFile:
        csvWriter = csv.writer(csvFile)
        for key, value in histogram.items():
            r, g, b = key
            csvWriter.writerow([r, g, b, value])

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: GenerateHistogram.py <directory> <filename.csv>")
        exit(1)
    createHistogram(sys.argv[1], sys.argv[2])



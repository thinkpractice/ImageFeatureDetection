from matplotlib import pyplot
from skimage.io import imread
import numpy as np
import sys
import csv
import glob
import os
import argparse

def isBlack(pixel):
    r,g,b = pixel
    return r == 0 and g == 0 and b == 0

def filterImage(image):
    return np.array([[pixel for pixel in row if not isBlack(pixel)] for row in image])

def normalizePixels(image):
    #Define normalized image space
    y = image[:,:,0].astype(float) + image[:,:,1].astype(float) + image[:,:,2].astype(float) + 1e-6
    Y = np.stack((y,y,y), axis=2)
    #print(Y[Y > 0])
    return np.nan_to_num(image / Y)

def loadImages(directory):
    imageFilenames = glob.glob1(directory, "*.png")
    for filename in imageFilenames:
        imagePath = os.path.join(directory, filename)
        yield filename, imread(imagePath)

def getNormalizedPictures(directory):
    for filename, image in loadImages(directory):
        yield filename, normalizePixels(image)


def getArgs():
    parser = argparse.ArgumentParser(description="usage: PlotHistogram <input file.csv> [#items per histograms] [plot intensities as colors=1]")
    parser.add_argument("directory", type=str, help="The directory with the images to calculate tthe statistics")
    parser.add_argument("outputFile", type=str, help="The directory with the images to calculate tthe statistics")
    return parser.parse_args()

def calculateCentroid(image):
    numPixels = image.shape[0] * image.shape[1]
    redSums = np.sum(image[:,:,0])
    blueSums = np.sum(image[:,:,2])
    return np.vstack((redSums, blueSums)) * (1 / numPixels)

def calculateStatistics(image):
    row = []
    row.append(calculateCentroid(image))
    return row

def main(argv):
    args = getArgs()
    with open(args.outputFile,"w") as csvFile:
        csvWriter = csv.writer(csvFile, delimiter=";")
        for filename, image in getNormalizedPictures(args.directory):
            row = [filename]
            row.extend(calculateStatistics(image))
            csvWriter.writerow(row)

if __name__ == "__main__":
    main(sys.argv)

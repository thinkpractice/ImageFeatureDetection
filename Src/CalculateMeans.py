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

def loadImages(directory):
    imageFilenames = glob.glob1(directory, "*.png")
    for filename in imageFilenames:
        imagePath = os.path.join(directory, filename)
        yield filename, imread(imagePath)

def getArgs():
    parser = argparse.ArgumentParser(description="usage: PlotHistogram <input file.csv> [#items per histograms] [plot intensities as colors=1]")
    parser.add_argument("directory", type=str, help="The directory with the images to calculate tthe statistics")
    parser.add_argument("--intensities", help="Calculates color intensities for images", required=False, action="store_true")
    parser.add_argument("--mean", help="Calculates color means for images", required=False, action="store_true")
    parser.add_argument("--std", help="Calculates color standard deviations for images", required=False, action="store_true")
    parser.add_argument("--median", help="Calculates color medians for images", required=False, action="store_true")
    return parser.parse_args()

def main(argv):
    args = getArgs()
    imageData = loadImages(argv[1])
    with open(sys.argv[2],"w") as csvFile:
        csvWriter = csv.writer(csvFile, delimiter=";")
        for filename, image in imageData:
            row = [filename]
            meanColor = np.mean(image, axis=(0,1))
            row.extend(meanColor)
            csvWriter.writerow(row)

if __name__ == "__main__":
    main(sys.argv)

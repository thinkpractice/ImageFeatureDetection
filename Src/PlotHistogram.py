from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import csv
import sys
import math
import argparse

def loadHistogramFile(filename):
    with open(filename, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        return [[int(value) for value in row] for row in csvReader]

def plotHistogram(histogram, plotIntensities):
    fig = pyplot.figure()
    ax = Axes3D(fig)
    r = []
    g = []
    b = []
    colors = []
    minV = sys.maxsize
    maxV = 0
    for row in histogram:
        x, y, z, v = row
        r.append(x)
        g.append(y)
        b.append(z)
        minV = min(v, minV)
        maxV = max(v, maxV)
        if plotIntensities:
            colors.append(v)
        else:
            colors.append([value / 255 for index, value in enumerate(row) if index < 3])

    print(maxV)
    print(minV)
    if plotIntensities:
        scaledValues = [(c - minV) / (maxV - minV) for c in colors]
        colors = pyplot.cm.jet(scaledValues)
        ax.scatter(r, g, b, c=colors)
    else:
        ax.scatter(r, g, b, c=colors)
    pyplot.show()

def main():
    parser = argparse.ArgumentParser(description="usage: PlotHistogram <input file.csv> [#items per histograms] [plot intensities as colors=1]")
    parser.add_argument("filename", type=str, help="The histogram csv file to plot")
    parser.add_argument("--noitems", type=int, help="The number of items in the csv file to plot per histogram", required=False, default=-1)
    parser.add_argument("--intensities", help="Displays color histogram values instead of the color value ", required=False, action="store_true")

    args = parser.parse_args()

    plotIntensities = False
    if args.intensities:
        plotIntensities = True

    histogramData = loadHistogramFile(args.filename)
    totalNumberOfItems = len(histogramData)

    print("Loaded histogram with {} items".format(totalNumberOfItems))
    if args.noitems != -1:
        itemsPerHistogram = args.noitems
    else:
        itemsPerHistogram = totalNumberOfItems-1

    histogram = []
    for index, histogramItem in enumerate(histogramData):
        histogram.append(histogramItem)
        if index > 0 and (index % itemsPerHistogram == 0):
            plotHistogram(histogram, plotIntensities)
            histogram = []

if __name__ == "__main__":
    main()

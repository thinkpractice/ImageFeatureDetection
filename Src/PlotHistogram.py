from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D
import csv
import sys

def loadHistogramFile(filename):
    histogram = []
    with open(filename, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        for row in csvReader:
            r, g, b, v = row
            histogram.append((int(r), int(g), int(b)))
    return histogram

def plotHistogram(histogram):
    fig = pyplot.figure()
    ax = Axes3D(fig)
    r = []
    g = []
    b = []
    colors = []
    for row in histogram:
        x, y, z = row
        r.append(x)
        g.append(y)
        b.append(z)
        colors.append([value / 255 for value in row])
    ax.scatter(r, g, b, c=colors)
    pyplot.show()

def main(args):
    if len(args) < 2:
        print("usage: PlotHistogram <input file.csv> [#histograms]")
        exit(1)
    if len(args) == 3:
        numberOfHistograms = int(args[2])
    histogram = loadHistogramFile(args[1])
    plotHistogram(histogram)


if __name__ == "__main__":
    args = sys.argv
    main(args)





from matplotlib import pyplot
import numpy as np
import sys
import csv

def loadHistogramFile(filename):
    with open(filename, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        return np.array([[int(value) for value in row] for row in csvReader])

def main(argv):
    histogramData = loadHistogramFile(argv[1])
    ind = np.arange(histogramData.shape[0])
    width = 0.35
    sortedCounts = np.sort(histogramData[:,3])
    pyplot.bar(ind + width, sortedCounts)
    pyplot.show()

if __name__ == "__main__":
    main(sys.argv)

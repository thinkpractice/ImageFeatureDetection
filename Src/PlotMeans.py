import csv
import sys
import numpy as np
from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

def loadData(filename):
    with open(filename) as csvFile:
        csvReader = csv.reader(csvFile, delimiter=";")
        return np.array([[float(cell) for index, cell in enumerate(row) if index > 0] for row in csvReader])

def main(argv):
    meanColors = loadData(argv[1])
    colors = [color / 255 for color in meanColors]
    fig = pyplot.figure()
    ax = Axes3D(fig)
    ax.scatter(meanColors[:,0], meanColors[:,1], meanColors[:,2], c=colors)
    pyplot.show()

if __name__ == "__main__":
    main(sys.argv)

import numpy as np
import sys
import csv
import matplotlib
from sklearn.cluster import KMeans
from matplotlib import pyplot

def loadHistogramFile(filename):
    with open(filename, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        return np.array([[int(value) for index, value in enumerate(row) if index < 3] for row in csvReader])

def normalizeColorData(data):
    n = (data[:,0] + data[:,1] + data[:,2] + 1e-6)
    return np.stack([data[:,0] / n, data[:,1] / n], axis=1)

def bin(x):
    y = np.bincount(x)
    ii = np.nonzero(y)[0]
    return zip(ii, y[ii])

def main(argv):
    histogramData1 = loadHistogramFile(argv[1])
    normalizedData1 = normalizeColorData(histogramData1)

    ones = np.ones([normalizedData1.shape[0],1])
    print(ones)
    classifiedData1 = np.hstack((normalizedData1, ones))


    histogramData2 = loadHistogramFile(argv[2])
    normalizedData2 = normalizeColorData(histogramData2)

    zeros = np.zeros([normalizedData2.shape[0],1])
    print(zeros)
    classifiedData2 = np.hstack((normalizedData2, zeros))

    allData = np.vstack((normalizedData2, normalizedData1))
    print(allData)

    allDataClassified = np.vstack((classifiedData1, classifiedData2))
    
    kmeans = KMeans(n_clusters=3)
    kmeans.fit(allData)

    prediction1 = kmeans.predict(normalizedData1)
    print([x for x in bin(prediction1)])

    prediction2 = kmeans.predict(normalizedData2)
    print([x for x in bin(prediction2)])
    
    colors = ["red", "blue"]
    pyplot.scatter(allData[:,0], allData[:,1], c=allDataClassified[:,2], cmap=matplotlib.colors.ListedColormap(colors))
    pyplot.show()

if __name__ == "__main__":
    main(sys.argv)

import numpy as np
import sys
import csv
from sklearn.decomposition import PCA
from matplotlib import pyplot

def loadHistogramFile(filename):
    with open(filename, 'r') as csvFile:
        csvReader = csv.reader(csvFile)
        return [[int(value) for index, value in enumerate(row) if index < 3] for row in csvReader]

def main(argv):
    histogramData = loadHistogramFile(argv[1])
    pca = PCA()
    pca.fit(histogramData)
    print("components={}".format(pca.components_))
    print("explained variance={}".format(pca.explained_variance_))
    print("explained variance ratio={}".format(pca.explained_variance_ratio_))
    print("singular values={}".format(pca.singular_values_))

    reduced = PCA(n_components=2).fit_transform(histogramData)
    pyplot.scatter(reduced[:,0], reduced[:, 1])
    pyplot.show()

if __name__ == "__main__":
    main(sys.argv)

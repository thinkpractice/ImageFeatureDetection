from sklearn import tree
from sklearn.model_selection import cross_val_score
import numpy as np
import sys
import csv
import graphviz

def loadFeatures(filename):
    with open(filename, "r") as csvFile:
        csvReader = csv.reader(csvFile, delimiter=";")
        x = []
        y = []
        header = next(csvReader)
        for row in csvReader:
            x.append([float(cell) for cell in row[1:-1]])
            y.append(row[-1])
        return header, np.array(x), np.array(y)

def train(features, classifications):
    clf = tree.DecisionTreeClassifier()
    return clf.fit(features, classifications)

def printFeatureImportance(header, featureImportances):
    featuresAndImportance = [(name, importance) for name, importance in zip(header[1:], featureImportances)]
    sortedFeatures = sorted(featuresAndImportance,key=lambda row: row[1], reverse=True)
    for feature in sortedFeatures:
        print(feature)

def main(argv):
    if len(argv) <= 1:
        print("usage: TrainClassifier <featurefile.csv>")
        exit(1)
    header, features, classifications = loadFeatures(argv[1])
    print(features)
    clf = train(features, classifications)
    printFeatureImportance(header, clf.feature_importances_)
    print(clf.classes_)
    print("cross validation scores= {}".format(cross_val_score(clf, features, classifications, scoring="accuracy")))
    dot_data = tree.export_graphviz(clf, out_file=None)
    graph = graphviz.Source(dot_data)
    graph.render("tree")

if __name__ == "__main__":
    main(sys.argv)

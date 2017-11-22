from sklearn import tree
from sklearn.model_selection import cross_val_score
from sklearn.decomposition import PCA
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
            featureVector = [float(cell) for cell in row[1:-1]]
            x.append(featureVector)
            y.append(int(row[-1]))
        return header, np.array(x), np.array(y)

def train(features, classifications):
    clf = tree.DecisionTreeClassifier(min_samples_leaf=5)
    return clf.fit(features, classifications)

def printFeatureImportance(header, featureImportances):
    featuresAndImportance = [(name, importance) for name, importance in zip(header[1:], featureImportances)]
    sortedFeatures = sorted(featuresAndImportance,key=lambda row: row[1], reverse=True)
    for feature in sortedFeatures:
        print(feature)

def filterOnFeatureImportance(features, featureImportances):
    return [[feature for feature, importance in zip(featureRow, featureImportances) if importance >= 0.01] for featureRow in features]

def filterHeader(header, featureImportances):
    return [name for name, importance in zip(header, featureImportances) if importance >= 0.01]

def exportTree(clf, featureNames, treeName):
    dot_data = tree.export_graphviz(clf, out_file=None, feature_names=featureNames,filled=True)
    graph = graphviz.Source(dot_data)
    graph.render(treeName)

def trainAndEvaluate(featureNames, features, classifications, exportName):
    clf = train(features, classifications)
    printFeatureImportance(featureNames, clf.feature_importances_)
    print(clf.classes_)
    print("cross validation scores= {}".format(cross_val_score(clf, features, classifications, scoring="accuracy")))
    exportTree(clf, featureNames, exportName)
    return clf

def main(argv):
    if len(argv) <= 1:
        print("usage: TrainClassifier <featurefile.csv>")
        exit(1)
    header, features, classifications = loadFeatures(argv[1])
    print(classifications)
    print(len(features))

    featureNames = header[1:-1]
    print(len(featureNames))
    clf = trainAndEvaluate(featureNames, features, classifications,"tree1")

    filteredFeatures = filterOnFeatureImportance(features, clf.feature_importances_)
    filteredHeader = filterHeader(featureNames, clf.feature_importances_)
    trainAndEvaluate(filteredHeader, filteredFeatures, classifications, "tree2")

    pca = PCA(n_components=15)
    filteredFeatures = pca.fit_transform(features)
    trainAndEvaluate(["pca_component{}".format(i) for i in range(len(filteredFeatures[0]))], filteredFeatures, classifications, "tree3")
    print("components={}".format(pca.components_))
    print(pca.explained_variance_ratio_)

if __name__ == "__main__":
    main(sys.argv)

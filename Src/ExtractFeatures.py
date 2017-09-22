from skimage.io import imread
import ImageStatistics
import glob
import csv
import sys
import os

class FeatureExtractor(object):
    @property
    def fields(self):
        return []

    def extractFeatureValues(self, image):
        return []

class FeatureExtractorCollection(object):
    @property
    def featureExtractors(self):
        return []

    @property
    def header(self):
        header = ["filename"]
        header.extend([fieldName for featureExtractor in self.featureExtractors for fieldName in featureExtractor.fields])
        header.append("class")
        return header

    def getImageFilenames(self, directory):
        return [os.path.join(directory, filename) for filename in glob.glob1(directory, "*.png")]

    def extractFeatures(directory, arePositives):
        features = []
        for filename in self.getImageFilenames():
            featureRow = [filename]
            image = imread(filename)
            for featureExtractor in self.featureExtractors:
                featureRow.extend(featureExtractor.extractFeatures(image))
            featureRow.append(1 if arePositives else 0)
            features.append(featureRow)

def saveFeatures(filename, header, features):
    with open(filename, "w") as csvFile:
        csvWriter = csv.writer(csvFile, delimiter=";")
        csvWriter.writerow(header)
        for feature in features:
            csvWriter.writerow(feature)

def main(argv):
    if len(argv) <= 3:
        print("usage: ExtractFeatures.py <directory with positives> <directory with negatives> <feature filename>")
        exit(1)

    featureExtractor = FeatureExtractorCollection()
    positives = featureExtractor.extractFeatures(argv[1], True)
    negatives = featureExtractor.extractFeatures(argv[2], False)
    allCases = positives
    allCases.extend(negatives)
    saveFeatures(argv[2], featureExtractor.header, allCases)

if __name__ == "__main__":
    main(sys.argv)

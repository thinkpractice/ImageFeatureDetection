from skimage.io import imread
import ImageStatistics
import glob
import csv
import sys
import os

class FeatureExtractor(object):
    def __init__(self, fields):
        self.__fields = fields

    @property
    def fields(self):
        return self.__fields

    def extractFeatureValues(self, image):
        return []

class MeanExtractor(FeatureExtractor):
    def __init__(self):
        super().__init__(["meanR", "meanG", "meanB"])

    def extractFeatureValues(self, image):
        return ImageStatistics.rgbImageMean(image)

class VarianceExtractor(FeatureExtractor):
    def __init__(self):
        super().__init__(["varR", "varG", "varB"])

    def extractFeatureValues(self, image):
        return ImageStatistics.rgbImageVariance(image)

class PercentileExtractor(FeatureExtractor):
    def __init__(self):
        super().__init__(["q1R", "q1G","q1B","q2R", "q2G","q2B","q3R", "q3G","q3B"])

    def extractFeatureValues(self, image):
        percentiles =[]
        for q in [25,50,75]:
            percentiles.extend(ImageStatistics.rgbPercentile(image, q))
        return percentiles

class MinMaxExtractor(FeatureExtractor):
    def __init__(self):
        super().__init__(["minR","minG", "minB", "maxR","maxG", "maxB"])

    def extractFeatureValues(self, image):
        features = ImageStatistics.rgbMinima(image)
        features.extend(ImageStatistics.rgbMaxima(image))
        return features

class Preprocessor(object):
    @property
    def prefix(self):
        return ""

    def process(self, image):
        return image

class FeatureExtractorCollection(object):
    @property
    def featureExtractors(self):
        return [MeanExtractor(),
                VarianceExtractor(),
                PercentileExtractor(),
                MinMaxExtractor()]

    @property
    def header(self):
        header = ["filename"]
        header.extend(["{}{}".format(preprocessor.prefix, fieldName) for preprocessor in self.preprocessors for featureExtractor in self.featureExtractors for fieldName in featureExtractor.fields])
        header.append("class")
        return header

    @property
    def preprocessors(self):
        return [Preprocessor()]

    def getImageFilenames(self, directory):
        return [os.path.join(directory, filename) for filename in glob.glob1(directory, "*.png")]

    def extractFeatures(self, directory, arePositives):
        features = []
        for filename in self.getImageFilenames(directory):
            featureRow = [filename]
            image = imread(filename)
            for preprocessor in self.preprocessors:
                processedImage = preprocessor.process(image)
                for featureExtractor in self.featureExtractors:
                    featureRow.extend(featureExtractor.extractFeatureValues(processedImage))
            featureRow.append(1 if arePositives else 0)
            features.append(featureRow)
        return features

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
    saveFeatures(argv[3], featureExtractor.header, allCases)

if __name__ == "__main__":
    main(sys.argv)

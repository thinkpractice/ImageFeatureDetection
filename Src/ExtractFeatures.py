from skimage.io import imread
from skimage.color import rgb2hsv
from statistics import mean, median
import numpy as np
import ImageStatistics
import glob
import csv
import sys
import os
import cv2

class FeatureExtractor(object):
    def __init__(self, fields):
        self.__fields = fields

    @property
    def fields(self):
        return self.__fields

    def handles(self, preprocessor):
        return True

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

class EntropyExtractor(FeatureExtractor):
    def __init__(self):
        super().__init__(["entropyR", "entropyG", "entropyB"])

    def extractFeatureValues(self, image):
        return ImageStatistics.rgbEntropy(image)

class MSERExtractor(FeatureExtractor):
    def __init__(self):
        super().__init__(["minWidth", "minHeight", "medianWidth", "medianHeight", "meanWidth", "meanHeight", "maxWidth", "maxHeight"] + ["mser_{}".format(i) for i in range(10)])

    def handles(self, preprocessor):
        return type(preprocessor) == Preprocessor

    def getMinAndMaxSizes(self, boundingBoxes):
        widths = [box[2] for box in boundingBoxes]
        heights = [box[3] for box in boundingBoxes]

        return min(widths), min(heights), median(widths), median(heights), mean(widths), mean(heights), max(widths), max(heights)

    def extractFeatureValues(self, image):
        mser = cv2.MSER_create()
        areas, boundingBoxes = mser.detectRegions(cv2.cvtColor(image, cv2.COLOR_RGB2BGR))
        hulls = [cv2.convexHull(p.reshape(-1, 1,2)) for p in areas]
        maskedImages = []
        for contour in hulls:
            mask = np.zeros(image.shape, dtype=np.uint8)
            cv2.drawContours(mask, [contour], -1, (255,255,255), -1)
            maskedImages.append(image * mask)
        pcaStatistics = []
        for image in maskedImages:
            pcaStatistics.extend(ImageStatistics.pca(image)[1])
        pcaStatLength = len(pcaStatistics)
        if pcaStatLength < 10:
            pcaStatistics.extend([0 for i in range(10 - pcaStatLength)])
        
        boxSizes = self.getMinAndMaxSizes(boundingBoxes)
        return list(boxSizes) + sorted(pcaStatistics, reverse=True)[0:10]

class CountColorExtractor(FeatureExtractor):
    pass

class Preprocessor(object):
    def __init__(self, prefix=""):
        self.__prefix = prefix

    @property
    def prefix(self):
        return self.__prefix

    def process(self, image):
        return image

class PcaPreprocessor(Preprocessor):
    def __init__(self):
        super().__init__("pca_")

    def process(self, image):
        pcaImage = ImageStatistics.pcaTransform(image)
        return ImageStatistics.rescaleImage(pcaImage) * 255

class HsvPreprocessor(Preprocessor):
    def __init__(self):
        super().__init__("hsv_")

    def process(self, image):
        return rgb2hsv(image)

class ExposurePreprocessor(Preprocessor):
    def __init__(self):
        super().__init__("exposure_")

    def process(self, image):
        return ImageStatistics.rgbAdjustSigmoid(image)

class SubstractionPreprocessor(Preprocessor):
    def __init__(self):
        super().__init__("substract_".format())
    
    def process(self, image):
        redMinGreen = image[:,:,0] - image[:,:,1]
        redMinBlue = image[:,:,0] - image[:,:,2]
        greenMinBlue = image[:,:,1] - image[:,:,2]
        return np.stack([redMinGreen, redMinBlue, greenMinBlue], axis=2)

class FeatureExtractorCollection(object):
    @property
    def featureExtractors(self):
        return [MeanExtractor(),
                VarianceExtractor(),
                PercentileExtractor(),
                MinMaxExtractor(),
                EntropyExtractor(),
                MSERExtractor()
                ]

    @property
    def preprocessors(self):
        return [Preprocessor(),
                PcaPreprocessor(),
                HsvPreprocessor(),
                ExposurePreprocessor(),
                SubstractionPreprocessor()
                ]

    @property
    def header(self):
        header = ["filename"]
        header.extend(["{}{}".format(preprocessor.prefix, fieldName) for preprocessor in self.preprocessors for featureExtractor in self.featureExtractors for fieldName in featureExtractor.fields if featureExtractor.handles(preprocessor)])
        header.append("class")
        return header

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
                    if featureExtractor.handles(preprocessor):
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

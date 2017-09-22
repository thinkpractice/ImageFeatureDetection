from skimage.io import imread
import sys
import ImageStatistics

def calculateStatistics(image):
    normalizedImage = ImageStatistics.normalizeImage(image)
    print("std2={}".format(ImageStatistics.rgbImageVariance(normalizedImage)))
    print("imageMeans={}".format(ImageStatistics.rgbImageMean(normalizedImage)))
    print("imageVariance={}".format(ImageStatistics.rgbImageVariance(normalizedImage)))
    print("image covariance matrix={}".format(ImageStatistics.rgbImageCovarianceMatrix(normalizedImage)))
    #print("pca={}".format(ImageStatistics.pca(normalizedImage)))

def main(argv):
    if len(argv) <= 1:
        print("usage: CompareHistograms <filename1> <filename2> ... <filenamex>")
        exit(1)
    
    numberOfImages = len(argv) - 1
    for fileIndex, filename in enumerate(argv[1:]):
        image = imread(filename)
        calculateStatistics(image)

if __name__ == "__main__":
    main(sys.argv)


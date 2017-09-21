from skimage.io import imread
import sys
import ImageStatistics

def main(argv):
    if len(argv) < 2:
        print ("usage: ImageStatistics.py <filename>")
        exit(1)

    image = imread(argv[1])
    print("std1={}".format(ImageStatistics.rgbImageVariance(image)))
    normalizedImage = ImageStatistics.normalizeImage(image)
    print("std2={}".format(ImageStatistics.rgbImageVariance(normalizedImage)))
    print("imageMeans={}".format(ImageStatistics.rgbImageMean(normalizedImage)))
    print("imageVariance={}".format(ImageStatistics.rgbImageVariance(normalizedImage)))
    print("image covariance matrix={}".format(ImageStatistics.rgbImageCovarianceMatrix(normalizedImage)))
    print("pca={}".format(ImageStatistics.pca(normalizedImage)))

if __name__ == "__main__":
    main(sys.argv)


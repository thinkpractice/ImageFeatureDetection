from skimage.io import imread
from skimage.morphology import disk
from skimage.filters.rank import median
from skimage.segmentation import random_walker
from sklearn.cluster import KMeans
from matplotlib import pyplot
import numpy as np
import sys

def normalizePixels(image):
    #Define normalized image space
    y = image[:,:,0].astype(float) + image[:,:,1].astype(float) + image[:,:,2].astype(float) + 1e-6
    Y = np.stack((y,y,y), axis=2)
    return np.nan_to_num(image / Y)

def calculateKmeans(image):
    kmeans = KMeans(n_clusters=6)
    
    filteredImage = np.stack((median(image[:,:,0]),median(image[:,:,1]), median(image[:,:,2])), axis=2)
    reshapedImage = filteredImage.reshape([-1,3])
    kmeans.fit(reshapedImage)

    centers = np.uint8(kmeans.cluster_centers_)
    centers = np.array([[1,0,0], [0,1,0],[0,0,1],[0,1,1],[1,1,0],[1,0,1]]).astype(float)
    kmeansImage = centers[kmeans.labels_]
    kmeansImage = kmeansImage.reshape(image.shape)

    labels = random_walker(image, kmeans.labels_, multichannel=True)
    segmentedImage = centers[labels]
    return kmeansImage, filteredImage, segmentedImage

def main(argv):
    image = imread(argv[1])
    normalizedImage = normalizePixels(image)

    kmeansImage, filteredImage, segmentedImage = calculateKmeans(image)
    normalizedKmeansImage, normalizedFilteredImage, normalizedSegmentedImage = calculateKmeans(normalizedImage)

    f, axes = pyplot.subplots(2, 4)
    axes[0,0].imshow(image)
    axes[0,1].imshow(filteredImage)
    axes[0,2].imshow(kmeansImage)
    axes[0,3].imshow(segmentedImage)
    axes[1,0].imshow(normalizedImage)
    axes[1,1].imshow(normalizedFilteredImage)
    axes[1,2].imshow(normalizedKmeansImage)
    axes[1,3].imshow(normalizedSegmentedImage)
    pyplot.show()

if __name__ == "__main__":
    main(sys.argv)


from skimage.io import imread
from skimage.morphology import disk
from skimage.filters.rank import median
from sklearn.cluster import KMeans
from matplotlib import pyplot
import numpy as np
import sys

def normalizePixels(image):
    #Define normalized image space
    y = image[:,:,0].astype(float) + image[:,:,1].astype(float) + image[:,:,2].astype(float) + 1e-6
    Y = np.stack((y,y,y), axis=2)
    #print(Y[Y > 0])
    return np.nan_to_num(image / Y)

def calculateKmeans(image):
    kmeans = KMeans(n_clusters=6)
    
    reshapedImage = image.reshape([-1,3])
    kmeans.fit(reshapedImage)

    centers = np.uint8(kmeans.cluster_centers_)
    centers = np.array([[1,0,0], [0,1,0],[0,0,1],[0,1,1],[1,1,0],[1,0,1]]).astype(float)
    kmeansImage = centers[kmeans.labels_]
    kmeansImage = kmeansImage.reshape(image.shape)

    filteredImage = np.stack((median(kmeansImage[:,:,0]),median(kmeansImage[:,:,1]), median(kmeansImage[:,:,2])), axis=2)
    return kmeansImage, filteredImage

def main(argv):
    image = imread(argv[1])
    normalizedImage = normalizePixels(image)

    kmeansImage, filteredImage = calculateKmeans(image)
    normalizedKmeansImage, normalizedFilteredImage = calculateKmeans(normalizedImage * 255)

    f, axes = pyplot.subplots(2, 3)
    axes[0,0].imshow(image)
    axes[0,1].imshow(kmeansImage)
    axes[0,2].imshow(filteredImage)
    axes[1,0].imshow(normalizedImage)
    axes[1,1].imshow(normalizedKmeansImage)
    axes[1,2].imshow(normalizedFilteredImage)
    pyplot.show()

if __name__ == "__main__":
    main(sys.argv)


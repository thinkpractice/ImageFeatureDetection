from skimage.io import imread
from skimage.filters import threshold_local
from matplotlib import pyplot
import numpy as np
import sys

def normalizePixels(image):
    #Define normalized image space
    y = image[:,:,0].astype(float) + image[:,:,1].astype(float) + image[:,:,2].astype(float) + 1e-6
    Y = np.stack((y,y,y), axis=2)
    return np.nan_to_num(image / Y)

def blueFilter(image):
    maxBlue = 0.85 * np.amax(image[:,:,2])
    print(maxBlue)
    redComponent = image[:,:,0]
    redComponent = redComponent[image[:,:,0] > 0]
    minRed = np.amin(redComponent)
    print(minRed)
    imageRedMask = image[:,:,0] <= minRed
    imageBlueMask = image[:,:,2] >= maxBlue
    filteredImage = np.zeros(image.shape)
    filteredImage[imageRedMask] = image[imageRedMask]
    filteredImage[imageBlueMask] = image[imageBlueMask]
    return filteredImage

def main(argv):
    image = imread(argv[1])
    normalizedImage = normalizePixels(image)
    filteredImage = blueFilter(normalizedImage)
    f, axes = pyplot.subplots(1, 3)
    axes[0].imshow(image)
    axes[1].imshow(normalizedImage)
    axes[2].imshow(filteredImage,cmap="gray")
    pyplot.show()

if __name__ == "__main__":
    main(sys.argv)

from skimage.io import imread
from skimage.segmentation import slic
from scipy.ndimage.filters import convolve
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import ImageStatistics
import sys

def plotColorValues(axes, image):
    imagePoints = ImageStatistics.flattenImage(image)
    axes.scatter(imagePoints[:,0], imagePoints[:,1], imagePoints[:,2])

def convolutionFilter(image, kernel):
    return convolve(image, kernel)

def mexicanHat3x3():
    kernel = np.array([[0,-1/4,0],[-1/4,1,-1/4],[0,-1/4,0]])
    return np.stack([kernel, kernel, kernel],axis=2)

def edgeDetector3x3():
    kernel = np.array([[-1/8,-1/8,-1/8],[-1/8,1,-1/8],[-1/8,-1/8,-1/8]])
    return np.stack([kernel, kernel, kernel],axis=2)

def lineDetector3x3():
    kernel = np.array([[-1,-1,-1],[2,2,2],[-1,-1,-1]])
    return np.stack([kernel, kernel, kernel],axis=2)

def main(argv):
    if len(argv) <= 1:
        print("usage: PcaTransformImage.py <filename>")
        exit(1)
    image = imread(argv[1])
    kernel3D = mexicanHat3x3()
    filteredImage = convolutionFilter(image, kernel3D)
    filteredImage = ImageStatistics.rgbRescaleImage(filteredImage)

    f, axes = plt.subplots(1,5)
    axes[0].imshow(image)
    axes[1].imshow(filteredImage[:,:,0])
    axes[2].imshow(filteredImage[:,:,1])
    axes[3].imshow(filteredImage[:,:,2])
    axes[4].imshow(filteredImage)
    
    plt.show()


if __name__ == "__main__":
    main(sys.argv)




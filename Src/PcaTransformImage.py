from skimage.io import imread
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import ImageStatistics
import sys

def plotColorValues(axes, image):
    imagePoints = ImageStatistics.flattenImage(image)
    axes.scatter(imagePoints[:,0], imagePoints[:,1], imagePoints[:,2])

def main(argv):
    if len(argv) <= 1:
        print("usage: PcaTransformImage.py <filename>")
        exit(1)
    image = imread(argv[1])
    print(ImageStatistics.imageCovariance(image[:,:,0], image[:,:,0]))
    print("image shape={}".format(image.shape))
    centeredImage = ImageStatistics.rgbCenterImage(image / 255)
    print("centered image shape={}".format(centeredImage.shape))
    transformedImage = ImageStatistics.pcaTransform(centeredImage)
    rescaledImage = ImageStatistics.rgbRescaleImage(transformedImage)
    


    f, axes = plt.subplots(1,4)
    axes[0].imshow(image)
    axes[1].imshow(rescaledImage[:,:,0])
    axes[2].imshow(rescaledImage[:,:,1])
    axes[3].imshow(rescaledImage[:,:,2])

    f2 = plt.figure(2)
    ax2 = f2.add_subplot(121, projection='3d')
    plotColorValues(ax2, centeredImage)
    ax3 = f2.add_subplot(122, projection='3d')
    plotColorValues(ax3, transformedImage)
    
    plt.show()


if __name__ == "__main__":
    main(sys.argv)




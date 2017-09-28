from skimage.io import imread
import numpy as np
import glob
import os
import sys

def getImagesInDirectory(directory):
    for filename in glob.glob1(directory, "*.png"):
        yield os.path.join(directory, filename)

def getImageSizes(directory):
    for filename in getImagesInDirectory(directory):
        image = imread(filename)
        yield image.shape

def main(argv):
    if len(argv) <= 1:
        print("usage: GetImageSizes <directory>")
        exit(0)

    imageSizes = np.array([size for size in getImageSizes(argv[1])])
    print(imageSizes)
    print("min height={}".format(np.min(imageSizes[:,0])))
    print("max height={}".format(np.max(imageSizes[:,0])))
    print("min width={}".format(np.min(imageSizes[:,1])))
    print("max width={}".format(np.max(imageSizes[:,1])))
    
if __name__ == "__main__":
    main(sys.argv)

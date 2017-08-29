from Src.Models.BoundingBox import BoundingBox
from skimage.draw import polygon
import numpy as np

class Polygon(object):
    def __init__(self, polygonArray):
        self.__points = polygonArray

    @property
    def points(self):
        return self.__points

    @property
    def boundingBox(self):
        xCoords, yCoords = self.points
        minX = int(round(xCoords.min()))
        maxX = int(round(xCoords.max()))
        minY = int(round(yCoords.min()))
        maxY = int(round(yCoords.max()))
        return BoundingBox([minX, minY, maxX-minX+1, maxY-minY+1])

    @property
    def polygonMask(self):
        xCoords, yCoords = self.points
        return polygon(yCoords, xCoords)

    def drawInto(self, tileImage):
        rr, cc = self.polygonMask
        tileImage[rr, cc] = (0, 0, 255)

    def maskImage(self, polygonImage):
        rr, cc = self.polygonMask
        maskedImage = polygonImage.copy()
        imageMask = np.zeros([maskedImage.shape[0], maskedImage.shape[1]], dtype=np.uint8)
        imageMask[rr, cc] = 1
        imageMask = imageMask != 1
        maskedImage[imageMask] = (0, 0, 0)
        return maskedImage

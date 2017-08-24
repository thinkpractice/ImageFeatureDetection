from skimage.io import imsave
from skimage.draw import polygon
import numpy as np
import os
import time

class Thumbnailer(object):
    def __init__(self, exportDirectory):
        self.__exportDirectory = exportDirectory

    @property
    def exportDirectory(self):
        return self.__exportDirectory

    def writeThumbnails(self, polygons, tileImage):
        startTime = time.time()
        numberOfThumbnails = 0
        for imageId, polygonArray in polygons:
            self.writeThumbnail(imageId, polygonArray, tileImage)
            numberOfThumbnails += 1
        endTime = time.time()
        print("Wrote {} thumbnails in {}s".format(numberOfThumbnails, endTime-startTime))

    def writeThumbnail(self, imageId, polygonArray, tileImage):
        filename = os.path.join(self.exportDirectory, "{}.png".format(imageId))
        boundingRect = self.getBoundingBox(polygonArray)
        polygonImage = self.getRectangleFromImage(tileImage, boundingRect)
        if polygonImage is None:
            print("Wrong image dimensions for: {} bbox: {}".format(filename, boundingRect))
            return

        translatedPolygonCoords = self.translateCoords(boundingRect, polygonArray)
        maskedImage = self.maskImageWithPolygon(polygonImage, translatedPolygonCoords)

        print("Writing maskedImage: {} bbox: {}".format(filename, boundingRect))
        imsave(filename, maskedImage)

    def maskImageWithPolygon(self, polygonImage, translatedPolygonCoords):
        rr, cc = self.getPolygonFromCoords(translatedPolygonCoords)
        maskedImage = polygonImage.copy()
        imageMask = np.zeros([maskedImage.shape[0], maskedImage.shape[1]], dtype=np.uint8)
        imageMask[rr, cc] = 1
        imageMask = imageMask != 1
        maskedImage[imageMask] = (0, 0, 0)
        return maskedImage

    def getPolygonFromCoords(self, polygonArray):
        xCoords, yCoords = polygonArray
        rr, cc = polygon(xCoords, yCoords)
        return rr, cc

    def translateCoords(self, boundingRect, polygonArray):
        xCoords, yCoords = polygonArray
        translatedXCoords = xCoords - boundingRect[0] - 1
        translatedYCoords = yCoords - boundingRect[1] - 1
        return translatedXCoords, translatedYCoords

    def getBoundingBox(self, polygonArray):
        xCoords, yCoords = polygonArray
        return (int(round(xCoords.min())), int(round(yCoords.min())), int(round(xCoords.max())), int(round(yCoords.max())))

    def getRectangleFromImage(self, image, boundingRect):
        minX = boundingRect[0]
        minY = boundingRect[1]
        maxX = boundingRect[2]
        maxY = boundingRect[3]
        if minX == maxX or minY == maxY:
            return None

        return image[minX:maxX, minY:maxY, :]

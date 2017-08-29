import os
import time
from skimage.io import imsave
from Src.Models.Polygon import Polygon

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
        p = Polygon(polygonArray)
        polygonImage = self.getRectangleFromImage(tileImage, p.boundingBox)
        if polygonImage is not None:
            print("Wrong image dimensions for: {} bbox: {}".format(filename, p.boundingBox))
            return
        print(polygonImage)
        translatedPolygonCoords = self.translateCoords(p.boundingBox, polygonArray)
        tp = Polygon(translatedPolygonCoords)
        maskedImage = tp.maskImage(polygonImage)

        print("Writing maskedImage: {} bbox: {}".format(filename, p.boundingBox))
        imsave(filename, maskedImage)

    def translateCoords(self, boundingRect, polygonArray):
        xCoords, yCoords = polygonArray
        translatedXCoords = xCoords - boundingRect.left - 1
        translatedYCoords = yCoords - boundingRect.top - 1
        return translatedXCoords, translatedYCoords

    def getRectangleFromImage(self, image, boundingRect):
        if boundingRect.width == 0 or boundingRect.height == 0:
            return None
        return image[boundingRect.yRange, boundingRect.xRange, :]

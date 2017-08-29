import os
import time
import numpy as np
from skimage.io import imsave
from Src.Models.Polygon import Polygon

class Thumbnailer(object):
    def __init__(self, exportDirectory):
        self.__exportDirectory = exportDirectory

    @property
    def exportDirectory(self):
        return self.__exportDirectory

    def writeThumbnails(self, polygons, imageTiler):
        startTime = time.time()
        totalThumbnails = 0
        numberOfThumbnails = 0
        exportedImageIds = []
        for imageId, polygonArray in polygons:
            if self.writeThumbnail(imageId, polygonArray, imageTiler):
                exportedImageIds.append(imageId)
                numberOfThumbnails += 1
            totalThumbnails += 1
        endTime = time.time()
        print("Wrote {} thumbnails out of {} in {}s ".format(numberOfThumbnails, totalThumbnails, endTime-startTime))
        return exportedImageIds

    def writeThumbnail(self, imageId, polygonArray, imageTiler):
        filename = os.path.join(self.exportDirectory, "{}.png".format(imageId))
        p = Polygon(polygonArray)
        polygonImage = imageTiler.getImageForBoundingBox(p.boundingBox)
        if polygonImage is None or np.all(polygonImage == 0):
            print("Wrong image dimensions for: {} bbox: {}".format(filename, p.boundingBox))
            return False
        translatedPolygonCoords = self.translateCoords(p.boundingBox, polygonArray)
        tp = Polygon(translatedPolygonCoords)
        maskedImage = tp.maskImage(polygonImage.image)

        print("Writing maskedImage: {} bbox: {}".format(filename, p.boundingBox))
        imsave(filename, maskedImage)
        return True

    def translateCoords(self, boundingRect, polygonArray):
        xCoords, yCoords = polygonArray
        translatedXCoords = xCoords - boundingRect.left - 1
        translatedYCoords = yCoords - boundingRect.top - 1
        return translatedXCoords, translatedYCoords

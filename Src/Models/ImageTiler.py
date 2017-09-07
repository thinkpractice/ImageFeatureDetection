import math
from collections import deque

from Src.Models.BoundingBox import BoundingBox
from Src.Models.ImageTile import ImageTile
import numpy as np
import logging

class ImageTiler(object):
    def __init__(self, map, blockXSize, blockYSize):
        self.__map = map
        self.__bufferedMaps = deque()
        self.__blockXSize = blockXSize
        self.__blockYSize = blockYSize
        self.__activeTileNumber = 0
        self.__currentTileCoordinates = (0, 0)
        self.__previousTileCoordinates = (0, 0)

    @property
    def map(self):
        return self.__map

    @property
    def activeTileNumber(self):
        return self.__activeTileNumber

    @property
    def currentTileCoordinates(self):
        return self.__currentTileCoordinates

    @property
    def blockXSize(self):
        return self.__blockXSize

    @property
    def blockYSize(self):
        return self.__blockYSize

    @property
    def numberOfRows(self):
        return math.ceil(self.map.heightInPixels / (1.0 * self.blockYSize))

    @property
    def numberOfColumns(self):
        return math.ceil(self.map.widthInPixels / (1.0 * self.blockXSize))

    @property
    def numberOfCells(self):
        return self.numberOfRows * self.numberOfColumns

    @property
    def activeTile(self):
        return  self.__bufferedMaps[0]

    def __iter__(self):
        return self

    def __next__(self):
        if (self.activeTileNumber == 0):
            x, y = self.getTileCoordinates(self.activeTileNumber)
            self.__bufferedMaps.append(self.readImageTile(x, y))
            self.__currentTileCoordinates = (x,y)
        if (self.activeTileNumber < self.numberOfCells):
            if self.activeTileNumber > 0:
                self.__currentTileCoordinates = self.__previousTileCoordinates
            if self.activeTileNumber+1 < self.numberOfCells:
                x, y = self.getTileCoordinates(self.activeTileNumber + 1)
                self.__bufferedMaps.append(self.readImageTile(x, y))
                self.__previousTileCoordinates = (x, y)

            if self.activeTileNumber > 1:
                self.__bufferedMaps.popleft()
            self.__activeTileNumber += 1
            return self.activeTile
        raise StopIteration()

    def inLoadedTiles(self, boundingBox):
        for imageTile in self.__bufferedMaps:
            if boundingBox.inBox(imageTile.boundingBox):
                return True
        return False

    def getImageForBoundingBox(self, boundingBox):
        logging.info("getImageForBoundingBox={}".format(boundingBox))
        image = np.zeros([boundingBox.height, boundingBox.width, 3], dtype=np.uint8)
        for index, imageTile in enumerate(self.__bufferedMaps):
            if not imageTile.inImage(boundingBox):
                continue
            logging.info("Outputting image for tile index={}".format(index))
            logging.info("Bbox imageTile = {}".format(imageTile.boundingBox))
            imagePart = imageTile.partInImage(boundingBox)
            #Calculate part of boundingBox in imageTile
            partOfBoundingBoxInTile = boundingBox.overlap(imageTile.boundingBox)
            translateX = partOfBoundingBoxInTile.left - boundingBox.left
            translateY = partOfBoundingBoxInTile.top - boundingBox.top

            logging.info("partOfBoundingBox={}".format(partOfBoundingBoxInTile))

            bbox = imagePart.boundingBox
            logging.info("bbox1={}, translateX={}, translateY={}".format(bbox, translateX, translateY))
            bbox.left += translateX
            bbox.top += translateY
            logging.info("bbox2={}".format(bbox))
            image[translateY:translateY+bbox.height, translateX:translateX+bbox.width, :] = imagePart.image
        return image

    def getTileCoordinates(self, tileNumber):
        rowNumber = tileNumber // self.numberOfColumns
        columnNumber = tileNumber % self.numberOfColumns
        topX = columnNumber * self.blockXSize
        topY = rowNumber * self.blockYSize
        return (topX, topY)

    def readImageTile(self, x, y):
        image = self.map.readTile(x, y, self.blockXSize, self.blockYSize)
        tileWidth = image.shape[1]
        tileHeight = image.shape[0]
        boundingBox = BoundingBox([x, y, tileWidth, tileHeight])
        return ImageTile(image, boundingBox)

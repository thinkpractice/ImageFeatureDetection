import math

class ImageTiler(object):
    def __init__(self, map, blockXSize, blockYSize):
        self.__map = map
        self.__blockXSize = blockXSize
        self.__blockYSize = blockYSize
        self.__activeTile = 0

    @property
    def map(self):
        return self.__map

    @property
    def activeTileNumber(self):
        return self.__activeTile

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

    def __iter__(self):
        return self

    def __next__(self):
        if (self.activeTileNumber == 0):
            x, y = self.getTileCoordinates(self.activeTileNumber)
            self.map.readTile(x, y, self.blockXSize, self.blockYSize)
        if (self.activeTileNumber < self.numberOfCells):
            x, y = self.getTileCoordinates(self.activeTileNumber + 1)
            self.map.readTile(x, y, self.blockXSize, self.blockYSize)
            self.__activeTile += 1

    def getTileCoordinates(self, tileNumber):
        rowNumber = tileNumber // self.numberOfColumns
        columnNumber = tileNumber % self.numberOfColumns
        topX = columnNumber * self.blockXSize
        topY = rowNumber * self.blockYSize
        return (topX, topY)

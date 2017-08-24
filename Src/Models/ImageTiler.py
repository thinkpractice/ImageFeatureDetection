import math

class ImageTiler(object):
    def __init__(self, map, blockXSize, blockYSize):
        self.__map = map
        self.__blockXSize = blockXSize
        self.__blockYSize = blockYSize

    @property
    def map(self):
        return self.__map

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
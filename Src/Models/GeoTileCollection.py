class GeoTileCollection(object):
    def __init__(self, geoMap):
        self.__topX = 0
        self.__topY = 0
        self.__tileWidth = 300
        self.__tileHeight = 300
        self.__geoMap = geoMap

    @property
    def geoMap(self):
        return self.__geoMap

    @property
    def topX(self):
        return self.__topX

    @topX.setter
    def topX(self, value):
        self.__topX = value

    @property
    def topY(self):
        return self.__topY

    @topY.setter
    def topY(self, value):
        self.__topY = value

    @property
    def tileWidth(self):
        return self.__tileWidth

    @tileWidth.setter
    def tileWidth(self, value):
        self.__tileWidth = value

    @property
    def tileHeight(self):
        return self.__tileHeight

    @tileHeight.setter
    def tileHeight(self, value):
        self.__tileHeight = value

    @property
    def numberOfRows(self):
        return 2

    @property
    def numberOfColumns(self):
        return 2

    def getTileAt(self, row, column):
        pass

    def next(self):
        self.topX += self.tileWidth
        if self.topX >= self.geoMap.widthInPixels:
            self.topX = 0
            self.topY += self.tileHeight
            if self.topY >= self.geoMap.heightInPixels:
                self.topY = 0

    def previous(self):
        self.topX -= self.tileWidth
        if self.topX < 0:
            self.topX = self.geoMap.widthInPixels
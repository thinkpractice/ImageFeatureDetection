class GeoTileCollection(object):
    def __init__(self, geoMap):
        self.__topX = 0
        self.__topY = 0
        self.__tileWidth = 2000
        self.__tileHeight = 2000
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
    def gpsCoordinates(self):
        long1, lat1 = self.geoMap.geoTransform.getGpsCoordinateFromRaster(self.topX, self.topY + self.tileHeight)
        long2, lat2 = self.geoMap.geoTransform.getGpsCoordinateFromRaster(self.topX + self.tileWidth, self.topY)
        return (long1, lat1, long2, lat2)

    def getCurrentTile(self):
        return self.geoMap.readTile(self.topX, self.topY, self.tileWidth, self.tileHeight)

    def next(self):
        self.topX += self.tileWidth
        if self.topX >= self.geoMap.widthInPixels:
            self.topX = 0
            self.topY += self.tileHeight
            if self.topY >= self.geoMap.heightInPixels:
                self.topY = 0

    def previous(self):
        self.topX -= self.tileWidth
        if self.topX <= 0:
            self.topX = self.geoMap.widthInPixels
            self.topY -= self.tileHeight
            if self.topY <= 0:
                self.topY = self.geoMap.heightInPixels

    def inMap(self, coordinate):
        return coordinate[0] >= 0 and coordinate[0] < self.tileWidth and \
            coordinate[1] >= 0 and coordinate[1] < self.tileHeight
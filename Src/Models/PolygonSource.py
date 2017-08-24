import numpy as np


class PolygonSource(object):
    def __init__(self, geoTileCollection):
        self.__polygons = []
        self.__geoTileCollection = geoTileCollection

    @property
    def polygons(self):
        return self.__polygons

    @polygons.setter
    def polygons(self, value):
        self.__polygons = value

    @property
    def geoTileCollection(self):
        return self.__geoTileCollection

    def query(self, gpsBoundingBox):
        pass

    def getPolygonCoordinatesFromList(self, geoTileCollection, gpsCoordinates):
        geoCoordinates = np.array(gpsCoordinates)
        rasterCoordinates = self.getRasterCoordinatesFromGps(geoTileCollection, geoCoordinates)
        if not geoTileCollection.inMapArray(rasterCoordinates):
            return None
        return (rasterCoordinates[1],rasterCoordinates[0])

    def getRasterCoordinatesFromGps(self, geoTileCollection, geoCoordinates):
        gps = geoTileCollection.geoMap.geoTransform.getRasterCoordsFromGps(geoCoordinates)
        return gps[0] - geoTileCollection.topX, gps[1] - geoTileCollection.topY
import numpy as np


class PolygonSource(object):
    def __init__(self, geoMap):
        self.__polygons = []
        self.__geoMap = geoMap
        self.__numberOfPolygons = 0

    @property
    def polygons(self):
        return self.__polygons

    @polygons.setter
    def polygons(self, value):
        self.__polygons = value

    @property
    def numberOfPolygons(self):
        return self.__numberOfPolygons

    @numberOfPolygons.setter
    def numberOfPolygons(self, value):
        self.__numberOfPolygons = value

    @property
    def geoMap(self):
        return self.__geoMap

    def query(self, gpsBoundingBox):
        pass

    def getPolygonCoordinatesFromList(self, gpsCoordinates):
        geoCoordinates = np.array(gpsCoordinates)
        rasterCoordinates = self.getRasterCoordinatesFromGps(geoCoordinates)
        return (rasterCoordinates[0], rasterCoordinates[1])

    def getRasterCoordinatesFromGps(self, geoCoordinates):
        gps = self.geoMap.geoTransform.getRasterCoordsFromGps(geoCoordinates)
        return gps[0], gps[1]
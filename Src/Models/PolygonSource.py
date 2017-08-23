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
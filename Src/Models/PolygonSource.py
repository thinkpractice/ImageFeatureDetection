class PolygonSource(object):
    def __init__(self, geoTileCollection):
        self.__polygons = []
        self.__geoTileCollection = None

    @property
    def polygons(self):
        return self.polygons

    @property
    def geoTileCollection(self):
        return self.__geoTileCollection
class GeoTileCollection(object):
    def __init__(self, geoMap):
        pass

    @property
    def tileWidth(self):
        return 300

    @property
    def tileHeight(self):
        return 300

    @property
    def numberOfRows(self):
        return 2
    
    @property
    def numberOfColumns(self):
        return 2

    def getTileAt(self, row, column):
        pass

    def next(self):
        pass

    def previous(self):
        pass
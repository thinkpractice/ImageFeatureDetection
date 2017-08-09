class GeoMapTileController(object):
    def __init__(self, model, view):
        self.__model = model
        self.__view = view

    def next(self):
        geoTileCollection = self.__model.next()
        self.__view.update(geoTileCollection)

    def previous(self):
        geoTileCollection = self.__model.previous()
        self.__view.update(geoTileCollection)
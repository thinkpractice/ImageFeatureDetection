class GeoMapTileController(object):
    def __init__(self, model, view):
        self.__model = model
        self.__view = view
        self.__view.update(self.__model)
        self.__view.nextButton.on_clicked(self.nextButtonClicked)
        self.__view.previousButton.on_clicked(self.previousButtonClicked)

    def next(self):
        geoTileCollection = self.__model.next()
        self.__view.update(geoTileCollection)

    def previous(self):
        geoTileCollection = self.__model.previous()
        self.__view.update(geoTileCollection)

    def nextButtonClicked(self, event):
        print ("next clicked")
        self.next()

    def previousButtonClicked(self, event):
        print ("previous clicked")
        self.previous()
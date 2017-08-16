import matplotlib.pyplot as plt
from matplotlib.widgets import Button

class MapView(object):
    def __init__(self):
        self.__figure = plt.figure()
        self.axes = self.__figure.add_subplot(1, 1, 1)
        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        self.__nextButton = Button(axnext, 'Next')

        axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
        self.__previousButton = Button(axprev, 'Previous')

    @property
    def nextButton(self):
        return self.__nextButton

    @property
    def previousButton(self):
        return self.__previousButton

    def update(self, geoTileCollection):
        tileImage = geoTileCollection.getCurrentTile()
        self.axes.clear()
        self.axes.imshow(tileImage, interpolation='nearest', vmin=0)
        print("New tile drawn, gps coordinates={}".format(geoTileCollection.gpsCoordinates))

        plt.draw()

    def show(self):
        plt.show()










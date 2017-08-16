import matplotlib.pyplot as plt
from matplotlib.widgets import Button

class MapView(object):
    def __init__(self):
        self.__nextButton = None
        self.__previousButton = None

    @property
    def nextButton(self):
        return self.__nextButton

    @property
    def previousButton(self):
        return self.__previousButton

    def update(self, geoTileCollection):
        tileImage = geoTileCollection.getCurrentTile()
        plt.imshow(tileImage, interpolation='nearest', vmin=0)

        axnext = plt.axes([0.81, 0.05, 0.1, 0.075])
        self.__nextButton = Button(axnext, 'Next')

        axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
        self.__previousButton = Button(axprev, 'Previous')
        plt.show()










import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import osmapi

def pretty(d, indent=0):
    for key, value in d.items():
        print('\t' * indent + str(key))
        if isinstance(value, dict):
            pretty(value, indent + 1)
        else:
            print('\t' * (indent + 1) + str(value))

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
        self.getOsmInfo(geoTileCollection.gpsCoordinates)

    def show(self):
        plt.show()

    def getOsmInfo(self, gpsCoordinates):
        api = osmapi.OsmApi()
        jsonList = api.Map(gpsCoordinates[0], gpsCoordinates[1], gpsCoordinates[2], gpsCoordinates[3])
        nodes = [dict for dict in jsonList if dict["type"].lower() == "way"] #"node"]
        bagNodes = [dict for dict in nodes if dict["data"]["tag"].get("source", "").lower() == "bag"]
        for dict in bagNodes:
            pretty(dict)











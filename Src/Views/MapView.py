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
        self.__figure, self.axes = plt.subplots()
        #self.axes = self.__figure.add_subplot(1, 1, 1)
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
        self.axes.imshow(tileImage, extent=[0, geoTileCollection.tileWidth, geoTileCollection.tileHeight, 0])
        print("New tile drawn, gps coordinates={}".format(geoTileCollection.gpsCoordinates))

        self.getOsmInfo(geoTileCollection)

    def show(self):
        plt.show()

    def getOsmInfo(self, geoTileCollection):
        gpsCoordinates = geoTileCollection.gpsCoordinates
        api = osmapi.OsmApi()
        jsonList = api.Map(gpsCoordinates[0], gpsCoordinates[1], gpsCoordinates[2], gpsCoordinates[3])
        nodes = [dict for dict in jsonList if dict["type"].lower() == "node"] #== "way"]
        bagNodes = [dict for dict in nodes if dict["data"]["tag"].get("source", "").lower() == "bag"]
        for dict in bagNodes:
            pretty(dict)
        rasterX, rasterY = self.getRasterCoordinatesFor(geoTileCollection, bagNodes)
        self.axes.scatter(x=rasterX, y=rasterY)

    def getRasterCoordinatesFor(self, geoTileCollection, bagNodes):
        rasterX = []
        rasterY = []
        for dict in bagNodes:
            data = dict["data"]
            if "lon" not in data or "lat" not in data:
                continue
            longitude = data["lon"]
            latitude = data["lat"]
            gps = geoTileCollection.geoMap.geoTransform.getRasterCoordsFromGps(longitude, latitude)
            rasterX.append(gps[0] - geoTileCollection.topX)
            rasterY.append(gps[1] - geoTileCollection.topY)
        return rasterX, rasterY











import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from skimage.draw import polygon
from Src.Models.OSMPolygonSource import OSMPolygonSource
from Src.Models.Thumbnailer import Thumbnailer


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
        self.getOsmInfo(geoTileCollection, tileImage)

        self.axes.clear()
        self.axes.imshow(tileImage, extent=[0, geoTileCollection.tileWidth, geoTileCollection.tileHeight, 0])
        print("New tile drawn, gps coordinates={}".format(geoTileCollection.gpsCoordinates))

    def show(self):
        plt.show()

    def drawPolygons(self, polygons, tileImage):
        for _, polygonArray in polygons:
            self.drawPolygon(tileImage, polygonArray)

    def getOsmInfo(self, geoTileCollection, tileImage):
        osmPolygonSource = OSMPolygonSource(geoTileCollection)
        osmPolygonSource.query(geoTileCollection.gpsCoordinates)
        self.drawPolygons(osmPolygonSource.polygons, tileImage)

        osmPolygonSource.query(geoTileCollection.gpsCoordinates)
        thumbnailer = Thumbnailer(r"/home/tjadejong/Documents/CBS/ZonnePanelen/Images")
        thumbnailer.writeThumbnails(osmPolygonSource.polygons, tileImage)

    # def retrieveWholeMapInfo(self, geoTileCollection):
    #     print("Retrieving info for whole map")
    #     result = self.performMapQuery(geoTileCollection.geoMap.gpsCoordinates)
    #     print("Query executed")
    #
    #     numberOfWays = 0
    #     numberOfNodes = 0
    #     for way in result.ways:
    #         numberOfWays += 1
    #         print("Name: %s" % way.tags.get("id", "n/a"))
    #         # print("  Highway: %s" % way.tags.get("highway", "n/a"))
    #         print("  Nodes:")
    #         for node in way.nodes:
    #             numberOfNodes += 1
    #             print("    Lat: %f, Lon: %f" % (node.lat, node.lon))
    #     print("Number of ways: {}, number of nodes: {}".format(numberOfWays, numberOfNodes))

    def getPolygonFromCoords(self, polygonArray):
        xCoords, yCoords = polygonArray
        rr, cc = polygon(xCoords, yCoords)
        return rr, cc

    def drawPolygon(self, tileImage, polygonArray):
        rr, cc = self.getPolygonFromCoords(polygonArray)
        tileImage[rr, cc] = (0,0,255)

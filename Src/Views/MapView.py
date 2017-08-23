import os
import matplotlib.pyplot as plt
import numpy as np
import osmapi
import overpy
import json

import time
from matplotlib.widgets import Button
from skimage.draw import polygon
from skimage.io import imsave
from skimage.measure import label, regionprops

from Src.Models.OSMPolygonSource import OSMPolygonSource


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
        #self.retrieveWholeMapInfo(geoTileCollection)
        self.drawPolygons(osmPolygonSource.polygons, tileImage)
        self.writeThumbnails(osmPolygonSource.polygons, tileImage)

    def retrieveWholeMapInfo(self, geoTileCollection):
        print("Retrieving info for whole map")
        result = self.performMapQuery(geoTileCollection.geoMap.gpsCoordinates)
        print("Query executed")

        numberOfWays = 0
        numberOfNodes = 0
        for way in result.ways:
            numberOfWays += 1
            print("Name: %s" % way.tags.get("id", "n/a"))
            # print("  Highway: %s" % way.tags.get("highway", "n/a"))
            print("  Nodes:")
            for node in way.nodes:
                numberOfNodes += 1
                print("    Lat: %f, Lon: %f" % (node.lat, node.lon))
        print("Number of ways: {}, number of nodes: {}".format(numberOfWays, numberOfNodes))

    def performMapQuery(self, gpsBoundary):
        overApi = overpy.Overpass()
        query = """
            way({},{},{},{})["source" = "BAG"];
            (._;>;);
            out body;
            """.format(gpsBoundary[1], gpsBoundary[0], gpsBoundary[3], gpsBoundary[2])
        print(query)
        result = overApi.query(query)
        return result

    def writeThumbnails(self, polygons, tileImage):
        startTime = time.time()
        numberOfThumbnails = 0
        for imageId, polygonArray in polygons:
            self.writeThumbnail(imageId, polygonArray, tileImage)
            numberOfThumbnails += 1
        endTime = time.time()
        print("Wrote {} thumbnails in {}s".format(numberOfThumbnails, endTime-startTime))

    def writeThumbnail(self, imageId, polygonArray, tileImage):
        boundingRect = self.getBoundingBox(polygonArray)
        polygonImage = self.getRectangleFromImage(tileImage, boundingRect)

        translatedPolygonCoords = self.translateCoords(boundingRect, polygonArray)
        maskedImage = self.maskImageWithPolygon(polygonImage, translatedPolygonCoords)

        filename = os.path.join(r"/home/tjadejong/Documents/CBS/ZonnePanelen/Images", "{}.png".format(imageId))
        imsave(filename, maskedImage)
        print("Writing maskedImage: {}".format(filename))

    def maskImageWithPolygon(self, polygonImage, translatedPolygonCoords):
        rr, cc = self.getPolygonFromCoords(translatedPolygonCoords)
        maskedImage = polygonImage.copy()
        imageMask = np.zeros([maskedImage.shape[0], maskedImage.shape[1]], dtype=np.uint8)
        imageMask[rr, cc] = 1
        imageMask = imageMask != 1
        maskedImage[imageMask] = (0, 0, 0)
        return maskedImage

    def translateCoords(self, boundingRect, polygonArray):
        xCoords, yCoords = polygonArray
        translatedXCoords = xCoords - boundingRect[0] - 1
        translatedYCoords = yCoords - boundingRect[1] - 1
        return translatedXCoords, translatedYCoords

    def getPolygonFromCoords(self, polygonArray):
        xCoords, yCoords = polygonArray
        rr, cc = polygon(xCoords, yCoords)
        return rr, cc

    def getBoundingBox(self, polygonArray):
        xCoords, yCoords = polygonArray
        return (int(xCoords.min()), int(yCoords.min()), int(xCoords.max()), int(yCoords.max()))

    def getRectangleFromImage(self, image, boundingRect):
        minX = boundingRect[0]
        minY = boundingRect[1]
        maxX = boundingRect[2]
        maxY = boundingRect[3]
        return image[minX:maxX, minY:maxY, :]

    def drawPolygon(self, tileImage, polygonArray):
        rr, cc = self.getPolygonFromCoords(polygonArray)
        tileImage[rr, cc] = (0,0,255)

    def getPolygonsFor(self, geoTileCollection, ways):
        for way in ways:
            imageId = way.id
            polygonCoordinates = self.getPolygonCoordinatesFromList(geoTileCollection, way.nodes)
            if not polygonCoordinates:
                continue
            yield imageId, polygonCoordinates

    def getPolygonCoordinatesFromList(self, geoTileCollection, nodes):
        geoCoordinates = np.array([[node.lon, node.lat] for node in nodes])
        rasterCoordinates = self.getRasterCoordinatesFromGps(geoTileCollection, geoCoordinates)
        if not geoTileCollection.inMapArray(rasterCoordinates):
            return None
        return (rasterCoordinates[1],rasterCoordinates[0])

    def getRasterCoordinatesFromGps(self, geoTileCollection, geoCoordinates):
        gps = geoTileCollection.geoMap.geoTransform.getRasterCoordsFromGps(geoCoordinates)
        return gps[0] - geoTileCollection.topX, gps[1] - geoTileCollection.topY


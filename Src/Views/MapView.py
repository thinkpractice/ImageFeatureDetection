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

    def getOsmInfo(self, geoTileCollection, tileImage):
        gpsCoordinates = geoTileCollection.gpsCoordinates
        api = osmapi.OsmApi()
        jsonList = api.Map(gpsCoordinates[0], gpsCoordinates[1], gpsCoordinates[2], gpsCoordinates[3])
        #nodes = [dict for dict in jsonList if dict["type"].lower() == "node"]
        nodes = [dict for dict in jsonList if dict["type"].lower() == "way"]
        bagNodes = [dict for dict in nodes if dict["data"]["tag"].get("source", "").lower() == "bag"]
        for dict in bagNodes:
            pretty(dict)

        self.retrieveWholeMapInfo(geoTileCollection)
        #with open(r"/home/tjadejong/Documents/CBS/ZonnePanelen/Images/bag_nodes.json", "w") as jsonFile:
        #    json.dump(bagNodes, jsonFile)
        #rasterX, rasterY = self.getRasterCoordinatesFor(geoTileCollection, bagNodes)
        #self.axes.scatter(x=rasterX, y=rasterY)
        self.writeThumbnails(bagNodes, geoTileCollection, tileImage)

    def retrieveWholeMapInfo(self, geoTileCollection):
        print("Retrieving info for whole map")
        mapGps = geoTileCollection.geoMap.gpsCoordinates
        overApi = overpy.Overpass()
        query = """
            way({},{},{},{})["source" = "BAG"];
            (._;>;);
            out body;
            """.format(mapGps[1], mapGps[0], mapGps[3], mapGps[2])
        print(query)
        result = overApi.query(query)
        print("Query executed")

        numberOfWays = 0
        numberOfNodes = 0
        for way in result.ways:
            numberOfWays += 1
            print("Name: %s" % way.tags.get("name", "n/a"))
            # print("  Highway: %s" % way.tags.get("highway", "n/a"))
            print("  Nodes:")
            for node in way.nodes:
                numberOfNodes += 1
                print("    Lat: %f, Lon: %f" % (node.lat, node.lon))
        print("Number of ways: {}, number of nodes: {}".format(numberOfWays, numberOfNodes))

    def writeThumbnails(self, bagNodes, geoTileCollection, tileImage):
        startTime = time.time()
        numberOfThumbnails = 0
        for imageId, polygonArray in self.getPolygonsFor(geoTileCollection, bagNodes):
            self.writeThumbnail(geoTileCollection, imageId, polygonArray, tileImage)

            self.drawPolygon(tileImage, polygonArray)
            numberOfThumbnails += 1
        endTime = time.time()
        print("Wrote {} thumbnails in {}s".format(numberOfThumbnails, endTime-startTime))


    def writeThumbnail(self, geoTileCollection, imageId, polygonArray, tileImage):
        maskedImage = tileImage.copy()
        rr, cc = polygonArray
        imageMask = np.zeros([geoTileCollection.tileHeight, geoTileCollection.tileWidth], dtype=np.uint8)
        imageMask[rr, cc] = 1
        labeledImage = label(imageMask)
        regions = regionprops(labeledImage)
        boundingRect = regions[0].bbox
        imageMask = imageMask != 1
        maskedImage[imageMask] = (0, 0, 0)
        minX = boundingRect[0]
        minY = boundingRect[1]
        maxX = boundingRect[2]
        maxY = boundingRect[3]
        maskedImage = maskedImage[minX:maxX, minY:maxY, :]
        filename = os.path.join(r"/home/tjadejong/Documents/CBS/ZonnePanelen/Images", "{}.png".format(imageId))
        imsave(filename, maskedImage)
        print("Writing maskedImage: {}".format(filename))

    def drawPolygon(self, tileImage, polygonArray):
        rr, cc = polygonArray
        tileImage[rr, cc] = (0,0,255)

    def getRasterCoordinatesFor(self, geoTileCollection, bagNodes):
        rasterX = []
        rasterY = []
        for dict in bagNodes:
            data = dict["data"]
            if "lon" not in data or "lat" not in data:
                continue
            longitude, latitude = self.getGpsCoordinateFromDict(data)
            x, y = self.getRasterCoordinatesFromGps(geoTileCollection, longitude, latitude)
            rasterX.append(x)
            rasterY.append(y)
        return rasterX, rasterY

    def getGpsCoordinateFromDict(self, data):
        return data["lon"], data["lat"]

    def getRasterCoordinatesFromGps(self, geoTileCollection, longitude, latitude):
        gps = geoTileCollection.geoMap.geoTransform.getRasterCoordsFromGps(longitude, latitude)
        return gps[0] - geoTileCollection.topX, gps[1] - geoTileCollection.topY

    def getPolygonsFor(self, geoTileCollection, bagNodes):
        for nodeDict in bagNodes:
            data = nodeDict["data"]
            if "tag" in data and "building" in data["tag"] and "nd" in data and "id" in data and "source" in data["tag"]:
                imageId = data["id"]
                #also other building types are possible house, appartments, etc.
                #isBuilding = data["tag"]["building"].lower() == "yes"
                #Only export BAG tags
                if data["tag"]["source"].lower() != "bag":
                    continue
                nodeIds = data["nd"]
                api = osmapi.OsmApi()
                nodesDict = api.NodesGet(nodeIds)
                #pretty(nodesDict)
                polygonCoordinates = self.getPolygonCoordinatesFromList(geoTileCollection, nodeIds, nodesDict)
                if not polygonCoordinates:
                    continue
                yield imageId, polygonCoordinates

    def getPolygonCoordinatesFromList(self, geoTileCollection, nodeIds, nodesDict):
        polygonCoordinates = dict()
        for key, value in nodesDict.items():
            if "lat" not in value and "lon" not in value:
                continue

            longitude, latitude = self.getGpsCoordinateFromDict(value)
            coordinate = self.getRasterCoordinatesFromGps(geoTileCollection, longitude, latitude)
            if not geoTileCollection.inMap(coordinate):
                return None
            polygonCoordinates[key] = coordinate

        xCoords = [polygonCoordinates[nodeId][0] for nodeId in nodeIds]
        yCoords = [polygonCoordinates[nodeId][1] for nodeId in nodeIds]
        return polygon(np.array(yCoords),np.array(xCoords))








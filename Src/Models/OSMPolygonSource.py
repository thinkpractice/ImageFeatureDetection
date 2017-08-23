from Src.Models.PolygonSource import PolygonSource
import overpy
import numpy as np

class OSMPolygonSource(PolygonSource):
    def __init__(self, geoTileCollection):
        super().__init__(geoTileCollection)

    def query(self, gpsBoundingBox):
        results = self.performMapQuery(gpsBoundingBox)
        self.polygons = self.getPolygonsFor(self, results.ways)

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



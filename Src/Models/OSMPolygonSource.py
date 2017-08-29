import overpy

from Src.Models.PolygonSource import PolygonSource


class OSMPolygonSource(PolygonSource):
    def __init__(self, geoMap):
        super().__init__(geoMap)

    def query(self, gpsBoundingBox):
        results = self.performMapQuery(gpsBoundingBox)
        self.polygons = self.getPolygonsFor(results.ways)

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

    def getPolygonsFor(self, ways):
        for way in ways:
            imageId = way.id
            polygonCoordinates = self.getPolygonCoordinatesFromList([[node.lon, node.lat] for node in way.nodes])
            if not polygonCoordinates:
                continue
            yield imageId, polygonCoordinates



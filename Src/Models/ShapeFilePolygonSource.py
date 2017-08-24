from Src.Models.PolygonSource import PolygonSource
import shapefile

class ShapeFilePolygonSource(PolygonSource):
    def __init__(self, geoTileCollection):
        super().__init__(geoTileCollection)

    def query(self, gpsBoundingBox):
        buildings = []
        buildingShapes = shapefile.Reader(r"/home/tjadejong/Documents/CBS/ZonnePanelen/Shapes/pand_parkstad_wgs84")
        for buildingShape in buildingShapes.iterShapeRecords():
            shapeBoundingBox = buildingShape.shape.bbox
            if self.withinBox(shapeBoundingBox, gpsBoundingBox):
                buildings.append(buildingShape)
        self.polygons = self.getPolygonsFor(self.geoTileCollection, buildings)

    def withinBox(self, shapeBbox, gpsBbox):
        return (shapeBbox[0] > gpsBbox[0] or shapeBbox[2] < gpsBbox[2]) and \
                (shapeBbox[1] > gpsBbox[1] or shapeBbox[3] < gpsBbox[3])

    def getPolygonsFor(self, geoTileCollection, buildings):
        for building in buildings:
            imageId = building.record[0]
            polygonCoordinates = self.getPolygonCoordinatesFromList(geoTileCollection,[[node[0], node[1]] for node in building.shape.points])
            if not polygonCoordinates:
                continue
            yield imageId, polygonCoordinates

    def indexOfField(self, shapefile, fieldName):
        for index, fieldTuple in enumerate(shapefile.fields):
            if fieldTuple[0] == fieldName:
                return index
        return None


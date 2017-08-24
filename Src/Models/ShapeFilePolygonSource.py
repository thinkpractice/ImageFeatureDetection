from Src.Models.PolygonSource import PolygonSource
import shapefile

class ShapeFilePolygonSource(PolygonSource):
    def __init__(self, geoTileCollection):
        super().__init__(geoTileCollection)

    def query(self, gpsBoundingBox):
        buildings = []
        buildingShapes = shapefile.Reader(r"/home/tjadejong/Documents/CBS/ZonnePanelen/Shapes/pand_parkstad_wgs84")
        for buildingShape in buildingShapes.iterShapes():
            shapeBoundingBox = buildingShape.bbox
            if self.withinBox(shapeBoundingBox, gpsBoundingBox):
                buildings.append(buildingShape)
        self.polygons = self.getPolygonsFor(self.geoTileCollection, buildings)

    def withinBox(self, shapeBbox, gpsBbox):
        return (shapeBbox[0] >= gpsBbox[0] or shapeBbox[2] <= gpsBbox[2]) and \
                (shapeBbox[1] >= gpsBbox[1] or shapeBbox[3] <= gpsBbox[3])

    def getPolygonsFor(self, geoTileCollection, buildings):
        for building in buildings:
            imageId = building.PNDID
            polygonCoordinates = self.getPolygonCoordinatesFromList(geoTileCollection,[[node.lon, node.lat] for node in building.points])
            if not polygonCoordinates:
                continue
            yield imageId, polygonCoordinates

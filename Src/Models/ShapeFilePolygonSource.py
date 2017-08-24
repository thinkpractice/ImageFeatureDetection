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

    def withinBox(self, shapeBbox, gpsBbox):
        return False
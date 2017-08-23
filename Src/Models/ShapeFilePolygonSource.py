from Src.Models.PolygonSource import PolygonSource
import shapefile

class ShapeFilePolygonSource(PolygonSource):
    def __init__(self, geoTileCollection):
        super().__init__(geoTileCollection)

    def query(self, gpsBoundingBox):
        sf = shapefile.Reader(r"/home/tjadejong/Documents/CBS/ZonnePanelen/Shapes/pand_parkstad_wgs84")
        shapes = sf.shapes()
from Src.Models.ImageTiler import ImageTiler
from Src.Models.Thumbnailer import Thumbnailer
from Src.Models.OSMPolygonSource import OSMPolygonSource
from Src.Models.ShapeFilePolygonSource import ShapeFilePolygonSource

class GeoMapThumbnailer(object):
    def __init__(self, map):
        self.__map = map
        self.__exportDirectory = r"/home/tjadejong/Documents/CBS/ZonnePanelen/Images"
        self.__exportedImages = dict()

    @property
    def map(self):
        return self.__map

    @property
    def exportDirectory(self):
        return self.__exportDirectory

    @property
    def exportedImages(self):
        return self.__exportedImages

    def createThumbnails(self, boundingBox):
        imageTiler = ImageTiler(self.map, self.map.blockXSize, 512)
        allPolygons = self.getAllPolygons(self.map, boundingBox)
        for imageTile in imageTiler:
            polygons = self.getPolygonsInImageTile(imageTile, allPolygons)

            thumbnailer = Thumbnailer(self.exportDirectory)
            thumbnailer.writeThumbnails(polygons, imageTile)

    def getAllPolygons(self, geoTileCollection, boundingBox):
        polygonSource = self.getPolygonSource(geoTileCollection, False)
        polygonSource.query(boundingBox)
        return polygonSource.polygons

    def getPolygonsInImageTile(self, imageTile, polygons):
        return (polygon for polygon in polygons if imageTile.inImage(polygon.boundingBox))

    def getPolygonSource(self, map, openStreetMap):
        if openStreetMap:
            return OSMPolygonSource(map)
        return ShapeFilePolygonSource(map)
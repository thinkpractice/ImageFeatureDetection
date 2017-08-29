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
        while next(imageTiler):
            print("Processing imageTile with {}".format(imageTiler.activeTile.boundingBox))
            polygons = self.getPolygonsInImageTile(imageTiler.activeTile, allPolygons)
            thumbnailer = Thumbnailer(self.exportDirectory)
            exportedImagesIds = thumbnailer.writeThumbnails(polygons, imageTiler)
            for imageId in exportedImagesIds:
                self.exportedImages[imageId] = True

    def getAllPolygons(self, map, boundingBox):
        polygonSource = self.getPolygonSource(map, False)
        polygonSource.query(boundingBox)
        return polygonSource.polygons

    def getPolygonsInImageTile(self, imageTile, polygons):
        return (polygon for imageId, polygon in polygons if self.doesPolygonNeedsToBeExportedForTile(imageTile, imageId, polygon))

    def doesPolygonNeedsToBeExportedForTile(self, imageTile, imageId, polygon):
        return imageTile.inImage(polygon.boundingBox) and not self.exportedImages.get(imageId, False)

    def getPolygonSource(self, map, openStreetMap):
        if openStreetMap:
            return OSMPolygonSource(map)
        return ShapeFilePolygonSource(map)
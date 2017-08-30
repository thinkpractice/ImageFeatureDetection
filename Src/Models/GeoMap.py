from gdalconst import *
from Src.Models.GeoTransform import GeoTransform
from Src.Models.BoundingBox import BoundingBox
import gdal
import numpy

class GeoMap(object):
    """This class represents a standard interface to a GeoMap.
    """
    def __init__(self, dataset):
        """Constructor

        :param gdal dataset: the gdal dataset for a GeoTiff file
        """
        self.__dataset = dataset

    @property
    def dataset(self):
        return self.__dataset

    @property
    def widthInPixels(self):
        """Returns the width in pixels of the opened raster map

        :return: the width in pixels

        :rtype: int
        """
        return self.dataset.RasterXSize

    @property
    def heightInPixels(self):
        """Returns the height in pixels of the opened raster map

        :return: the height in pixels

        :rtype: int
        """
        return self.dataset.RasterYSize

    @property
    def boundingBox(self):
        return BoundingBox([0, 0, self.widthInPixels, self.heightInPixels])

    @property
    def blockXSize(self):
        return self.dataset.GetRasterBand(1).GetBlockSize()[0]

    @property
    def blockYSize(self):
        return self.dataset.GetRasterBand(1).GetBlockSize()[1]

    @property
    def geoTransform(self):
        transform = self.dataset.GetGeoTransform()
        return GeoTransform(transform)

    @property
    def gpsCoordinates(self):
        """Returns the gps coordinates of the whole area of the map. The gps coordinates indicate
        the bottom left corner and the top right corner in the image.

        :return: a tuple with the longitude and latitude of the bottom left corner and the
        longitude and latitude of top right corner.

        :rtype: tuple[4]
        """
        long1, lat1 = self.geoTransform.getGpsCoordinateFromRaster(0, self.heightInPixels)
        long2, lat2 = self.geoTransform.getGpsCoordinateFromRaster(self.widthInPixels, 0)
        return (long1, lat1, long2, lat2)

    @classmethod
    def open(cls, filename):
        """Opens a GeoTiff file with filename and returns a GeoMap object for it

        :param str filename: the filename of the GeoTiff file to open

        :return: a GeoMap object for the GeoTiff file

        :rtype: GeoMap
        """
        dataset = gdal.Open(filename, GA_ReadOnly)
        return GeoMap(dataset)

    def readTile(self, startX, startY, width, height):
        """Reads a tile from the map of a size specified by the method parameters

        :param int startX: the x position of the topleft corner of the tile in pixels
        :param int startY: the y position of the topleft corner of the tile in pixels
        :param int width: the width of the tile in pixels
        :param int height: the height of the tile in pixels

        :return: a numpy array with the RGB information for the tile

        :rtype: ndarray
        """
        R = self.dataset.GetRasterBand(1)
        G = self.dataset.GetRasterBand(2)
        B = self.dataset.GetRasterBand(3)

        print("readTile({},{},{},{})".format(startX, startY, width, height))

        redArray = R.ReadAsArray(xoff=startX, yoff=startY, win_xsize=width, win_ysize=height)
        greenArray = G.ReadAsArray(xoff=startX, yoff=startY, win_xsize=width, win_ysize=height)
        blueArray = B.ReadAsArray(xoff=startX, yoff=startY, win_xsize=width, win_ysize=height)

        redArray = numpy.expand_dims(redArray, axis=2)
        greenArray = numpy.expand_dims(greenArray, axis=2)
        blueArray = numpy.expand_dims(blueArray, axis=2)

        stacked = numpy.append(redArray, greenArray, axis=2)
        return numpy.append(stacked, blueArray, axis=2)


from gdalconst import *
import gdal
import numpy

class GeoMap(object):
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
        """

        :param int startX:
        :param int startY:
        :param int width:
        :param int height:

        :return:
        """
        R = self.dataset.GetRasterBand(1)
        G = self.dataset.GetRasterBand(2)
        B = self.dataset.GetRasterBand(3)

        redArray = R.ReadAsArray(xoff=startX, yoff=startY, win_xsize=width, win_ysize=height)
        greenArray = G.ReadAsArray(xoff=startX, yoff=startY, win_xsize=width, win_ysize=height)
        blueArray = B.ReadAsArray(xoff=startX, yoff=startY, win_xsize=width, win_ysize=height)

        redArray = numpy.expand_dims(redArray, axis=2)
        greenArray = numpy.expand_dims(greenArray, axis=2)
        blueArray = numpy.expand_dims(blueArray, axis=2)

        stacked = numpy.append(redArray, greenArray, axis=2)
        return numpy.append(stacked, blueArray, axis=2)
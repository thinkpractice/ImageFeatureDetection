from pyproj import Proj, transform

class GeoTransform(object):
    """This class performs all the necessary transformations from one projection coordinate system
    to another
    """
    def __init__(self, transform):
        """Constructor

        :param List transform: the affine transformation coefficients for transforming between pixel coordinates
        and map projection coordinates.
        """
        self.__transform = transform

    @property
    def transform(self):
        return self.__transform

    def getProjectionCoords(self, x, y):
        """This method converts the pixel coordinate (x, y) into the coordinate system used
        by the projection of the map.
        The equations used are:

        Xp = transform[0] + x * transform[1] + y * tranform[2]
        
        Yp = transform[3] + x * transform[4] + y * transform[5]
        
        :param int x: the pixel x coordinate
        
        :param int y: the pixel y coordinate

        :return: a tuple with the coordinates in projection space.

        :rtype: tuple (double, double)
        """
        Xp = self.transform[0] + x * self.transform[1] + y * self.transform[2]
        Yp = self.transform[3] + x * self.transform[4] + y * self.transform[5]
        return (Xp, Yp)

    def getRasterCoords(self, Xp, Yp):
        """This method converts a coordinate in projection space to a raster coordinate.

        :param double Xp: the x coordinate in projection space

        :param double Yp: the y coordinate in projection space

        :return: a tuple with the coordinate in raster coordinates

        :rtype: tuple (int, int)
        """
        x = self.numeratorX(Xp, Yp) / self.denominatorX()
        y = self.numeratorY(Xp, Yp) / self.denominatorY()
        return (int(x), y)

    def numeratorY(self, Xp, Yp):
        return self.transform[1] * (Yp - self.transform[3]) - self.transform[4] * Xp + self.transform[4] * \
                                                              self.transform[0]
    def denominatorY(self):
        return self.transform[1] * self.transform[5] - self.transform[2] * self.transform[4]

    def numeratorX(self, Xp, Yp):
        return self.transform[5] * Xp - self.transform[0] * self.transform[5] - self.transform[2] * Yp + self.transform[
                                                                                                             2] * \
                                                                                                         self.transform[3]
    def denominatorX(self):
        return self.transform[1] * self.transform[5] - self.transform[4] * self.transform[2]

    def getGpsCoordinate(self, mapX, mapY):
        mapProjection = Proj(init='epsg:28992')
        gpsProjection = Proj(init='epsg:4326')
        longitude, latitude = transform(mapProjection, gpsProjection, mapX, mapY)
        return longitude, latitude

    def getGpsCoordinateFromRaster(self, x, y):
        Xp, Yp = self.getProjectionCoords(x, y)
        return self.getGpsCoordinate(Xp, Yp)


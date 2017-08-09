class GeoTransform(object):
    """Docstring for Ge. """
    def __init__(self, transform):
        """Constructor

        :param List transform: the affine transformation coefficients for transforming between pixel coordinates
        and map projection coordinates.
        """
        self.__transform = transform

    def getProjectionCoords(self, x, y):
        """This method converts the pixel coordinates (x, y) into the coordinate system used
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
        Yp = 0
        return (Xp, Yp)


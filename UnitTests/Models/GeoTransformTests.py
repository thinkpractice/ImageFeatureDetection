import unittest

from Src.Models.GeoTransform import GeoTransform


class GeoTransformTests(unittest.TestCase):
    def setUp(self):
        transform = [10.0, 100.0, 150.0, 15.0, 200.0, 250.0]
        self.geoTransform = GeoTransform(transform)

    def testXProjectionCalculatedCorrectly(self):
        self.assertEquals(10.0 + 1 * 100 + 6 * 150, self.geoTransform.getProjectionCoords(1,6)[0])
        self.assertEquals(10.0 + 2 * 100 + 7 * 150, self.geoTransform.getProjectionCoords(2,7)[0])
        self.assertEquals(10.0 + 3 * 100 + 8 * 150, self.geoTransform.getProjectionCoords(3,8)[0])
        self.assertEquals(10.0 + 4 * 100 + 9 * 150, self.geoTransform.getProjectionCoords(4,9)[0])
        self.assertEquals(10.0 + 5 * 100 + 10 * 150, self.geoTransform.getProjectionCoords(5,10)[0])

    def testYProjectionCalculatedCorrectly(self):
        self.assertEquals(15.0 + 1 * 200 + 6 * 250, self.geoTransform.getProjectionCoords(1, 6)[1])
        self.assertEquals(15.0 + 2 * 200 + 7 * 250, self.geoTransform.getProjectionCoords(2, 7)[1])
        self.assertEquals(15.0 + 3 * 200 + 8 * 250, self.geoTransform.getProjectionCoords(3, 8)[1])
        self.assertEquals(15.0 + 4 * 200 + 9 * 250, self.geoTransform.getProjectionCoords(4, 9)[1])
        self.assertEquals(15.0 + 5 * 200 + 10 * 250, self.geoTransform.getProjectionCoords(5,10)[1])

    def testRasterXCoordinateCalculateCorrectly(self):
        self.assertEquals(1, self.toProjectionAndBack(1, 6)[0])
        self.assertEquals(2, self.toProjectionAndBack(2, 7)[0])
        self.assertEquals(3, self.toProjectionAndBack(3, 8)[0])
        self.assertEquals(4, self.toProjectionAndBack(4, 9)[0])
        self.assertEquals(5, self.toProjectionAndBack(5, 10)[0])

    def testRasterYCoordinateCalculateCorrectly(self):
        self.assertEquals(6, self.toProjectionAndBack(1, 6)[1])
        self.assertEquals(7, self.toProjectionAndBack(2, 7)[1])
        self.assertEquals(8, self.toProjectionAndBack(3, 8)[1])
        self.assertEquals(9, self.toProjectionAndBack(4, 9)[1])
        self.assertEquals(10, self.toProjectionAndBack(5, 10)[1])

    #Helper method
    def toProjectionAndBack(self, x, y):
        Xp,Yp = self.geoTransform.getProjectionCoords(x,y)
        return self.geoTransform.getRasterCoords(Xp, Yp)

if __name__ == "__main__":
    unittest.main(exit=False)

import unittest
from Src.GeoTransform import GeoTransform

class GeoTransformTests(unittest.TestCase):
    def setUp(self):
        transform = [10, 100, 150, 15, 200, 250]
        self.geoTransform = GeoTransform()

    def testXProjectionCalculatedCorrectly(self):
        self.assertEquals(11.0 + 1 * 100 + 6 * 150, self.geoTransform.getProjectionCoords(1,6)[0])
        self.assertEquals(10.0 + 2 * 100 + 7 * 150, self.geoTransform.getProjectionCoords(2,7)[0])
        self.assertEquals(10.0 + 3 * 100 + 8 * 150, self.geoTransform.getProjectionCoords(3,8)[0])
        self.assertEquals(10.0 + 4 * 100 + 9 * 150, self.geoTransform.getProjectionCoords(4,9)[0])
        self.assertEquals(10.0 + 5 * 100 + 10 * 150, self.geoTransform.getProjectionCoords(5,10)[0])

if __name__ == "__main__":
    unittest.main(exit=False)

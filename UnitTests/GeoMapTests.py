import unittest

from Src.Models.GeoMap import GeoMap


class GeoMapTests(unittest.TestCase):
    def setUp(self):
        self.geoMap = GeoMap.open(r"/home/tjadejong/Documents/CBS/ZonnePanelen/Parkstad.tif")

    def testReturnsWidthInPixelsCorrectly(self):
        self.assertEquals(52281, self.geoMap.widthInPixels)

    def testReturnsHeightInPixelsCorrectly(self):
        self.assertEquals(31844, self.geoMap.heightInPixels)

if __name__ == '__main__':
    unittest.main()

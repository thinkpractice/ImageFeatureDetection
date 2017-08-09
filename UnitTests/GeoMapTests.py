import unittest
import gdal
from gdalconst import *
from Src.GeoMap import GeoMap

class GeoMapTests(unittest.TestCase):
    def setUp(self):
        self.dataset = gdal.Open(r"/home/tjadejong/Documents/CBS/ZonnePanelen/Parkstad.tif", GA_ReadOnly)
        self.geoMap = GeoMap(self.dataset)

    def testDataSetSetCorrectly(self):
        self.assertEquals(self.dataset, self.geoMap.dataset)

    def testReturnsWidthInPixelsCorrectly(self):
        self.assertEquals(52281, self.geoMap.widthInPixels)

    def testReturnsHeightInPixelsCorrectly(self):
        self.assertEquals(31844, self.geoMap.heightInPixels)

if __name__ == '__main__':
    unittest.main()

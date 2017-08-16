import unittest
from unittest.mock import MagicMock, PropertyMock
from Src.Models.GeoTileCollection import GeoTileCollection

class GeoTileCollectionTests(unittest.TestCase):
    def setUp(self):
        self.geoMap = MagicMock()
        type(self.geoMap).widthInPixels = PropertyMock(return_value=100)
        type(self.geoMap).heightInPixels = PropertyMock(return_value=100)
        self.geoTileCollection = GeoTileCollection(self.geoMap)
        self.geoTileCollection.tileWidth = 30
        self.geoTileCollection.tileHeight = 30

    def testNextMovesTopXByIncrement(self):
        self.assertEqual(0, self.geoTileCollection.topX)
        self.geoTileCollection.next()
        self.assertEquals(30, self.geoTileCollection.topX)
        self.geoTileCollection.next()
        self.assertEquals(60, self.geoTileCollection.topX)
        self.geoTileCollection.next()
        self.assertEquals(90, self.geoTileCollection.topX)
        self.geoTileCollection.next()
        self.assertEquals(0, self.geoTileCollection.topX)

    def testPreviousMovesTopXByNegativeIncrement(self):
        self.assertEqual(0, self.geoTileCollection.topX)
        self.geoTileCollection.previous()
        self.assertEquals(100, self.geoTileCollection.topX)
        self.geoTileCollection.previous()
        self.assertEquals(70, self.geoTileCollection.topX)
        self.geoTileCollection.previous()
        self.assertEquals(40, self.geoTileCollection.topX)
        self.geoTileCollection.previous()
        self.assertEquals(10, self.geoTileCollection.topX)

    def testNextMovesTopYByIncrement(self):
        yValues = [0, 30, 60, 90, 0]
        for rowIndex in range(5):
            for _ in range(4):
                self.assertEquals(yValues[rowIndex], self.geoTileCollection.topY, "rowIndex={}".format(rowIndex))
                self.geoTileCollection.next()

if __name__ == '__main__':
    unittest.main()

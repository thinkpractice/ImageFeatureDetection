import unittest
from unittest.mock import MagicMock, PropertyMock
from Src.Models.GeoTileCollection import GeoTileCollection

class GeoTileCollectionTests(unittest.TestCase):
    def setUp(self):
        self.geoMap = MagicMock()
        self.tileCollectionWith()

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

    def testGetTileCallsGeoMapWithCoordinates(self):
        tileCollection1 = self.tileCollectionWith(100, 200, 10, 20)
        tileCollection1.getCurrentTile()
        self.geoMap.readTile.assert_called_with(0, 0, 10, 20)

        tileCollection1.next()
        tileCollection1.getCurrentTile()
        self.geoMap.readTile.assert_called_with(10, 0, 10, 20)

        tileCollection2 = self.tileCollectionWith(100, 200, 20, 30)
        for _ in range(5):
            tileCollection2.next()

        tileCollection2.getCurrentTile()
        self.geoMap.readTile.assert_called_with(0, 30, 20, 30)

        tileCollection2.next()
        tileCollection2.getCurrentTile()
        self.geoMap.readTile.assert_called_with(20, 30, 20, 30)

        tileCollection2.next()
        tileCollection2.getCurrentTile()
        self.geoMap.readTile.assert_called_with(40, 30, 20, 30)

    #Helper methods
    def tileCollectionWith(self, totalWidth=100, totalHeight=100, tileWidth=30, tileHeight=30):
        type(self.geoMap).widthInPixels = PropertyMock(return_value=totalWidth)
        type(self.geoMap).heightInPixels = PropertyMock(return_value=totalHeight)
        self.geoTileCollection = GeoTileCollection(self.geoMap)
        self.geoTileCollection.tileWidth = tileWidth
        self.geoTileCollection.tileHeight = tileHeight
        return self.geoTileCollection

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import MagicMock, PropertyMock, call
from Src.Models.ImageTiler import ImageTiler

class ImageTilerTests(unittest.TestCase):
    def setUp(self):
        self.map = MagicMock()

    def testImageTilerBlockXSizeSetCorrectly(self):
        self.assertEquals(32, ImageTiler(self.map, 32, 100).blockXSize)
        self.assertEquals(64, ImageTiler(self.map, 64, 200).blockXSize)
        self.assertEquals(128, ImageTiler(self.map, 128, 300).blockXSize)
        self.assertEquals(256, ImageTiler(self.map, 256, 400).blockXSize)
        self.assertEquals(512, ImageTiler(self.map, 512, 500).blockXSize)

    def testImageTilerBlockYSizeSetCorrectly(self):
        self.assertEquals(100, ImageTiler(self.map, 32, 100).blockYSize)
        self.assertEquals(200, ImageTiler(self.map, 64, 200).blockYSize)
        self.assertEquals(300, ImageTiler(self.map, 128, 300).blockYSize)
        self.assertEquals(400, ImageTiler(self.map, 256, 400).blockYSize)
        self.assertEquals(500, ImageTiler(self.map, 512, 500).blockYSize)

    def testImageTilerCalculatesNumberOfRows(self):
        self.assertEquals(1, ImageTiler(self.mapWithHeight(90), 32, 100).numberOfRows)
        self.assertEquals(2, ImageTiler(self.mapWithHeight(201), 32, 200).numberOfRows)
        self.assertEquals(3, ImageTiler(self.mapWithHeight(601), 64, 300).numberOfRows)
        self.assertEquals(4, ImageTiler(self.mapWithHeight(1599), 64, 400).numberOfRows)
        self.assertEquals(5, ImageTiler(self.mapWithHeight(2001), 64, 500).numberOfRows)

    def testImageTilerCalculatesNumberOfColumns(self):
        self.assertEquals(1, ImageTiler(self.mapWithWidth(32), 32, 100).numberOfColumns)
        self.assertEquals(2, ImageTiler(self.mapWithWidth(63), 32, 200).numberOfColumns)
        self.assertEquals(3, ImageTiler(self.mapWithWidth(129), 64, 300).numberOfColumns)
        self.assertEquals(4, ImageTiler(self.mapWithWidth(255), 64, 400).numberOfColumns)
        self.assertEquals(5, ImageTiler(self.mapWithWidth(257), 64, 500).numberOfColumns)

    def testGetTileCoordinatesReturnsCoordinatesForTileNumber(self):
        self.assertEquals((0,0), ImageTiler(self.mapWith(68, 100), 32, 64).getTileCoordinates(0))
        self.assertEquals((32,0), ImageTiler(self.mapWith(68, 100), 32, 64).getTileCoordinates(1))
        self.assertEquals((64,0), ImageTiler(self.mapWith(68, 100), 32, 64).getTileCoordinates(2))
        self.assertEquals((0,64), ImageTiler(self.mapWith(68, 100), 32, 64).getTileCoordinates(3))
        self.assertEquals((32,64), ImageTiler(self.mapWith(68, 100), 32, 64).getTileCoordinates(4))
        self.assertEquals((64,64), ImageTiler(self.mapWith(68, 100), 32, 64).getTileCoordinates(5))

    def testImageTilerBoundingBoxInTiler(self):
        pass

    def testImageTilerLoadsNextTiles(self):
        map = self.mapWith(100, 200)
        imageTiler = ImageTiler(map, 100, 64)
        self.assertEquals(0, imageTiler.activeTileNumber)
        next(imageTiler)
        map.readTile.assert_has_calls([call(0, 0, 100, 64),
        call(0, 64, 100, 64)])
        self.assertEquals(1, imageTiler.activeTileNumber)
        next(imageTiler)
        map.readTile.assert_called_with(0, 128, 100, 64)
        self.assertEquals(2, imageTiler.activeTileNumber)
        next(imageTiler)
        map.readTile.assert_called_with(0, 192, 100, 64)
        self.assertEquals(3, imageTiler.activeTileNumber)
        next(imageTiler)

    def testCurrentTileCoordinatesUpdatedCorrectly(self):
        imageTiler =  ImageTiler(self.mapWith(68, 100), 32, 64)
        next(imageTiler)
        self.assertEquals((0, 0), imageTiler.currentTileCoordinates)
        next(imageTiler)
        self.assertEquals((32, 0), imageTiler.currentTileCoordinates)
        next(imageTiler)
        self.assertEquals((64, 0), imageTiler.currentTileCoordinates)
        next(imageTiler)
        self.assertEquals((0, 64), imageTiler.currentTileCoordinates)
        next(imageTiler)
        self.assertEquals((32, 64), imageTiler.currentTileCoordinates)
        next(imageTiler)
        self.assertEquals((64, 64), imageTiler.currentTileCoordinates)

    #Helper methods
    def mapWith(self, width, height):
        map = MagicMock()
        type(map).widthInPixels = PropertyMock(return_value=width)
        type(map).heightInPixels = PropertyMock(return_value=height)
        return map

    def mapWithWidth(self, width):
        map = MagicMock()
        type(map).widthInPixels = PropertyMock(return_value=width)
        return map

    def mapWithHeight(self, height):
        map = MagicMock()
        type(map).heightInPixels = PropertyMock(return_value=height)
        return map

if __name__ == '__main__':
    unittest.main()

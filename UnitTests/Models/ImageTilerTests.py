import unittest
from unittest.mock import MagicMock, PropertyMock
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

    def testImageTilerBoundingBoxInTiler(self):
        pass

    def testImageTilerLoadsNextTiles(self):
        map = self.mapWith(100, 100)
        imageTiler = ImageTiler(map, 32, 64)
        next(imageTiler)
        map.readTile(0, 0, 32, 64)
        next(imageTiler)
        map.readTile(32, 0, 32, 64)
        next(imageTiler)
        map.readTile(64, 0, 32, 64)
        next(imageTiler)
        map.readTile(96, 0, 4, 64)


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
